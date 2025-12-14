# Contributing

## Making a pull request

* If your pull requests involves contributing to the docstrings, see the guidance below on [writing docstrings](#writing-docstrings), then you need to test if the documentation can build without error (all of the make commands apart from `create-api-docs` require [docker](https://docs.docker.com/), for more information on these make commands see the [website section below](#website)):

```bash
make create-api-docs # This command automatically generates the API documentation that the website serves
make build-docs
```

If it does fail, you can serve the documentation locally:

``` bash
make develop-docs
```

If the error message is not clear, feel free to comment on this in your pull request.

The last part of any pull request is to update the [CHANGELOG](./CHANGELOG.md) with notes of your contribution in the "Unreleased" section at the top of the markdown file.

### Changing / Updating Python requirements

If you are changing/updating a core requirement i.e. a requirement needed to run `pymusas` see [#core](#core) else if it is only for development of the project see [#development](#development).

**Note**:

1. In all cases you may need to add this requirement to the `tool.isort` section `known_third_party` list of the [./pyproject.toml file.](./pyproject.toml).
2. Add the requirement to [./binder/environment.yml](./binder/environment.yml)

#### Core

``` bash
uv add REQUIREMENT
```

#### Development

``` bash
uv add --dev REQUIREMENT
```

#### Extra

``` bash
uv add --optional EXTRA_NAME REQUIREMENT
```

For example to add a requirement to the extra `neural`

``` bash
uv add --optional neural REQUIREMENT
```

### Writing docstrings
[A lot of this has been copied from the AllenNLP CONTRIBUTING guidelines, which I think are really great!](https://github.com/allenai/allennlp/blob/main/CONTRIBUTING.md)

Our docstrings are written in a syntax that is essentially just Markdown with additional special syntax for writing parameter descriptions and linking to within project modules, classes, functions, and attributes.

#### Class docstrings

Class docstrings should start with a description of the class, followed by a `# Parameters` section that lists the names, types, and purpose of all parameters to the class's `__init__()` method. In addition the class docstring should list both the class and instance level attributes using the `# Class Attributes` and `# Instance Attributes` sections, if any such attributes exists.

When the class is created using a [dataclass decorator](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass) and the `# Parameters` to the `__init__` are the same as the `# Instance Attributes`, only write the `# Instance Attributes` section and leave a note just before the section stating they are the same, for example.

``` markdown
**Note** the parameters to the __init__ are the same as the Instance Attributes.

# Instance Attributes
```

#### Module docstrings

Module docstrings can start with a description of the module, within that description it can include an `# Attributes` section that lists the (global) variables that can be accessed through the module. In some case the `# Attributes` you list do not have to be a complete list, but rather a list of the attributes that need explaining.

#### Method and Function docstrings

Method and function docstrings should on their first sentence/paragraph describe what it does and what the return value is (if it returns anything).

#### Valid docstring sections

1. `# Parameters`, should like:

``` markdown
# Parameters

name : `type`
    Description of the parameter, indented by four spaces.
```

Optional parameters can also be written like this:

``` markdown
# Parameters

name : `type`, optional (default = `default_value`)
    Description of the parameter, indented by four spaces.
```

Sometimes you can omit the description if the parameter is self-explanatory.

2. `# Attributes`, for listing attributes within a **module** docstring. These should be formatted in the same way as parameters.
3. `# Class Attributes` and `# Instance Attributes`, for listing class and instance attributes within a **class** docstring. These should be formatted in the same way as parameters.
4. `# Raises`, for listing any errors that the function or method might intentionally raise.
5. `# Examples`, where you can include code snippets -- these code snippets will be tested using [doctest with pytest](https://docs.pytest.org/en/6.2.x/doctest.html), these tests ensure that the example code snippet will run as expected, if the example is not expected to output anything leave a blank like between the last `>>>` line and ``` as shown in the following example for `# Examples`

```` markdown
# Examples

``` python
>>> from pymusas.lexicon_collection import LexiconCollection
>>> from pymusas.taggers.rule_based import USASRuleBasedTagger
>>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
>>> lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
>>> lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
>>> tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)

``` 
````

The above expects no output as there is a blank line between `>>> tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)` and ```.

However the example below expects the output of the last line to be `'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'` **Note** that there is a new line between the expected output and ```.

```` markdown
# Examples

``` python
>>> from pymusas.lexicon_collection import LexiconCollection
>>> from pymusas.taggers.rule_based import USASRuleBasedTagger
>>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
>>> welsh_lexicon_url
'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'

``` 
````

We also have a custom way of including a blank line, this is achieved by using an ellipsis, `...`, without any whitespace after it, as shown in the example below after the following line `_ = new_tagger.from_disk(temp_dir)`:

```` markdown
# Examples

```python
>>> from tempfile import TemporaryDirectory
>>> from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
>>> tagger = USASRuleBasedTagger()
>>> tagger.lexicon_lookup = {'example|noun': ['A1']}
>>> new_tagger = USASRuleBasedTagger()
>>> with TemporaryDirectory() as temp_dir:
...     tagger.to_disk(temp_dir)
...     _ = new_tagger.from_disk(temp_dir)
...
>>> assert new_tagger.lexicon_lookup == tagger.lexicon_lookup
>>> assert new_tagger.pos_mapper is None

```
````
The blank line is required after an indentation block so that if a user copies and pastes this example block of code, from the [API documentation website](https://ucrel.github.io/pymusas/api/file_utils), into a Python interpreter/REPL it will run smoothly without syntax error.

For more information on doctest see the [doctest documentation](https://docs.python.org/3/library/doctest.html)


#### Within project class, module, function, and attribute linking

To create hyper links to within project modules, classes, functions, and variables write:

- :class:\`pymusas.basic_tagger.RuleBasedTagger\`
- :mod:\`pymusas.basic_tagger\`
- :func:\`pymusas.file_utils.download_url_file\`
- :var:\`pymusas.config.PYMUSAS_CACHE_HOME\`

If the within project reference is within the same file you do not have to include the project or modules names, for example the above could be re-written like so:

- :class:\`RuleBasedTagger\`
- :mod:\`basic_tagger\`
- :func:\`download_url_file\`
- :var:\`PYMUSAS_CACHE_HOME\`

**To note** in some cases if you are trying to link to a method, you can do this using `:func:` but sometimes it requires you to remove the class name, this is not perfect as you can have two classes in a module with 2 identical naming methods, of which I do not know how to solve this issue yet but we have not had a need yet to solve this.

#### Example docstrings

TO DO.

## Website

The documentation is built with [docusaurus v3.9.2](https://docusaurus.io/), a static site generator that is based on the [Jamstack](https://jamstack.org/) with pages generated through markup and can be enhanced using Javascript e.g. React components.

The only part of the website that is automatically generated are the API pages, this is done through the: `make create-api-docs` command. These API pages are stored in the [./docs/docs/api folder](./docs/docs/api)

The pages that can be added too are the usage pages of which these should be something like a guide or use case example page to help the users better understand and get started using the code base. These can be written using markdown with or without React components (for more details on how to write a documentation [page](https://docusaurus.io/docs/create-doc), a link to a more [advance guide](https://docusaurus.io/docs/markdown-features)). The usage pages should be stored in the [./docs/docs/usage](./docs/docs/usage/).

### Commands

**Note**: we are assuming that you are running these commands either within the dev container or have installed locally yarn. For more information on how to setup either of these see the development setup part of the README.

By default when running the documentation website locally it is hosted at: [http://localhost:3000/pymusas/](http://localhost:3000/pymusas/)

* To run the docs locally in development mode: `make develop-docs`
* To build the documentation files: `make docs/build`
* To build the static documentation files and serve them locally: `make serve-built-docs`
* To generate the API pages from the code base: `make create-api-docs`


To update to the latest docusaurs version, the easiest way is to (before doing this ensure that any changes you have not committed to git within `./docs` have been committed.):

(Does require you to enter `y` to proceed when creating the docusaurus website directory)
```
make create-docs
```