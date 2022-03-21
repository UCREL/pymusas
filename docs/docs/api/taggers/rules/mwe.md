<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><i>.rules</i><strong>.mwe</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rules/mwe.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.rules.mwe.MWERule"></a>

## MWERule

```python
class MWERule(Rule):
 | ...
 | def __init__(
 |     self,
 |     mwe_lexicon_lookup: Dict[str, List[str]],
 |     pos_mapper: Optional[Dict[str, List[str]]] = None
 | ) -> None
```

A Multi Word Expression (MWE) rule match can be one of the following matches:

1. `MWE_NON_SPECIAL` match - whereby the combined token/lemma and POS
is found within the given MWE Lexicon Collection (`self.mwe_lexicon_collection`).
2. `MWE_WILDCARD` match - whereby the combined token/lemma and POS matches
a wildcard MWE template that is within the MWE Lexicon Collection
(`self.mwe_lexicon_collection`).

All rule matches use the
`pymusas.lexicon_collection.MWELexiconCollection.mwe_match`
method for matching. Matches are found based on the original token/lemma and
lower cased versions of the token/lemma.

<h4 id="mwerule.parameters">Parameters<a className="headerlink" href="#mwerule.parameters" title="Permanent link">&para;</a></h4>


- __mwe\_lexicon\_lookup__ : `Dict[str, List[str]]` <br/>
    The data to create `mwe_lexicon_collection` instance attribute. A
    Dictionary where the keys are MWE templates, of any
    [`pymusas.lexicon_collection.LexiconType`](/pymusas/api/lexicon_collection/#lexicontype),
    and the values are a list of associated semantic tags.
- __pos\_mapper__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>
    If not `None`, maps from the `mwe_lexicon_lookup` POS tagset to the
    desired POS tagset,whereby the mapping is a `List` of tags,
    at the moment there is no preference order in this list of POS tags.
    **Note** the longer the `List[str]` for
    each POS mapping the slower the tagger, a one to one mapping will have
    no speed impact on the tagger. A selection of POS mappers can be found in
    [`pymusas.pos_mapper`](/pymusas/api/pos_mapper).

<h4 id="mwerule.instance_attributes">Instance Attributes<a className="headerlink" href="#mwerule.instance_attributes" title="Permanent link">&para;</a></h4>


- __mwe\_lexicon\_collection__ : `pymusas.lexicon_collection.MWELexiconCollection` <br/>
    A [`pymusas.lexicon_collection.MWELexiconCollection`](/pymusas/api/lexicon_collection/#mwelexiconcollection) instance that
    has been initialised using the `mwe_lexicon_lookup` and `pos_mapper`
    parameters. This collection is used to find MWE rule matches.

<a id="pymusas.taggers.rules.mwe.MWERule.__call__"></a>

### \_\_call\_\_

```python
class MWERule(Rule):
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
the [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object based on
the rule matches stated in the class docstring above.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `List[str]` <br/>
    The tokens that are within the text.
- __lemmas__ : `List[str]` <br/>
    The lemmas of the tokens.
- __pos\_tags__ : `List[str]` <br/>
    The Part Of Speech tags of the tokens.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[List[RankingMetaData]]` <br/>

<a id="pymusas.taggers.rules.mwe.MWERule.to_bytes"></a>

### to\_bytes

```python
class MWERule(Rule):
 | ...
 | def to_bytes() -> bytes
```

Serialises the [`MWERule`](#mwerule) to a bytestring.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.taggers.rules.mwe.MWERule.from_bytes"></a>

### from\_bytes

```python
class MWERule(Rule):
 | ...
 | @staticmethod
 | def from_bytes(bytes_data: bytes) -> "MWERule"
```

Loads [`MWERule`](#mwerule) from the given bytestring and returns it.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`MWERule`](#mwerule) <br/>

