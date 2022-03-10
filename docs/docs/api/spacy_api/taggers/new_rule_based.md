<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><i>.taggers</i><strong>.new_rule_based</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/taggers/new_rule_based.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.spacy_api.taggers.new_rule_based.RuleBasedTagger"></a>

## RuleBasedTagger

```python
class RuleBasedTagger:
 | ...
 | def __init__(
 |     self,
 |     pymusas_tags_token_attr: str = 'pymusas_tags',
 |     pos_attribute: str = 'pos_',
 |     lemma_attribute: str = 'lemma_'
 | ) -> None
```

[spaCy pipeline component](https://spacy.io/usage/processing-pipelines)
of the [`pymusas.taggers.new_rule_based.RuleBasedTagger`](/pymusas/api/taggers/new_rule_based/#rulebasedtagger).

This component applies one or more [`pymusas.taggers.rules.rule.Rule`](/pymusas/api/taggers/rules/rule/#rule)s
to create a list of possible candidate tags for each token in the sequence.
Each candidate, represented as a
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object, for each
token is then Ranked using a
[`pymusas.rankers.lexicon_entry.LexiconEntryRanker`](/pymusas/api/rankers/lexicon_entry/#lexiconentryranker) ranker. The best
candidate and it's associated tag(s) for each token are then returned along
with a `List` of token indexes indicating if the token is part of a Multi
Word Expression (MWE).

**NOTE** this tagger has been designed to be flexible with the amount of
resources avaliable, for example if you do not have a POS tagger or
lemmatiser in your spaCy pipeline this ok, but you will need to assign
an empty String to the `pos_attribute` or `lemma_attribute` respectively
before calling this component in the spaCy pipeline.

<h4 id="rulebasedtagger.assigned_attributes">Assigned Attributes<a className="headerlink" href="#rulebasedtagger.assigned_attributes" title="Permanent link">&para;</a></h4>


The component assigns the predicted tags to each spaCy [Token](https://spacy.io/api/token) under
`Token._.pymusas_tags` attribute by default, this can be changed with the
`pymusas_tags_token_attr` parameter to another attribute of
the `Token._`, e.g. if `pymusas_tags_token_attr=semantic_tags` then the attribute
the predicted tags will be assigned to for each token will be `Token._.semantic_tags`.

| Location             | Type        | Value                                                                    |
|----------------------|-------------|--------------------------------------------------------------------------|
| Token._.pymusas_tags | `List[str]` | Prediced tags, the first tag in the List of tags is the most likely tag. |

<h4 id="rulebasedtagger.config_and_implementation">Config and implementation<a className="headerlink" href="#rulebasedtagger.config_and_implementation" title="Permanent link">&para;</a></h4>


The default config is defined by the pipeline component factory and describes
how the component should be configured. You can override its settings via the `config`
argument on [nlp.add_pipe](https://spacy.io/api/language#add_pipe) or in your
[config.cfg for training](https://spacy.io/usage/training#config).

| Setting                 | Description                  |
|-------------------------|------------------------------|
| pymusas_tags_token_attr | See parameters section below |
| pos_attribute           | See parameters section below |
| lemma_attribute         | See parameters section below |

<h4 id="rulebasedtagger.parameters">Parameters<a className="headerlink" href="#rulebasedtagger.parameters" title="Permanent link">&para;</a></h4>


- __pymusas\_tags\_token\_attr__ : `str`, optional (default = `pymusas_tags`) <br/>
    The name of the attribute to assign the predicted tags too under
    the `Token._` class.

- __pos\_attribute__ : `str`, optional (default = `pos_`) <br/>
    The name of the attribute that the Part Of Speech (POS) tag is assigned too
    within the `Token` class. The POS tag value that comes from this attribute
    has to be of type `str`. With the current default we take the POS tag
    from `Token.pos_`. The POS tag can be an empty string if you do not require
    POS information or if you do not have a POS tagger. **NOTE** that if you
    do not have a POS tagger the default value for `Token.pos_` is an empty
    string.

- __lemma\_attribute__ : `str`, optional (default = `lemma_`) <br/>
    The name of the attribute that the lemma is assigned too within the `Token`
    class. The lemma value that comes from this attribute has to be of
    type `str`. With the current default we take the lemma from `Token.lemma_`.
    The lemma can be an empty string if you do not require
    lemma information or if you do not have a lemmatiser. **NOTE** that if you
    do not have a lemmatiser the default value for `Token.lemma_` is an empty
    string.

<h4 id="rulebasedtagger.instance_attributes">Instance Attributes<a className="headerlink" href="#rulebasedtagger.instance_attributes" title="Permanent link">&para;</a></h4>


- __pymusas\_tags\_token\_attr__ : `str`, optional (default = `pymusas_tags`) <br/>

- __pos\_attribute__ : `str`, optional (default = `pos_`) <br/>

- __lemma\_attribute__ : `str`, optional (default = `lemma_`) <br/>

<h4 id="rulebasedtagger.examples">Examples<a className="headerlink" href="#rulebasedtagger.examples" title="Permanent link">&para;</a></h4>


``` python
import spacy
from pymusas.spacy_api.taggers import rule_based
# Construction via spaCy pipeline
nlp = spacy.blank('en')
# Using default config
tagger = nlp.add_pipe('usas_tagger')
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

<a id="pymusas.spacy_api.taggers.new_rule_based.RuleBasedTagger.__call__"></a>

### \_\_call\_\_

```python
class RuleBasedTagger:
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

<a id="pymusas.spacy_api.taggers.new_rule_based.RuleBasedTagger.to_bytes"></a>

### to\_bytes

```python
class RuleBasedTagger:
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

<a id="pymusas.spacy_api.taggers.new_rule_based.RuleBasedTagger.from_bytes"></a>

### from\_bytes

```python
class RuleBasedTagger:
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

<a id="pymusas.spacy_api.taggers.new_rule_based.RuleBasedTagger.to_disk"></a>

### to\_disk

```python
class RuleBasedTagger:
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

<a id="pymusas.spacy_api.taggers.new_rule_based.RuleBasedTagger.from_disk"></a>

### from\_disk

```python
class RuleBasedTagger:
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

