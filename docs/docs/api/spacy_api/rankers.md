<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><strong>.rankers</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/rankers.py">[SOURCE]</a></p>
</div>
<div></div>

---

spaCy registered functions for creating the following rankers:
* [`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`](/pymusas/api/rankers/lexicon_entry/#contextualrulebasedranker)

<a id="pymusas.spacy_api.rankers.contextual_rule_based_ranker"></a>

### contextual\_rule\_based\_ranker

```python
@spacy.util.registry.misc('pymusas.rankers.ContextualRuleBasedRanker.v1')
def contextual_rule_based_ranker(
    rules: List[Rule]
) -> ContextualRuleBasedRanker
```

`pymusas.rankers.ContextualRuleBasedRanker.v1` is a registered function
under the `@misc` function register.

The parameters of this function are passed to the
[`pymusas.rankers.lexicon_entry.get_construction_arguments`](/pymusas/api/rankers/lexicon_entry/#get_construction_arguments)
function of which the output of this function is then used as arguments
to the [`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`](/pymusas/api/rankers/lexicon_entry/#contextualrulebasedranker)
constructor.

<h4 id="contextual_rule_based_ranker.parameters">Parameters<a className="headerlink" href="#contextual_rule_based_ranker.parameters" title="Permanent link">&para;</a></h4>


- __rules__ : `List[Rule]` <br/>
    A `List` of [`pymusas.taggers.rules.rule.Rule`](/pymusas/api/taggers/rules/rule/#rule).

<h4 id="contextual_rule_based_ranker.returns">Returns<a className="headerlink" href="#contextual_rule_based_ranker.returns" title="Permanent link">&para;</a></h4>


- [`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`](/pymusas/api/rankers/lexicon_entry/#contextualrulebasedranker) <br/>

