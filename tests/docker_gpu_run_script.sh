#! /bin/bash
uv add spacy[cuda12x]
uv run coverage run --append -m pytest tests/unit_tests
uv run coverage run --append -m pytest tests/functional_tests
uv run coverage run --append -m pytest --doctest-modules pymusas/
uv run coverage report