'''
spaCy registered functions for creating the following rankers:
* :class:`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`
'''
from typing import List

import spacy

from pymusas.taggers.rules.rule import Rule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker


@spacy.util.registry.misc('pymusas.rankers.ContextualRuleBasedRanker.v1')
def contextual_rule_based_ranker(rules: List[Rule]) -> ContextualRuleBasedRanker:
    '''
    `pymusas.rankers.ContextualRuleBasedRanker.v1` is a registered function
    under the `@misc` function register.

    The parameters of this function are passed to the
    :func:`pymusas.rankers.lexicon_entry.get_construction_arguments`
    function of which the output of this function is then used as arguments
    to the :class:`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`
    constructor.

    # Parameters

    rules : `List[Rule]`
        A `List` of :class:`pymusas.taggers.rules.rule.Rule`.

    # Returns
    
    :class:`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`
    '''
    maximum_n_gram_length, maximum_number_wildcards \
        = ContextualRuleBasedRanker.get_construction_arguments(rules)
    return ContextualRuleBasedRanker(maximum_n_gram_length,
                                     maximum_number_wildcards)
