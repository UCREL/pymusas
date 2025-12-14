from typing import List, Optional, Tuple

import pytest

from pymusas.lexicon_collection import LexiconCollection, LexiconType, MWELexiconCollection
from pymusas.rankers.lexical_match import LexicalMatch
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker, LexiconEntryRanker
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule


RANKING_META_DATA = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 1,
                                    False, LexicalMatch.TOKEN, 1, 3,
                                    'snow_noun boot_noun', ('Z5', 'Z4'))


def test_lexicon_entry_ranker() -> None:
    
    class TestRanker(LexiconEntryRanker):

        def __call__(self, token_ranking_data: List[List[RankingMetaData]]
                     ) -> Tuple[List[List[int]], List[Optional[RankingMetaData]]]:
            return ([[0]], [None])

        def to_bytes(self) -> bytes:
            return b'test'

        @staticmethod
        def from_bytes(bytes_data: bytes) -> 'TestRanker':
            return TestRanker()

        def __eq__(self, other: object) -> bool:
            return True

    concrete_ranker = TestRanker()
    assert ([[0]], [None]) == concrete_ranker([[RANKING_META_DATA]])
    assert isinstance(concrete_ranker, LexiconEntryRanker)

    assert b'test' == concrete_ranker.to_bytes()
    assert isinstance(concrete_ranker.from_bytes(b'test'), TestRanker)
    assert concrete_ranker == TestRanker()


def test_contextual_rule_based_ranker__init__() -> None:
    ranker = ContextualRuleBasedRanker(0, 0)

    assert isinstance(ranker, LexiconEntryRanker)

    assert 1 == ranker.n_gram_number_indexes
    assert 1 == ranker.wildcards_number_indexes
    assert {} == ranker.n_gram_ranking_dictionary

    ranker = ContextualRuleBasedRanker(10, 10)
    assert 2 == ranker.n_gram_number_indexes
    assert 2 == ranker.wildcards_number_indexes
    assert {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1} \
        == ranker.n_gram_ranking_dictionary
    
    ranker = ContextualRuleBasedRanker(10, 2)
    assert 2 == ranker.n_gram_number_indexes
    assert 1 == ranker.wildcards_number_indexes
    assert {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1} \
        == ranker.n_gram_ranking_dictionary
    
    ranker = ContextualRuleBasedRanker(2, 10)
    assert 1 == ranker.n_gram_number_indexes
    assert 2 == ranker.wildcards_number_indexes
    assert {1: 2, 2: 1} == ranker.n_gram_ranking_dictionary


def test_contextual_rule_based_ranker_to_from_bytes() -> None:
    maximum_n_gram_length = 2
    maximum_number_wildcards = 1
    ranker = ContextualRuleBasedRanker(maximum_n_gram_length,
                                       maximum_number_wildcards)
    ranker_from_bytes = ContextualRuleBasedRanker.from_bytes(ranker.to_bytes())
    assert 1 == ranker_from_bytes.n_gram_number_indexes
    assert 1 == ranker_from_bytes.wildcards_number_indexes
    assert {2: 1, 1: 2} == ranker_from_bytes.n_gram_ranking_dictionary


def test_contextual_rule_based_ranker__eq__() -> None:
    ranker = ContextualRuleBasedRanker(1, 2)
    assert 1 != ranker

    assert ranker != ContextualRuleBasedRanker(1, 1)
    assert ranker != ContextualRuleBasedRanker(2, 1)
    assert ranker == ContextualRuleBasedRanker(1, 2)


def test_contextual_rule_based_ranker__call__() -> None:
    ranker = ContextualRuleBasedRanker(2, 1)
    assert ([], []) == ranker([])

    # Test that it assigns [] and None to tokens that have
    # no rank meta data objects

    token_ranking_data: List[List[RankingMetaData]] = [
        []
    ]
    assert ([[]], [None]) == ranker(token_ranking_data)

    snow = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                           True, LexicalMatch.TOKEN, 1, 2,
                           'Snow', ('Z1',))
    token_ranking_data = [
        [],
        [
            snow
        ]
    ]
    assert ([[], [420211]], [None, snow]) == ranker(token_ranking_data)

    # Test average use case
    snow_wild_mwe = RankingMetaData(LexiconType.MWE_WILDCARD, 2, 1,
                                    False, LexicalMatch.TOKEN, 0, 2,
                                    'Snow_noun *_noun', ('Z1', 'Z2'))
    snow_boot_mwe = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0,
                                    False, LexicalMatch.LEMMA, 0, 2,
                                    'Snow_noun boot_noun', ('Z1',))
    snow_noun = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                                False, LexicalMatch.TOKEN, 0, 1,
                                'Snow|noun', ('Z1',))
    snow = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                           True, LexicalMatch.TOKEN, 0, 1,
                           'Snow', ('Z1',))
    boot_noun_token = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                                      False, LexicalMatch.TOKEN, 1, 2,
                                      'boot|noun', ('Z1',))
    boot_noun_lemma = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                                      False, LexicalMatch.LEMMA, 1, 2,
                                      'boot|noun', ('Z1',))
    boot_noun_token_lower = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                                            False, LexicalMatch.TOKEN_LOWER, 1, 2,
                                            'boot|noun', ('Z1',))
    boot_noun_lemma_lower = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                                            False, LexicalMatch.LEMMA_LOWER, 1, 2,
                                            'boot|noun', ('Z1',))
    token_ranking_data = [
        [
            snow_wild_mwe,
            snow_boot_mwe,
            snow_noun,
            snow
        ],
        [
            snow_wild_mwe,
            snow_boot_mwe,
            boot_noun_token,
            boot_noun_lemma,
            boot_noun_token_lower,
            boot_noun_lemma_lower,
        ]
    ]
    expected_ranks = [
        [
            211110,
            110120,
            420110,
            420210
        ],
        [
            211110,
            110120,
            420111,
            420121,
            420131,
            420141
        ]
    ]
    expected_lowest_ranked_matches: List[Optional[RankingMetaData]]
    expected_lowest_ranked_matches = [snow_boot_mwe, snow_boot_mwe]
    assert (expected_ranks, expected_lowest_ranked_matches) \
        == ranker(token_ranking_data)
    
    # Testing the global ranking function, in this test we make sure that it can
    # handle ranking global decisions over local.
    north_east_mwe = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0,
                                     False, LexicalMatch.TOKEN, 0, 2,
                                     'North_noun East_noun', ('Z1',))
    north_noun = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
                                 False, LexicalMatch.TOKEN, 0, 1,
                                 'North|noun', ('Z1',))
    east_london_brewery_mwe = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 3, 0,
                                              False, LexicalMatch.TOKEN, 1, 4,
                                              'East_noun London_noun brewery_noun', ('Z1',))
    ranker = ContextualRuleBasedRanker(3, 0)
    token_ranking_data = [
        [
            north_east_mwe,
            north_noun
            
        ],
        [
            north_east_mwe,
            east_london_brewery_mwe
            
        ],
        [
            east_london_brewery_mwe
        ],
        [
            east_london_brewery_mwe
        ]
    ]
    expected_ranks = [
        [
            120110,
            430110
        ],
        [
            120110,
            110111
            
        ],
        [
            110111
        ],
        [
            110111
        ]
    ]
    expected_lowest_ranked_matches = [north_noun, east_london_brewery_mwe,
                                      east_london_brewery_mwe, east_london_brewery_mwe]
    assert (expected_ranks, expected_lowest_ranked_matches) \
        == ranker(token_ranking_data)
    
    # Testing the global ranking function, in this test we make sure that it can
    # handle ranking global decision over local to the extent that the global
    # lowest rank is None due token overlap in the first token.
    token_ranking_data = [
        [
            north_east_mwe
        ],
        [
            east_london_brewery_mwe,
            north_east_mwe
        ],
        [
            east_london_brewery_mwe
        ],
        [
            east_london_brewery_mwe
        ]
    ]
    expected_ranks = [
        [
            120110
        ],
        [
            110111,
            120110
        ],
        [
            110111
        ],
        [
            110111
        ]
    ]
    expected_lowest_ranked_matches = [None, east_london_brewery_mwe,
                                      east_london_brewery_mwe, east_london_brewery_mwe]
    assert (expected_ranks, expected_lowest_ranked_matches) \
        == ranker(token_ranking_data)

    # Testing the global ranking function, in this test we make sure that it can
    # handle ranking global decisions over local, but in this version we have
    # multiple optimal local decision.
    london_brewery_company_owners_mwe = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 4, 0,
                                                        False, LexicalMatch.TOKEN, 2, 6,
                                                        'London_noun brewery_noun company_noun owners_noun',
                                                        ('Z1',))
    ranker = ContextualRuleBasedRanker(4, 0)
    token_ranking_data = [
        [
            north_east_mwe,
            north_noun
        ],
        [
            east_london_brewery_mwe,
            north_east_mwe
        ],
        [
            east_london_brewery_mwe,
            london_brewery_company_owners_mwe
        ],
        [
            east_london_brewery_mwe,
            london_brewery_company_owners_mwe
        ],
        [
            london_brewery_company_owners_mwe
        ],
        [
            london_brewery_company_owners_mwe
        ]
    ]
    expected_ranks = [
        [
            130110,
            440110
        ],
        [
            120111,
            130110
        ],
        [
            120111,
            110112
        ],
        [
            120111,
            110112
        ],
        [
            110112
        ],
        [
            110112
        ]
    ]
    expected_lowest_ranked_matches = [north_east_mwe, north_east_mwe,
                                      london_brewery_company_owners_mwe,
                                      london_brewery_company_owners_mwe,
                                      london_brewery_company_owners_mwe,
                                      london_brewery_company_owners_mwe]
    assert (expected_ranks, expected_lowest_ranked_matches) \
        == ranker(token_ranking_data)

    # Edge case whereby n-gram is greater than 9.
    ski_boot_ten_mwe = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 10, 0, False,
                                       LexicalMatch.TOKEN, 0, 10,
                                       'The_det ski_noun Boot_noun is_det part_det of_det a_det test_det it_det is_det',
                                       ('Z1',))
    ski_boot_nine_mwe = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 9, 0, False,
                                        LexicalMatch.TOKEN, 0, 9,
                                        '*_det ski_noun Boot_noun is_det part_det of_det a_det test_det it_det is_det',
                                        ('Z1',))
    ranker = ContextualRuleBasedRanker(10, 0)
    ranking_data = [
        ski_boot_ten_mwe,
        ski_boot_nine_mwe
    ]
    token_ranking_data = [ranking_data] * 9
    token_ranking_data.append([
        ski_boot_ten_mwe
    ])
    expected_ranks = [
        [10101100,
         10201100]
    ] * 9
    expected_ranks.append([10101100])
    expected_lowest_ranked_matches = [ski_boot_ten_mwe] * 10
    assert (expected_ranks, expected_lowest_ranked_matches) \
        == ranker(token_ranking_data)

    # Edge case of token start index greater than 9
    ski_start_index_ten = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0, False,
                                          LexicalMatch.TOKEN, 10, 11,
                                          'ski_noun',
                                          ('Z1',))
    token_ranking_data.append([ski_start_index_ten])
    expected_ranks.append([41001110])
    expected_lowest_ranked_matches = [ski_boot_ten_mwe] * 10
    expected_lowest_ranked_matches.append(ski_start_index_ten)
    assert (expected_ranks, expected_lowest_ranked_matches) \
        == ranker(token_ranking_data)

    # Edge case whereby the number of wildcards in a token is greater than 9
    # Of which the wildcard that has 10 wildcards and is only 2 gram long
    # should be ranked lower than the 9 wildcards that is a wildcard
    ranker = ContextualRuleBasedRanker(2, 10)
    ski_wild_mwe = RankingMetaData(LexiconType.MWE_WILDCARD, 2, 10, False,
                                   LexicalMatch.TOKEN, 0, 2,
                                   'ski_***** *****_noun', ('Z1',))
    wild_boot_mwe = RankingMetaData(LexiconType.MWE_WILDCARD, 2, 9, False,
                                    LexicalMatch.TOKEN, 0, 2,
                                    '****_noun Boot_*****', ('Z1',))
    ranking_data = [
        ski_wild_mwe,
        wild_boot_mwe
    ]
    token_ranking_data = [ranking_data] * 2
    expected_ranks = [
        [2110110,
         2109110]
    ] * 2
    expected_lowest_ranked_matches = [wild_boot_mwe, wild_boot_mwe]
    assert (expected_ranks, expected_lowest_ranked_matches) \
        == ranker(token_ranking_data)


def test_contextual_rule_based_ranker_int_2_str() -> None:
    assert '2' == ContextualRuleBasedRanker.int_2_str(2, 1)
    assert '02' == ContextualRuleBasedRanker.int_2_str(2, 2)
    assert '312' == ContextualRuleBasedRanker.int_2_str(312, 3)
    assert '0312' == ContextualRuleBasedRanker.int_2_str(312, 4)

    with pytest.raises(ValueError):
        ContextualRuleBasedRanker.int_2_str(312, 2)


def test_contextual_rule_based_ranker_get_global_lowest_ranks() -> None:
    north_east = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0,
                                 False, LexicalMatch.TOKEN, 0, 2,
                                 'North_noun East_noun', ('Z1',))
    east_london_brewery = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 3, 0,
                                          False, LexicalMatch.TOKEN, 1, 4,
                                          'East_noun London_noun brewery_noun', ('Z1',))
    token_ranking_data = [
        [
            north_east
        ],
        [
            north_east,
            east_london_brewery
        ],
        [
            east_london_brewery
        ],
        [
            east_london_brewery
        ]
    ]
    token_rankings = [[120110], [120110, 110111], [110111], [110111]]
    expected_lowest_ranked_matches = [None, east_london_brewery,
                                      east_london_brewery, east_london_brewery]
    assert (ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data,
                                                              token_rankings, None)
            == expected_lowest_ranked_matches)
    
    # Test that it can exclude matches
    expected_lowest_ranked_matches = [north_east, north_east, None, None]
    ranking_data_to_exclude = {east_london_brewery}
    assert (ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data, token_rankings,
                                                              ranking_data_to_exclude)
            == expected_lowest_ranked_matches)
    
    # Test that it raises assertion errors when the length of the inner and
    # outer lists of token ranking data and rankings do not match.

    # Outer assertion error test
    token_ranking_data = [
        [
            north_east
        ],
        [
            north_east
        ]
    ]
    token_rankings = [[120110]]
    with pytest.raises(AssertionError):
        ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data,
                                                          token_rankings)
    
    # Inner assertion error test
    token_rankings = [[120110], [120110, 110111]]
    with pytest.raises(AssertionError):
        ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data,
                                                          token_rankings)


def test_contextual_rule_based_ranker_get_construction_arguments() -> None:
    rules: List[Rule] = []
    # Empty case
    assert (0, 0) == ContextualRuleBasedRanker.get_construction_arguments(rules)

    # Single Word Rules
    pt_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Portuguese/semantic_lexicon_pt.tsv"
    single_lexicon = LexiconCollection.from_tsv(pt_lexicon_url)
    single_lemma_lexicon = LexiconCollection.from_tsv(pt_lexicon_url, False)
    single_word_rule = SingleWordRule(single_lexicon, single_lemma_lexicon)
    rules.append(single_word_rule)
    assert (1, 0) == ContextualRuleBasedRanker.get_construction_arguments(rules)

    pt_mwe_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Portuguese/mwe-pt.tsv"
    mwe_lexicon = MWELexiconCollection.from_tsv(pt_mwe_lexicon_url)
    mwe_word_rule = MWERule(mwe_lexicon)
    rules.append(mwe_word_rule)
    assert (9, 4) == ContextualRuleBasedRanker.get_construction_arguments(rules)

    es_mwe_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Spanish/mwe-es.tsv"
    es_mwe_lexicon = MWELexiconCollection.from_tsv(es_mwe_lexicon_url)
    es_mwe_word_rule = MWERule(es_mwe_lexicon)
    rules.append(es_mwe_word_rule)
    assert (9, 4) == ContextualRuleBasedRanker.get_construction_arguments(rules)

    del rules[1]
    assert (9, 1) == ContextualRuleBasedRanker.get_construction_arguments(rules)
