#! /bin/bash
source .venv/bin/activate
coverage run --append -m pytest tests/unit_tests
coverage run --append -m pytest tests/functional_tests
coverage run --append -m pytest --doctest-modules pymusas/
coverage report