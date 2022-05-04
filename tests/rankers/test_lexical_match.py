from pymusas.rankers.lexical_match import LexicalMatch


def test_lexical_match() -> None:
    expected_name_values = [('TOKEN', 1), ('LEMMA', 2),
                            ('TOKEN_LOWER', 3), ('LEMMA_LOWER', 4)]
    for name, value in expected_name_values:
        assert value == getattr(LexicalMatch, name)
    
    assert 2 < LexicalMatch.LEMMA_LOWER
    assert 2 > LexicalMatch.TOKEN

    eval(LexicalMatch.TOKEN.__repr__())
    assert LexicalMatch.TOKEN == eval(LexicalMatch.TOKEN.__repr__())
