# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Python Guidelines

- Use `match`/`case` syntax instead of `if`/`elif`/`else` for pattern matching, but do use `if/elif/else` for non-pattern matching. Reserve `match`/`case` for genuinely multi-way structural dispatch, e.g. matching several dataclass/enum variants, or destructuring nested sequences/mappings where the binding syntax saves real work. A two-way branch on a single `isinstance` check or a membership test (`"key" in d`) reads more clearly as a plain `if`/`else`, even though it's technically "type-based" — don't convert those just because `match`/`case` is available.
- Use built-in generics (`list[str]`, `dict[str, int]`, `tuple[int, int]`, `set[str]`) and `|` unions
  (`str | None`, `int | str`) instead of the deprecated `typing` aliases (`List`, `Dict`, `Optional`, `Union`, ...).
  Import abstract types such as `Callable`, `Iterable` and `Iterator` from `collections.abc`, and use `typing` only
  for names without a built-in form (`Any`, `cast`, `Protocol`, ...). Ruff's pyupgrade rules (`UP006`, `UP007`,
  `UP035`, `UP045`) enforce this. Write docstring types the same way, e.g. `` `list[str] | None` ``.
- Write code compatible with strict static analysis. This project uses
  ruff (linting and import sorting) and ty (type checking), both configured in
  `pyproject.toml`. Ruff's `ANN` rules require every function to be fully annotated.
  ty only honours `# type: ignore` and `# ty: ignore[<rule>]`, not mypy-style
  `# type: ignore[<code>]`. Prefer fixing the types over suppressing them.
- Use `pathlib.Path` for all filesystem operations instead of `os.path`.
- Follow PEP 8. Prefer f-strings, comprehensions, and context managers where they improve clarity.
- Prioritise readability — avoid deeply nested `if` statements or complex one-liner comprehensions.

## Docstrings

See @CONTRIBUTING.md 


## Development Environment

This project uses `uv` for environment and dependency management.
**Never invoke `python` or `pip` directly** — always go through `uv`.


### Setup

```bash
uv sync --all-extras
```

### Dependency management

| Task                        | Command                      |
|-----------------------------|------------------------------|
| Add a runtime dependency    | `uv add <package>`           |
| Add a dev dependency        | `uv add --dev <package>`     |
| Remove a dependency         | `uv remove <package>`        |
| Run a script                | `uv run <script.py>`         |

### Linting and tests

Use the `make` commands when finalising a feature or fix, otherwise use `make` or the underlying tools:

- `make lint` — `uv run ruff check --fix-only pymusas tests scripts benchmarks`, then `uv run ruff check pymusas tests scripts benchmarks`, then `uv run ty check`.
- `make tests` — `uv run coverage run` (runs `pytest` under the hood via
  `[tool.coverage.run] command_line` within @pyproject.toml) then `uv run coverage report`.
  Only `tests/unit_tests` is collected by default (`testpaths`).
- `make doc-tests` -- to run the documentation tests which is `uv run coverage run -m pytest --doctest-modules pymusas/`
  and then `uv run coverage report`

Running a subset while iterating:

```bash
uv run pytest tests/unit_tests/taggers/rules/test_mwe.py            # one file
uv run pytest tests/unit_tests/taggers/rules/test_mwe.py::test_name # one test
uv run pytest --doctest-modules pymusas/taggers/rule_based.py       # one module's doctests
make failed-tests                                                   # re-run last failures
```

Functional tests (`tests/functional_tests`) are end-to-end tests of the *built
wheel*. They are not collected by `make tests`. Run them with
`make full-coverage-tests`, which builds the wheel and runs unit, doc and
functional tests. That target runs the functional tests twice in isolated
environments, once without and once with the `neural` extra, because each test
branches on whether the neural packages are installed. The target also rewrites
`pyproject.toml` temporarily and restores it at the end. Because of
`.ONESHELL` without `set -e`, a failing step does not stop the target and the
exit code only reflects the last command, so check the output for test
failures and `error:` lines rather than the exit code. Running
`uv run pytest tests/functional_tests` directly tests the source tree in the dev
environment, which has all extras installed, so it only covers the
neural-installed path.

Notes on test dependencies:

- Neural and hybrid tests and doctests load the HuggingFace model
  `ucrelnlp/PyMUSAS-Neural-English-Small-BEM`. The first run downloads it; to
  pre-fetch it, run `uv run tests/model_download.py <hf-cache-dir>`.
- Many doctests download lexicon TSVs from GitHub (`Multilingual-USAS`) through
  `pymusas.file_utils.download_url_file`, and cache them under `PYMUSAS_HOME`
  (default `~/.cache/pymusas`). Those doctests need network access the first time.
- CI runs `ruff check` without fixing, so run `make lint` (which applies ruff's
  fixes, such as import sorting) before committing.

### Handy makefile commands

For other handy commands that can be ran by `make HANDY-COMMAND` see the makefile; @makefile

## Architecture

The code is in two layers: framework-agnostic taggers, and spaCy pipeline
components that wrap them.

### Core layer (`pymusas/`, no spaCy dependency in the tagging logic)

The taggers take parallel `list[str]` inputs (tokens, lemmas, POS tags). For each
token they return `(tags, mwe_indexes)`, where `mwe_indexes` is a list of
`(start, end)` token spans. More than one span means a discontinuous MWE.

- `taggers/rule_based.RuleBasedTagger`: runs every `Rule` in `taggers/rules/`
  (`SingleWordRule`, `MWERule`). Each rule produces candidate
  `rankers.ranking_meta_data.RankingMetaData` for each token. The outputs of all
  the rules are concatenated and passed to a `LexiconEntryRanker`, usually
  `rankers.lexicon_entry.ContextualRuleBasedRanker`, which picks the best
  candidate per token and resolves overlapping MWEs. Tokens left untagged fall
  back to `PUNCT`, `N1` or `Z99`, depending on their POS tag.
- `taggers/neural.NeuralTagger`: a wrapper around a `wsd_torch_models` BEM
  model. It tags single words only.
- `taggers/hybrid.HybridTagger`: subclasses `RuleBasedTagger`. Tokens the rules
  would tag `Z99` get the neural tagger's prediction instead.
- `lexicon_collection.py`: `LexiconCollection` and `MWELexiconCollection`, which
  load USAS lexicon TSV files into the dict lookups the rules consume.
- `pos_mapper.py`: mappings between tagsets (UPOS, Penn Chinese Treebank,
  CorCenCC) and the USAS core POS tagset. They're passed to rules as a
  `pos_mapper`.
- `base.Serialise`: the `to_bytes`/`from_bytes` ABC that `Rule` and
  `LexiconEntryRanker` implement. `serialise_object_to_bytes` records the class
  and module names, so rules and rankers can be reloaded generically. Any new
  rule or ranker must implement both methods and `__eq__`.

### spaCy layer (`pymusas/spacy_api/`)

- `spacy_api/taggers/{rule_based,neural,hybrid}.py`: `spacy.pipeline.Pipe`
  subclasses registered as spaCy factories. They're exposed through
  `[project.entry-points.spacy_factories]` in `pyproject.toml`, so the entry
  points must be updated when a factory is renamed or added. They read POS and
  lemma from configurable token attributes (`pos_`, `lemma_`) and write results
  to custom token extensions (`pymusas_tags`, `pymusas_mwe_indexes`). Rules and
  the ranker are supplied in `initialize()`, not `__init__`, and are serialised
  by `to_bytes`/`to_disk`.
- `spacy_api/{lexicon_collection,pos_mapper,rankers}.py` and
  `spacy_api/taggers/rules.py`: functions registered in spaCy's `@misc`
  registry (e.g. `pymusas.taggers.rules.SingleWordRule.v1`). They build the core
  objects from a spaCy config file.

### Optional `neural` extra

`torch`, `transformers` and `wsd_torch_models` are only installed with the
`neural` extra. Neural modules import them inside `try`/`except`, and call
`pymusas.utils.neural_extra_installed()` before using them. Keep that pattern:
importing `pymusas` or the rule-based tagger must never require the neural
dependencies.

### Other directories

- `docs/`: a Docusaurus site. `docs/docs/api` is generated from docstrings by
  `scripts/py2md.py` (`make create-api-docs`), so don't edit it by hand.
- `benchmarks/`: benchmark scripts. They're linted and type-checked with the
  rest of the code.
