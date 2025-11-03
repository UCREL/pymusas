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

Can be installed on all operating systems and supports Python version >= `3.10` < `3.14`, to install run:

``` bash
pip install pymusas
```

If using [uv](https://docs.astral.sh/uv/):

``` bash
uv add pymusas
```

## Development

### Setup

You can either use the dev container with your favourite editor, e.g. VSCode. Or you can create your setup locally below we demonstrate both.

In both cases they share the same tools, of which these tools are:
* [uv](https://docs.astral.sh/uv/) for Python packaging and development
* [node](https://nodejs.org/en/download) for building and serving the documentation.
* [make](https://www.gnu.org/software/make/) (OPTIONAL) for automation of tasks, not strictly required but makes life easier.

#### Dev Container

A [dev container](https://containers.dev/) uses a docker container to create the required development environment, the Dockerfile we use for this dev container can be found at [./.devcontainer/Dockerfile](./.devcontainer/Dockerfile). To run it locally it requires docker to be installed, you can also run it in a cloud based code editor, for a list of supported editors/cloud editors see [the following webpage.](https://containers.dev/supporting)

To run for the first time on a local VSCode editor (a slightly more detailed and better guide on the [VSCode website](https://code.visualstudio.com/docs/devcontainers/tutorial)):
1. Ensure docker is running.
2. Ensure the VSCode [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension is installed in your VSCode editor.
3. Open the command pallete `CMD + SHIFT + P` and then select `Dev Containers: Rebuild and Reopen in Container`

You should now have everything you need to develop, `uv`, `node`, `npx`, `yarn`, `make`, for VSCode various extensions like `Pylance`, etc.

If you have any trouble see the [VSCode website.](https://code.visualstudio.com/docs/devcontainers/tutorial).

#### Local

To run locally first ensure you have the following tools installted locally:
* [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python packaging and development. (version `0.9.6`)
* [node](https://nodejs.org/en/download) using `nvm` with `yarn`. (version `24`). **After installing this run the following** `cd docs && corepack use yarn` it install the correct version of `yarn`.
* [make](https://www.gnu.org/software/make/) (OPTIONAL) for automation of tasks, not strictly required but makes life easier.
  * Ubuntu: `apt-get install make`
  * Mac: [Xcode command line tools](https://mac.install.guide/commandlinetools/4) includes `make` else you can use [brew.](https://formulae.brew.sh/formula/make)
  * Windows: Various solutions proposed in this [blog post](https://earthly.dev/blog/makefiles-on-windows/) on how to install on Windows, inclduing `Cygwin`, and `Windows Subsystem for Linux`.

When developing on the project you will want to install the Python package locally in editable format with all the extra requirements, this can be done like so:

```bash
uv sync
```

### Running linters and tests

This code base uses isort, flake8 and mypy to ensure that the format of the code is consistent and contain type hints. ISort and mypy settings can be found within [./pyproject.toml](./pyproject.toml) and the flake8 settings can be found in [./.flake8](./.flake8). To run these linters:

``` bash
make lint
```

To run the tests with code coverage (**NOTE** these are the code coverage tests that the Continuos Integration (CI) reports at the top of this README, the doc tests are not part of this report):

``` bash
make tests
```

To run the [doc tests](https://docs.python.org/3/library/doctest.html), these are tests to ensure that examples within the documentation run as expected:

``` bash
make doc-tests
```

### Setting a different default python version

The default or recommended Python version is shown in [.python-version](./.python-version, currently `3.12`, this can be changed using the [uv command](https://docs.astral.sh/uv/reference/cli/#uv-python-pin):

``` bash
uv python pin
# uv python pin 3.13
```

## Team

PyMUSAS is an open-source project that has been created and funded by the [University Centre for Computer Corpus Research on Language](https://ucrel.lancs.ac.uk/) (UCREL) at [Lancaster University](https://www.lancaster.ac.uk/). For more information on who has contributed to this code base see the [contributions page.](https://github.com/UCREL/pymusas/graphs/contributors) 