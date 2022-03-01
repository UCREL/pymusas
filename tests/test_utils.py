import pytest

from pymusas.utils import unique_pos_tags_in_lexicon_entry


def test_unique_pos_tags_in_lexicon_entry() -> None:
    assert set() == unique_pos_tags_in_lexicon_entry('')

    mwe_template = 'East_noun London_noun is_det great_adj'
    assert ({'noun', 'adj', 'det'}
            == unique_pos_tags_in_lexicon_entry(mwe_template))
    single_word_lexicon = 'East_noun'
    assert {'noun'} == unique_pos_tags_in_lexicon_entry(single_word_lexicon)

    single_word_lexicon = ' East_noun'
    assert {'noun'} == unique_pos_tags_in_lexicon_entry(single_word_lexicon)

    single_word_lexicon = 'East_noun '
    assert {'noun'} == unique_pos_tags_in_lexicon_entry(single_word_lexicon)

    with pytest.raises(ValueError):
        unique_pos_tags_in_lexicon_entry('Ea_st_noun')
    
    with pytest.raises(ValueError):
        unique_pos_tags_in_lexicon_entry('East_noun __adj')
