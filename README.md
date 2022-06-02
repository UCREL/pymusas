# PyMUSAS 

**Py**thon **M**ultilingual **U**crel **S**emantic **A**nalysis **S**ystem, is a rule based token and Multi Word Expression semantic tagger. The tagger can support any semantic tagset, however the tagset we have concentrated on and released pre-configured spaCy components for is the [Ucrel Semantic Analysis System (USAS)](https://ucrel.lancs.ac.uk/usas/).

<hr/>

<p align="center">
    <a href="https://github.com/UCREL/pymusas/actions/workflows/ci.yml">
        <img alt="CI" src="https://github.com/UCREL/pymusas/actions/workflows/ci.yml/badge.svg?branch=main&event=push"/>
    </a>
    <a href="https://github.com/UCREL/pymusas/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/pypi/l/pymusas"/>
    </a>
    <a href="https://codecov.io/gh/UCREL/pymusas">
        <img alt="Code coverage" src="https://codecov.io/gh/UCREL/pymusas/branch/main/graph/badge.svg" />
    </a>

</p>
<p align="center">
    <a href="https://pypi.org/project/pymusas/">
        <img alt="PyPI Version" src="https://img.shields.io/pypi/v/pymusas"/>
    </a>
    <img alt="Supported Python Versions" src="https://img.shields.io/pypi/pyversions/pymusas" />
</p>
<p align="center">
    <img alt="Number of PyMUSAS PyPI downloads for the last month" 
         src="https://img.shields.io/pypi/dm/pymusas" />
    <a href="https://mybinder.org/v2/gh/UCREL/pymusas/binder-main?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252FUCREL%252Fpymusas%26urlpath%3Dlab%252Ftree%252Fpymusas%252F%26branch%3Dmain">
        <img alt="Launch Binder" src="https://static.mybinder.org/badge_logo.svg">
    </a>
</p>

## Documentation

* 📚 [Usage Guides](https://ucrel.github.io/pymusas/) - What the package is, tutorials, how to guides, and explanations.
* 🔎 [API Reference](https://ucrel.github.io/pymusas/api/spacy_api/taggers/rule_based) - The docstrings of the library, with minimum working examples.
* 🚀 [Roadmap](./ROADMAP.md)

## Language support

PyMUSAS currently support 10 different languages with pre-configured spaCy components that can be downloaded, each language has it's own [guide on how to tag text using PyMUSAS](https://ucrel.github.io/pymusas/usage/how_to/tag_text). Below we show the languages supported, if the model for that language supports Multi Word Expression (MWE) identification and tagging (all languages support token level tagging by default), and size of the model:

| Language (BCP 47 language code) | MWE Support | Size |
| --- | --- | --- |
| Mandarin Chinese (cmn) | :heavy_check_mark: | 1.28MB |
| Welsh (cy) | :heavy_check_mark: | 1.09MB |
| Spanish, Castilian (es) | :heavy_check_mark: | 0.20MB |
| Finnish (fi) | :x: | 0.63MB |
| French (fr) | :x: | 0.08MB |
| Indonesian (id) | :x: | 0.24MB |
| Italian (it) | :heavy_check_mark: | 0.50MB |
| Dutch, Flemish (nl) | :x: | 0.15MB |
| Portuguese (pt) | :heavy_check_mark: | 0.27MB |
| English (en) | :heavy_check_mark: | 0.88MB |

## Install PyMUSAS

Can be installed on all operating systems and supports Python version >= `3.7`, to install run:

```
pip install pymusas
```

## Development

When developing on the project you will want to install the Python package locally in editable format with all the extra requirements, this can be done like so:

```bash
pip install -e .[tests]
```

For a `zsh` shell, which is the default shell for the new Macs you will need to escape with `\` the brackets:

```zsh
pip install -e .\[tests\]
```

### Running linters and tests

This code base uses flake8 and mypy to ensure that the format of the code is consistent and contain type hints. The flake8 settings can be found in [./setup.cfg](./setup.cfg) and the mypy settings within [./pyproject.toml](./pyproject.toml). To run these linters:

``` bash
isort pymusas tests scripts
flake8
mypy
```

To run the tests with code coverage (**NOTE** these are the code coverage tests that the Continuos Integration (CI) reports at the top of this README, the doc tests are not part of this report):

``` bash
coverage run # Runs the tests (uses pytest)
coverage report # Produces a report on the test coverage
```

To run the [doc tests](https://docs.python.org/3/library/doctest.html), these are tests to ensure that examples within the documentation run as expected:

``` bash
coverage run -m pytest --doctest-modules pymusas/ # Runs the doc tests
coverage report # Produces a report on the doc tests coverage
```

## Team

PyMUSAS is an open-source project that has been created and funded by the [University Centre for Computer Corpus Research on Language](https://ucrel.lancs.ac.uk/) (UCREL) at [Lancaster University](https://www.lancaster.ac.uk/). For more information on who has contributed to this code base see the [contributions page.](https://github.com/UCREL/pymusas/graphs/contributors) 