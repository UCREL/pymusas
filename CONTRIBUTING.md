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

Method and function docstrings are similar, but should also include a `# Returns`
section when the return value is not obvious. Other valid sections are

- `# Attributes`, for listing class attributes. These should be formatted in the same
    way as parameters.
- `# Raises`, for listing any errors that the function or method might intentionally raise.
- `# Examples`, where you can include code snippets.

To create hyper links to within project modules, classes, and functions write:

- :class:`pymusas.basic_tagger.RuleBasedTagger`
- :mod:`pymusas.basic_tagger`
- :func:`pymusas.file_utils.download_url_file`

If the within project reference is within the same file you do not have to include the project or modules names, for example the above could be re-written like so:

- :class:`RuleBasedTagger`
- :mod:`basic_tagger`
- :func:`download_url_file`
 

Here is an example of what the docstrings should look like in a class:

EXAMPLE TO BE GIVEN.