<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><strong>.new_rule_based</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/new_rule_based.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.new_rule_based.RuleBasedTagger"></a>

## RuleBasedTagger

```python
class RuleBasedTagger:
 | ...
 | def __init__(
 |     self,
 |     rules: List[Rule],
 |     ranker: LexiconEntryRanker
 | ) -> None
```

The tagger when called, through [`__call__`](#__call__), and given a sequence of
tokens and their associated lingustic data (lemma, Part Of Speech (POS))
to tag will apply one or more [`pymusas.taggers.rules.rule.Rule`](/pymusas/api/taggers/rules/rule/#rule)s
to create a list of possible candidate tags for each token in the sequence.
Each candidate, represented as a
[`pymusas.rankers.lexicon_entry.RankingMetaData`](/pymusas/api/rankers/lexicon_entry/#rankingmetadata) object, for each
token is then Ranked using a
`[`pymusas.rankers.lexicon_entry.LexiconEntryRanker`](/pymusas/api/rankers/lexicon_entry/#lexiconentryranker) ranker. The best
candidate and it's associated tag(s) for each token are then returned.

If we cannot tag a token the default assigned tag is `Z99`.

<h4 id="rulebasedtagger.parameters">Parameters<a className="headerlink" href="#rulebasedtagger.parameters" title="Permanent link">&para;</a></h4>


- __rules__ : `List[pymusas.taggers.rules.rule.Rule]` <br/>
    A list of rules to apply to the sequence of tokens in the
    [`__call__`](#__call__). The output from each rule is concatendated and given
    to the `ranker`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker` <br/>
    A ranker to rank the output from all of the `rules`.

<h4 id="rulebasedtagger.instance_attributes">Instance Attributes<a className="headerlink" href="#rulebasedtagger.instance_attributes" title="Permanent link">&para;</a></h4>


- __rules__ : `List[pymusas.taggers.rules.rule.Rule]` <br/>
    The given `rules`.
- __ranker__ : `pymusas.rankers.lexicon_entry.LexiconEntryRanker` <br/>
    The given `ranker`.

<h4 id="rulebasedtagger.examples">Examples<a className="headerlink" href="#rulebasedtagger.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.new_rule_based import RuleBasedTagger
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

<a id="pymusas.taggers.new_rule_based.RuleBasedTagger.__call__"></a>

### \_\_call\_\_

```python
class RuleBasedTagger:
 | ...
 | def __call__(
 |     self,
 |     tokens: List[str],
 |     lemmas: List[str],
 |     pos_tags: List[str]
 | ) -> List[List[str]]
```

Given a `List` of tokens, their associated lemmas and Part Of Speech tags
it returns for each token a list of tags. These tags are generated based
on the rules and ranker given to this model.

The first tag in the `List` of tags is the most likely tag.

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


- `List[List[str]]` <br/>

<h4 id="__call__.raises">Raises<a className="headerlink" href="#__call__.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the length of the `tokens`, `lemmas`, and `pos_tags` are not of
    the same legnth.

