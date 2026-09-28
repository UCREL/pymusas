---
description: Write or correct docstrings (with doctest examples) for a file, class, or function, matching this repo's conventions
argument-hint: <file path | class-or-function name>
allowed-tools: Read, Edit, Grep, Glob, Bash(uv run *), Bash(make *)
---

Document: $ARGUMENTS

Follow this process:

1. **Locate the target.** If a file path was given, read it directly. Otherwise search
   `pymusas/` for the named class or function. Read the whole containing file, not
   just the target — sibling classes/functions establish the docstring conventions to match.

2. **Style reference.** Follow the "Docstrings" section of `CLAUDE.md`

3. **For every public class and function in scope:**
   - Add a docstring if missing.
   - If one exists, review it for accuracy against the current code (params renamed/added,
     behavior changed, wrong `Raises`) and correct it — don't just leave stale prose.
   - Class docstrings: summarize purpose/behavior; document only attributes defined directly
     in the class body (e.g. `name`, compiled regex patterns) under `Attributes`, if they're
     part of the public surface. Do **not** list instance attributes assigned in `__init__`
     (e.g. `self.language`) there — those are documented as `__init__` `Args` instead, per
     `filters.py`/`formatters.py` convention.
   - `__init__`: document constructor `Args` (covers all `self.x = ...` assignments) and any
     `Raises`.
   - Methods/functions: document `Args`, `Returns`, and `Raises` for documented error paths.

4. **Add doctest-style `Examples:`** for methods whose behavior is simple, deterministic, and
   illustrative (pure text transforms, small static/classmethod helpers). Skip them where setup
   is heavy or output is non-deterministic/verbose (e.g. wrapping an external parser with
   many plugins) — a plain `Args`/`Returns` description is enough there.

5. **Escaping gotcha:** docstrings are normal (non-raw) triple-quoted strings. A literal `\n`
   or `\command` typed directly in an `Examples:` block gets unescaped by Python at *module
   parse time*, corrupting the doctest source/output. Backslashes meant to appear in the
   doctest's Python code (e.g. `"a\nb"`, `{"\pagebreak"}`) must be doubled in the source file.

6. **Verify**, in order, fixing any failures before reporting done:
   ```
   uv run python3 -m doctest <path/to/file.py> -v
   make lint
   # Runs the code tests
   make tests
   # Runs the documentation tests
   make doc-tests
   ```
