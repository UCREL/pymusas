from collections.abc import Iterable
from typing import List, Set, Tuple

import pytest

from pymusas.utils import token_pos_tags_in_lexicon_entry, unique_pos_tags_in_lexicon_entry


@pytest.fixture
def examples() -> List[str]:
    return [
        'East_noun London_noun is_det great_adj',
        'East_noun',
        ' East_noun',
        'East_noun '
    ]
    

@pytest.fixture
def example_unique_pos_tags() -> List[Set[str]]:
    return [
        set({'noun', 'adj', 'det'}),
        set({'noun'}),
        set({'noun'}),
        set({'noun'})
    ]


@pytest.fixture
def example_token_pos_tags() -> List[List[Tuple[str, str]]]:
    return [
        [
            ('East', 'noun'),
            ('London', 'noun'),
            ('is', 'det'),
            ('great', 'adj')
        ],
        [('East', 'noun')],
        [('East', 'noun')],
        [('East', 'noun')]
    ]


@pytest.fixture
def value_error_examples() -> List[str]:
    return [
        'Ea_st_noun',
        'East_noun __adj'
    ]


def test_token_pos_tags_in_lexicon_entry(examples: List[str],
                                         example_token_pos_tags: List[List[Tuple[str, str]]],
                                         value_error_examples: List[str]) -> None:
    for example, token_pos_tags in zip(examples, example_token_pos_tags):
        generated_token_pos_tags = token_pos_tags_in_lexicon_entry(example)
        assert isinstance(generated_token_pos_tags, Iterable)
        assert token_pos_tags == list(generated_token_pos_tags)
    
    for value_error_example in value_error_examples:
        with pytest.raises(ValueError):
            list(token_pos_tags_in_lexicon_entry(value_error_example))


def test_unique_pos_tags_in_lexicon_entry(examples: List[str],
                                          example_unique_pos_tags: List[Set[str]],
                                          value_error_examples: List[str]) -> None:
    for example, unique_pos_tag in zip(examples, example_unique_pos_tags):
        assert unique_pos_tag == unique_pos_tags_in_lexicon_entry(example)

    for value_error_example in value_error_examples:
        with pytest.raises(ValueError):
            unique_pos_tags_in_lexicon_entry(value_error_example)
