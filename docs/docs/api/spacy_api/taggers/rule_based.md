<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><i>.taggers</i><strong>.rule_based</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/taggers/rule_based.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger"></a>

## USASRuleBasedTagger

```python
class USASRuleBasedTagger:
 | ...
 | def __init__(
 |     self,
 |     usas_tags_token_attr: str = 'usas_tags',
 |     pos_attribute: str = 'pos_',
 |     lemma_attribute: str = 'lemma_'
 | ) -> None
```

[spaCy pipeline component](https://spacy.io/usage/processing-pipelines)
for rule based USAS tagger.

This component allows you to add [USAS semantic tags](http://ucrel.lancs.ac.uk/usas/)
to each spaCy [Token](https://spacy.io/api/token), whereby these USAS tags
have been predicted through the following [rules](#usasrulebasedtagger.rules), all of these rules depend on
two Lexicon like data structures, the `lexicon_lookup` and the `lemma_lexicon_lookup`.
Both of these lexicons are of type `Dict[str, List[str]]` which map a lemma
(with or without it's Part Of Speech (POS) ) to a `List` of USAS tags. The
first semantic tag in the `List` of tags is the most likely tag.

Furthermore, the optional POS mapper, `pos_mapper`, is used in this tagger when the POS tagset
within the lexicons does not match the tagset used by the POS model, which has
preceding this tagger in the spaCy pipeline. The POS mapper is expected to
map from the tagset of the POS model to the tagset of the lexicons, whereby the
mapping is a one-to-many mapping. The first tag in the `List` is assumed to be the
most relevant and the last to be the least. Some pre-compiled Dictionaries can be
found in the [`pymusas.pos_mapper`](/pymusas/api/pos_mapper) module, e.g. the UPOS to USAS
core [`pymusas.pos_mapper.UPOS_TO_USAS_CORE`](/pymusas/api/pos_mapper/#upos_to_usas_core).

<h4 id="usasrulebasedtagger.rules">Rules<a className="headerlink" href="#usasrulebasedtagger.rules" title="Permanent link">&para;</a></h4>


1. **If `pos_mapper` is not `None`**, map the POS, from the POS model,
to the first POS value in the `List` from the `pos_mapper`s `Dict`. **If** the
`pos_mapper` cannot map the POS, from the POS model, go to step 9.
2. If `POS==punc` label as `PUNCT`
3. Lookup token and POS tag
4. Lookup lemma and POS tag
5. Lookup lower case token and POS tag
6. Lookup lower case lemma and POS tag
7. if `POS==num` label as `N1`
8. **If there is another POS value in the `pos_mapper`** go back to step 2
with this new POS value else carry on to step 9.
9. Lookup token with any POS tag and choose first entry in lexicon.
10. Lookup lemma with any POS tag and choose first entry in lexicon.
11. Lookup lower case token with any POS tag and choose first entry in lexicon.
12. Lookup lower case lemma with any POS tag and choose first entry in lexicon.
13. Label as `Z99`, this is the unmatched semantic tag.

**NOTE** this tagger has been designed to be flexible with the amount of
resources avaliable, if you do not have a POS tagger in the spaCy pipeline
it will not use POS information. If you do not have a lexicon file with
POS information then `lexicon_lookup` will be an empty `Dict`. However, the fewer
resources avaliable, less rules, stated above, will be applied making the
tagger less effective.

<h4 id="usasrulebasedtagger.assigned_attributes">Assigned Attributes<a className="headerlink" href="#usasrulebasedtagger.assigned_attributes" title="Permanent link">&para;</a></h4>


The component assigns the predicted USAS tags to each spaCy [Token](https://spacy.io/api/token) under
`Token._.usas_tags` attribute by default, this can be changed with the
`usas_tags_token_attr` parameter to another attribute of
the `Token._`, e.g. if `usas_tags_token_attr=semantic_tags` then the attribute
the USAS tags will be assigned to for each token will be `Token._.semantic_tags`.

| Location | Type | Value |
|----------|------|-------|
| Token._.usas_tags | `List[str]` | Prediced USAS tags, the first semantic tag in the List of tags is the most likely tag. |

<h4 id="usasrulebasedtagger.config_and_implementation">Config and implementation<a className="headerlink" href="#usasrulebasedtagger.config_and_implementation" title="Permanent link">&para;</a></h4>


The default config is defined by the pipeline component factory and describes
how the component should be configured. You can override its settings via the `config`
argument on [nlp.add_pipe](https://spacy.io/api/language#add_pipe) or in your
[config.cfg for training](https://spacy.io/usage/training#config).

| Setting | Description |
|---------|-------------|
| usas_tags_token_attr | See parameters section below |
| pos_attribute | See parameters section below |
| lemma_attribute | See parameters section below |

<h4 id="usasrulebasedtagger.parameters">Parameters<a className="headerlink" href="#usasrulebasedtagger.parameters" title="Permanent link">&para;</a></h4>


- __usas\_tags\_token\_attr__ : `str`, optional (default = `usas_tags`) <br/>
    The name of the attribute to assign the predicted USAS tags too under
    the `Token._` class.

- __pos\_attribute__ : `str`, optional (default = `pos_`) <br/>
    The name of the attribute that the Part Of Speech (POS) tag is assigned too
    within the `Token` class. The POS tag value that comes from this attribute
    has to be of type `str`. With the current default we take the POS tag
    from `Token.pos_`

- __lemma\_attribute__ : `str`, optional (default = `lemma_`) <br/>
    The name of the attribute that the lemma is assigned too within the `Token`
    class. The lemma value that comes from this attribute has to be of
    type `str`. With the current default we take the lemma from `Token.lemma_`

<h4 id="usasrulebasedtagger.instance_attributes">Instance Attributes<a className="headerlink" href="#usasrulebasedtagger.instance_attributes" title="Permanent link">&para;</a></h4>


- __usas\_tags\_token\_attr__ : `str`, optional (default = `usas_tags`) <br/>

- __pos\_attribute__ : `str`, optional (default = `pos_`) <br/>

- __lemma\_attribute__ : `str`, optional (default = `lemma_`) <br/>

- __lexicon\_lookup__ : `Dict[str, List[str]]` <br/>
    The lexicon data structure with both lemma and POS information mapped
    to a `List` of USAS semantic tags e.g. `{'Car|noun': ['Z2', 'Z1']}`.
    By default this is an empty `Dict`, but can be added to either by setting
    it, e.g. `self.leixcon_lookup={'Car|noun': ['Z1']}` or through adding to
    the existing dictionary, e.g. `self.lexicon_lookup['Car|noun'] = ['Z1']`

- __lemma\_lexicon\_lookup__ : `Dict[str, List[str]]` <br/>
    The lexicon data structure with only lemma information mapped to a
    `List` of USAS semantic tags e.g. `{'Car': ['Z2', 'Z1']}`.
    By default this is an empty `Dict`, but can be added to either by setting
    it, e.g. `self.lemma_leixcon_lookup={'Car': ['Z1']}` or through adding to
    the existing dictionary, e.g. `self.lemma_lexicon_lookup['Car'] = ['Z1']`

- __pos\_mapper__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>
    If not `None`, maps from the POS model tagset to the lexicon data POS
    tagset, whereby the mapping is a `List` of tags, the first in the list is
    assumed to be the most relevant and the last to be the least.

<h4 id="usasrulebasedtagger.examples">Examples<a className="headerlink" href="#usasrulebasedtagger.examples" title="Permanent link">&para;</a></h4>


``` python
import spacy
from pymusas.spacy_api.taggers import rule_based
# Construction via spaCy pipeline
nlp = spacy.blank('en')
tagger = nlp.add_pipe('usas_tagger') # Using default config
tagger.lemma_lexicon_lookup = {'car': ['Z1']}
token = nlp('car')
assert token[0]._.usas_tags == ['Z1']

# Construction from class, same defaults as the default config
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
tagger = USASRuleBasedTagger()

# Custom config
custom_config = {'usas_tags_token_attr': 'semantic_tags'}
nlp = spacy.blank('en')
tagger = nlp.add_pipe('usas_tagger', config=custom_config)
tagger.lemma_lexicon_lookup = {'car': ['Z1']}
token = nlp('car')
assert token[0]._.semantic_tags == ['Z1']
```

<a id="pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.__call__"></a>

### \_\_call\_\_

```python
class USASRuleBasedTagger:
 | ...
 | def __call__(doc: Doc) -> Doc
```

Applies the tagger to the spaCy document, modifies it in place, and
returns it. This usually happens under the hood when the `nlp` object is
called on a text and all pipeline components are applied to the `Doc` in
order.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __doc__ : `Doc` <br/>
    A [spaCy `Doc`](https://spacy.io/api/doc)

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `Doc` <br/>

<a id="pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.to_bytes"></a>

### to\_bytes

```python
class USASRuleBasedTagger:
 | ...
 | def to_bytes(
 |     self,
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> bytes
```

Serialises the USAS tagger's lexicon lookups and POS mapper to a bytestring.

<h4 id="to_bytes.parameters">Parameters<a className="headerlink" href="#to_bytes.parameters" title="Permanent link">&para;</a></h4>


- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<h4 id="to_bytes.examples">Examples<a className="headerlink" href="#to_bytes.examples" title="Permanent link">&para;</a></h4>


```python
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
tagger = USASRuleBasedTagger()
tagger_bytes = tagger.to_bytes()
```

<a id="pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.from_bytes"></a>

### from\_bytes

```python
class USASRuleBasedTagger:
 | ...
 | def from_bytes(
 |     self,
 |     bytes_data: bytes,
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> "USASRuleBasedTagger"
```

This modifies the USASRuleBasedTagger in place and returns it. It loads
in the data from the given bytestring.

The easiest way to generate a bytestring to load from is through the
[`to_bytes`](#to_bytes) method.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`USASRuleBasedTagger`](#usasrulebasedtagger) <br/>

<h4 id="from_bytes.examples">Examples<a className="headerlink" href="#from_bytes.examples" title="Permanent link">&para;</a></h4>


```python
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
custom_lexicon = {'example|noun': ['A1']}
tagger = USASRuleBasedTagger()
tagger.lexicon_lookup = custom_lexicon
tagger_bytes = tagger.to_bytes()
new_tagger = USASRuleBasedTagger()
_ = new_tagger.from_bytes(tagger_bytes)
assert new_tagger.lexicon_lookup == tagger.lexicon_lookup
```

<a id="pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.to_disk"></a>

### to\_disk

```python
class USASRuleBasedTagger:
 | ...
 | def to_disk(
 |     self,
 |     path: Union[str, Path],
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> None
```

Saves the follwing information, if it exists, to the given `path`, we assume the `path`
is an existing directory.

* `lexicon_lookup` -- as a JSON file at the following path `path/lexicon_lookup.json`
* `lemma_lexicon_lookup` -- as a JSON file at the following path `path/lemma_lexicon_lookup.json`
* `pos_mapper` -- as a JSON file at the following path `path/pos_mapper.json`

<h4 id="to_disk.parameters">Parameters<a className="headerlink" href="#to_disk.parameters" title="Permanent link">&para;</a></h4>


- __path__ : `Union[str, Path]` <br/>
    Path to an existing direcotry. Path may be either strings or `Path`-like objects.

- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="to_disk.returns">Returns<a className="headerlink" href="#to_disk.returns" title="Permanent link">&para;</a></h4>


- `None` <br/>

<h4 id="to_disk.examples">Examples<a className="headerlink" href="#to_disk.examples" title="Permanent link">&para;</a></h4>


```python
from pathlib import Path
from tempfile import TemporaryDirectory
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
tagger = USASRuleBasedTagger()
tagger.lexicon_lookup = {'example|noun': ['A1']}
with TemporaryDirectory() as temp_dir:
    tagger.to_disk(temp_dir)
    assert Path(temp_dir, 'lexicon_lookup.json').exists()
    assert not Path(temp_dir, 'lemma_lexicon_lookup.json').exists()
    assert not Path(temp_dir, 'pos_mapper.json').exists()
```

<a id="pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger.from_disk"></a>

### from\_disk

```python
class USASRuleBasedTagger:
 | ...
 | def from_disk(
 |     self,
 |     path: Union[str, Path],
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> "USASRuleBasedTagger"
```

Loads the following information in place and returns the USASRuleBasedTagger
from the given `path`, we assume the `path` is an existing directory.
None of the following information is required to exist and no error or
debug information will be raised or outputted if it does not exist.

* `lexicon_lookup` -- loads from the following path `path/lexicon_lookup.json`
* `lemma_lexicon_lookup` --  loads from the following path `path/lemma_lexicon_lookup.json`
* `pos_mapper` -- loads from the following path `path/pos_mapper.json`

<h4 id="from_disk.parameters">Parameters<a className="headerlink" href="#from_disk.parameters" title="Permanent link">&para;</a></h4>


- __path__ : `Union[str, Path]` <br/>
    Path to an existing direcotry. Path may be either strings or `Path`-like objects.

- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="from_disk.returns">Returns<a className="headerlink" href="#from_disk.returns" title="Permanent link">&para;</a></h4>


- [`USASRuleBasedTagger`](#usasrulebasedtagger) <br/>

<h4 id="from_disk.examples">Examples<a className="headerlink" href="#from_disk.examples" title="Permanent link">&para;</a></h4>


```python
from tempfile import TemporaryDirectory
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
tagger = USASRuleBasedTagger()
tagger.lexicon_lookup = {'example|noun': ['A1']}
new_tagger = USASRuleBasedTagger()
with TemporaryDirectory() as temp_dir:
    tagger.to_disk(temp_dir)
    _ = new_tagger.from_disk(temp_dir)

assert new_tagger.lexicon_lookup == tagger.lexicon_lookup
assert new_tagger.pos_mapper is None
```

