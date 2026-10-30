# Evaluation

This directory contains the scripts to evaluate the English rule based tagger, so that we can check whether a change to the tagger, e.g. adding the autotag lexicon, makes it better or worse. Each tagger is evaluated for:

* Accuracy - top-n accuracy on the English gold datasets of the [USAS Evaluation Framework](https://github.com/UCREL/USAS-Evaluation-Framework).
* Coverage - the percentage of tokens the tagger can tag, see [coverage](#coverage).
* Speed - tokens per second.
* Resources - memory required to load and run the whole pipeline, spaCy and the tagger, and the size of the tagger on disk.

The taggers that are evaluated are:

| Tagger | What it is | pymusas version |
| --- | --- | --- |
| `pymusas-models en_dual_none_contextual_none 0.4.0` | The pre-built [pymusas-models](https://github.com/UCREL/pymusas-models) English rule based model, the current release. | The latest release that the model supports, from PyPI. |
| `lexicons@73d2313` | The tagger built from the [Multilingual-USAS](https://github.com/apmoore1/Multilingual-USAS/tree/73d2313fa356acaef30e838f001b10ecd8188935/English) English single word and Multi Word Expression (MWE) lexicons. | This repository's working tree. |
| `lexicons@73d2313 + autotag` | As above, plus the English autotag lexicon. | This repository's working tree. |

Comparing the taggers tells us:

* `lexicons@73d2313 + autotag` against `lexicons@73d2313` - the effect of the autotag lexicon on its own, as everything else is the same.
* `lexicons@73d2313 + autotag` against `pymusas-models ...` - whether we are better than the current release. This mixes the changes to the code with the changes to the lexicons, as the pre-built model was built from an older version of the lexicons.

## How to run the evaluation

We assume you have the development setup installed following these [instructions in the main README](../../README.md#setup), the requirements for the evaluation are in the `evaluation` dependency group of the [pyproject.toml](../../pyproject.toml), which is installed with the development setup.

To evaluate all three taggers and print the results as markdown tables to stdout (this takes around 25 minutes with the default 100,000 token finewiki sample, see [run time](#run-time) for how to make it quicker);

``` bash
./run_evaluation.sh > evaluation_results.md
```

`./run_evaluation.sh --help` lists the options, which are the size of the finewiki sample (`--wiki-token-limit`), whether each finewiki text is a paragraph or a whole article (`--text-unit`), the number of times the finewiki sample is tagged when measuring speed (`--speed-repeats`), and the Python version every tagger is evaluated with (`--python-version`, default `3.13`).

### Run time

Most of the run time is the tagger itself, not downloading data, as all of the data is cached after the first run. The tagger processes around 1,300 tokens per second, so one pass over the default 100,000 token finewiki sample takes around 75 seconds, and each tagger makes around five passes over it: three to measure speed (`--speed-repeats 3`), one to measure coverage, and one to measure peak memory. Therefore each tagger takes around 7 to 8 minutes.

To make it quicker:

* `--speed-repeats 1` is the easiest option, it saves around 2.5 minutes per tagger, but the speed results are less reliable as they come from one run rather than the fastest of three.
* `--wiki-token-limit` reduces the size of the finewiki sample, e.g. `--wiki-token-limit 50000` roughly halves the run time and `--wiki-token-limit 5000` takes a few minutes in total, which is useful as a quick check while you are making a change. The speed, memory, and finewiki coverage results are less reliable with a smaller sample.

Use the default options when creating results that you want to compare.

To evaluate a single tagger configuration, e.g. while you are making a change, use `evaluate_rule_based_tagger.py`, `--help` lists all of the options;

``` bash
PYTHONHASHSEED=0 uv run evaluate_rule_based_tagger.py --autotag
```

To use your own lexicon files, push them to a GitHub repository and use the `--lexicon-repo` and `--lexicon-commit` options. The results of different runs can be combined into one set of tables by saving them with `--output-file results.jsonl` and then running `uv run format_evaluation_results.py results.jsonl`.

**Note** `evaluate_rule_based_tagger.py` uses the development environment, which contains `torch` from the `neural` extra. When `torch` is installed spaCy imports it, which adds a few hundred MB to the peak memory, so the peak memory of a single run is not comparable with the peak memory from `run_evaluation.sh`.

### Reproducible results

The tagger's output can depend on Python's hash randomisation: when lexicon entries that have the same rank match the same tokens, which entry is used depends on the iteration order of a `set` in `ContextualRuleBasedRanker`. Therefore `run_evaluation.sh` sets `PYTHONHASHSEED=0`, and `evaluate_rule_based_tagger.py` warns if `PYTHONHASHSEED` is not set. With the hash seed set, the accuracy and coverage results are identical between runs.

### Isolated environments

`run_evaluation.sh` evaluates each tagger in its own isolated uv environment;

* The pre-built model uses the latest released version of pymusas from PyPI, and the pre-built model, which are stated in [./pymusas_model_requirements.txt](./pymusas_model_requirements.txt). Therefore the baseline is not affected by changes to this repository, including breaking changes.
* The lexicon taggers use this repository's working tree.

All other requirements, e.g. spaCy and `en_core_web_sm`, are exported from `uv.lock` so that they are the same in every environment, and every environment uses the same Python version, which is `3.13` by default and can be changed with `--python-version`. The environments only contain the `evaluation` dependency group, therefore they do not contain `torch`, which spaCy imports when it is installed.

When a new version of pymusas is released, update the `pymusas` version in [./pymusas_model_requirements.txt](./pymusas_model_requirements.txt), and when a new pre-built model is released update the model's URL in the same file and the `PRE_BUILT_MODEL_NAME` in [./tagger_utils.py](./tagger_utils.py) if its name has changed.

**Note for editing the evaluation code**: the same scripts, e.g. [./tagger_utils.py](./tagger_utils.py), run in both kinds of environment, so they are also run with the released version of pymusas when evaluating the pre-built model. That version does not have the newest pymusas code, e.g. `AutotagLexiconCollection`, so importing it at the top of a module would raise an `ImportError` when evaluating the pre-built model, even though that tagger never uses it. Therefore import anything that is not in the released version inside the function that needs it, which is only called for the lexicon taggers, see `add_lexicon_tagger` in [./tagger_utils.py](./tagger_utils.py). If the evaluation code ever needs a newer pymusas API for the pre-built model too, then evaluate the pre-built model with its own small script instead.

## Example results

<details>
<summary>Results from <code>./run_evaluation.sh</code> with the default options, run on 2026-10-29 on a CPU only Linux machine</summary>

The speed and memory results depend on the machine they are run on, therefore only compare them with results from the same machine.

### Accuracy (%)

| Tagger | Dataset | Scored Tokens | Punctuation Excluded | Top-1 Micro | Top-1 Macro | Top-5 Micro | Top-5 Macro |
| --- | --- | --- | --- | --- | --- | --- | --- |
| pymusas-models en_dual_none_contextual_none 0.4.0 | Benedict English | 3,468 | 431 | 71.83 | 63.93 | 81.34 | 73.97 |
| pymusas-models en_dual_none_contextual_none 0.4.0 | English Wikipedia | 3,505 | 530 | 71.10 | 61.17 | 77.77 | 73.20 |
| lexicons@73d2313 | Benedict English | 3,468 | 431 | 71.83 | 63.93 | 81.34 | 73.97 |
| lexicons@73d2313 | English Wikipedia | 3,505 | 530 | 71.10 | 61.17 | 77.77 | 73.20 |
| lexicons@73d2313 + autotag | Benedict English | 3,468 | 431 | 71.83 | 63.93 | 81.37 | 74.03 |
| lexicons@73d2313 + autotag | English Wikipedia | 3,505 | 530 | 71.18 | 61.23 | 77.92 | 73.30 |

### Coverage (%)

| Tagger | Dataset | Tokens | Non-Punctuation Tokens | Lexicon Coverage | Lexicon Coverage (No Punctuation) | Lexicon Coverage (Scored Tokens) | Tag Coverage | Tag Coverage (No Punctuation) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pymusas-models en_dual_none_contextual_none 0.4.0 | Benedict English | 3,899 | 3,468 | 88.20 | 99.16 | 99.16 | 99.67 | 99.63 |
| pymusas-models en_dual_none_contextual_none 0.4.0 | English Wikipedia | 4,036 | 3,506 | 81.07 | 93.18 | 93.18 | 95.27 | 94.64 |
| pymusas-models en_dual_none_contextual_none 0.4.0 | finewiki (paragraph) | 101,672 | 83,541 | 69.36 | 84.41 | - | 90.99 | 89.03 |
| lexicons@73d2313 | Benedict English | 3,899 | 3,468 | 88.20 | 99.16 | 99.16 | 99.67 | 99.63 |
| lexicons@73d2313 | English Wikipedia | 4,036 | 3,506 | 81.07 | 93.18 | 93.18 | 95.02 | 94.38 |
| lexicons@73d2313 | finewiki (paragraph) | 101,672 | 83,541 | 69.36 | 84.41 | - | 90.95 | 88.98 |
| lexicons@73d2313 + autotag | Benedict English | 3,899 | 3,468 | 88.61 | 99.63 | 99.63 | 99.67 | 99.63 |
| lexicons@73d2313 + autotag | English Wikipedia | 4,036 | 3,506 | 82.41 | 94.72 | 94.72 | 95.09 | 94.47 |
| lexicons@73d2313 + autotag | finewiki (paragraph) | 101,672 | 83,541 | 73.43 | 89.36 | - | 91.22 | 89.31 |

### Resources (finewiki)

| Tagger | Text Unit | Tokens | pymusas Tokens Per Second | Pipeline Tokens Per Second | Load Peak Memory (MB) | Peak Memory (MB) | Saved Tagger (MB) | Lexicon Files (MB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pymusas-models en_dual_none_contextual_none 0.4.0 | paragraph | 101,672 | 1,385.73 | 1,155.46 | 254.67 | 450.81 | 2.44 | - |
| lexicons@73d2313 | paragraph | 101,672 | 1,391.19 | 1,161.65 | 238.42 | 449.22 | 2.44 | 1.84 |
| lexicons@73d2313 + autotag | paragraph | 101,672 | 1,377.77 | 1,013.78 | 238.27 | 449.89 | 2.44 | 1.85 |

</details>

## Data

* Gold datasets, from the [USAS Evaluation Framework](https://github.com/UCREL/USAS-Evaluation-Framework) at a pinned commit:
    * Benedict English, licensed [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
    * English Wikipedia, licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
* A sample of English Wikipedia articles from the [HuggingFaceFW/finewiki dataset](https://huggingface.co/datasets/HuggingFaceFW/finewiki), licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The gold datasets are too small to measure speed and memory, and their coverage only reflects their vocabulary, so speed, memory, and coverage are also measured on this sample. The articles are read in order from the first English parquet file at a pinned revision of the dataset, and are processed in the same way as the [resource benchmarks](../resource_benchmarking/), articles that contain a table are skipped and markdown headers are removed. The sample has no gold labels.

All of the data is downloaded once and cached in the pymusas cache directory, `~/.cache/pymusas` by default, which can be changed with the `PYMUSAS_HOME` environment variable.

The gold datasets are already split into sentences, and each sentence is tagged as its own text using the gold tokenisation. Each finewiki text is a paragraph (a non-empty line of an article) by default, or a whole article with `--text-unit document`, which is tokenised by spaCy. No sentence splitter is used.

The POS tags and lemmas that the tagger requires come from the `en_core_web_sm` spaCy model. `evaluate_rule_based_tagger.py` can use another spaCy model with `--spacy-model`, e.g. `en_core_web_trf`, which you need to install yourself, `run_evaluation.sh` always uses `en_core_web_sm` so that the POS tags and lemmas are the same in every environment.

## Metrics

### Punctuation

A token is punctuation when it is labelled `PUNCT` or `Z9`, as both of these semantic tags can represent punctuation, e.g. Benedict English uses `PUNCT` and English Wikipedia uses `Z9`. For the gold datasets the gold label is used, and for the finewiki sample, which has no gold labels, the tagger's top predicted tag is used, therefore the number of non-punctuation finewiki tokens can differ slightly between taggers.

### Accuracy

Top-n accuracy (micro and macro averaged), using the USAS Evaluation Framework's `top_n_accuracy`, for each `n` in `--top-n` (default 1 and 5), whereby a token is correct if one of its gold tags is within the top `n` predicted tags. Tokens labelled as punctuation, or `Z99`, are not scored (`Punctuation Excluded`), and so the accuracy is over the `Scored Tokens`.

Before the predicted tags are compared with the gold tags, they are normalised in the same way as the gold tags; the `+`/`-` markers and the `f`, `m`, `c`, `n`, `%`, `@` markers are removed, e.g. `X5.2+` becomes `X5.2` and `Z2/S2mf` becomes `Z2/S2`.

### Coverage

Coverage has two definitions, each reported over all tokens and over non-punctuation tokens, and for the gold datasets also over the scored tokens:

* Lexicon coverage, the main measure, is the percentage of tokens that a lexicon rule matched (single word, autotag, or MWE).
* Tag coverage is the percentage of tokens that were not tagged `Z99`.

Lexicon coverage is needed because tokens that no lexicon rule matches are tagged by a POS fallback; `PUNCT` for punctuation, `N1` for numbers, and Z99 otherwise (a token that falls back to Z99 does not count towards lexicon coverage, as it is the unknown tag; a token matched by a lexicon entry whose tag is Z99 (this should not occur but can with MWEs that use the `Df` tag) does count towards lexicon coverage, but not towards tag coverage). Most of the English autotag lexicon entries match numbers, which would otherwise be tagged `N1` by the fallback, so tag coverage would hide most of the effect of the autotag lexicon.

### Speed

Measured on the finewiki sample:

* pymusas Tokens Per Second - only the pymusas tagger is timed, as the POS tags and lemmas are created beforehand. The finewiki sample is tagged `--speed-repeats` times and the fastest time is used.
* Pipeline Tokens Per Second - the whole spaCy pipeline, i.e. the time to create the POS tags and lemmas plus the pymusas tagger time.

### Resources

The memory statistics are in MB, and are the memory required to run the whole pipeline that creates the pymusas tags, i.e. the spaCy model that creates the tokens, POS tags, and lemmas, as well as the pymusas tagger. They are the peak memory of a new process, that only imports spaCy, pymusas, and psutil, so that the memory used by the rest of the evaluation, e.g. the gold datasets, is not included:

* Load Peak Memory - the peak memory after loading the spaCy model and the pymusas tagger.
* Peak Memory - the peak memory after also running the pipeline over the finewiki sample. This is the memory required to run pymusas.

On Linux the peak memory is `VmHWM` from `/proc/self/status`, on Windows it is `peak_wset` from `psutil`, and on macOS, and on Linux when `VmHWM` is unavailable, it is `ru_maxrss` from `resource.getrusage`. `VmHWM` is used on Linux as `ru_maxrss` is preserved across `execve`, so a process started by multiprocessing's `spawn` could report the peak of the larger process it was forked from. Values are in MiB (1024² bytes) and include file-backed pages, e.g. memory-mapped model files.

The finewiki sample is small (100,000 tokens is around 0.6 MB of text) compared to the spaCy model and tagger, and the documents are discarded as they are tagged, so the sample does not need to be streamed or reduced to measure memory. The peak is set by the models and the largest batch or article in flight, not by the number of texts, so a much smaller sample could miss the longest articles and under-report it.
* Saved Tagger - the size of the tagger when saved to disk.
* Lexicon Files - the size of the lexicon files the tagger was built from, `-` for the pre-built model.

## Brief description of the files

* `run_evaluation.sh` -- evaluates the three taggers in isolated environments and prints the combined results.
* `evaluate_rule_based_tagger.py` -- evaluates one tagger configuration.
* `format_evaluation_results.py` -- formats the results of one or more runs of `evaluate_rule_based_tagger.py` as markdown tables.
* `evaluation_utils.py` -- NOT A SCRIPT, functions to load the data and evaluate a tagger.
* `tagger_utils.py` -- NOT A SCRIPT, functions to build or load the tagger and measure its memory. It only imports spaCy, pymusas, and psutil, as it is imported by the processes that measure memory.
* `pymusas_model_requirements.txt` -- the released pymusas version and pre-built model used for the baseline.
