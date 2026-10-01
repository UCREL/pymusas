'''
spaCy registered functions for creating the following tagger rules:
* :class:`pymusas.taggers.rules.single_word.SingleWordRule`
* :class:`pymusas.taggers.rules.mwe.MWERule`

And helper functions for the rules.
'''

import spacy

from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule


@spacy.util.registry.misc('pymusas.taggers.rules.SingleWordRule.v1')
def single_word_rule(lexicon_collection: dict[str, list[str]],
                     lemma_lexicon_collection: dict[str, list[str]],
                     pos_mapper: dict[str, list[str]] | None = None
                     ) -> SingleWordRule:
    '''
    `pymusas.taggers.rules.SingleWordRule.v1` is a registered function under the
    `@misc` function register.

    See the :class:`pymusas.taggers.rules.single_word.SingleWordRule` for
    details on parameters to this function.

    # Returns
    
    :class:`pymusas.taggers.rules.single_word.SingleWordRule`
    '''
    return SingleWordRule(lexicon_collection, lemma_lexicon_collection,
                          pos_mapper)


@spacy.util.registry.misc('pymusas.taggers.rules.MWERule.v1')
def mwe_rule(mwe_lexicon_lookup: dict[str, list[str]],
             pos_mapper: dict[str, list[str]] | None = None
             ) -> MWERule:
    '''
    `pymusas.taggers.rules.MWERule.v1` is a registered function under the
    `@misc` function register.

    Compared to `pymusas.taggers.rules.MWERule.v2`, if a matching MWE rule
    contains a (`Df`) semantic tag, the `Df` tag is replaced with `Z99`.

    See the :class:`pymusas.taggers.rules.mwe.MWERule` for details on
    parameters to this function.

    # Returns

    :class:`pymusas.taggers.rules.mwe.MWERule`
    '''
    return MWERule(mwe_lexicon_lookup, pos_mapper)


@spacy.util.registry.misc('pymusas.taggers.rules.MWERule.v2')
def mwe_rule_v2(mwe_lexicon_lookup: dict[str, list[str]],
                pos_mapper: dict[str, list[str]] | None = None,
                single_word_rule: SingleWordRule | None = None
                ) -> MWERule:
    '''
    `pymusas.taggers.rules.MWERule.v2` is a registered function under the
    `@misc` function register. Compared to `pymusas.taggers.rules.MWERule.v1`
    it also accepts a `single_word_rule`, which is used to replace default
    (`Df`) semantic tags.

    See the :class:`pymusas.taggers.rules.mwe.MWERule` for details on
    parameters to this function.

    # Returns

    :class:`pymusas.taggers.rules.mwe.MWERule`
    '''
    return MWERule(mwe_lexicon_lookup, pos_mapper, single_word_rule)


@spacy.util.registry.misc('pymusas.taggers.rules.rule_list')
def rule_list(*rules: Rule) -> list[Rule]:
    '''
    `pymusas.taggers.rules.rule_list` is a registered function under the
    `@misc` function register. The function is required when wanting to create
    a `list` of rules within a
    [config file](https://thinc.ai/docs/usage-config). We
    found it not possible to specify a `list` of custom objects within a config
    file, but is possible when using
    [variable position arguments](https://thinc.ai/docs/usage-config#registries-args),
    which this function accepts as input.
    
    This function is most likely to be
    used when creating a :class:`pymusas.spacy_api.taggers.rule_based.RuleBasedTagger`.


    # Parameters
    
    rules : `Rule`
        The :class:`pymusas.taggers.rules.rule.Rule`s to convert into a `list`
        of `Rule`s.
    
    # Returns
    
    `list[Rule]`
    '''
    return list(rules)
