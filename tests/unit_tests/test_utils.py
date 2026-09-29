from collections.abc import Iterable
from typing import List, Optional, Set, Tuple

import pytest

from pymusas.utils import (
    contains_default_tag,
    default_token_index,
    resolve_default_tags,
    token_pos_tags_in_lexicon_entry,
    unique_pos_tags_in_lexicon_entry,
)


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


@pytest.mark.parametrize("semantic_tags, expected", [
    (['Df'], True),
    (['Df+++'], True),
    (['Dfc'], True),
    (['I4/Dfc'], True),
    (['Df/X5.2++mfn'], True),
    (['Df%'], True),
    (['Df@'], True),
    (['Df-m%'], True),
    (['Df@mf'], True),
    (['C1/Df+@'], True),
    (['Df%+'], True),
    (['Dfm+'], True),
    (['Dfmf-%'], True),
    (['Df+m-'], True),
    (['Df1'], False),
    (['Df.1'], False),
    (['Z3', 'Df/O2'], True),
    (['Z3', 'A1/B2'], False),
    (['Dfx1'], False),
    (['ADf'], False),
    ([], False),
])
def test_contains_default_tag(semantic_tags: List[str], expected: bool) -> None:
    assert expected == contains_default_tag(semantic_tags)


@pytest.mark.parametrize("mwe_template, expected", [
    ('*_ADJ style_NOUN', 0),
    ('*ing_NOUN job*_*', 0),
    ('half_DET a*_DET *_NOUN', 2),
    ('on_ADP the_DET *_ADJ side_NOUN', 2),
    ('*_* minded_*', 0),
    ('ski_NOUN boot*_NOUN', None),
    ('ski_* boot_*', None),
])
def test_default_token_index(mwe_template: str, expected: Optional[int]) -> None:
    assert expected == default_token_index(mwe_template)


@pytest.mark.parametrize("semantic_tags, replacement, expected", [
    (['Df'], 'A1/Z3', ['A1']),
    (['C1/Df'], 'A1/Z3', ['C1/A1']),
    (['Df++'], 'A1', ['A1++']),
    (['Df+++'], 'N3.8+', ['N3.8+++']),
    (['Df'], 'N3.8+', ['N3.8']),
    (['Df'], 'A5.1+++mfnc', ['A5.1']),
    (['Dfc'], 'I2.1mf', ['I2.1c']),
    (['I4/Dfc'], 'I2.1', ['I4/I2.1c']),
    (['Df/X5.2++mfn'], 'E2-', ['E2/X5.2++mfn']),
    (['Df%'], 'A1', ['A1%']),
    (['Df+@'], 'A1', ['A1+@']),
    (['Df-m%'], 'A1', ['A1-m%']),
    (['Df@mf'], 'A1', ['A1@mf']),
    (['Dfm+'], 'A1', ['A1m+']),
    (['Df%+'], 'A1', ['A1%+']),
    (['Dfmf--@'], 'A1', ['A1mf--@']),
    (['Df'], 'A1+@', ['A1']),
    (['Df'], 'S2mf%', ['S2']),
    (['Df%'], None, ['Z99']),
    (['Df/O2', 'Df'], 'B5', ['B5/O2', 'B5']),
    (['Z3'], 'A1', ['Z3']),
    (['Df'], None, ['Z99']),
    (['Df+++'], None, ['Z99']),
    (['C1/Df', 'Z3'], None, ['C1/Z99', 'Z3']),
])
def test_resolve_default_tags(semantic_tags: List[str],
                              replacement: Optional[str],
                              expected: List[str]) -> None:
    assert expected == resolve_default_tags(semantic_tags, replacement)
