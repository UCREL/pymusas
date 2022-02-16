<div className="source-div">
 <p><i>pymusas</i><i>.rankers</i><strong>.lexicon_entry</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/rankers/lexicon_entry.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.rankers.lexicon_entry.LexicalMatch"></a>

## LexicalMatch

```python
class LexicalMatch(IntEnum)
```

Descriptions of the lexical matches and their ordering in tagging priority
during ranking. Lower the value and rank the higher the tagging priority.

The `value` attribute of each instance attribute is of type `int`. For the
best explanation see the example below.

<h4 id="lexicalmatch.instance_attributes">Instance Attributes<a className="headerlink" href="#lexicalmatch.instance_attributes" title="Permanent link">&para;</a></h4>


- __TOKEN__ : `int` <br/>
    The lexicon entry matched on the token text.
- __LEMMA__ : `int` <br/>
    The lexicon entry matched on the lemma of the token.
- __TOKEN\_LOWER__ : `int` <br/>
    The lexicon entry matched on the lower cased token text.
- __LEMMA\_LOWER__ : `int` <br/>
    The lexicon entry matched on the lower cased lemma of the token.

<h4 id="lexicalmatch.examples">Examples<a className="headerlink" href="#lexicalmatch.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.rankers.lexicon_entry import LexicalMatch
assert 1 == LexicalMatch.TOKEN
assert 'TOKEN' == LexicalMatch.TOKEN.name
assert 1 == LexicalMatch.TOKEN.value

assert 2 == LexicalMatch.LEMMA
assert 3 == LexicalMatch.TOKEN_LOWER
assert 4 == LexicalMatch.LEMMA_LOWER

assert 2 < LexicalMatch.LEMMA_LOWER
```

<a id="pymusas.rankers.lexicon_entry.LexicalMatch.TOKEN"></a>

#### TOKEN

```python
class LexicalMatch(IntEnum):
 | ...
 | TOKEN = 1
```

<a id="pymusas.rankers.lexicon_entry.LexicalMatch.LEMMA"></a>

#### LEMMA

```python
class LexicalMatch(IntEnum):
 | ...
 | LEMMA = 2
```

<a id="pymusas.rankers.lexicon_entry.LexicalMatch.TOKEN_LOWER"></a>

#### TOKEN\_LOWER

```python
class LexicalMatch(IntEnum):
 | ...
 | TOKEN_LOWER = 3
```

<a id="pymusas.rankers.lexicon_entry.LexicalMatch.LEMMA_LOWER"></a>

#### LEMMA\_LOWER

```python
class LexicalMatch(IntEnum):
 | ...
 | LEMMA_LOWER = 4
```

<a id="pymusas.rankers.lexicon_entry.LexicalMatch.__repr__"></a>

### \_\_repr\_\_

```python
class LexicalMatch(IntEnum):
 | ...
 | def __repr__() -> str
```

Machine readable string. When printed and run `eval()` over the string
you should be able to recreate the object.

<a id="pymusas.rankers.lexicon_entry.RankingMetaData"></a>

## RankingMetaData

```python
@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class RankingMetaData
```

A RankingMetaData object contains all of the meta data about a lexicon
entry match during the tagging process. This meta data can then be used
to determine the ranking of the match comapred to other matches within the
same text/sentence that is being tagged.

<h4 id="rankingmetadata.instance_attributes">Instance Attributes<a className="headerlink" href="#rankingmetadata.instance_attributes" title="Permanent link">&para;</a></h4>


- __lexicon\_type__ : `LexiconType` <br/>
    Type associated to the lexicon entry.
- __lexicon\_n\_gram\_length__ : `int` <br/>
    The n-gram size of the lexicon entry, e.g. `*_noun boot*_noun` will be
    of length 2 and all single word lexicon entries will be of length 1.
- __lexicon\_wildcard\_count__ : `int` <br/>
    Number of wildcards in the lexicon entry, e.g. `*_noun boot*_noun` will
    be 2 and `ski_noun boot_noun` will be 0.
- __exclude\_pos\_information__ : `bool` <br/>
    Whether the POS information was excluded in the match. This is only `True`
    when the match ignores the POS information for single word lexicon entries.
    This is always `False` when used in a Multi Word Expression (MWE) lexicon
    entry match.
- __lexical\_match__ : `LexicalMatch` <br/>
    What [`LexicalMatch`](#lexicalmatch) the lexicon entry matched on.
- __token\_match\_start\_index__ : `int` <br/>
    Index of the first token in the lexicon entry match.
- __token\_match\_end\_index__ : `int` <br/>
    Index of the last token in the lexicon entry match.

<a id="pymusas.rankers.lexicon_entry.RankingMetaData.lexicon_type"></a>

#### lexicon\_type

```python
class RankingMetaData:
 | ...
 | lexicon_type: LexiconType = None
```

<a id="pymusas.rankers.lexicon_entry.RankingMetaData.lexicon_n_gram_length"></a>

#### lexicon\_n\_gram\_length

```python
class RankingMetaData:
 | ...
 | lexicon_n_gram_length: int = None
```

<a id="pymusas.rankers.lexicon_entry.RankingMetaData.lexicon_wildcard_count"></a>

#### lexicon\_wildcard\_count

```python
class RankingMetaData:
 | ...
 | lexicon_wildcard_count: int = None
```

<a id="pymusas.rankers.lexicon_entry.RankingMetaData.exclude_pos_information"></a>

#### exclude\_pos\_information

```python
class RankingMetaData:
 | ...
 | exclude_pos_information: bool = None
```

<a id="pymusas.rankers.lexicon_entry.RankingMetaData.lexical_match"></a>

#### lexical\_match

```python
class RankingMetaData:
 | ...
 | lexical_match: LexicalMatch = None
```

<a id="pymusas.rankers.lexicon_entry.RankingMetaData.token_match_start_index"></a>

#### token\_match\_start\_index

```python
class RankingMetaData:
 | ...
 | token_match_start_index: int = None
```

<a id="pymusas.rankers.lexicon_entry.RankingMetaData.token_match_end_index"></a>

#### token\_match\_end\_index

```python
class RankingMetaData:
 | ...
 | token_match_end_index: int = None
```

<a id="pymusas.rankers.lexicon_entry.LexiconEntryRanker"></a>

## LexiconEntryRanker

```python
class LexiconEntryRanker(ABC)
```

An **abstract class** that defines the basic method, `__call__`, that is
required for all [`LexiconEntryRanker`](#lexiconentryranker)s.

A LexcionEntryRanker when called, `__call__`, ranks the lexicon entry matches
for each token, whereby each match is represented by a [`RankingMetaData`](#rankingmetadata)
object.

**Lower ranked lexicon entry matches should be given priority when making
tagging decisions.**

<a id="pymusas.rankers.lexicon_entry.LexiconEntryRanker.__call__"></a>

### \_\_call\_\_

```python
class LexiconEntryRanker(ABC):
 | ...
 | @abstractmethod
 | def __call__(
 |     self,
 |     token_ranking_data: List[List[RankingMetaData]]
 | ) -> List[List[int]]
```

For each token it returns a `List` of rankings for each lexicon entry
match.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __token\_ranking\_data__ : `List[List[RankingMetaData]]` <br/>
    For each token a `List` of [`RankingMetaData`](#rankingmetadata) representing
    the lexicon entry match.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[List[int]]` <br/>

<a id="pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker"></a>

## ContextualRuleBasedRanker

```python
class ContextualRuleBasedRanker(LexiconEntryRanker)
```

The contextual rule based ranker creates ranks based on the rules stated below.

These rankings are fully interpretable as each rank is a *n* digit integer,
whereby the first 5 digit indexes corresponds to the first 5 ranking rules
below, e.g. first digit index corresponds to the first rule. The last *m*
digits correspond to the start index which relates to the sixth/last rule.
For example the rank `12111020` the first 5 digits `12111` correspond to the
first 5 rules below and `020` means that the start index was 20 for the
lexicon match which relates to rule 6, the reason for the 0 before 20 was can
be due to the text sequence containing start indexes of more than 99 and less
than 1000.

**Lower ranked lexicon entry matches should be given priority when making
tagging decisions.** For example a rank of 0 is better than a rank of 1.

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

In the case whereby the ranker has no more rules to apply and lexicon entry
matches per token have joint ranks, then those joint ranks will be returned
and the tagger will have to decide what to do with those joint ranked lexicon
matches.

<a id="pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.__call__"></a>

### \_\_call\_\_

```python
class ContextualRuleBasedRanker(LexiconEntryRanker):
 | ...
 | def __call__(
 |     self,
 |     token_ranking_data: List[List[RankingMetaData]]
 | ) -> List[List[int]]
```

For each token it returns a `List` of rankings for each lexicon entry
match. See the ranking rules in the class docstring for details on how
each lexicon entry match is ranked.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __token\_ranking\_data__ : `List[List[RankingMetaData]]` <br/>
    For each token a `List` of [`RankingMetaData`](#rankingmetadata) representing
    the lexicon entry match.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[List[int]]` <br/>

<h4 id="__call__.examples">Examples<a className="headerlink" href="#__call__.examples" title="Permanent link">&para;</a></h4>

```python
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.rankers.lexicon_entry import RankingMetaData
from pymusas.rankers.lexicon_entry import LexiconType
from pymusas.rankers.lexicon_entry import LexicalMatch
token_ranking_data = [
   [
       RankingMetaData(LexiconType.MWE_WILDCARD, 2, 1, False, LexicalMatch.TOKEN, 2, 3),
       RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0, False, LexicalMatch.LEMMA, 2, 3),
   ],
   [
       RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0, True, LexicalMatch.TOKEN_LOWER, 21, 23),
   ]
]
expected_rankings = [[2211102, 1201202], [4102321]]
ranker = ContextualRuleBasedRanker()
assert expected_rankings == ranker(token_ranking_data)
```

