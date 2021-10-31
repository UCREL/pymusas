<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><strong>.rule_based</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rule_based.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.rule_based.USASRuleBasedTagger"></a>

## USASRuleBasedTagger

```python
class USASRuleBasedTagger:
 | ...
 | def __init__(
 |     self,
 |     lexicon_lookup: Optional[Dict[str, List[str]]] = None,
 |     lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None
 | ) -> None
```

The USAS Rule Based Tagger is based around the
[USAS Semantic Lexicon(s).](https://github.com/UCREL/Multilingual-USAS)
The Tagger expects two Lexicon like data structure, both in the format of
`Dict[str, List[str]]`, this structure maps a lemma (with or without it's
Part Of Speech (POS)) to a `List` of USAS semantic tags. The easiest way
of producing such a data structure is through
[`pymusas.lexicon_collection.from_tsv`](/pymusas/api/lexicon_collection/#from_tsv)
whereby the TSV file path would be to a USAS Semantic Lexicon.

The class requires two Lexicon data structure the first, `lexicon_lookup`,
requires both the lemma and POS, whereas the second, `lemma_lexicon_lookup`,
only requires the lemma.

Using these lexicon lookups the following rules are applied to assign a
`List` of USAS semantic tags from the lexicon lookups to the given tokens
in the given text. The text given is assumed to have been tokenised,
lemmatised, and POS tagged:

**Rules:**

1. If `POS==punc` label as `PUNCT`
2. Lookup token and POS tag
3. Lookup lemma and POS tag
4. Lookup lower case token and POS tag
5. Lookup lower case lemma and POS tag
6. if `POS==num` label as `N1`
7. Lookup token with any POS tag and choose first entry in lexicon.
8. Lookup lemma with any POS tag and choose first entry in lexicon.
9. Lookup lower case token with any POS tag and choose first entry in lexicon.
10. Lookup lower case lemma with any POS tag and choose first entry in lexicon.
11. Label as `Z99`, this is the unmatched semantic tag.

<h4 id="usasrulebasedtagger.parameters">Parameters<a className="headerlink" href="#usasrulebasedtagger.parameters" title="Permanent link">&para;</a></h4>


- __lexicon\_lookup__ : `Optional[List[str]]`, optional (default = `None`) <br/>
    The lexicon data structure with both lemma and POS information mapped to
    a `List` of USAS semantic tags e.g. `{'car_noun': ['Z2', 'Z1']}`
- __lemma\_lexicon\_lookup__ : `Optional[List[str]]`, optional (default = `None`) <br/>
    The lexicon data structure with only lemma information mapped to
    a `List` of USAS semantic tags e.g. `{'car': ['Z2', 'Z1']}`

<h4 id="usasrulebasedtagger.attributes">Attributes<a className="headerlink" href="#usasrulebasedtagger.attributes" title="Permanent link">&para;</a></h4>


- __lexicon\_lookup__ : `Dict[str, List[str]]` <br/>
    The given `lexicon_lookup` data, if that was `None` then this becomes
    an empty dictionary e.g. `{}`
- __lemma\_lexicon\_lookup__ : `Dict[str, List[str]]` <br/>
    The given `lemma_lexicon_lookup` data, if that was `None` then this
    becomes an empty dictionary e.g. `{}`

<h4 id="usasrulebasedtagger.examples">Examples<a className="headerlink" href="#usasrulebasedtagger.examples" title="Permanent link">&para;</a></h4>

``` python
 from pymusas.lexicon_collection import LexiconCollection
 from pymusas.taggers.rule_base import USASRuleBasedTagger
 welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
 lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
 lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
 tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
```

<a id="pymusas.taggers.rule_based.USASRuleBasedTagger.tag_token"></a>

### tag\_token

```python
class USASRuleBasedTagger:
 | ...
 | def tag_token(token: Tuple[str, str, str]) -> List[str]
```

Given a tokens with the relevant lingustic information it returns
a list of possible USAS semantic tags, tagged according
to the tagger's rules (see class doc string for tagger's rules). The
first semantic tag in the `List` of tags is the most likely tag.

<h4 id="tag_token.parameters">Parameters<a className="headerlink" href="#tag_token.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `List[Tuple[str, str, str]]` <br/>
    Each tuple represents a token. The tuple must contain the
    following lingustic information per token;
    1. Full text form e.g. `cars`
    2. Lemma/base form e.g. `car`
    3. Part Of Speech e.g. `Noun`

<h4 id="tag_token.returns">Returns<a className="headerlink" href="#tag_token.returns" title="Permanent link">&para;</a></h4>


- `List[str]` <br/>

<a id="pymusas.taggers.rule_based.USASRuleBasedTagger.tag_tokens"></a>

### tag\_tokens

```python
class USASRuleBasedTagger:
 | ...
 | def tag_tokens(
 |     self,
 |     tokens: Iterable[Tuple[str, str, str]]
 | ) -> Iterator[List[str]]
```

Given a list/iterable of tokens with the relevant lingustic
information it returns for each token a list of possible USAS semantic
tags, tagged according to the tagger's rules (see class doc string for
tagger's rules). The first semantic tag in the `List` of tags is the
most likely tag.

<h4 id="tag_tokens.parameters">Parameters<a className="headerlink" href="#tag_tokens.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `Iterable[Tuple[str, str, str]]` <br/>
    Each tuple represents a token. The tuple must contain the
    following lingustic information per token;
    1. Full text form e.g. `cars`
    2. Lemma/base form e.g. `car`
    3. Part Of Speech e.g. `Noun`

<h4 id="tag_tokens.returns">Returns<a className="headerlink" href="#tag_tokens.returns" title="Permanent link">&para;</a></h4>


- `Iterator[List[str]]` <br/>

