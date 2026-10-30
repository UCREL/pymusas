Here are the improvements I'd suggest, most valuable first. I haven't implemented any of them.

## High value

**1. Show which tokens changed between two taggers.**
The accuracy differences are tiny. Autotag moves English Wikipedia top-1 micro by 0.08 points, which is 3 tokens, and the tables can't say which 3. Saving each token's predicted tags and gold tags per run, then adding a comparison command that lists tokens whose prediction changed, would answer what a lexicon change actually did. I think this is the most useful addition for reviewing lexicon changes. Roughly half a day.

**2. Check that `lexicon_matches` still agrees with the pipe.**
Coverage re-runs the rules and ranker outside the pipe, so if the pipe's `__call__` changes, coverage could quietly go wrong. A cheap safeguard: in the same pass, rebuild each token's tags from the best match plus the POS fallback, and raise an error if they differ from `token._.pymusas_tags`. Better still, the pipe could optionally record whether each token's tag came from a lexicon match, which removes the duplication entirely. That's a change to pymusas itself.

**3. Fix the ranker's tie-breaking in pymusas.**
`ContextualRuleBasedRanker.get_global_lowest_ranks` iterates a `set`, so equally ranked matches are chosen in hash order. Sorting each set by a stable key, such as the lexicon entry and token span, would make tagging deterministic for users as well. The evaluation would then no longer need `PYTHONHASHSEED`. This belongs in its own PR, because it may change some tags.

**4. Unit tests for the evaluation code.**
Nothing tests `normalise_tags` beyond its doctest, nor `coverage_counts`, the punctuation and labelled masks, or `format_results`. These are pure functions and easy to test with small hand-built docs. The test runner only collects `tests/unit_tests`, so they'd need either a new test path or a mention in the README.

## Medium value

**5. Keep results when a run fails or is killed.**
`run_evaluation.sh` writes to a temporary file and deletes it on exit, so the killed run lost two completed taggers. Writing to a lasting file, e.g. `--output-file results.jsonl`, and letting one failing tagger not stop the others would avoid that.

**6. Break lexicon coverage down by rule type.**
Each match already records its lexicon type: single word, autotag, multi-word wildcard, and so on. Reporting coverage per type would show directly how many tokens autotag contributes, separately from multi-word expressions.

**7. Show how much accuracy differences can be trusted.**
With about 3,500 scored tokens per dataset, small differences are mostly noise. Bootstrap confidence intervals, or a paired test on the tokens where two taggers differ, would show whether an improvement is real.

**8. Gold data where autotag matters.**
Most autotag entries match numbers, money, ordinals and percentages, which are rare in the gold sets. A small hand-labelled set of such tokens, or reporting accuracy only on tokens where an autotag entry matched, would measure autotag's accuracy rather than just its coverage.

**9. Make the pipeline speed figure reliable, or drop it.**
spaCy preprocessing is timed once, so "Pipeline Tokens Per Second" is noisy: it showed 1,014 against about 1,160 with identical pymusas speed. Either time it with repeats like the pymusas figure, or remove the column.

**10. One pass instead of two.**
Coverage re-runs the rules and ranker after the speed timing. Combining that with item 2 would save about 75 seconds per tagger with no change to the results.

## Lower value / housekeeping

**11. The resource benchmarks share three problems this work fixed.** `benchmarks/resource_benchmarking` still:
- measures memory with system-wide `virtual_memory()`
- runs with `torch` installed, which spaCy imports
- streams finewiki through `datasets`, which hangs at exit here

Moving the peak-memory function, the finewiki sampler and the isolated-environment approach into shared code would fix all three and remove duplication.

**12. Record the machine in the results.**
Speed and memory are only comparable on the same machine. Saving CPU model, core count, OS and architecture with each result would make that visible. Committing a results file per release would also give a history to compare against.

**13. Include a format version in the finewiki cache key.**
The cache key covers revision, token limit and text unit, but not the sampling logic. If that logic changes, an old cached sample would be reused silently.

**14. Rethink how CI gets the evaluation requirements.**
With `default-groups = "all"`, every CI job clones the framework and downloads `en_core_web_sm`. An alternative is to leave `evaluation` out of the default groups and have `make lint` and CI install it explicitly for `ty`. A scheduled CI job could also run a small evaluation and flag regressions.

**15. Extend to other taggers and languages.**
The code is organised for it: `TaggerConfig`, plus the gold datasets the framework provides for other languages. Neural and hybrid taggers would mainly need a separate peak-memory setup, since they need `torch`.

**16. macOS peak memory is untested.**
It still uses `ru_maxrss`, which may carry over the parent process's memory, as it did on Linux. It needs checking on a Mac, and if it's affected, the memory process could be started differently.

If I were choosing three, I'd do 1, 2 and 3: they make the evaluation more trustworthy and more useful for judging lexicon changes, and 3 fixes a real bug for users.