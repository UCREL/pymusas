from typing import List

import pytest

from pymusas.taggers.rules.util import n_gram_indexes, n_grams


def test_n_grams() -> None:
    test_tokens: List[str] = []
    empty_n_grams = n_grams(test_tokens, 1, 3)
    assert [] == list(empty_n_grams)

    test_tokens.extend(['hello', 'how', 'are', 'you', ','])
    expected_n_grams = [['hello'], ['how'], ['are'], ['you'], [',']]
    assert expected_n_grams == list(n_grams(test_tokens, 1, 1))

    expected_n_grams = [['hello', 'how', 'are'], ['how', 'are', 'you'], ['are', 'you', ','],
                        ['hello', 'how'], ['how', 'are'], ['are', 'you'], ['you', ',']]
    assert expected_n_grams == list(n_grams(test_tokens, 2, 3))

    assert [['hello', 'how', 'are', 'you', ',']] == list(n_grams(test_tokens, 5, 8))
    
    assert [] == list(n_grams(test_tokens, 6, 8))

    with pytest.raises(ValueError):
        list(n_grams(test_tokens, 0, 1))

    with pytest.raises(ValueError):
        list(n_grams(test_tokens, 2, 1))


def test_n_gram_indexes() -> None:
    test_tokens: List[str] = []
    empty_n_grams = n_gram_indexes(test_tokens, 1, 3)
    assert [] == list(empty_n_grams)

    test_tokens.extend(['hello', 'how', 'are', 'you', ','])
    expected_n_gram_indexes = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    assert expected_n_gram_indexes == list(n_gram_indexes(test_tokens, 1, 1))

    expected_n_gram_indexes = [(0, 3), (1, 4), (2, 5), (0, 2), (1, 3), (2, 4), (3, 5)]
    assert expected_n_gram_indexes == list(n_gram_indexes(test_tokens, 2, 3))

    assert [(0, 5)] == list(n_gram_indexes(test_tokens, 5, 8))
    
    assert [] == list(n_gram_indexes(test_tokens, 6, 8))

    with pytest.raises(ValueError):
        list(n_gram_indexes(test_tokens, 0, 1))

    with pytest.raises(ValueError):
        list(n_gram_indexes(test_tokens, 2, 1))
