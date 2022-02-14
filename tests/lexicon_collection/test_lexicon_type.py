from pymusas.lexicon_collection import LexiconType


def test_lexicon_type() -> None:
    assert 4 == len(LexiconType)

    expected_output = {
        'SINGLE_NON_SPECIAL': 'Single Non Special',
        'MWE_NON_SPECIAL': 'MWE Non Special',
        'MWE_WILDCARD': 'MWE Wildcard',
        'MWE_CURLY_BRACES': 'MWE Curly Braces'
    }
    
    for lexicon_type in LexiconType:
        assert isinstance(lexicon_type.name, str)
        assert isinstance(lexicon_type.value, str)
        assert expected_output[lexicon_type.name] == lexicon_type.value
    
    lexicon_types = [
        LexiconType.SINGLE_NON_SPECIAL,
        LexiconType.MWE_NON_SPECIAL,
        LexiconType.MWE_WILDCARD,
        LexiconType.MWE_CURLY_BRACES
    ]
    for lexicon_type in lexicon_types:
        lexicon_type == eval(lexicon_type.__repr__())
