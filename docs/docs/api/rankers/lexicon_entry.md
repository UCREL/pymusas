<div className="source-div">
 <p><i>pymusas</i><i>.rankers</i><strong>.lexicon_entry</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/rankers/lexicon_entry.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.rankers.lexicon_entry.LexiconEntryRanker"></a>

## LexiconEntryRanker

```python
class LexiconEntryRanker(ABC)
```

An **abstract class** that defines the basic method, `__call__`, that is
required for all [`LexiconEntryRanker`](#lexiconentryranker)s.

Each lexicon entry match is represented by a
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object.

**Lower ranked lexicon entry matches should be given priority when making
tagging decisions. A rank of 0 is better than a rank of 1.**

A LexcionEntryRanker when called, `__call__`, returns a tuple of two `List`s
whereby each entry in the list corresponds to a token:

1. Contains the ranks of the lexicon entry matches as a `List[int]`.
**Note** that the `List` can be empty if a token has no lexicon entry matches.
2. An `Optional[RankingMetaData]` that is the global lowest ranked entry
match for that token. If the value is `None` then no global lowest ranked
entry can be found for that token. If the `RankingMetaData` represents more
than one token, like a Multi Word Expression (MWE) match, then those associated tokens
will have the same `RankingMetaData` object as the global lowest ranked entry match.

**The tagger will have to make a decision how to handle global lowest ranked
matches of value `None`, a suggested approach would be to assign an
unmatched/unknown semantic tag to those tokens.**

The reason for the adding the second list is that the **global** lowest
ranked match is not the same as the local/token lowest ranked match, this is
due to the potential of overlapping matches, e.g. `North East London brewery`
can have a match of `North East`, `North`, and `East London brewery` in this
case the lowest rank for `North` would be `North East`, but as we have a
lower match that uses `East` which is `East London brewery` then the
**global** lowest rank for `North` would be `North`.

<a id="pymusas.rankers.lexicon_entry.LexiconEntryRanker.__call__"></a>

### \_\_call\_\_

```python
class LexiconEntryRanker(ABC):
 | ...
 | @abstractmethod
 | def __call__(
 |     self,
 |     token_ranking_data: List[List[RankingMetaData]]
 | ) -> Tuple[List[List[int]], List[Optional[RankingMetaData]]]
```

For each token it returns a `List` of rankings for each lexicon entry
match and the optional [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata)
object of the **global** lowest ranked match for each token.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __token\_ranking\_data__ : `List[List[RankingMetaData]]` <br/>
    For each token a `List` of [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata)
    representing the lexicon entry match.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `Tuple[List[List[int]], List[Optional[RankingMetaData]]]` <br/>

<a id="pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker"></a>

## ContextualRuleBasedRanker

```python
class ContextualRuleBasedRanker(LexiconEntryRanker):
 | ...
 | def __init__(
 |     self,
 |     maximum_n_gram_length: int,
 |     maximum_number_wildcards: int
 | ) -> None
```

The contextual rule based ranker creates ranks based on the rules stated below.

Each lexicon entry match is represented by a
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object.

**Lower ranked lexicon entry matches should be given priority when making
tagging decisions. See the [`LexiconEntryRanker`](#lexiconentryranker) class docstring for
more details on the returned value of the `__call__` method.**

**Ranking Rules:**

The ranking of lexicon entires is based off the following rules, these rules
are based on the 6 heuristic stated at the top of column 2 on page 4 of
[Piao et al. 2003](https://aclanthology.org/W03-1807.pdf):

First we create an initial ranking based on lexicon entry type:

1. Multi Word Expression (MWE) entries ranked lower than single and Non-Special
entries are ranked lower than wild card entires.

Then within these rankings we further rank based on:

2. Longer entries, based on n-gram length, are ranked lower.
3. Entries with fewer wildcards are ranked lower.

Then we apply the following contextual ranking rules:

4. Whether the POS information was excluded in the match if so these are ranked
higher. This is only `True` when the match ignores the POS information for
single word lexicon entries. This is always `False` when used in a
MWE lexicon entry match.
5. Whether the lexicon entry was matched on Token < Lemma <
Lower cased token < Lower cased lemma. Token is the lowest ranked and lower
cased lemma is highest.
6. The lexicon entry that first appears in the text is ranked lowest,
this is required for matches that do not apply to the same sequence
of tokens.

In the case whereby the global lowest ranked lexicon entry match is joint
ranked with another entry then it is random which lexicon entry match is chosen.

<h4 id="contextualrulebasedranker.parameters">Parameters<a className="headerlink" href="#contextualrulebasedranker.parameters" title="Permanent link">&para;</a></h4>


- __maximum\_n\_gram\_length__ : `int` <br/>
    The largest n_gram rule match that will be encountered, e.g. a match
    of `ski_noun boot_noun` will have a n-gram length of 2.
- __maximum\_number\_wildcards__ : `int` <br/>
    The number of wildcards in the rule that contains the most wildcards, e.g.
    the rule `ski_* *_noun` would contain 2 wildcards. This can be 0 if you
    have no wildcard rules.

<h4 id="contextualrulebasedranker.instance_attributes">Instance Attributes<a className="headerlink" href="#contextualrulebasedranker.instance_attributes" title="Permanent link">&para;</a></h4>


- __n\_gram\_number\_indexes__ : `int` <br/>
    The number of indexes that each n-gram length value should have when
    converting the n-gram length to a string using
    `pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.int_2_str`.
- __wildcards\_number\_indexes__ : `int` <br/>
    The number of indexes that each wildcard count value should have when
    converting the wildcard count value to a string using
    `pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.int_2_str`.
- __n\_gram\_ranking\_dictionary__ : `Dict[int, int]` <br/>
    Maps the n-gram length to it's rank value, as the n-gram length is
    inverse to it's rank, as the larger the n-gram length the lower it's
    rank.

<a id="pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.get_construction_arguments"></a>

### get\_construction\_arguments

```python
class ContextualRuleBasedRanker(LexiconEntryRanker):
 | ...
 | @staticmethod
 | def get_construction_arguments(
 |     rules: List['Rule']
 | ) -> Tuple[int, int]
```

Given a `List` of rules it will return the `maximum_n_gram_length` and
`maximum_number_wildcards` from the lexicon collections that those
[`pymusas.taggers.rules.rule.Rule`](/pymusas/api/taggers/rules/rule/#rule)(s) are based on. The output from
this function can then be used as the arguments to the constructor of
[`ContextualRuleBasedRanker`](#contextualrulebasedranker).

<h4 id="get_construction_arguments.parameters">Parameters<a className="headerlink" href="#get_construction_arguments.parameters" title="Permanent link">&para;</a></h4>


- __rules__ : `List[Rule]` <br/>
    A `List` of rules. This `List` is typically required when creating
    a [`pymusas.taggers.new_rule_based.RuleBasedTagger`](/pymusas/api/taggers/new_rule_based/#rulebasedtagger) tagger.

<h4 id="get_construction_arguments.returns">Returns<a className="headerlink" href="#get_construction_arguments.returns" title="Permanent link">&para;</a></h4>


- `Tuple[int, int]` <br/>

<h4 id="get_construction_arguments.examples">Examples<a className="headerlink" href="#get_construction_arguments.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.mwe import MWERule
from pymusas.lexicon_collection import MWELexiconCollection
pt_mwe_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/mwe-pt.tsv"
mwe_dict = MWELexiconCollection.from_tsv(pt_mwe_lexicon_url)
mwe_rule = MWERule(mwe_dict)
ranker_construction_arguments = ContextualRuleBasedRanker.get_construction_arguments([mwe_rule])
ranker = ContextualRuleBasedRanker(*ranker_construction_arguments)
```

<a id="pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.int_2_str"></a>

### int\_2\_str

```python
class ContextualRuleBasedRanker(LexiconEntryRanker):
 | ...
 | @staticmethod
 | def int_2_str(int_value: int, number_indexes: int) -> str
```

Converts the integer, `int_value`, to a string with `number_indexes`,
e.g. `10` and `05` both have `number_indexes` of 2 and `001`, `020`,
and `211` have `number_indexes` of 3.

<h4 id="int_2_str.parameters">Parameters<a className="headerlink" href="#int_2_str.parameters" title="Permanent link">&para;</a></h4>


- __int\_value__ : `int` <br/>
    The integer to converts to a string with the given `number_indexes`.
- __number\_indexes__ : `int` <br/>
    The number of indexes the `int_value` should have in the returned
    string.

<h4 id="int_2_str.returns">Returns<a className="headerlink" href="#int_2_str.returns" title="Permanent link">&para;</a></h4>


- `str` <br/>

<h4 id="int_2_str.raises">Raises<a className="headerlink" href="#int_2_str.raises" title="Permanent link">&para;</a></h4>


- ValueError <br/>
    If the `number_indexes` of the `int_value` when converted to a
    string is greater than the given `number_indexes`.

<a id="pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.get_global_lowest_ranks"></a>

### get\_global\_lowest\_ranks

```python
class ContextualRuleBasedRanker(LexiconEntryRanker):
 | ...
 | @staticmethod
 | def get_global_lowest_ranks(
 |     token_ranking_data: List[List[RankingMetaData]],
 |     token_rankings: List[List[int]],
 |     ranking_data_to_exclude: Optional[Set[RankingMetaData]] = None
 | ) -> List[Optional[RankingMetaData]]
```

Returns the global lowest ranked entry match for each token. If the value
is `None` then no global lowest ranked entry can be found for that token.
If the `RankingMetaData` represents more than one token, like a Multi
Word Expression (MWE) match, then those associated tokens will have the
same `RankingMetaData` object as the global lowest ranked entry match.

Time Complexity, given *N* is the number of tokens, *M* is the number
of unique ranking data, and *P* is the number of ranking data (non-unique)
then the time complexity is:

O(N + P) + O(M log M) + O(M)

<h4 id="get_global_lowest_ranks.parameters">Parameters<a className="headerlink" href="#get_global_lowest_ranks.parameters" title="Permanent link">&para;</a></h4>


- __token\_ranking\_data__ : `List[List[RankingMetaData]]` <br/>
    For each token a `List` of
    [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) representing
    the lexicon entry match.
- __token\_rankings__ : `List[List[int]]` <br/>
    For each token contains the ranks of the lexicon entry matches.
    **Note** that the `List` can be empty if a token has no lexicon
    entry matches.
- __ranking\_data\_to\_exclude__ : `Set[RankingMetaData]`, optional (default = `None`) <br/>
    Any [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) to
    exclude from the ranking selection, this can be useful when wanting
    to get the next best global rank for each token.

<h4 id="get_global_lowest_ranks.raises">Raises<a className="headerlink" href="#get_global_lowest_ranks.raises" title="Permanent link">&para;</a></h4>


- `AssertionError` <br/>
    If the length of `token_ranking_data` is not equal to the length of
    `token_rankings`, for both the outer and inner `List`s.

<h4 id="get_global_lowest_ranks.examples">Examples<a className="headerlink" href="#get_global_lowest_ranks.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexical_match import LexicalMatch
north_east = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0,
                             False, LexicalMatch.TOKEN, 0, 2,
                             'North_noun East_noun', ('Z1',))
east_london_brewery = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 3, 0,
                                      False, LexicalMatch.TOKEN, 1, 4,
                                      'East_noun London_noun brewery_noun', ('Z1',))
token_ranking_data = [
    [
        north_east
    ],
    [
        north_east,
        east_london_brewery
    ],
    [
        east_london_brewery
    ],
    [
        east_london_brewery
    ]
]
token_rankings = [[120110], [120110, 110111], [110111], [110111]]
expected_lowest_ranked_matches = [None, east_london_brewery,
                                  east_london_brewery, east_london_brewery]
assert (ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data, token_rankings, None)
        == expected_lowest_ranked_matches)
```

Following on from the previous example, we now want to find the next best
global match for each token so we exclude the current best global match
for each token which is the `east_london_brewery` match:

``` python
expected_lowest_ranked_matches = [north_east, north_east, None, None]
ranking_data_to_exclude = {east_london_brewery}
assert (ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data, token_rankings,
                                                         ranking_data_to_exclude)
        == expected_lowest_ranked_matches)
```

<a id="pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.__call__"></a>

### \_\_call\_\_

```python
class ContextualRuleBasedRanker(LexiconEntryRanker):
 | ...
 | def __call__(
 |     self,
 |     token_ranking_data: List[List[RankingMetaData]]
 | ) -> Tuple[List[List[int]], List[Optional[RankingMetaData]]]
```

For each token it returns a `List` of rankings for each lexicon entry
match and the optional [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata)
object of the **global** lowest ranked match for each token.

See the ranking rules in the class docstring for details on how
each lexicon entry match is ranked.

Time Complexity, given *N* is the number of tokens, *M* is the number
of unique ranking data, and *P* is the number of ranking data (non-unique)
then the time complexity is:

O(3(N + P)) + O(M log M) + O(M)

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __token\_ranking\_data__ : `List[List[RankingMetaData]]` <br/>
    For each token a `List` of [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata)
    representing the lexicon entry match.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `Tuple[List[List[int]], List[Optional[RankingMetaData]]]` <br/>

<h4 id="__call__.examples">Examples<a className="headerlink" href="#__call__.examples" title="Permanent link">&para;</a></h4>

```python
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexical_match import LexicalMatch
north_east = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0,
                             False, LexicalMatch.TOKEN, 0, 2,
                             'North_noun East_noun', ('Z1',))
east_london_brewery = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 3, 0,
                                      False, LexicalMatch.TOKEN, 1, 4,
                                      'East_noun London_noun brewery_noun', ('Z1',))
token_ranking_data = [
    [
        north_east
    ],
    [
        north_east,
        east_london_brewery
    ],
    [
        east_london_brewery
    ],
    [
        east_london_brewery
    ]
]
expected_ranks = [[120110], [120110, 110111], [110111], [110111]]
expected_lowest_ranked_matches = [None, east_london_brewery,
                                  east_london_brewery, east_london_brewery]
ranker = ContextualRuleBasedRanker(3, 0)
assert ((expected_ranks, expected_lowest_ranked_matches)
        == ranker(token_ranking_data))
```

