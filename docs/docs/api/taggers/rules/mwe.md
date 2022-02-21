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
 | def __init__(mwe_lexicon_lookup: Dict[str, List[str]]) -> None
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

<h4 id="mwerule.instance_attributes">Instance Attributes<a className="headerlink" href="#mwerule.instance_attributes" title="Permanent link">&para;</a></h4>


- __mwe\_lexicon\_collection__ : `pymusas.lexicon_collection.MWELexiconCollection` <br/>
    A [`pymusas.lexicon_collection.MWELexiconCollection`](/pymusas/api/lexicon_collection/#mwelexiconcollection) instance that
    has been initialised using the `data` parameter. This collection is used
    to find MWE rule matches.

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
the [`pymusas.rankers.lexicon_entry.RankingMetaData`](/pymusas/api/rankers/lexicon_entry/#rankingmetadata) object based on
the rule matches states in the class docstring above.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `List[str]` <br/>
    The tokens that are within the text.
- __lemmas__ : `List[str]` <br/>
    The lemmas of the tokens.
- __pos\_tags__ : `List[str]` <br/>
    The Part Of Speech tags of the tokens.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[List[RankingMetaData]]` <br/>

