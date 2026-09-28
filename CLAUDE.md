# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Python Guidelines

- Use `match`/`case` syntax instead of `if`/`elif`/`else` for pattern matching, but do use `if/elif/else` for non-pattern matching. Reserve `match`/`case` for genuinely multi-way structural dispatch, e.g. matching several dataclass/enum variants, or destructuring nested sequences/mappings where the binding syntax saves real work. A two-way branch on a single `isinstance` check or a membership test (`"key" in d`) reads more clearly as a plain `if`/`else`, even though it's technically "type-based" — don't convert those just because `match`/`case` is available.
- Use modern type hints through the `typing` module `Optional`, `Union`, `Dict`, `List`.
- Write code compatible with strict static analysis. This project uses
  isort, flake8, and mypy.
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

- `make lint` — `uv run isort pymusas tests scripts benchmarks`, then `uv run flake8 --config ./.flake8 pymusas/** tests/** scripts/** benchmarks/**`, then `uv run mypy`, 
- `make test` — `uv run coverage run` (runs `pytest` under the hood via
  `[tool.coverage.run] command_line` within @pyproject.toml) then `uv run coverage report`.
- `make doc-tests` -- to run the documentation tests which is `uv run coverage run -m pytest --doctest-modules pymusas/`
  and then `uv run coverage report`

### Handy makefile commands

For other handy commands that can be ran by `make HANDY-COMMAND` see the makefile; @makefile
