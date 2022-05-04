<div className="source-div">
 <p><i>pymusas</i><i>.rankers</i><strong>.ranking_meta_data</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/rankers/ranking_meta_data.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData"></a>

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
- __lexicon\_entry\_match__ : `str` <br/>
    The lexicon entry match, which can be either a single word or MWE entry
    match. In the case for single word this could be `Car|noun` and in the
    case for a MWE it would be it's template, e.g. `snow_noun boots_noun`.
- __semantic\_tags__ : `Tuple[str, ...]` <br/>
    The semantic tags associated with the lexicon entry. The semantic tags
    are in rank order, the most likely tag is the first tag in the tuple.
    The Tuple can be of variable length hence the `...` in the
    type annotation.

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_type"></a>

#### lexicon\_type

```python
class RankingMetaData:
 | ...
 | lexicon_type: LexiconType = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_n_gram_length"></a>

#### lexicon\_n\_gram\_length

```python
class RankingMetaData:
 | ...
 | lexicon_n_gram_length: int = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_wildcard_count"></a>

#### lexicon\_wildcard\_count

```python
class RankingMetaData:
 | ...
 | lexicon_wildcard_count: int = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.exclude_pos_information"></a>

#### exclude\_pos\_information

```python
class RankingMetaData:
 | ...
 | exclude_pos_information: bool = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.lexical_match"></a>

#### lexical\_match

```python
class RankingMetaData:
 | ...
 | lexical_match: LexicalMatch = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.token_match_start_index"></a>

#### token\_match\_start\_index

```python
class RankingMetaData:
 | ...
 | token_match_start_index: int = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.token_match_end_index"></a>

#### token\_match\_end\_index

```python
class RankingMetaData:
 | ...
 | token_match_end_index: int = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.lexicon_entry_match"></a>

#### lexicon\_entry\_match

```python
class RankingMetaData:
 | ...
 | lexicon_entry_match: str = None
```

<a id="pymusas.rankers.ranking_meta_data.RankingMetaData.semantic_tags"></a>

#### semantic\_tags

```python
class RankingMetaData:
 | ...
 | semantic_tags: Tuple[str, ...] = None
```

