<div className="source-div">
 <p><i>pymusas</i><i>.rankers</i><strong>.single_word</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/rankers/single_word.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.rankers.single_word.SingleWordRanker"></a>

## SingleWordRanker

```python
class SingleWordRanker
```

A stateless ranker that ranks the single word lexicon entry matches of
**one** token, represented by a `List` of
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) objects, e.g. the
matches returned by [`pymusas.taggers.rules.single_word.SingleWordRule`](/pymusas/api/taggers/rules/single_word/#singlewordrule)
for one token.

Matches are ranked using the single word ranking rules of
[`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`](/pymusas/api/rankers/lexicon_entry/#contextualrulebasedranker), as the other
rules are the same for all single word matches of one token:

1. Matches that use POS information are ranked lower than those that do not. (Contextual Rule Based Ranker rule 4).
2. Matches on Token < Lemma < Lower cased token < Lower cased lemma. (Contextual Rule Based Ranker rule 5).

**Lower ranked matches should be given priority.** As the ranker has no
state it does not need to be created or serialised, all methods are static.

<h4 id="singlewordranker.examples">Examples<a className="headerlink" href="#singlewordranker.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.rankers.single_word import SingleWordRanker
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexical_match import LexicalMatch
lemma_pos = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                            False, LexicalMatch.LEMMA, 0, 1,
                            'act|ADJ', ('A1',))
token_no_pos = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                               True, LexicalMatch.TOKEN, 0, 1,
                               'acting', ('A2',))
assert lemma_pos == SingleWordRanker.best_match([token_no_pos, lemma_pos])
assert SingleWordRanker.best_match([]) is None
```

<a id="pymusas.rankers.single_word.SingleWordRanker.sort_key"></a>

### sort\_key

```python
class SingleWordRanker:
 | ...
 | @staticmethod
 | def sort_key(match: RankingMetaData) -> Tuple[bool, int]
```

Returns the key used to rank the given single word `match`, a lower key
is a better ranked match. It can be used as the `key` argument of
`sorted`, `min`, etc.

<h4 id="sort_key.parameters">Parameters<a className="headerlink" href="#sort_key.parameters" title="Permanent link">&para;</a></h4>


- __match__ : `RankingMetaData` <br/>
    A single word lexicon entry match.

<h4 id="sort_key.returns">Returns<a className="headerlink" href="#sort_key.returns" title="Permanent link">&para;</a></h4>


- `Tuple[bool, int]` <br/>

<a id="pymusas.rankers.single_word.SingleWordRanker.best_match"></a>

### best\_match

```python
class SingleWordRanker:
 | ...
 | @staticmethod
 | def best_match(
 |     matches: List[RankingMetaData]
 | ) -> Optional[RankingMetaData]
```

Returns the lowest ranked, best, single word match from the given
`matches` of one token, or `None` if `matches` is empty. When matches
are joint ranked the first of those matches in `matches` is returned.

<h4 id="best_match.parameters">Parameters<a className="headerlink" href="#best_match.parameters" title="Permanent link">&para;</a></h4>


- __matches__ : `List[RankingMetaData]` <br/>
    The single word lexicon entry matches of one token.

<h4 id="best_match.returns">Returns<a className="headerlink" href="#best_match.returns" title="Permanent link">&para;</a></h4>


- `Optional[RankingMetaData]` <br/>

