from collections.abc import MutableMapping
import importlib
import os
from pathlib import Path
import tempfile

import pytest
import responses

from pymusas import config
from pymusas.lexicon_collection import MWELexiconCollection


MWE_TEMPLATES = {
    'A_pnoun Arnoia_pnoun': ['Z2'],
    'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': ['Z2'],
    'a_prep carta_noun cabal_adj': ['A4', 'A5.1']
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
    assert not empty_collection.data

    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert len(lexicon_collection.data) == 3


def test_mwe_lexicon_collection_len() -> None:

    empty_collection = MWELexiconCollection()
    assert 0 == len(empty_collection)

    lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert len(lexicon_collection) == 3


def test_mwe_lexicon_collection_set_get_del_item() -> None:

    empty_collection = MWELexiconCollection()
    assert not empty_collection.data

    empty_collection['A_pnoun Arnoia_pnoun'] = ['Z2']
    empty_collection['A_pnoun Arnoia_pnoun'] = ['Z1']
    empty_collection['a_prep carta_noun cabal_adj'] = ['A4', 'A5.1']
    assert empty_collection['A_pnoun Arnoia_pnoun'] == ['Z1']
    assert len(empty_collection) == 2

    del empty_collection['a_prep carta_noun cabal_adj']
    assert len(empty_collection) == 1


def test_mwe_lexicon_collection_iter() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert list(MWE_TEMPLATES) == list(mwe_lexicon_collection)


def test_mwe_lexicon_collection_keys() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert (list(MWE_TEMPLATES)
            == [key for key in mwe_lexicon_collection.keys()])


def test_mwe_lexicon_collection_values() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert (list(MWE_TEMPLATES.values())
            == [value for value in mwe_lexicon_collection.values()])


def test_mwe_lexicon_collection_items() -> None:

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    assert (list(MWE_TEMPLATES.items())
            == [item for item in mwe_lexicon_collection.items()])


def test_mwe_lexicon_collection_repr() -> None:

    empty_collection = MWELexiconCollection()
    assert 'MWELexiconCollection(data={})' == empty_collection.__repr__()
    assert empty_collection == eval(empty_collection.__repr__())

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    mwe_lexicon_repr = ("MWELexiconCollection(data={'A_pnoun Arnoia_pnoun': ['Z2'], "
                        "'A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': ['Z2'], "
                        "'a_prep carta_noun cabal_adj': ['A4', 'A5.1']})")
    assert mwe_lexicon_repr == mwe_lexicon_collection.__repr__()
    assert mwe_lexicon_collection == eval(mwe_lexicon_collection.__repr__())


def test_mwe_lexicon_collection_str() -> None:

    empty_collection = MWELexiconCollection()
    assert 'MWELexiconCollection() (0 entires in the collection)' == str(empty_collection)

    mwe_lexicon_collection = MWELexiconCollection(MWE_TEMPLATES)
    expected_str = ("MWELexiconCollection(('A_pnoun Arnoia_pnoun': ['Z2']), "
                    "('A_pnoun Pobra_pnoun de_pnoun Trives_pnoun': ['Z2']), ... )"
                    " (3 entires in the collection)")
    assert expected_str == str(mwe_lexicon_collection)


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
