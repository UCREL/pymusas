from collections.abc import MutableMapping
import importlib
import os
from pathlib import Path
import re
import tempfile

import pytest
import responses

from pymusas import config
from pymusas.lexicon_collection import LexiconType, MWELexiconCollection


MWE_TEMPLATES = {
    'A_pnoun Arnoia_pnoun': ['Z2'],
    'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': ['Z2'],
    'a_prep carta_noun cabal_adj': ['A4', 'A5.1'],
    '***_prep carta_* cabal_adj': ['A4', 'A5.1'],
    'ano*_prep carta_noun': ['B4', 'B5.1'],
    'bno*_prep carta_noun': ['C4', 'C5.1'],
}
MWE_TEMPLATE_ITEMS = {
    'A_pnoun Arnoia_pnoun': (['Z2'], 2, LexiconType.MWE_NON_SPECIAL),
    'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': (['Z2'], 4, LexiconType.MWE_NON_SPECIAL),
    'a_prep carta_noun cabal_adj': (['A4', 'A5.1'], 3, LexiconType.MWE_NON_SPECIAL),
    '***_prep carta_* cabal_adj': (['A4', 'A5.1'], 3, LexiconType.MWE_WILDCARD),
    'ano*_prep carta_noun': (['B4', 'B5.1'], 2, LexiconType.MWE_WILDCARD),
    'bno*_prep carta_noun': (['C4', 'C5.1'], 2, LexiconType.MWE_WILDCARD),
}
DATA_DIR = Path(__file__, '..', '..', 'data').resolve()
LEXICON_DATA_DIR = Path(DATA_DIR, 'lexicon_collection', 'MWELexiconCollection')
MWE_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'mwe_lexicon.tsv')
EXTRA_FIELDS_MWE_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'extra_fields_lexicon.tsv')
ERROR_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'error_lexicon.tsv')
NO_HEADER_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'no_header_lexicon.tsv')
DUPLICATE_LEXICON_FILE_PATH = Path(LEXICON_DATA_DIR, 'duplicate_key_lexicon.tsv')


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
    
    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert len(lexicon_collection.meta_data) == 6
    assert len(lexicon_collection.mwe_regular_expression_lookup) == 2
    assert 4 == lexicon_collection.longest_non_special_mwe_template
    assert 3 == lexicon_collection.longest_wildcard_mwe_template


def test_mwe_lexicon_collection_len() -> None:

    empty_collection = MWELexiconCollection()
    assert 0 == len(empty_collection)

    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert len(lexicon_collection) == 6


def test_mwe_lexicon_collection_set_get_del_item() -> None:

    empty_collection = MWELexiconCollection()
    assert not empty_collection.meta_data

    empty_collection['A_pnoun Arnoia_pnoun'] = ['Z2']
    empty_collection['A_pnoun Arnoia_pnoun'] = ['Z1']
    empty_collection['a_prep carta_noun cabal_adj'] = ['A4', 'A5.1']
    assert empty_collection['A_pnoun Arnoia_pnoun'] == (['Z1'], 2, LexiconType.MWE_NON_SPECIAL)
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    assert 3 == empty_collection.longest_non_special_mwe_template
    assert 0 == empty_collection.longest_wildcard_mwe_template
    assert len(empty_collection) == 2

    del empty_collection['a_prep carta_noun cabal_adj']
    assert len(empty_collection) == 1
    assert 2 == empty_collection.longest_non_special_mwe_template
    assert 0 == empty_collection.longest_wildcard_mwe_template
    assert len(empty_collection.mwe_regular_expression_lookup) == 0
    
    empty_collection['a_prep *_noun cabal_adj'] = ['A4', 'A5.1']
    assert len(empty_collection) == 2
    assert 2 == empty_collection.longest_non_special_mwe_template
    assert 3 == empty_collection.longest_wildcard_mwe_template
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


def test_mwe_lexicon_collection_iter() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert list(MWE_TEMPLATE_ITEMS) == list(mwe_lexicon_collection)


def test_mwe_lexicon_collection_keys() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert (list(MWE_TEMPLATE_ITEMS)
            == [key for key in mwe_lexicon_collection.keys()])


def test_mwe_lexicon_collection_values() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert (list(MWE_TEMPLATE_ITEMS.values())
            == [value for value in mwe_lexicon_collection.values()])


def test_mwe_lexicon_collection_items() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert (list(MWE_TEMPLATE_ITEMS.items())
            == [item for item in mwe_lexicon_collection.items()])


def test_mwe_lexicon_collection_repr() -> None:

    empty_collection = MWELexiconCollection()
    assert 'MWELexiconCollection(data={})' == empty_collection.__repr__()
    assert empty_collection == eval(empty_collection.__repr__())

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    mwe_lexicon_repr = ("MWELexiconCollection(data={'A_pnoun Arnoia_pnoun': ['Z2'], "
                        "'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': ['Z2'], "
                        "'a_prep carta_noun cabal_adj': ['A4', 'A5.1'], "
                        "'***_prep carta_* cabal_adj': ['A4', 'A5.1'], "
                        "'ano*_prep carta_noun': ['B4', 'B5.1'], "
                        "'bno*_prep carta_noun': ['C4', 'C5.1']})")
    assert mwe_lexicon_repr == mwe_lexicon_collection.__repr__()
    assert mwe_lexicon_collection == eval(mwe_lexicon_collection.__repr__())


def test_mwe_lexicon_collection_str() -> None:

    empty_collection = MWELexiconCollection()
    assert 'MWELexiconCollection() (0 entires in the collection)' == str(empty_collection)

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    expected_str = (f"MWELexiconCollection(('A_pnoun Arnoia_pnoun': (['Z2'], 2, {LexiconType.MWE_NON_SPECIAL})), "
                    f"('A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': (['Z2'], 4, {LexiconType.MWE_NON_SPECIAL})), ... )"
                    " (6 entires in the collection)")
    assert expected_str == str(mwe_lexicon_collection)


def test_escape_mwe() -> None:
    test_expected_mwe_templates = [('', ''),
                                   ('ano_prep carta_noun', r'ano_prep\ carta_noun'),
                                   ('ano*_prep carta_noun', r'ano[^\s_]*_prep\ carta_noun'),
                                   ('***_prep carta_* cabal_adj',
                                    r'[^\s_]*[^\s_]*[^\s_]*_prep\ carta_[^\s_]*\ cabal_adj'),
                                   ('+++_prep carta_+ cabal_adj',
                                    r'\+\+\+_prep\ carta_\+\ cabal_adj')]
    for test, expected in test_expected_mwe_templates:
        assert expected == MWELexiconCollection.escape_mwe(test)


def test_mwe_match() -> None:
    empty_collection = MWELexiconCollection()
    assert [] == empty_collection.mwe_match('walking_noun boot_noun',
                                            LexiconType.MWE_NON_SPECIAL)
    assert [] == empty_collection.mwe_match('walking_noun boot_noun',
                                            LexiconType.MWE_WILDCARD)
    mwe_lexicon_collection = MWELexiconCollection()
    mwe_lexicon_collection['walking_noun *_noun'] = ['Z2']
    assert (['walking_noun *_noun']
            == mwe_lexicon_collection.mwe_match('walking_noun boot_noun',
                                                LexiconType.MWE_WILDCARD))
    
    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert [] == mwe_lexicon_collection.mwe_match('walking_noun boot_noun',
                                                  LexiconType.MWE_NON_SPECIAL)
    assert [] == mwe_lexicon_collection.mwe_match('walking_noun boot_noun',
                                                  LexiconType.MWE_WILDCARD)
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


def test_to_dictionary() -> None:

    empty_collection = MWELexiconCollection()
    assert dict() == empty_collection.to_dictionary()

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert MWE_TEMPLATES == mwe_lexicon_collection.to_dictionary()


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
