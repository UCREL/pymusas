<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><i>.rules</i><strong>.single_word</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rules/single_word.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.rules.single_word.SingleWordRule"></a>

## SingleWordRule

```python
class SingleWordRule(Rule):
 | ...
 | def __init__(
 |     self,
 |     lexicon_collection: dict[str, list[str]],
 |     lemma_lexicon_collection: dict[str, list[str]],
 |     pos_mapper: dict[str, list[str]] | None = None
 | ) -> None
```

A single word rule match, is a rule that matches on single word lexicon
entries. Entires can be matched on:

1. Token and the token's Part Of Speech (POS) tag, e.g. `driving|adj`
2. Lemma and the lemma's POS tag, e.g. `drive|adj`
3. Token, e.g. `driving`
4. Lemma, e.g. `drive`

In all cases matches are found based on the original token/lemma and lower
cased versions of the token/lemma. These matches are found through searching
the `lexicon_collection` and `lemma_lexicon_collection` attributes.


<h4 id="singlewordrule.parameters">Parameters<a className="headerlink" href="#singlewordrule.parameters" title="Permanent link">&para;</a></h4>


- __lexicon\_collection__ : `dict[str, list[str]]` <br/>
    The data to create `lexicon_collection` instance attribute. A
    Dictionary where the keys are a combination of
    lemma/token and POS in the following format: `{lemma}|{POS}` and the
    values are a list of associated semantic tags.
- __lemma\_lexicon\_collection__ : `dict[str, list[str]]` <br/>
    The data to create `lemma_lexicon_collection` instance attribute. A
    Dictionary where the keys are either just a lemma/token
    in the following format: `{lemma}` and the
    values are a list of associated semantic tags.
- __pos\_mapper__ : `dict[str, list[str]]`, optional (default = `None`) <br/>
    If not `None`, maps from the given token's POS tagset to the desired
    POS tagset, whereby the mapping is a `list` of tags, at the moment there
    is no preference order in this list of POS tags. The POS mapping is
    useful in situtation whereby the token's POS tagset is different to
    those used in the lexicons. **Note** the longer the `list[str]` for
    each POS mapping the slower the tagger, a one to one mapping will have
    no speed impact on the tagger. A selection of POS mappers can be found in
    [`pymusas.pos_mapper`](/pymusas/api/pos_mapper).

<h4 id="singlewordrule.instance_attributes">Instance Attributes<a className="headerlink" href="#singlewordrule.instance_attributes" title="Permanent link">&para;</a></h4>


- __lexicon\_collection__ : `pymusas.lexicon_collection.LexiconCollection` <br/>
    A [`pymusas.lexicon_collection.LexiconCollection`](/pymusas/api/lexicon_collection/#lexiconcollection) instance that
    has been initialised using the `lexicon_collection` parameter.
- __lemma\_lexicon\_collection__ : `pymusas.lexicon_collection.LexiconCollection` <br/>
    A [`pymusas.lexicon_collection.LexiconCollection`](/pymusas/api/lexicon_collection/#lexiconcollection) instance that
    has been initialised using the `lemma_lexicon_collection` parameter.
- __pos\_mapper__ : `dict[str, list[str]]`, optional (default = `None`) <br/>
    The given `pos_mapper`.

<a id="pymusas.taggers.rules.single_word.SingleWordRule.__call__"></a>

### \_\_call\_\_

```python
class SingleWordRule(Rule):
 | ...
 | def __call__(
 |     self,
 |     tokens: list[str],
 |     lemmas: list[str],
 |     pos_tags: list[str]
 | ) -> list[list[RankingMetaData]]
```

Given the tokens, lemmas, and POS tags for each word in a text,
it returns for each token a `list` of rules matches defined by
the [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata)
object based on the rule matches stated in the class docstring above.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `list[str]` <br/>
    The tokens that are within the text.
- __lemmas__ : `list[str]` <br/>
    The lemmas of the tokens.
- __pos\_tags__ : `list[str]` <br/>
    The Part Of Speech tags of the tokens.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `list[list[RankingMetaData]]` <br/>

<a id="pymusas.taggers.rules.single_word.SingleWordRule.best_match"></a>

### best\_match

```python
class SingleWordRule(Rule):
 | ...
 | def best_match(
 |     self,
 |     token: str,
 |     lemma: str,
 |     pos_tag: str
 | ) -> RankingMetaData | None
```

Returns the best single word rule match for the given token, lemma, and
POS tag, or `None` if there is no match. The matches are found using
[`__call__`](#__call__) and ranked using
[`pymusas.rankers.single_word.SingleWordRanker`](/pymusas/api/rankers/single_word/#singlewordranker).

<h4 id="best_match.parameters">Parameters<a className="headerlink" href="#best_match.parameters" title="Permanent link">&para;</a></h4>


- __token__ : `str` <br/>
    The token.
- __lemma__ : `str` <br/>
    The lemma of the token.
- __pos\_tag__ : `str` <br/>
    The Part Of Speech tag of the token.

<h4 id="best_match.returns">Returns<a className="headerlink" href="#best_match.returns" title="Permanent link">&para;</a></h4>


- `RankingMetaData | None` <br/>

<h4 id="best_match.examples">Examples<a className="headerlink" href="#best_match.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.taggers.rules.single_word import SingleWordRule
rule = SingleWordRule({'act|ADJ': ['A1']}, {'acting': ['A2']})
best_match = rule.best_match('acting', 'act', 'ADJ')
assert best_match is not None
assert ('A1',) == best_match.semantic_tags
assert rule.best_match('style', 'style', 'NOUN') is None
```

<a id="pymusas.taggers.rules.single_word.SingleWordRule.to_bytes"></a>

### to\_bytes

```python
class SingleWordRule(Rule):
 | ...
 | def to_bytes() -> bytes
```

Serialises the [`SingleWordRule`](#singlewordrule) to a bytestring.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.taggers.rules.single_word.SingleWordRule.from_bytes"></a>

### from\_bytes

```python
class SingleWordRule(Rule):
 | ...
 | @staticmethod
 | def from_bytes(bytes_data: bytes) -> "SingleWordRule"
```

Loads [`SingleWordRule`](#singlewordrule) from the given bytestring and returns it.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`SingleWordRule`](#singlewordrule) <br/>

<a id="pymusas.taggers.rules.single_word.SingleWordRule.__eq__"></a>

### \_\_eq\_\_

```python
class SingleWordRule(Rule):
 | ...
 | def __eq__(other: object) -> bool
```

Given another object to compare too it will return `True` if the other
object is the same class and initialised using with the same argument
values.

<h4 id="__eq__.parameters">Parameters<a className="headerlink" href="#__eq__.parameters" title="Permanent link">&para;</a></h4>


- __other__ : `object` <br/>
    The object to compare too.

<h4 id="__eq__.returns">Returns<a className="headerlink" href="#__eq__.returns" title="Permanent link">&para;</a></h4>


- `True` <br/>

