<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><i>.taggers</i><strong>.rules</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/taggers/rules.py">[SOURCE]</a></p>
</div>
<div></div>

---

spaCy registered functions for creating the following tagger rules:
* [`pymusas.taggers.rules.single_word.SingleWordRule`](/pymusas/api/taggers/rules/single_word/#singlewordrule)
* [`pymusas.taggers.rules.mwe.MWERule`](/pymusas/api/taggers/rules/mwe/#mwerule)

And helper functions for the rules.

<a id="pymusas.spacy_api.taggers.rules.single_word_rule"></a>

### single\_word\_rule

```python
@spacy.util.registry.misc('pymusas.taggers.rules.SingleWordRule.v1')
def single_word_rule(
    lexicon_collection: dict[str, list[str]],
    lemma_lexicon_collection: dict[str, list[str]],
    pos_mapper: dict[str, list[str]] | None = None
) -> SingleWordRule
```

`pymusas.taggers.rules.SingleWordRule.v1` is a registered function under the
`@misc` function register.

See the [`pymusas.taggers.rules.single_word.SingleWordRule`](/pymusas/api/taggers/rules/single_word/#singlewordrule) for
details on parameters to this function.

<h4 id="single_word_rule.returns">Returns<a className="headerlink" href="#single_word_rule.returns" title="Permanent link">&para;</a></h4>


- [`pymusas.taggers.rules.single_word.SingleWordRule`](/pymusas/api/taggers/rules/single_word/#singlewordrule) <br/>

<a id="pymusas.spacy_api.taggers.rules.mwe_rule"></a>

### mwe\_rule

```python
@spacy.util.registry.misc('pymusas.taggers.rules.MWERule.v1')
def mwe_rule(
    mwe_lexicon_lookup: dict[str, list[str]],
    pos_mapper: dict[str, list[str]] | None = None
) -> MWERule
```

`pymusas.taggers.rules.MWERule.v1` is a registered function under the
`@misc` function register.

Compared to `pymusas.taggers.rules.MWERule.v2`, if a matching MWE rule
contains a (`Df`) semantic tag, the `Df` tag is replaced with `Z99`.

See the [`pymusas.taggers.rules.mwe.MWERule`](/pymusas/api/taggers/rules/mwe/#mwerule) for details on
parameters to this function.

<h4 id="mwe_rule.returns">Returns<a className="headerlink" href="#mwe_rule.returns" title="Permanent link">&para;</a></h4>


- [`pymusas.taggers.rules.mwe.MWERule`](/pymusas/api/taggers/rules/mwe/#mwerule) <br/>

<a id="pymusas.spacy_api.taggers.rules.mwe_rule_v2"></a>

### mwe\_rule\_v2

```python
@spacy.util.registry.misc('pymusas.taggers.rules.MWERule.v2')
def mwe_rule_v2(
    mwe_lexicon_lookup: dict[str, list[str]],
    pos_mapper: dict[str, list[str]] | None = None,
    single_word_rule: SingleWordRule | None = None
) -> MWERule
```

`pymusas.taggers.rules.MWERule.v2` is a registered function under the
`@misc` function register. Compared to `pymusas.taggers.rules.MWERule.v1`
it also accepts a `single_word_rule`, which is used to replace default
(`Df`) semantic tags.

See the [`pymusas.taggers.rules.mwe.MWERule`](/pymusas/api/taggers/rules/mwe/#mwerule) for details on
parameters to this function.

<h4 id="mwe_rule_v2.returns">Returns<a className="headerlink" href="#mwe_rule_v2.returns" title="Permanent link">&para;</a></h4>


- [`pymusas.taggers.rules.mwe.MWERule`](/pymusas/api/taggers/rules/mwe/#mwerule) <br/>

<a id="pymusas.spacy_api.taggers.rules.rule_list"></a>

### rule\_list

```python
@spacy.util.registry.misc('pymusas.taggers.rules.rule_list')
def rule_list(*rules: Rule) -> list[Rule]
```

`pymusas.taggers.rules.rule_list` is a registered function under the
`@misc` function register. The function is required when wanting to create
a `list` of rules within a
[config file](https://thinc.ai/docs/usage-config). We
found it not possible to specify a `list` of custom objects within a config
file, but is possible when using
[variable position arguments](https://thinc.ai/docs/usage-config#registries-args),
which this function accepts as input.

This function is most likely to be
used when creating a [`pymusas.spacy_api.taggers.rule_based.RuleBasedTagger`](/pymusas/api/spacy_api/taggers/rule_based/#rulebasedtagger).


<h4 id="rule_list.parameters">Parameters<a className="headerlink" href="#rule_list.parameters" title="Permanent link">&para;</a></h4>


- __rules__ : `Rule` <br/>
    The [`pymusas.taggers.rules.rule.Rule`](/pymusas/api/taggers/rules/rule/#rule)s to convert into a `list`
    of `Rule`s.

<h4 id="rule_list.returns">Returns<a className="headerlink" href="#rule_list.returns" title="Permanent link">&para;</a></h4>


- `list[Rule]` <br/>

