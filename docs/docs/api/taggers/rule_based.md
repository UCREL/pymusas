<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><strong>.rule_based</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rule_based.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.rule_based.RuleBasedTagger"></a>

## RuleBasedTagger

```python
class RuleBasedTagger:
 | ...
 | def __init__(
 |     self,
 |     rules: List[Rule],
 |     ranker: LexiconEntryRanker,
 |     default_punctuation_tags: Optional[Set[str]] = None,
 |     default_number_tags: Optional[Set[str]] = None
 | ) -> None
```

The tagger when called, through [`__call__`](#__call__), and given a sequence of
tokens and their associated lingustic data (lemma, Part Of Speech (POS))
will apply one or more [`pymusas.taggers.rules.rule.Rule`](/pymusas/api/taggers/rules/rule/#rule)s
to create a list of possible candidate tags for each token in the sequence.
Each candidate, represented as a
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object, for each
token is then Ranked using a
[`pymusas.rankers.lexicon_entry.LexiconEntryRanker`](/pymusas/api/rankers/lexicon_entry/#lexiconentryranker) ranker. The best
candidate and it's associated tag(s) for each token are then returned along
with a `List` of token indexes indicating if the token is part of a Multi
Word Expression (MWE).

If we cannot tag a token then the following process will happen:
1. If the token's POS tag is in `default_punctuation_tags` then it will assign the
tag `PUNCT`.
2. If the token's POS tag is in `default_number_tags` then it will assign the tag
`N1`.
3. Assign the default tag `Z99`.

<h4 id="rulebasedtagger.parameters">Parameters<a className="headerlink" href="#rulebasedtagger.parameters" title="Permanent link">&para;</a></h4>


- __rules__ : `List[pymusas.taggers.rules.rule.Rule]` <br/>
    A list of rules to apply to the sequence of tokens in the
    [`__call__`](#__call__). The output from each rule is concatendated and given
    to the `ranker`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker` <br/>
    A ranker to rank the output from all of the `rules`.
- __default\_punctuation\_tags__ : `Set[str]`, optional (default = `None`) <br/>
    The POS tags that represent punctuation. If `None` then we will use
    the `Set`: `set(['punc'])`.
- __default\_number\_tags__ : `Set[str]`, optional (default = `None`) <br/>
    The POS tags that represent numbers. If `None` then we will use
    the `Set`: `set(['num'])`.

<h4 id="rulebasedtagger.instance_attributes">Instance Attributes<a className="headerlink" href="#rulebasedtagger.instance_attributes" title="Permanent link">&para;</a></h4>


- __rules__ : `List[pymusas.taggers.rules.rule.Rule]` <br/>
    The given `rules`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker` <br/>
    The given `ranker`.
- __default\_punctuation\_tags__ : `Set[str]` <br/>
    The given `default_punctuation_tags`
- __default\_number\_tags__ : `Set[str]` <br/>
    The given `default_number_tags`

<h4 id="rulebasedtagger.examples">Examples<a className="headerlink" href="#rulebasedtagger.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.rule_based import RuleBasedTagger
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.pos_mapper import BASIC_CORCENCC_TO_USAS_CORE
welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
single_word_rule = SingleWordRule(lexicon_lookup, lemma_lexicon_lookup,
                                  BASIC_CORCENCC_TO_USAS_CORE)
ranker = ContextualRuleBasedRanker(1, 0)
tagger = RuleBasedTagger([single_word_rule], ranker)
```

<a id="pymusas.taggers.rule_based.RuleBasedTagger.__call__"></a>

### \_\_call\_\_

```python
class RuleBasedTagger:
 | ...
 | def __call__(
 |     self,
 |     tokens: List[str],
 |     lemmas: List[str],
 |     pos_tags: List[str]
 | ) -> List[Tuple[List[str],
 |                                                     List[Tuple[int, int]]
 |                                                     ]]
```

Given a `List` of tokens, their associated lemmas and
Part Of Speech (POS) tags it returns for each token:

1. A `List` of tags. The first tag in the `List` of tags is the most likely tag.
2. A `List` of `Tuples` whereby each `Tuple` indicates the start and end
token index of the associated Multi Word Expression (MWE). If the `List` contains
more than one `Tuple` then the MWE is discontinuous. For single word
expressions the `List` will only contain 1 `Tuple` which will be
(token_start_index, token_start_index + 1).

All the generated tags and MWEs are based on the rules and ranker given
to this model.

**NOTE** this tagger has been designed to be flexible with the amount of
resources avaliable, if you do not have POS or lemma information assign
them a `List` of empty strings.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `List[str]` <br/>
    A List of full text form of the tokens to be tagged.
- __lemmas__ : `List[str]` <br/>
    The List of lemma/base form of the tokens to be tagged.
- __pos\_tags__ : `List[str]` <br/>
    The List of POS tags of the tokens to be tagged.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[Tuple[List[str], List[Tuple[int, int]]]]` <br/>

<h4 id="__call__.raises">Raises<a className="headerlink" href="#__call__.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the length of the `tokens`, `lemmas`, and `pos_tags` are not of
    the same legnth.

