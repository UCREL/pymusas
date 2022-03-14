<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><strong>.utils</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/utils.py">[SOURCE]</a></p>
</div>
<div></div>

---

Helper functions for anything [spaCy](https://spacy.io/) related in the code
base.

<a id="pymusas.spacy_api.utils.set_custom_token_extension"></a>

### set\_custom\_token\_extension

```python
def set_custom_token_extension(extension_name: str) -> None
```

Defines a custom attribute of the spaCy Token which becomes avaliable
via `Token._.{extension_name}`. The difference between this and using the
spaCy [Token.set_extension method](https://spacy.io/api/token#set_extension)
is this method will check if the extension exists already and if so will force it
through and output a log message that it has had to force this through.

<h4 id="set_custom_token_extension.parameters">Parameters<a className="headerlink" href="#set_custom_token_extension.parameters" title="Permanent link">&para;</a></h4>


- __extension\_name__ : `str` <br/>
    Name of the custom attribute that will become avaliable through
    `Token._.{extension_name}`.

<a id="pymusas.spacy_api.utils.update_factory_attributes"></a>

### update\_factory\_attributes

```python
def update_factory_attributes(
    factory_name: str,
    new_attribute_name: str,
    old_attribute_name: str
) -> None
```

Updates the [spaCy Language required attributes meta information](https://spacy.io/api/language#factorymeta)
for the given component, find through it's factory name,
by replacing the `old_attribute_name` with the `new_attribute_name`.

<h4 id="update_factory_attributes.parameters">Parameters<a className="headerlink" href="#update_factory_attributes.parameters" title="Permanent link">&para;</a></h4>


- __factory\_name__ : `str` <br/>
    The name of the component factory, e.g. `pymusas_rule_based_tagger`
- __new\_attribute\_name__ : `str` <br/>
    The name of the new `{new_attribute_name}` attribute that is
    required for this component. An example, `token.pos`
- __old\_attribute\_name__ : `str` <br/>
    The name of the `{old_attribute_name}` that is to be replaced with
    the `new_attribute_name`. An example, `token.tag`

