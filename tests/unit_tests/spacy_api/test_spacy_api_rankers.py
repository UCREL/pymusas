from typing import Callable, List

import spacy

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.spacy_api import rankers  # noqa: F401
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule


def test_contextual_rule_based_ranker() -> None:
    contextual_rule_based_ranker: Callable[[List[Rule]],
                                           ContextualRuleBasedRanker] \
        = spacy.util.registry.misc.get('pymusas.rankers.ContextualRuleBasedRanker.v1')
    rules: List[Rule] = []
    ranker = contextual_rule_based_ranker(rules)
    assert isinstance(ranker, ContextualRuleBasedRanker)
    assert ranker._maximum_n_gram_length == 0
    assert ranker._maximum_number_wildcards == 0

    # Single Word Rules
    pt_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/semantic_lexicon_pt.tsv"
    single_lexicon = LexiconCollection.from_tsv(pt_lexicon_url)
    single_lemma_lexicon = LexiconCollection.from_tsv(pt_lexicon_url, False)
    single_word_rule = SingleWordRule(single_lexicon, single_lemma_lexicon)
    rules.append(single_word_rule)
    ranker = contextual_rule_based_ranker(rules)
    assert ranker._maximum_n_gram_length == 1
    assert ranker._maximum_number_wildcards == 0

    pt_mwe_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/mwe-pt.tsv"
    mwe_lexicon = MWELexiconCollection.from_tsv(pt_mwe_lexicon_url)
    mwe_word_rule = MWERule(mwe_lexicon)
    rules.append(mwe_word_rule)
    ranker = contextual_rule_based_ranker(rules)
    assert ranker._maximum_n_gram_length == 9
    assert ranker._maximum_number_wildcards == 4

    es_mwe_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Spanish/mwe-es.tsv"
    es_mwe_lexicon = MWELexiconCollection.from_tsv(es_mwe_lexicon_url)
    es_mwe_word_rule = MWERule(es_mwe_lexicon)
    rules.append(es_mwe_word_rule)
    ranker = contextual_rule_based_ranker(rules)
    assert ranker._maximum_n_gram_length == 9
    assert ranker._maximum_number_wildcards == 4

    del rules[1]
    ranker = contextual_rule_based_ranker(rules)
    assert ranker._maximum_n_gram_length == 9
    assert ranker._maximum_number_wildcards == 1
