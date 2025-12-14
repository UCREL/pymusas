<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><i>.taggers</i><strong>.rule_based</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/taggers/rule_based.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger"></a>

## RuleBasedTagger

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def __init__(
 |     self,
 |     name: str = 'pymusas_rule_based_tagger',
 |     pymusas_tags_token_attr: str = 'pymusas_tags',
 |     pymusas_mwe_indexes_attr: str = 'pymusas_mwe_indexes',
 |     pos_attribute: str = 'pos_',
 |     lemma_attribute: str = 'lemma_'
 | ) -> None
```

[spaCy pipeline component](https://spacy.io/usage/processing-pipelines)
of the [`pymusas.taggers.rule_based.RuleBasedTagger`](/pymusas/api/taggers/rule_based/#rulebasedtagger).

This component applies one or more [`pymusas.taggers.rules.rule.Rule`](/pymusas/api/taggers/rules/rule/#rule)s
to create a list of possible candidate tags for each token in the sequence.
Each candidate, represented as a
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object, for each
token is then Ranked using a
[`pymusas.rankers.lexicon_entry.LexiconEntryRanker`](/pymusas/api/rankers/lexicon_entry/#lexiconentryranker) ranker. The best
candidate and it's associated tag(s) for each token are then assigned to the
`Token._.pymusas_tags` attribute in addition a `List` of token indexes
indicating if the token is part of a Multi Word Expression (MWE) is assigned
to the `Token._.pymusas_mwe_indexes`.

If we cannot tag a token then the following process will happen:
1. If the token's POS tag is in `default_punctuation_tags` then it will assign the
tag `PUNCT`.
2. If the token's POS tag is in `default_number_tags` then it will assign the tag
`N1`.
3. Assign the default tag `Z99`.

**NOTE** this tagger has been designed to be flexible with the amount of
resources avaliable, for example if you do not have a POS tagger or
lemmatiser in your spaCy pipeline this ok, just use the default
`pos_attribute` and `lemma_attribute`.

<h4 id="rulebasedtagger.assigned_attributes">Assigned Attributes<a className="headerlink" href="#rulebasedtagger.assigned_attributes" title="Permanent link">&para;</a></h4>


<table>
    <tr>
        <th> Location </th>
        <th> Type </th>
        <th> Value </th>
    </tr>
    <tr>
        <td> Token._.pymusas_tags </td>
        <td> `List[str]` </td>
        <td> Prediced tags, the first tag in the List of tags is the
        most likely tag.</td>
    </tr>
    <tr>
        <td> Token._.pymusas_mwe_indexes </td>
        <td> `List[Tuple[int, int]]` </td>
        <td> Each `Tuple` indicates the start and end token index of the
        associated Multi Word Expression (MWE). If the `List` contains
        more than one `Tuple` then the MWE is discontinuous. For single word
        expressions the `List` will only contain 1 `Tuple` which will be
        (token_start_index, token_start_index + 1).</td>
    </tr>
</table>

<h4 id="rulebasedtagger.config_and_implementation">Config and implementation<a className="headerlink" href="#rulebasedtagger.config_and_implementation" title="Permanent link">&para;</a></h4>


The default config is defined by the pipeline component factory and describes
how the component should be configured. You can override its settings via the `config`
argument on [nlp.add_pipe](https://spacy.io/api/language#add_pipe) or in your
[config.cfg for training](https://spacy.io/usage/training#config).

| Setting                  | Description                  |
|--------------------------|------------------------------|
| pymusas_tags_token_attr  | See parameters section below |
| pymusas_mwe_indexes_attr | See parameters section below |
| pos_attribute            | See parameters section below |
| lemma_attribute          | See parameters section below |

<h4 id="rulebasedtagger.parameters">Parameters<a className="headerlink" href="#rulebasedtagger.parameters" title="Permanent link">&para;</a></h4>


- __name__ : `str`, optional (default = `pymusas_rule_based_tagger`) <br/>
    The component name. Defaults to the same name as the class variable
    `COMPONENT_NAME`.
- __pymusas\_tags\_token\_attr__ : `str`, optional (default = `pymusas_tags`) <br/>
    The name of the attribute to assign the predicted tags too under
    the `Token._` class.
- __pymusas\_mwe\_indexes\_attr__ : `str`, optional (default = `pymusas_mwe_indexes`) <br/>
    The name of the attribute to assign the start and end token index of the
    associated MWE too under the `Token._` class.
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


- __name__ : `str` <br/>
    The component name.
- __rules__ : `List[pymusas.taggers.rules.rule.Rule]`, optional (default = `None`) <br/>
    The `rules` is set through the [`initialize`](#initialize) method. Before it is
    set by the [`initialize`](#initialize) method the value of this attribute is `None`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker`, optional (default = `None`) <br/>
    The `ranker` is set through the [`initialize`](#initialize) method. Before it is
    set by the [`initialize`](#initialize) method the value of this attribute is `None`.
- __default\_punctuation\_tags__ : `Set[str]` <br/>
    The `default_punctuation_tags` is set through the [`initialize`](#initialize) method.
- __default\_number\_tags__ : `Set[str]` <br/>
    The `default_number_tags` is set through the [`initialize`](#initialize) method.
- __pymusas\_tags\_token\_attr__ : `str`, optional (default = `pymusas_tags`) <br/>
    The given `pymusas_tags_token_attr`
- __pymusas\_mwe\_indexes\_attr__ : `str`, optional (default = `pymusas_mwe_indexes`) <br/>
    The given `pymusas_mwe_indexes_attr`
- __pos\_attribute__ : `str`, optional (default = `pos_`) <br/>
    The given `pos_attribute`
- __lemma\_attribute__ : `str`, optional (default = `lemma_`) <br/>
    The given `lemma_attribute`

<h4 id="rulebasedtagger.class_attributes">Class Attributes<a className="headerlink" href="#rulebasedtagger.class_attributes" title="Permanent link">&para;</a></h4>


- __COMPONENT\_NAME__ : `str` <br/>
    Name of component factory that this component is registered under. This
    is used as the first argument to
    [`Language.add_pipe`](https://spacy.io/api/language#add_pipe)
    if you want to add this component to your spaCy pipeline.

<h4 id="rulebasedtagger.examples">Examples<a className="headerlink" href="#rulebasedtagger.examples" title="Permanent link">&para;</a></h4>


``` python
import spacy
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.pos_mapper import BASIC_CORCENCC_TO_USAS_CORE
from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
# Construction via spaCy pipeline
nlp = spacy.blank('en')
# Using default config
single_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Welsh/semantic_lexicon_cy.tsv'
single_lexicon = LexiconCollection.from_tsv(single_lexicon_url)
single_lemma_lexicon = LexiconCollection.from_tsv(single_lexicon_url,
                                                  include_pos=False)
single_rule = SingleWordRule(single_lexicon, single_lemma_lexicon,
                             pos_mapper=BASIC_CORCENCC_TO_USAS_CORE)
rules = [single_rule]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
tagger = nlp.add_pipe('pymusas_rule_based_tagger')
tagger.rules = rules
tagger.ranker = ranker
token = nlp('aberth')
assert token[0]._.pymusas_tags == ['S9', 'A9-']
assert token[0]._.pymusas_mwe_indexes == [(0, 1)]
# Custom config
custom_config = {'pymusas_tags_token_attr': 'semantic_tags',
                 'pymusas_mwe_indexes_attr': 'mwe_indexes'}
nlp = spacy.blank('en')
tagger = nlp.add_pipe('pymusas_rule_based_tagger', config=custom_config)
tagger.rules = rules
tagger.ranker = ranker
token = nlp('aberth')
assert token[0]._.semantic_tags == ['S9', 'A9-']
assert token[0]._.mwe_indexes == [(0, 1)]
```

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger.COMPONENT_NAME"></a>

#### COMPONENT\_NAME

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | COMPONENT_NAME = 'pymusas_rule_based_tagger'
```

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger.initialize"></a>

### initialize

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def initialize(
 |     self,
 |     get_examples: Optional[Callable[[], Iterable[Example]]] = None,
 |     *,
 |     nlp: Optional[Language] = None,
 |     rules: Optional[List[Rule]] = None,
 |     ranker: Optional[LexiconEntryRanker] = None,
 |     default_punctuation_tags: Optional[List[str]] = None,
 |     default_number_tags: Optional[List[str]] = None
 | ) -> None
```

Initialize the tagger and load any of the resources given. The method is
typically called by
[`Language.initialize`](https://spacy.io/api/language#initialize)
and lets you customize arguments it receives via the
[`initialize.components`](https://spacy.io/api/data-formats#config-initialize)
block in the config. The loading only happens during initialization,
typically before training. At runtime, all data is load from disk.

<h4 id="initialize.parameters">Parameters<a className="headerlink" href="#initialize.parameters" title="Permanent link">&para;</a></h4>


- __rules__ : `List[pymusas.taggers.rules.rule.Rule]` <br/>
    A list of rules to apply to the sequence of tokens in the
    [`__call__`](#__call__). The output from each rule is concatenated and given
    to the `ranker`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker` <br/>
    A ranker to rank the output from all of the `rules`.
- __default\_punctuation\_tags__ : `List[str]`, optional (default = `None`) <br/>
    The POS tags that represent punctuation. If `None` then we will use
    `['punc']`. The list will be converted into a `Set` before assigning
    to the `default_punctuation_tags` attribute.
- __default\_number\_tags__ : `List[str]`, optional (default = `None`) <br/>
    The POS tags that represent numbers. If `None` then we will use
    `['num']`. The list will be converted into a `Set` before assigning
    to the `default_number_tags` attribute.

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger.__call__"></a>

### \_\_call\_\_

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
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

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger.to_bytes"></a>

### to\_bytes

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def to_bytes(
 |     self,
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> bytes
```

Serialises the tagger to a bytestring.

<h4 id="to_bytes.parameters">Parameters<a className="headerlink" href="#to_bytes.parameters" title="Permanent link">&para;</a></h4>


- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<h4 id="to_bytes.examples">Examples<a className="headerlink" href="#to_bytes.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
tagger = RuleBasedTagger()
tagger.initialize(rules=rules, ranker=ranker)
tagger_bytes = tagger.to_bytes()
```

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger.from_bytes"></a>

### from\_bytes

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def from_bytes(
 |     self,
 |     bytes_data: bytes,
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> "RuleBasedTagger"
```

Loads the tagger from the given bytestring in place and returns it.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.
- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`RuleBasedTagger`](#rulebasedtagger) <br/>

<h4 id="from_bytes.examples">Examples<a className="headerlink" href="#from_bytes.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
tagger = RuleBasedTagger()
tagger.initialize(rules=rules, ranker=ranker)
# Create a new tagger, tagger 2
tagger_2 = RuleBasedTagger()
# Show that it is not the same as the original tagger
assert tagger_2.rules != rules
# Tagger 2 will now load in the data from the original tagger
_ = tagger_2.from_bytes(tagger.to_bytes())
assert tagger_2.rules == rules
assert tagger_2.ranker == ranker
```

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger.to_disk"></a>

### to\_disk

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def to_disk(
 |     self,
 |     path: Union[str, Path],
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> None
```

Serialises the tagger to the given `path`.

<h4 id="to_disk.parameters">Parameters<a className="headerlink" href="#to_disk.parameters" title="Permanent link">&para;</a></h4>


- __path__ : `Union[str, Path]` <br/>
    Path to a direcotry. Path may be either string or `Path`-like
    object. If the directory does not exist it attempts to create a
    directory at the given `path`.

- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="to_disk.returns">Returns<a className="headerlink" href="#to_disk.returns" title="Permanent link">&para;</a></h4>


- `None` <br/>

<h4 id="to_disk.examples">Examples<a className="headerlink" href="#to_disk.examples" title="Permanent link">&para;</a></h4>


```python
from pathlib import Path
from tempfile import TemporaryDirectory
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
tagger = RuleBasedTagger()
tagger.initialize(rules=rules, ranker=ranker)
with TemporaryDirectory() as temp_dir:
    _ = tagger.to_disk(temp_dir)

```

<a id="pymusas.spacy_api.taggers.rule_based.RuleBasedTagger.from_disk"></a>

### from\_disk

```python
class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def from_disk(
 |     self,
 |     path: Union[str, Path],
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> "RuleBasedTagger"
```

Loads the tagger from the given `path` in place and returns it.

<h4 id="from_disk.parameters">Parameters<a className="headerlink" href="#from_disk.parameters" title="Permanent link">&para;</a></h4>


- __path__ : `Union[str, Path]` <br/>
    Path to an existing direcotry. Path may be either string or
    `Path`-like object.

- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="from_disk.returns">Returns<a className="headerlink" href="#from_disk.returns" title="Permanent link">&para;</a></h4>


- [`RuleBasedTagger`](#rulebasedtagger) <br/>

<h4 id="from_disk.examples">Examples<a className="headerlink" href="#from_disk.examples" title="Permanent link">&para;</a></h4>


```python
from pathlib import Path
from tempfile import TemporaryDirectory
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
tagger = RuleBasedTagger()
tagger.initialize(rules=rules, ranker=ranker)
# Create an empty second tagger
tagger_2 = RuleBasedTagger()
assert tagger_2.rules is None
with TemporaryDirectory() as temp_dir:
    _ = tagger.to_disk(temp_dir)
    _ = tagger_2.from_disk(temp_dir)

assert tagger_2.rules is not None
assert tagger_2.rules == tagger.rules
```

