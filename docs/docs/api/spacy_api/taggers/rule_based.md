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
from tempfile import TemporaryDirectory
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
tagger = USASRuleBasedTagger()
tagger.lexicon_lookup = {'example|noun': ['A1']}
with TemporaryDirectory() as temp_dir:
...     tagger.to_disk(temp_dir)
...     assert Path(temp_dir, 'lexicon_lookup.json').exists()
...     assert not Path(temp_dir, 'lemma_lexicon_lookup.json').exists()
...     assert not Path(temp_dir, 'pos_mapper.json').exists()
```

