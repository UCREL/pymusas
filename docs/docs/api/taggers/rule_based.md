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
 |     rules: list[Rule],
 |     ranker: LexiconEntryRanker,
 |     default_punctuation_tags: set[str] | None = None,
 |     default_number_tags: set[str] | None = None
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
with a `list` of token indexes indicating if the token is part of a Multi
Word Expression (MWE).

If we cannot tag a token then the following process will happen:
1. If the token's POS tag is in `default_punctuation_tags` then it will assign the
tag `PUNCT`.
2. If the token's POS tag is in `default_number_tags` then it will assign the tag
`N1`.
3. Assign the default tag `Z99`.

<h4 id="rulebasedtagger.parameters">Parameters<a className="headerlink" href="#rulebasedtagger.parameters" title="Permanent link">&para;</a></h4>


- __rules__ : `list[pymusas.taggers.rules.rule.Rule]` <br/>
    A list of rules to apply to the sequence of tokens in the
    [`__call__`](#__call__). The output from each rule is concatenated and given
    to the `ranker`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker` <br/>
    A ranker to rank the output from all of the `rules`.
- __default\_punctuation\_tags__ : `set[str]`, optional (default = `None`) <br/>
    The POS tags that represent punctuation. If `None` then we will use
    the `set`: `set(['punc'])`.
- __default\_number\_tags__ : `set[str]`, optional (default = `None`) <br/>
    The POS tags that represent numbers. If `None` then we will use
    the `set`: `set(['num'])`.

<h4 id="rulebasedtagger.instance_attributes">Instance Attributes<a className="headerlink" href="#rulebasedtagger.instance_attributes" title="Permanent link">&para;</a></h4>


- __rules__ : `list[pymusas.taggers.rules.rule.Rule]` <br/>
    The given `rules`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker` <br/>
    The given `ranker`.
- __default\_punctuation\_tags__ : `set[str]` <br/>
    The given `default_punctuation_tags`
- __default\_number\_tags__ : `set[str]` <br/>
    The given `default_number_tags`

<h4 id="rulebasedtagger.examples">Examples<a className="headerlink" href="#rulebasedtagger.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.rule_based import RuleBasedTagger
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.pos_mapper import BASIC_CORCENCC_TO_USAS_CORE
welsh_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Welsh/semantic_lexicon_cy.tsv'
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
 |     tokens: list[str],
 |     lemmas: list[str],
 |     pos_tags: list[str]
 | ) -> list[tuple[list[str],
 |                                                     list[tuple[int, int]]
 |                                                     ]]
```

Given a `list` of tokens, their associated lemmas and
Part Of Speech (POS) tags it returns for each token:

1. A `list` of tags. The first tag in the `list` of tags is the most likely tag.
2. A `list` of `Tuples` whereby each `tuple` indicates the start and end
token index of the associated Multi Word Expression (MWE). If the `list` contains
more than one `tuple` then the MWE is discontinuous. For single word
expressions the `list` will only contain 1 `tuple` which will be
(token_start_index, token_start_index + 1).

All the generated tags and MWEs are based on the rules and ranker given
to this model.

**NOTE** this tagger has been designed to be flexible with the amount of
resources available, if you do not have POS or lemma information assign
them a `list` of empty strings.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `list[str]` <br/>
    A `list` of full text form of the tokens to be tagged.
- __lemmas__ : `list[str]` <br/>
    The `list` of lemma/base form of the tokens to be tagged.
- __pos\_tags__ : `list[str]` <br/>
    The `list` of POS tags of the tokens to be tagged.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `list[tuple[list[str], list[tuple[int, int]]]]` <br/>

<h4 id="__call__.raises">Raises<a className="headerlink" href="#__call__.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the length of the `tokens`, `lemmas`, and `pos_tags` are not of
    the same length.

