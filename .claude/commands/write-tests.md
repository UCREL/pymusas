---
description: Write pytest tests for a given function or class, matching this repo's conventions
argument-hint: <function-or-class-name> [file path]
allowed-tools: Read, Edit, Write, Bash(uv run *), Bash(make *), Grep, Glob
---

Write tests for: $ARGUMENTS

Follow this process:

1. **Locate the target.** If a file path was given, read it directly. Otherwise search
   `pymusas/` for the named function or class. Read the whole containing file,
   not just the target — sibling code often reveals conventions (e.g. helper fixtures,
   error types, edge cases already handled elsewhere).

2. **Find the matching test file.** Tests live in `tests/`, named `test_<module>.py` for
   `pymusas/<module>.py` (e.g. `utils.py` -> `tests/test_utils.py`). Read the
   existing test file in full before writing anything — match its style exactly:
   - Plain `assert result == expected` comparisons against constructed Pydantic models
     , not attribute-by-attribute checks.
   - `@pytest.mark.parametrize` for cases that vary a single input across the whole test
     body, but a single
     test function with multiple inline cases and comments when testing one function's
     behavior across varied inputs.
   - Reuse existing fixtures from `tests/utils_test.py` rather than duplicating
     path logic. Add a new fixture only if the target needs test data that doesn't fit
     an existing one.
   - One `pytest.raises` test per distinct error condition for functions with `Raises:`
     documented in their docstring.
   - Short comment above each case/block explaining what it covers, not what the code does.

3. **Cover, at minimum:**
   - The documented `Examples:` from the docstring.
   - Every documented `Raises:` condition.
   - Empty/boundary inputs (empty string, empty set/list, whitespace-only).
   - Any `strict`/optional-flag parameters, in both states, if present.
   - Interaction with other public functions in the module when the target composes them
     (e.g. a filter function built on a parser should be tested against the parser's own
     edge cases, not just happy-path input).

4. **Do not** invent new fixtures, helper modules, or test data files unless the target
   genuinely requires fixture data that isn't already covered — check `tests/data/` first.

5. **Verify** by running the new test(s) directly, then the full suite:
   ```
   uv run coverage run -m pytest tests/test_<module>.py::test_<name> -v
   # Runs the code tests
   make tests
   # Runs the documentation tests
   make doc-tests
   ```
   Fix any failures before reporting done.