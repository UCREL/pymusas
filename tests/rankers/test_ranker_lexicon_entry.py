from dataclasses import FrozenInstanceError
from typing import List

import pytest

from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker, LexicalMatch, LexiconEntryRanker, RankingMetaData


RANKING_META_DATA = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 1,
                                    False, LexicalMatch.TOKEN, 1, 3)


def test_lexical_match() -> None:
    expected_name_values = [('TOKEN', 1), ('LEMMA', 2),
                            ('TOKEN_LOWER', 3), ('LEMMA_LOWER', 4)]
    for name, value in expected_name_values:
        assert value == getattr(LexicalMatch, name)
    
    assert 2 < LexicalMatch.LEMMA_LOWER
    assert 2 > LexicalMatch.TOKEN

    eval(LexicalMatch.TOKEN.__repr__())
    assert LexicalMatch.TOKEN == eval(LexicalMatch.TOKEN.__repr__())


def test_ranking_meta_data() -> None:
    assert 2 == RANKING_META_DATA.lexicon_n_gram_length
    assert LexiconType.MWE_NON_SPECIAL == RANKING_META_DATA.lexicon_type
    assert 1 == RANKING_META_DATA.lexicon_wildcard_count
    assert not RANKING_META_DATA.exclude_pos_information
    assert LexicalMatch.TOKEN == RANKING_META_DATA.lexical_match
    assert 1 == RANKING_META_DATA.token_match_start_index
    assert 3 == RANKING_META_DATA.token_match_end_index

    expected_str = ("RankingMetaData(lexicon_type=LexiconType.MWE_NON_SPECIAL, "
                    "lexicon_n_gram_length=2, "
                    "lexicon_wildcard_count=1, exclude_pos_information=False,"
                    " lexical_match=LexicalMatch.TOKEN, "
                    "token_match_start_index=1, token_match_end_index=3)")
    assert expected_str == str(RANKING_META_DATA)

    with pytest.raises(FrozenInstanceError):
        for attribute in ['lexicon_n_gram_length', 'lexicon_type',
                          'lexicon_wildcard_count', 'exclude_pos_information',
                          'lexical_match', 'token_match_start_index',
                          'token_match_end_index']:
            setattr(RANKING_META_DATA, attribute, 'test')
    
    assert RANKING_META_DATA != RankingMetaData(LexiconType.MWE_NON_SPECIAL, 1,
                                                1, False, LexicalMatch.TOKEN, 1, 3)
    assert RANKING_META_DATA == RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2,
                                                1, False, LexicalMatch.TOKEN, 1, 3)
    eval(RANKING_META_DATA.__repr__())
    assert RANKING_META_DATA == eval(RANKING_META_DATA.__repr__())


def test_lexicon_entry_ranker() -> None:
    
    class TestRanker(LexiconEntryRanker):

        def __call__(self, token_ranking_data: List[List[RankingMetaData]]
                     ) -> List[List[int]]:
            return [[0]]

    concrete_ranker = TestRanker()
    assert [[0]] == concrete_ranker([[RANKING_META_DATA]])
    isinstance(concrete_ranker, LexiconEntryRanker)


def test_contextual_rule_based_ranker() -> None:
    assert isinstance(ContextualRuleBasedRanker(), LexiconEntryRanker)

    ranker = ContextualRuleBasedRanker()
    assert [[]] == ranker([])

    token_ranking_data = [
        [
            RankingMetaData(LexiconType.MWE_WILDCARD, 2, 1, False, LexicalMatch.TOKEN, 2, 3),
            RankingMetaData(LexiconType.MWE_WILDCARD, 2, 1, False, LexicalMatch.LEMMA, 2, 3),
            RankingMetaData(LexiconType.MWE_WILDCARD, 2, 1, False, LexicalMatch.TOKEN_LOWER, 2, 3),
            RankingMetaData(LexiconType.MWE_WILDCARD, 2, 1, False, LexicalMatch.LEMMA_LOWER, 2, 3)
        ],
        [
            RankingMetaData(LexiconType.MWE_CURLY_BRACES, 1, 1, False, LexicalMatch.TOKEN, 2, 3),
            RankingMetaData(LexiconType.MWE_NON_SPECIAL, 1, 1, False, LexicalMatch.TOKEN, 3, 4),
            RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 1, True, LexicalMatch.TOKEN, 1, 5)
        ]
    ]
    expected_ranks = [
        [
            221112,
            221122,
            221132,
            221142
        ],
        [
            311112,
            111113,
            411211
        ]
    ]
    assert expected_ranks == ranker(token_ranking_data)

    # Edge case whereby the token_match_start_index is a large number
    token_ranking_data = [
        [
            RankingMetaData(LexiconType.MWE_WILDCARD, 1, 1, False, LexicalMatch.TOKEN, 200, 350),
            RankingMetaData(LexiconType.MWE_WILDCARD, 1, 2, False, LexicalMatch.TOKEN, 200, 350)
        ],
        [
            RankingMetaData(LexiconType.MWE_WILDCARD, 1, 1, False, LexicalMatch.TOKEN, 220, 370)
        ]
    ]

    expected_ranks = [
        [
            21111200,
            21211200
        ],
        [
            21111220
        ]
    ]
    assert expected_ranks == ranker(token_ranking_data)
