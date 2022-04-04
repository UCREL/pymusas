from collections.abc import MutableMapping
from copy import deepcopy
import importlib
import os
from pathlib import Path
import re
import tempfile
from typing import Any, DefaultDict, Dict, List, Optional, Union

import pytest
import responses

from pymusas import config
from pymusas.lexicon_collection import LexiconMetaData, LexiconType, MWELexiconCollection


MWE_TEMPLATES = {
    'A_pnoun Arnoia_pnoun': ['Z2'],
    'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': ['Z2'],
    'a_prep carta_noun cabal_adj': ['A4', 'A5.1'],
    '***_prep carta_* cabal_adj': ['A4', 'A5.1'],
    'ano*_prep carta_noun': ['B4', 'B5.1'],
    'bno*_prep carta_noun': ['C4', 'C5.1'],
}
MWE_TEMPLATES_POS_MAPPING_NON_SPECIAL = {
    'A_NN Arnoia_NN': 'A_pnoun Arnoia_pnoun',
    'A_NN Pobra_NN de_NN Trives_NN': 'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun'
}
MWE_TEMPLATES_POS_MAPPING_REGULAR_EXPRESSIONS = {
    LexiconType.MWE_NON_SPECIAL: {
        3: {
            'a': {
                'a_prep carta_noun cabal_adj': re.compile(r'a_prep\ carta_noun\ cabal_(?:ADJ|JJ)')
            }
        }
    },
    LexiconType.MWE_WILDCARD: {
        3: {
            '*': {
                '***_prep carta_* cabal_adj': re.compile(r'[^\s_]*[^\s_]*[^\s_]*_prep\ carta_[^\s_]*\ cabal_(?:ADJ|JJ)')
            }
            
        },
        2: {
            'a': {
                'ano*_prep carta_noun': re.compile(r'ano[^\s_]*_prep\ carta_noun'),
            },
            'b': {
                'bno*_prep carta_noun': re.compile(r'bno[^\s_]*_prep\ carta_noun')
            }
        }
    }
}
MWE_TEMPLATE_ITEMS = {
    'A_pnoun Arnoia_pnoun': LexiconMetaData(['Z2'], 2, LexiconType.MWE_NON_SPECIAL, 0),
    'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': LexiconMetaData(['Z2'], 4, LexiconType.MWE_NON_SPECIAL, 0),
    'a_prep carta_noun cabal_adj': LexiconMetaData(['A4', 'A5.1'], 3, LexiconType.MWE_NON_SPECIAL, 0),
    '***_prep carta_* cabal_adj': LexiconMetaData(['A4', 'A5.1'], 3, LexiconType.MWE_WILDCARD, 4),
    'ano*_prep carta_noun': LexiconMetaData(['B4', 'B5.1'], 2, LexiconType.MWE_WILDCARD, 1),
    'bno*_prep carta_noun': LexiconMetaData(['C4', 'C5.1'], 2, LexiconType.MWE_WILDCARD, 1),
}
POS_MAPPER = {
    "pnoun": ['NN'],
    "adj": ['ADJ', 'JJ']
}
DATA_DIR = Path(__file__, '..', '..', 'data').resolve()
LEXICON_DATA_DIR = Path(DATA_DIR, 'lexicon_collection', 'MWELexiconCollection')
MWE_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'mwe_lexicon.tsv')
EXTRA_FIELDS_MWE_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'extra_fields_lexicon.tsv')
ERROR_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'error_lexicon.tsv')
NO_HEADER_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'no_header_lexicon.tsv')
DUPLICATE_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'duplicate_key_lexicon.tsv')


def compare_nested_dictionaries(dict_1: Dict[Any, Any],
                                dict_2: Union[Dict[Any, Any],
                                              DefaultDict[Any, Any]]) -> bool:
    
    dictionary_length_error = ('Lengths of the dictionaries are not equal: '
                               f'{len(dict_1)}, {len(dict_2)}.\n Dictionaries:'
                               f' Dict 1: {dict_1}\nDict 2: {dict_2}')
    assert len(dict_1) == len(dict_2), dictionary_length_error
    
    dict_1_keys = list(dict_1)
    dict_2_keys = list(dict_2)
    non_equal_keys_error = (f'Keys of the dictionaries are not equal: '
                            f'{dict_1_keys}, {dict_2_keys}')
    for key_1, value_1 in dict_1.items():
        if key_1 not in dict_2:
            raise KeyError(non_equal_keys_error)
        value_2 = dict_2[key_1]
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            if not compare_nested_dictionaries(value_1, value_2):
                return False
        else:
            assert value_1 == value_2
    return True


def test_mwe_lexicon_collection_class_type() -> None:
    empty_collection = MWELexiconCollection()
    assert isinstance(empty_collection, MWELexiconCollection)
    assert isinstance(empty_collection, MutableMapping)


def test_mwe_lexicon_collection_init() -> None:

    empty_collection = MWELexiconCollection()
    assert not empty_collection.meta_data
    assert not empty_collection.mwe_regular_expression_lookup
    assert 0 == empty_collection.longest_non_special_mwe_template
    assert 0 == empty_collection.longest_wildcard_mwe_template
    assert 0 == empty_collection.longest_mwe_template
    assert 0 == empty_collection.most_wildcards_in_mwe_template
    assert {} == empty_collection.pos_mapper
    assert set() == empty_collection.one_to_many_pos_tags
    assert {} == empty_collection.pos_mapping_lookup
    assert not empty_collection.pos_mapping_regular_expression_lookup
    
    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert len(lexicon_collection.meta_data) == 6
    assert len(lexicon_collection.mwe_regular_expression_lookup) == 2
    assert 4 == lexicon_collection.longest_non_special_mwe_template
    assert 3 == lexicon_collection.longest_wildcard_mwe_template
    assert 4 == lexicon_collection.longest_mwe_template
    assert 4 == lexicon_collection.most_wildcards_in_mwe_template
    assert {} == lexicon_collection.pos_mapper
    assert set() == lexicon_collection.one_to_many_pos_tags
    assert {} == lexicon_collection.pos_mapping_lookup
    assert not lexicon_collection.pos_mapping_regular_expression_lookup

    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, POS_MAPPER)
    assert len(lexicon_collection.meta_data) == 6
    assert len(lexicon_collection.mwe_regular_expression_lookup) == 0
    assert 4 == lexicon_collection.longest_non_special_mwe_template
    assert 3 == lexicon_collection.longest_wildcard_mwe_template
    assert 4 == lexicon_collection.longest_mwe_template
    assert 4 == lexicon_collection.most_wildcards_in_mwe_template
    assert POS_MAPPER == lexicon_collection.pos_mapper
    assert {'adj'} == lexicon_collection.one_to_many_pos_tags
    assert MWE_TEMPLATES_POS_MAPPING_NON_SPECIAL == lexicon_collection.pos_mapping_lookup
    assert MWE_TEMPLATES_POS_MAPPING_REGULAR_EXPRESSIONS == lexicon_collection.pos_mapping_regular_expression_lookup


def test_mwe_lexicon_collection_len() -> None:

    empty_collection = MWELexiconCollection()
    assert 0 == len(empty_collection)

    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert len(lexicon_collection) == 6


def test_mwe_lexicon_collection__eq__() -> None:
    empty_collection = MWELexiconCollection()
    
    assert 1 != empty_collection

    assert empty_collection == MWELexiconCollection()

    empty_collection['snow_noun boots_noun'] = ['Z1']
    assert empty_collection != MWELexiconCollection(MWE_TEMPLATES)

    for key, value in MWE_TEMPLATES.items():
        empty_collection[key] = value
    del empty_collection['A_pnoun Arnoia_pnoun']
    assert empty_collection != MWELexiconCollection(MWE_TEMPLATES)
    
    del empty_collection['snow_noun boots_noun']
    empty_collection['A_pnoun Arnoia_pnoun'] = ['Z2']
    assert empty_collection == MWELexiconCollection(MWE_TEMPLATES)
    assert empty_collection != MWELexiconCollection(MWE_TEMPLATES, POS_MAPPER)


def test_mwe_lexicon_collection_set_get_del_item() -> None:

    empty_collection = MWELexiconCollection()
    assert not empty_collection.meta_data

    empty_collection['A_pnoun Arnoia_pnoun'] = ['Z2']
    empty_collection['A_pnoun Arnoia_pnoun'] = ['Z1']
    empty_collection['a_prep carta_noun cabal_adj'] = ['A4', 'A5.1']
    expected_meta_data = LexiconMetaData(['Z1'], 2, LexiconType.MWE_NON_SPECIAL, 0)
    assert expected_meta_data == empty_collection['A_pnoun Arnoia_pnoun']
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert 3 == empty_collection.longest_non_special_mwe_template
    assert 0 == empty_collection.longest_wildcard_mwe_template
    assert 3 == empty_collection.longest_mwe_template
    assert 0 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection) == 2

    del empty_collection['a_prep carta_noun cabal_adj']
    assert len(empty_collection) == 1
    assert 2 == empty_collection.longest_non_special_mwe_template
    assert 0 == empty_collection.longest_wildcard_mwe_template
    assert 2 == empty_collection.longest_mwe_template
    assert 0 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    
    empty_collection['a_prep *_noun cabal_adj'] = ['A4', 'A5.1']
    assert len(empty_collection) == 2
    assert 2 == empty_collection.longest_non_special_mwe_template
    assert 3 == empty_collection.longest_wildcard_mwe_template
    assert 3 == empty_collection.longest_mwe_template
    assert 1 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 1
    
    assert ('a_prep *_noun cabal_adj'
            in empty_collection.mwe_regular_expression_lookup[3]['a'])
    del empty_collection['a_prep *_noun cabal_adj']
    assert ('a_prep *_noun cabal_adj'
            not in empty_collection.mwe_regular_expression_lookup[3]['a'])

    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert len(lexicon_collection.mwe_regular_expression_lookup) == 2

    assert (lexicon_collection.mwe_regular_expression_lookup[2]['a']['ano*_prep carta_noun']
            == re.compile(r'ano[^\s_]*_prep\ carta_noun'))
    assert (lexicon_collection.mwe_regular_expression_lookup[2]['b']['bno*_prep carta_noun']
            == re.compile(r'bno[^\s_]*_prep\ carta_noun'))
    assert (lexicon_collection.mwe_regular_expression_lookup[3]['*']['***_prep carta_* cabal_adj']
            == re.compile(r'[^\s_]*[^\s_]*[^\s_]*_prep\ carta_[^\s_]*\ cabal_adj'))

    # Test that warning is raised when trying to add a MWE tempalate that contains
    # a curly brace, as we currently do not support curly braces.
    with pytest.warns(UserWarning):
        MWELexiconCollection({'cynllun*_NOUN {NOUN} bws_NOUN am_PREP ddim_NOUN': ['Z1']})


def test_mwe_lexicon_collection_set_get_del_item_pos_mapped() -> None:

    # Test adding data to an empty collection
    empty_collection = MWELexiconCollection(pos_mapper=POS_MAPPER)
    assert not empty_collection.meta_data

    for template, tags in MWE_TEMPLATES.items():
        empty_collection[template] = tags
    expected_meta_data = LexiconMetaData(['Z2'], 2, LexiconType.MWE_NON_SPECIAL, 0)
    assert expected_meta_data == empty_collection['A_pnoun Arnoia_pnoun']
    assert len(empty_collection.meta_data) == 6
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert 4 == empty_collection.longest_non_special_mwe_template
    assert 3 == empty_collection.longest_wildcard_mwe_template
    assert 4 == empty_collection.longest_mwe_template
    assert 4 == empty_collection.most_wildcards_in_mwe_template
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert MWE_TEMPLATES_POS_MAPPING_NON_SPECIAL == empty_collection.pos_mapping_lookup
    assert MWE_TEMPLATES_POS_MAPPING_REGULAR_EXPRESSIONS == empty_collection.pos_mapping_regular_expression_lookup
    
    # Test deleting the largest NON Special MWE template that is one-to-one
    # POS mapped
    del empty_collection['A_pnoun Pobra_pnoun de_pnoun Trives_pnoun']
    assert len(empty_collection) == 5
    assert 3 == empty_collection.longest_non_special_mwe_template
    assert 3 == empty_collection.longest_wildcard_mwe_template
    assert 3 == empty_collection.longest_mwe_template
    assert 4 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert {'A_NN Arnoia_NN': 'A_pnoun Arnoia_pnoun'} == empty_collection.pos_mapping_lookup
    assert MWE_TEMPLATES_POS_MAPPING_REGULAR_EXPRESSIONS == empty_collection.pos_mapping_regular_expression_lookup
    
    # Test deleting the smallest NON Special MWE template that is one-to-one
    # POS mapped
    empty_collection['A_pnoun Pobra_pnoun de_pnoun Trives_pnoun'] = ['Z2']
    del empty_collection['A_pnoun Arnoia_pnoun']
    assert len(empty_collection) == 5
    assert 4 == empty_collection.longest_non_special_mwe_template
    assert 3 == empty_collection.longest_wildcard_mwe_template
    assert 4 == empty_collection.longest_mwe_template
    assert 4 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert {'A_NN Pobra_NN de_NN Trives_NN': 'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun'} == empty_collection.pos_mapping_lookup
    assert MWE_TEMPLATES_POS_MAPPING_REGULAR_EXPRESSIONS == empty_collection.pos_mapping_regular_expression_lookup
    
    # Test deleting all the NON Special MWE templates that are one-to-one
    # POS mapped
    del empty_collection['A_pnoun Pobra_pnoun de_pnoun Trives_pnoun']
    assert len(empty_collection) == 4
    assert 3 == empty_collection.longest_non_special_mwe_template
    assert 3 == empty_collection.longest_wildcard_mwe_template
    assert 3 == empty_collection.longest_mwe_template
    assert 4 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert {} == empty_collection.pos_mapping_lookup
    assert MWE_TEMPLATES_POS_MAPPING_REGULAR_EXPRESSIONS == empty_collection.pos_mapping_regular_expression_lookup
    
    # Test deleting all the NON Special MWE templates including one-to-many
    # POS mapped
    temp_expected_pos_mapping_regular_expressions = deepcopy(MWE_TEMPLATES_POS_MAPPING_REGULAR_EXPRESSIONS)
    del temp_expected_pos_mapping_regular_expressions[LexiconType.MWE_NON_SPECIAL][3]['a']['a_prep carta_noun cabal_adj']
    del empty_collection['a_prep carta_noun cabal_adj']
    assert len(empty_collection) == 3
    assert 0 == empty_collection.longest_non_special_mwe_template
    assert 3 == empty_collection.longest_wildcard_mwe_template
    assert 3 == empty_collection.longest_mwe_template
    assert 4 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert {} == empty_collection.pos_mapping_lookup
    compare_nested_dictionaries(temp_expected_pos_mapping_regular_expressions, empty_collection.pos_mapping_regular_expression_lookup)
    assert temp_expected_pos_mapping_regular_expressions == empty_collection.pos_mapping_regular_expression_lookup

    # Test deleting the longest wildcard MWE template
    del empty_collection['***_prep carta_* cabal_adj']
    del temp_expected_pos_mapping_regular_expressions[LexiconType.MWE_WILDCARD][3]['*']['***_prep carta_* cabal_adj']
    assert len(empty_collection) == 2
    assert 0 == empty_collection.longest_non_special_mwe_template
    assert 2 == empty_collection.longest_wildcard_mwe_template
    assert 2 == empty_collection.longest_mwe_template
    assert 1 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert {} == empty_collection.pos_mapping_lookup
    assert temp_expected_pos_mapping_regular_expressions == empty_collection.pos_mapping_regular_expression_lookup

    # Test deleting all wildcard MWE template
    del empty_collection['ano*_prep carta_noun']
    del empty_collection['bno*_prep carta_noun']
    del temp_expected_pos_mapping_regular_expressions[LexiconType.MWE_WILDCARD][2]['a']['ano*_prep carta_noun']
    del temp_expected_pos_mapping_regular_expressions[LexiconType.MWE_WILDCARD][2]['b']['bno*_prep carta_noun']
    assert len(empty_collection) == 0
    assert 0 == empty_collection.longest_non_special_mwe_template
    assert 0 == empty_collection.longest_wildcard_mwe_template
    assert 0 == empty_collection.longest_mwe_template
    assert 0 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert {} == empty_collection.pos_mapping_lookup
    assert temp_expected_pos_mapping_regular_expressions == empty_collection.pos_mapping_regular_expression_lookup

    # Test adding a POS one-to-many NON-SPECIAL lexicon entry so that it proves
    # it can update the longest_non_special_mwe_template attribute.
    empty_collection['a_prep carta_noun cabal_adj'] = ['Z2']
    temp_expected_pos_mapping_regular_expressions[LexiconType.MWE_NON_SPECIAL][3]['a']['a_prep carta_noun cabal_adj'] \
        = re.compile(r'a_prep\ carta_noun\ cabal_(?:ADJ|JJ)')
    assert len(empty_collection) == 1
    assert 3 == empty_collection.longest_non_special_mwe_template
    assert 0 == empty_collection.longest_wildcard_mwe_template
    assert 3 == empty_collection.longest_mwe_template
    assert 0 == empty_collection.most_wildcards_in_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert POS_MAPPER == empty_collection.pos_mapper
    assert {'adj'} == empty_collection.one_to_many_pos_tags
    assert {} == empty_collection.pos_mapping_lookup
    assert temp_expected_pos_mapping_regular_expressions == empty_collection.pos_mapping_regular_expression_lookup

    # Test that it raises a ValueError when inserting a template which contains
    # a wildcard in the POS tag when the POS tags need to be mapped
    with pytest.raises(ValueError):
        empty_collection['it_det was_det great_adj*'] = ['Z1']

    with pytest.raises(ValueError):
        empty_collection['it_det was_det great_*adj'] = ['Z1']

    with pytest.raises(ValueError):
        empty_collection['it_det was_det great_ad*j'] = ['Z1']

    # Test that warning is raised when trying to add a MWE tempalate that contains
    # a curly brace, as we currently do not support curly braces.
    with pytest.warns(UserWarning):
        MWELexiconCollection({'cynllun*_NOUN {NOUN} bws_NOUN am_PREP ddim_NOUN': ['Z1']},
                             pos_mapper=POS_MAPPER)


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_mwe_lexicon_collection_iter(pos_mapper: Optional[Dict[str, List[str]]]
                                     ) -> None:
    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    assert list(MWE_TEMPLATE_ITEMS) == list(mwe_lexicon_collection)


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_mwe_lexicon_collection_keys(pos_mapper: Optional[Dict[str, List[str]]]
                                     ) -> None:
    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    assert (list(MWE_TEMPLATE_ITEMS)
            == [key for key in mwe_lexicon_collection.keys()])


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_mwe_lexicon_collection_values(pos_mapper: Optional[Dict[str, List[str]]]
                                       ) -> None:
    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    assert (list(MWE_TEMPLATE_ITEMS.values())
            == [value for value in mwe_lexicon_collection.values()])


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_mwe_lexicon_collection_items(pos_mapper: Optional[Dict[str, List[str]]]
                                      ) -> None:
    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    assert (list(MWE_TEMPLATE_ITEMS.items())
            == [item for item in mwe_lexicon_collection.items()])


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_mwe_lexicon_collection_repr(pos_mapper: Optional[Dict[str, List[str]]]
                                     ) -> None:
    str_pos_mapper = pos_mapper
    if str_pos_mapper is None:
        str_pos_mapper = {}

    empty_collection = MWELexiconCollection(pos_mapper=pos_mapper)
    expected_empty_collection = ('MWELexiconCollection(data={}, '
                                 f'pos_mapper={str_pos_mapper})')
    assert expected_empty_collection == empty_collection.__repr__()
    assert empty_collection == eval(empty_collection.__repr__())

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    mwe_lexicon_repr = ("MWELexiconCollection(data={'A_pnoun Arnoia_pnoun': ['Z2'], "
                        "'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': ['Z2'], "
                        "'a_prep carta_noun cabal_adj': ['A4', 'A5.1'], "
                        "'***_prep carta_* cabal_adj': ['A4', 'A5.1'], "
                        "'ano*_prep carta_noun': ['B4', 'B5.1'], "
                        "'bno*_prep carta_noun': ['C4', 'C5.1']},"
                        f" pos_mapper={str_pos_mapper})")
    assert mwe_lexicon_repr == mwe_lexicon_collection.__repr__()
    assert mwe_lexicon_collection == eval(mwe_lexicon_collection.__repr__())


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_mwe_lexicon_collection_str(pos_mapper: Optional[Dict[str, List[str]]]
                                    ) -> None:

    empty_collection = MWELexiconCollection(pos_mapper=pos_mapper)
    expected_str = 'MWELexiconCollection() (0 entires in the collection)'
    if pos_mapper is not None:
        expected_str += ' (Using a POS Mapper)'
    assert expected_str \
        == str(empty_collection)

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    expected_str = ("MWELexiconCollection(('A_pnoun Arnoia_pnoun': "
                    "LexiconMetaData(semantic_tags=['Z2'], n_gram_length=2, "
                    f"lexicon_type={LexiconType.MWE_NON_SPECIAL.__str__()}, "
                    "wildcard_count=0)), "
                    "('A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': "
                    "LexiconMetaData(semantic_tags=['Z2'], n_gram_length=4, "
                    f"lexicon_type={LexiconType.MWE_NON_SPECIAL.__str__()}, "
                    "wildcard_count=0)), ... )"
                    " (6 entires in the collection)")
    if pos_mapper is not None:
        expected_str += ' (Using a POS Mapper)'
    assert expected_str == str(mwe_lexicon_collection)


def test_escape_mwe() -> None:
    # The last test shows that POS tags do not escape regular expression syntax,
    # in this case `+`
    test_expected_mwe_templates = [('', ''),
                                   ('ano_prep carta_noun', r'ano_prep\ carta_noun'),
                                   ('ano*_prep carta_noun', r'ano[^\s_]*_prep\ carta_noun'),
                                   ('***_prep carta_* cabal_adj',
                                    r'[^\s_]*[^\s_]*[^\s_]*_prep\ carta_[^\s_]*\ cabal_adj'),
                                   ('+++_prep carta_+ cabal_adj',
                                    r'\+\+\+_prep\ carta_+\ cabal_adj')]
    for test, expected in test_expected_mwe_templates:
        assert expected == MWELexiconCollection.escape_mwe(test)


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_mwe_match(pos_mapper: Optional[Dict[str, List[str]]]) -> None:
    empty_collection = MWELexiconCollection(pos_mapper=pos_mapper)
    assert [] == empty_collection.mwe_match('walking_noun boot_noun',
                                            LexiconType.MWE_NON_SPECIAL)
    assert [] == empty_collection.mwe_match('walking_noun boot_noun',
                                            LexiconType.MWE_WILDCARD)
    mwe_lexicon_collection = MWELexiconCollection(pos_mapper=pos_mapper)
    mwe_lexicon_collection['walking_noun *_noun'] = ['Z2']
    assert (['walking_noun *_noun']
            == mwe_lexicon_collection.mwe_match('walking_noun boot_noun',
                                                LexiconType.MWE_WILDCARD))
    
    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    assert [] == mwe_lexicon_collection.mwe_match('walking_noun boot_noun',
                                                  LexiconType.MWE_NON_SPECIAL)
    assert [] == mwe_lexicon_collection.mwe_match('walking_noun boot_noun',
                                                  LexiconType.MWE_WILDCARD)
    if pos_mapper is not None:
        assert (['A_pnoun Arnoia_pnoun']
                == mwe_lexicon_collection.mwe_match('A_NN Arnoia_NN',
                                                    LexiconType.MWE_NON_SPECIAL))
        assert [] == mwe_lexicon_collection.mwe_match('A_NN Arnoia_NN',
                                                      LexiconType.MWE_WILDCARD)
    else:
        assert (['A_pnoun Arnoia_pnoun']
                == mwe_lexicon_collection.mwe_match('A_pnoun Arnoia_pnoun',
                                                    LexiconType.MWE_NON_SPECIAL))
        assert [] == mwe_lexicon_collection.mwe_match('A_pnoun Arnoia_pnoun',
                                                      LexiconType.MWE_WILDCARD)
        
    assert [] == mwe_lexicon_collection.mwe_match('ano*_prep carta_noun',
                                                  LexiconType.MWE_NON_SPECIAL)
    assert (['ano*_prep carta_noun']
            == mwe_lexicon_collection.mwe_match('ano*_prep carta_noun',
                                                LexiconType.MWE_WILDCARD))
    assert (['ano*_prep carta_noun']
            == mwe_lexicon_collection.mwe_match('anonon_prep carta_noun',
                                                LexiconType.MWE_WILDCARD))
    
    mwe_lexicon_collection['ano*_prep *_noun'] = ['Z3']
    assert [] == mwe_lexicon_collection.mwe_match('ano*_prep carta_noun',
                                                  LexiconType.MWE_NON_SPECIAL)
    assert (['ano*_prep *_noun']
            == mwe_lexicon_collection.mwe_match('ano*_prep cart_noun',
                                                LexiconType.MWE_WILDCARD))
    test_matches = mwe_lexicon_collection.mwe_match('anonon_prep carta_noun',
                                                    LexiconType.MWE_WILDCARD)
    assert 2 == len(test_matches)
    expected_matches = ['ano*_prep carta_noun', 'ano*_prep *_noun']
    for match in expected_matches:
        assert match in test_matches

    # Test that it only uses wildcard regular expressions and no others, e.g. +
    del mwe_lexicon_collection['ano*_prep *_noun']
    mwe_lexicon_collection['ano+_prep *_noun'] = ['Z3']
    assert ['ano*_prep carta_noun'] == mwe_lexicon_collection.mwe_match('anoo_prep carta_noun',
                                                                        LexiconType.MWE_WILDCARD)
    test_matches = mwe_lexicon_collection.mwe_match('ano+_prep carta_noun',
                                                    LexiconType.MWE_WILDCARD)
    assert 2 == len(test_matches)
    expected_matches = ['ano*_prep carta_noun', 'ano+_prep *_noun']
    for match in expected_matches:
        assert match in test_matches

    # Test edge cases
    # empty string
    assert [] == mwe_lexicon_collection.mwe_match('', LexiconType.MWE_NON_SPECIAL)
    assert [] == mwe_lexicon_collection.mwe_match('', LexiconType.MWE_WILDCARD)

    # Wrong MWE template syntax, extra `_`
    assert [] == mwe_lexicon_collection.mwe_match('ano__prep carta_noun',
                                                  LexiconType.MWE_WILDCARD)
    # extra whitespace
    assert [] == mwe_lexicon_collection.mwe_match('ano _prep carta_noun',
                                                  LexiconType.MWE_WILDCARD)
    # Partial match
    assert [] == mwe_lexicon_collection.mwe_match('aano_prep carta_noun',
                                                  LexiconType.MWE_WILDCARD)
    # MWE templates that include what would be normally regular expressions
    mwe_lexicon_collection['.+h*lo_noun today_noun'] = ['Z2']
    assert [] == mwe_lexicon_collection.mwe_match('ahello_noun today_noun',
                                                  LexiconType.MWE_WILDCARD)
    assert (['.+h*lo_noun today_noun']
            == mwe_lexicon_collection.mwe_match('.+hello_noun today_noun',
                                                LexiconType.MWE_WILDCARD))
    
    if pos_mapper is not None:
        mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
        assert (['***_prep carta_* cabal_adj']
                == mwe_lexicon_collection.mwe_match('hello_prep carta_NN cabal_ADJ',
                                                    LexiconType.MWE_WILDCARD))
        assert (['***_prep carta_* cabal_adj']
                == mwe_lexicon_collection.mwe_match('hello_prep carta_NN cabal_JJ',
                                                    LexiconType.MWE_WILDCARD))
        assert ([]
                == mwe_lexicon_collection.mwe_match('hello_prep carta_NN cabal_ADJJJ',
                                                    LexiconType.MWE_WILDCARD))


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_to_dictionary(pos_mapper: Optional[Dict[str, List[str]]]
                       ) -> None:

    empty_collection = MWELexiconCollection(pos_mapper=pos_mapper)
    assert dict() == empty_collection.to_dictionary()

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    assert MWE_TEMPLATES == mwe_lexicon_collection.to_dictionary()


@pytest.mark.parametrize("pos_mapper", [None, POS_MAPPER])
def test_to_from_bytes(pos_mapper: Optional[Dict[str, List[str]]]
                       ) -> None:
    expected_pos_mapper = pos_mapper if pos_mapper is not None else {}
    
    empty_collection = MWELexiconCollection(pos_mapper=pos_mapper)
    a_collection = MWELexiconCollection.from_bytes(empty_collection.to_bytes())
    
    assert expected_pos_mapper == a_collection.pos_mapper
    assert dict() == a_collection.to_dictionary()
    
    del a_collection

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES, pos_mapper)
    a_collection = MWELexiconCollection.from_bytes(mwe_lexicon_collection.to_bytes())
    assert expected_pos_mapper == a_collection.pos_mapper
    assert MWE_TEMPLATES == a_collection.to_dictionary()


def test_mwe_lexicon_collection_from_tsv() -> None:

    mwe_lexicon_collection = MWELexiconCollection.from_tsv(MWE_LEXICON_FILE_PATH)
    assert isinstance(mwe_lexicon_collection, dict)
    assert 9 == len(mwe_lexicon_collection)
    assert mwe_lexicon_collection['East_noun London_noun'] == ['Z2']
    
    # Testing that additional fields are ignored.
    assert mwe_lexicon_collection == MWELexiconCollection.from_tsv(EXTRA_FIELDS_MWE_LEXICON_FILE_PATH)

    # Test that it removes duplicate keys in the file
    mwe_lexicon_collection = MWELexiconCollection.from_tsv(DUPLICATE_LEXICON_FILE_PATH)
    assert 9 == len(mwe_lexicon_collection)
    assert mwe_lexicon_collection['East_noun London_noun'] == ['Z1']

    # Test that it raises a ValueError when the minimum fields names are not
    # present
    with pytest.raises(ValueError):
        MWELexiconCollection.from_tsv(ERROR_LEXICON_FILE_PATH)
    # Test that it raises a ValueError when no fields names exist
    with pytest.raises(ValueError):
        MWELexiconCollection.from_tsv(NO_HEADER_LEXICON_FILE_PATH)
    
    # Test using a string rather than a Path like object
    mwe_lexicon_collection = MWELexiconCollection.from_tsv(str(MWE_LEXICON_FILE_PATH))
    assert 9 == len(mwe_lexicon_collection)
    assert mwe_lexicon_collection['all_adv well_adj'] == ['A4']
    
    # Test using a URL
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['PYMUSAS_HOME'] = temp_dir
        importlib.reload(config)
        with responses.RequestsMock() as rsps:
            req_kwargs = {"stream": True}
            expected_response = 'mwe_template\tsemantic_tags\na_det contragosto_noun\tX7- X5.2-\n'
            lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/mwe-pt.tsv'
            rsps.add(responses.GET, lexicon_url, status=200,
                     body=expected_response,
                     match=[responses.matchers.request_kwargs_matcher(req_kwargs)])
            url_lexicon_collection = MWELexiconCollection.from_tsv(lexicon_url)
            assert 1 == len(url_lexicon_collection)
            url_lexicon_collection['a_det contragosto_noun'] == ['X7-', 'X5.2-']
