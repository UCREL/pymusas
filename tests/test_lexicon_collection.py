from collections.abc import MutableMapping
from dataclasses import FrozenInstanceError
import importlib
import os
from pathlib import Path
import tempfile
from typing import Dict, List

import pytest
import responses

from pymusas import config
from pymusas.lexicon_collection import LexiconCollection, LexiconEntry


DATA_DIR = Path(__file__, '..', 'data').resolve()
LEXICON_FILE_PATH = Path(DATA_DIR, 'lexicon.tsv')
EXTRA_FIELDS_LEXICON_FILE_PATH = Path(DATA_DIR, 'extra_fields_lexicon.tsv')
MINIMUM_LEXICON_FILE_PATH = Path(DATA_DIR, 'minimum_lexicon.tsv')
ERROR_LEXICON_FILE_PATH = Path(DATA_DIR, 'error_lexicon.tsv')
NO_HEADER_LEXICON_FILE_PATH = Path(DATA_DIR, 'no_header_lexicon.tsv')

LEXICON_ENTRY = LexiconEntry('London', ['Z2'], 'noun')
LEXICON_ENTRY_MULTI_SEM = LexiconEntry('Laptop', ['Z3', 'Z0'], 'noun')
NON_POS_ENTRY = LexiconEntry('London', ['Z2'])

LEXICON_ENTRIES: Dict[str, List[str]] = {}
for entry in [LEXICON_ENTRY, LEXICON_ENTRY_MULTI_SEM, NON_POS_ENTRY]:
    lemma = entry.lemma
    if entry.pos is not None:
        lemma += f'|{entry.pos}'
    LEXICON_ENTRIES[lemma] = entry.semantic_tags
LEXICON_KEYS = ['London|noun', 'Laptop|noun', 'London']
LEXICON_VALUES = [["Z2"], ["Z3", "Z0"], ["Z2"]]
LEXICON_ITEMS = [(key, value) for key, value in zip(LEXICON_KEYS, LEXICON_VALUES)]


def test_lexicon_entry() -> None:
        
    assert LEXICON_ENTRY.lemma == "London"
    assert LEXICON_ENTRY.pos == "noun"
    assert LEXICON_ENTRY.semantic_tags == ["Z2"]
    assert str(LEXICON_ENTRY) == "LexiconEntry(lemma='London', semantic_tags=['Z2'], pos='noun')"
    
    with pytest.raises(FrozenInstanceError):
        for attribute in ['lemma', 'pos', 'semantic_tags']:
            setattr(LEXICON_ENTRY, attribute, 'test')

    assert LEXICON_ENTRY_MULTI_SEM.lemma == "Laptop"
    assert LEXICON_ENTRY_MULTI_SEM.pos == "noun"
    assert LEXICON_ENTRY_MULTI_SEM.semantic_tags == ["Z3", "Z0"]
    assert str(LEXICON_ENTRY_MULTI_SEM) == "LexiconEntry(lemma='Laptop', semantic_tags=['Z3', 'Z0'], pos='noun')"

    assert LEXICON_ENTRY != LEXICON_ENTRY_MULTI_SEM
    assert LEXICON_ENTRY == LexiconEntry('London', pos='noun', semantic_tags=['Z2'])

    assert str(NON_POS_ENTRY) == "LexiconEntry(lemma='London', semantic_tags=['Z2'], pos=None)"
    assert NON_POS_ENTRY == LexiconEntry('London', ['Z2'], None)


def test_lexicon_collection_class_type() -> None:
    empty_collection = LexiconCollection()
    assert isinstance(empty_collection, LexiconCollection)
    assert isinstance(empty_collection, MutableMapping)


def test_lexicon_collection_init() -> None:

    empty_collection = LexiconCollection()
    assert not empty_collection.data

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    assert len(lexicon_collection.data) == 3


def test_lexicon_collection_len() -> None:

    empty_collection = LexiconCollection()
    assert 0 == len(empty_collection)

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    assert len(lexicon_collection) == 3


def test_lexicon_collection_set_get_del_item() -> None:

    empty_collection = LexiconCollection()
    assert not empty_collection.data

    empty_collection['another'] = ['Z2']
    empty_collection['another'] = ['Z1']
    empty_collection['bottle'] = ['Z0']
    assert empty_collection['another'] == ['Z1']
    assert len(empty_collection) == 2

    del empty_collection['another']
    assert len(empty_collection) == 1


def test_lexicon_collection_iter() -> None:

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    assert LEXICON_KEYS == list(lexicon_collection)


def test_lexicon_collection_keys() -> None:

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    assert LEXICON_KEYS == [key for key in lexicon_collection.keys()]


def test_lexicon_collection_values() -> None:

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    assert LEXICON_VALUES == [value for value in lexicon_collection.values()]


def test_lexicon_collection_items() -> None:

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    assert LEXICON_ITEMS == [item for item in lexicon_collection.items()]


def test_lexicon_collection_repr() -> None:

    empty_collection = LexiconCollection()
    assert 'LexiconCollection(data={})' == empty_collection.__repr__()
    assert empty_collection == eval(empty_collection.__repr__())

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    lexicon_repr = ("LexiconCollection(data={'London|noun': ['Z2'], "
                    "'Laptop|noun': ['Z3', 'Z0'], 'London': ['Z2']})")
    assert lexicon_repr == lexicon_collection.__repr__()
    assert lexicon_collection == eval(lexicon_collection.__repr__())


def test_lexicon_collection_str() -> None:

    empty_collection = LexiconCollection()
    assert 'LexiconCollection() (0 entires in the collection)' == str(empty_collection)

    lexicon_collection = LexiconCollection(LEXICON_ENTRIES)
    expected_str = ("LexiconCollection(('London|noun': ['Z2']), "
                    "('Laptop|noun': ['Z3', 'Z0']), ... )"
                    " (3 entires in the collection)")
    assert expected_str == str(lexicon_collection)


def test_lexicon_collection_add_lexicon_entry() -> None:

    lexicon_collection = LexiconCollection()
    lexicon_collection.add_lexicon_entry(LEXICON_ENTRY)
    assert lexicon_collection['London|noun'] == ['Z2']

    lexicon_collection.add_lexicon_entry(LEXICON_ENTRY, include_pos=False)
    assert lexicon_collection['London'] == ['Z2']
    assert 2 == len(lexicon_collection)


def test_lexicon_collection_to_dictionary() -> None:
    lexicon_collection = LexiconCollection()
    assert dict() == lexicon_collection.to_dictionary()

    lexicon_collection.add_lexicon_entry(LEXICON_ENTRY)
    expected_dictionary = {'London|noun': ['Z2']}
    assert expected_dictionary == lexicon_collection.to_dictionary()
    assert isinstance(lexicon_collection.to_dictionary(), dict)


def test_lexicon_collection_from_tsv() -> None:

    lexicon_collection = LexiconCollection.from_tsv(LEXICON_FILE_PATH)
    assert isinstance(lexicon_collection, dict)
    assert 16 == len(lexicon_collection)
    assert lexicon_collection['Laptop|noun'] == ['Z3', 'Z0']

    # Testing that additional fields are ignored.
    assert lexicon_collection == LexiconCollection.from_tsv(EXTRA_FIELDS_LEXICON_FILE_PATH)

    # Test file that contains only the minimum fields
    minimum_lexicon_collection = LexiconCollection.from_tsv(MINIMUM_LEXICON_FILE_PATH)
    # 15 and not 16 as one of the entries is repeated in the TSV file
    assert 15 == len(minimum_lexicon_collection)
    assert minimum_lexicon_collection['Laptop'] == ['Z3', 'Z0']
    assert minimum_lexicon_collection != lexicon_collection

    # Test that it raises a ValueError when the minimum fields names are not
    # present
    with pytest.raises(ValueError):
        LexiconCollection.from_tsv(ERROR_LEXICON_FILE_PATH)
    # Test that it raises a ValueError when no fields names exist
    with pytest.raises(ValueError):
        LexiconCollection.from_tsv(NO_HEADER_LEXICON_FILE_PATH)
    
    # Test `include_pos`
    assert LexiconCollection.from_tsv(LEXICON_FILE_PATH, include_pos=False) == minimum_lexicon_collection

    # Test using a string rather than a Path like object
    lexicon_collection = LexiconCollection.from_tsv(str(LEXICON_FILE_PATH))
    assert 16 == len(lexicon_collection)
    assert lexicon_collection['Laptop|noun'] == ['Z3', 'Z0']
    
    # Test using a URL
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['PYMUSAS_HOME'] = temp_dir
        importlib.reload(config)
        with responses.RequestsMock() as rsps:
            req_kwargs = {"stream": True}
            expected_response = 'lemma\tsemantic_tags\nhello\tZ5 Z2\n'
            lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.usas'
            rsps.add(responses.GET, lexicon_url, status=200,
                     body=expected_response,
                     match=[responses.matchers.request_kwargs_matcher(req_kwargs)])
            url_lexicon_collection = LexiconCollection.from_tsv(lexicon_url)
            assert 1 == len(url_lexicon_collection)
            url_lexicon_collection['hello'] == ['Z5', 'Z2']
