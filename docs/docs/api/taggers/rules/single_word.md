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
 |     lexicon_collection: Dict[str, List[str]],
 |     lemma_lexicon_collection: Dict[str, List[str]],
 |     pos_mapper: Optional[Dict[str, List[str]]] = None
 | )
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


- __lexicon\_collection__ : `Dict[str, List[str]]` <br/>
    The data to create `lexicon_collection` instance attribute. A
    Dictionary where the keys are a combination of
    lemma/token and POS in the following format: `{lemma}|{POS}` and the
    values are a list of associated semantic tags.
- __lemma\_lexicon\_collection__ : `Dict[str, List[str]]` <br/>
    The data to create `lemma_lexicon_collection` instance attribute. A
    Dictionary where the keys are either just a lemma/token
    in the following format: `{lemma}` and the
    values are a list of associated semantic tags.
- __pos\_mapper__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>
    If not `None`, maps from the given token's POS tagset to the desired
    POS tagset, whereby the mapping is a `List` of tags, at the moment there
    is no preference order in this list of POS tags. The POS mapping is
    useful in situtation whereby the token's POS tagset is different to
    those used in the lexicons. **Note** the longer the `List[str]` for
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
- __pos\_mapper__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>
    The given `pos_mapper`.

<a id="pymusas.taggers.rules.single_word.SingleWordRule.__call__"></a>

### \_\_call\_\_

```python
class SingleWordRule(Rule):
 | ...
 | def __call__(
 |     self,
 |     tokens: List[str],
 |     lemmas: List[str],
 |     pos_tags: List[str]
 | ) -> List[List[RankingMetaData]]
```

Given the tokens, lemmas, and POS tags for each word in a text,
it returns for each token a `List` of rules matches defined by
the [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata)
object based on the rule matches stated in the class docstring above.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `List[str]` <br/>
    The tokens that are within the text.
- __lemmas__ : `List[str]` <br/>
    The lemmas of the tokens.
- __pos\_tags__ : `List[str]` <br/>
    The Part Of Speech tags of the tokens.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[List[RankingMetaData]]` <br/>

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

