'''
spaCy registered functions for creating the following tagger rules:
* :class:`pymusas.taggers.rules.single_word.SingleWordRule`
* :class:`pymusas.taggers.rules.mwe.MWERule`
'''
from typing import Dict, List

import spacy

from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.single_word import SingleWordRule


@spacy.util.registry.misc('pymusas.taggers.rules.SingleWordRule.v1')
def single_word_rule(lexicon_collection: Dict[str, List[str]],
                     lemma_lexicon_collection: Dict[str, List[str]],
                     pos_mapper: Dict[str, List[str]]) -> SingleWordRule:
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
def mwe_rule(mwe_lexicon_lookup: Dict[str, List[str]],
             pos_mapper: Dict[str, List[str]]) -> MWERule:
    '''
    `pymusas.taggers.rules.MWERule.v1` is a registered function under the
    `@misc` function register.

    See the :class:`pymusas.taggers.rules.mwe.MWERule` for details on
    parameters to this function.

    # Returns

    :class:`pymusas.taggers.rules.mwe.MWERule`
    '''
    return MWERule(mwe_lexicon_lookup, pos_mapper)
