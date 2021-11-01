# Contributing

## Making a pull request

* If your pull requests involves contributing to the docstrings, see the guidance below on [writing docstrings](#writing-docstrings), then you need to test if the documentation can build without error (all of the make commands apart from `create-api-docs` require **docker**, for more information on these make commands see the [website section below](#website)):

```bash
make create-api-docs # This command automatically generates the API documentation that the website serves
make build-docs
```

If it does fail, you can serve the documentation locally:

``` bash
make develop-docs
```

If the error message is not clear, feel free to comment on this in your pull request.

### Changing / Updating Python requirements

If you are changing the Python requirements, this needs to be done in a few different places:

1. If it is a development only requirement, not required to run the core code base within [./pymusas](./pymusas), then update:
    * [./dev_requirements.txt](./dev_requirements.txt)
    * [./binder/environment.yml](./binder/environment.yml)
    * [The `tests` section of ./setup.cfg](./setup.cfg)
2. If it is a requirement that is needed to run the core code base within [./pymusas](./pymusas), then update:
    * [./requirements.txt](./requirements.txt)
    * [./binder/environment.yml](./binder/environment.yml)
    * [The `install_requires` section of ./setup.cfg](./setup.cfg)

In all cases you may need to add this requirement to the `tool.isort` section `known_third_party` list of the [./pyproject.toml file.](./pyproject.toml) 

### Writing docstrings
[A lot of this has been copied from the AllenNLP CONTRIBUTING guidelines, which I think are really great!](https://github.com/allenai/allennlp/blob/main/CONTRIBUTING.md)

Our docstrings are written in a syntax that is essentially just Markdown with additional special syntax for writing parameter descriptions and linking to within project modules, classes, and functions.

Class docstrings should start with a description of the class, followed by a `# Parameters` section that lists the names, types, and purpose of all parameters to the class's `__init__()` method.

Parameter descriptions should look like:

```
name : `type`
    Description of the parameter, indented by four spaces.
```

Optional parameters can also be written like this:

```
name : Optional[`type`], optional (default = `default_value`)
    Description of the parameter, indented by four spaces.
```

Sometimes you can omit the description if the parameter is self-explanatory.

Method and function docstrings are similar, but should also include a `# Returns` section when the return value is not obvious. Other valid sections are

- `# Attributes`, for listing class attributes. These should be formatted in the same
    way as parameters.
- `# Raises`, for listing any errors that the function or method might intentionally raise.
- `# Examples`, where you can include code snippets -- these code snippets will be tested using [doctest with pytest](https://docs.pytest.org/en/6.2.x/doctest.html), these tests ensure that the example code snippet will run as expected, if the example is not expected to output anything leave a blank like between the last `>>>` line and ``` as shown in the [example below](#example-docstring). For more information on doctest see the [doctest documentation](https://docs.python.org/3/library/doctest.html)

To create hyper links to within project modules, classes, and functions write:

- :class:`pymusas.basic_tagger.RuleBasedTagger`
- :mod:`pymusas.basic_tagger`
- :func:`pymusas.file_utils.download_url_file`

If the within project reference is within the same file you do not have to include the project or modules names, for example the above could be re-written like so:

- :class:`RuleBasedTagger`
- :mod:`basic_tagger`
- :func:`download_url_file`

#### Example docstrings

##### Class
```
The USAS Rule Based Tagger is based around the
[USAS Semantic Lexicon(s).](https://github.com/UCREL/Multilingual-USAS)
The Tagger expects two Lexicon like data structure, both in the format of
`Dict[str, List[str]]`, this structure maps a lemma (with or without it's
Part Of Speech (POS)) to a `List` of USAS semantic tags. The easiest way
of producing such a data structure is through
:func:`pymusas.lexicon_collection.from_tsv`
whereby the TSV file path would be to a USAS Semantic Lexicon.

The class requires two Lexicon data structure the first, `lexicon_lookup`,
requires both the lemma and POS, whereas the second, `lemma_lexicon_lookup`,
only requires the lemma.

Using these lexicon lookups the following rules are applied to assign a
`List` of USAS semantic tags from the lexicon lookups to the given tokens
in the given text. The text given is assumed to have been tokenised,
lemmatised, and POS tagged:

**Rules:**

1. If `POS==punc` label as `PUNCT`
2. Lookup token and POS tag
3. Lookup lemma and POS tag
4. Lookup lower case token and POS tag
5. Lookup lower case lemma and POS tag
6. if `POS==num` label as `N1`
7. Lookup token with any POS tag and choose first entry in lexicon.
8. Lookup lemma with any POS tag and choose first entry in lexicon.
9. Lookup lower case token with any POS tag and choose first entry in lexicon.
10. Lookup lower case lemma with any POS tag and choose first entry in lexicon.
11. Label as `Z99`, this is the unmatched semantic tag.

# Parameters

lexicon_lookup : `Optional[List[str]]`, optional (default = `None`)
    The lexicon data structure with both lemma and POS information mapped to
    a `List` of USAS semantic tags e.g. `{'car_noun': ['Z2', 'Z1']}`
lemma_lexicon_lookup : `Optional[List[str]]`, optional (default = `None`)
    The lexicon data structure with only lemma information mapped to
    a `List` of USAS semantic tags e.g. `{'car': ['Z2', 'Z1']}`

# Attributes

lexicon_lookup : `Dict[str, List[str]]`
    The given `lexicon_lookup` data, if that was `None` then this becomes
    an empty dictionary e.g. `{}`
lemma_lexicon_lookup : `Dict[str, List[str]]`
    The given `lemma_lexicon_lookup` data, if that was `None` then this
    becomes an empty dictionary e.g. `{}`

# Examples
``` python
>>> from pymusas.lexicon_collection import LexiconCollection
>>> from pymusas.taggers.rule_based import USASRuleBasedTagger
>>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
>>> lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
>>> lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
>>> tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)

\`\`\` 
```
## Website

The documentation is built with [docusaurus v2](https://docusaurus.io/), a static site generator that is based on the [Jamstack](https://jamstack.org/) with pages generated through markup and can be enhanced using Javascript e.g. React components.

The only part of the website that is automatically generated are the API pages, this is done through the: `make create-api-docs` command. These API pages are stored in the [./docs/docs/api folder](./docs/docs/api)

The pages that can be added too are the documentation pages of which these should be something like a guide or usage example page to help the user's better understand and get started using the code base. These can be written using markdown with or without React components (for more details on how to write a documentation [page](https://docusaurus.io/docs/create-doc), more [advance guide](https://docusaurus.io/docs/markdown-features)). The documentation pages should be stored in the [./docs/docs/documentation folder](./docs/docs/documentation).

### Commands

**Note**: all of the commands require docker.

By default when running the documentation website locally it is hosted at: [http://localhost:3000/pymusas/](http://localhost:3000/pymusas/)

The website is ran using a node based docker container, dockerfile that is used can be found at [./Docs_Docker.dockerfile](./Docs_Docker.dockerfile)


* To run the docs locally in development mode: `make develop-docs`
* To build the documentation files: `make build-docs`
* To build the static documentation files and serve them locally: `make serve-built-docs`
* To generate the API pages from the code base: `make create-api-docs`
* To create the documentation website from scratch (this should never be needed but just in case it does): `make create-docs`