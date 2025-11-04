from dataclasses import FrozenInstanceError

import pytest

from pymusas.lexicon_collection import LexiconMetaData, LexiconType


LEXICON_META_DATA = LexiconMetaData(['Z1', 'Z2'], 2, LexiconType.MWE_NON_SPECIAL, 0)


def test_lexicon_meta_data() -> None:
        
    assert LEXICON_META_DATA.semantic_tags == ['Z1', 'Z2']
    assert LEXICON_META_DATA.n_gram_length == 2
    assert LEXICON_META_DATA.lexicon_type == LexiconType.MWE_NON_SPECIAL
    assert LEXICON_META_DATA.wildcard_count == 0
    expected_str = ("LexiconMetaData(semantic_tags=['Z1', 'Z2'], "
                    "n_gram_length=2, "
                    "lexicon_type=LexiconType.MWE_NON_SPECIAL,"
                    " wildcard_count=0)")
    assert str(LEXICON_META_DATA) == expected_str
    
    with pytest.raises(FrozenInstanceError):
        for attribute in ['semantic_tags', 'n_gram_length', 'lexicon_type', 'wildcard_count']:
            setattr(LEXICON_META_DATA, attribute, 'test')

    assert LEXICON_META_DATA != LexiconMetaData(['Z2', 'Z1'], 2,
                                                LexiconType.MWE_NON_SPECIAL, 0)
    assert LEXICON_META_DATA == LexiconMetaData(['Z1', 'Z2'], 2,
                                                LexiconType.MWE_NON_SPECIAL, 0)
    eval(LEXICON_META_DATA.__repr__())
    assert LEXICON_META_DATA == eval(LEXICON_META_DATA.__repr__())
