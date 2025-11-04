from dataclasses import FrozenInstanceError

import pytest

from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexical_match import LexicalMatch
from pymusas.rankers.ranking_meta_data import RankingMetaData


RANKING_META_DATA = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 1,
                                    False, LexicalMatch.TOKEN, 1, 3,
                                    'snow_noun boot_noun', ('Z5', 'Z4'))


def test_ranking_meta_data() -> None:
    assert 2 == RANKING_META_DATA.lexicon_n_gram_length
    assert LexiconType.MWE_NON_SPECIAL == RANKING_META_DATA.lexicon_type
    assert 1 == RANKING_META_DATA.lexicon_wildcard_count
    assert not RANKING_META_DATA.exclude_pos_information
    assert LexicalMatch.TOKEN == RANKING_META_DATA.lexical_match
    assert 1 == RANKING_META_DATA.token_match_start_index
    assert 3 == RANKING_META_DATA.token_match_end_index
    assert 'snow_noun boot_noun' == RANKING_META_DATA.lexicon_entry_match
    assert ('Z5', 'Z4') == RANKING_META_DATA.semantic_tags

    expected_str = ("RankingMetaData(lexicon_type=LexiconType.MWE_NON_SPECIAL, "
                    "lexicon_n_gram_length=2, "
                    "lexicon_wildcard_count=1, exclude_pos_information=False,"
                    " lexical_match=LexicalMatch.TOKEN, "
                    "token_match_start_index=1, token_match_end_index=3,"
                    " lexicon_entry_match='snow_noun boot_noun', "
                    "semantic_tags=('Z5', 'Z4'))")
    assert expected_str == str(RANKING_META_DATA)

    with pytest.raises(FrozenInstanceError):
        for attribute in ['lexicon_n_gram_length', 'lexicon_type',
                          'lexicon_wildcard_count', 'exclude_pos_information',
                          'lexical_match', 'token_match_start_index',
                          'token_match_end_index', 'lexicon_entry_match',
                          'semantic_tags']:
            setattr(RANKING_META_DATA, attribute, 'test')
    
    assert RANKING_META_DATA != RankingMetaData(LexiconType.MWE_NON_SPECIAL, 1,
                                                1, False, LexicalMatch.TOKEN, 1,
                                                3, 'snow_noun boot_noun',
                                                ('Z5', 'Z4'))
    assert RANKING_META_DATA == RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2,
                                                1, False, LexicalMatch.TOKEN, 1,
                                                3, 'snow_noun boot_noun',
                                                ('Z5', 'Z4'))
    eval(RANKING_META_DATA.__repr__())
    assert RANKING_META_DATA == eval(RANKING_META_DATA.__repr__())
