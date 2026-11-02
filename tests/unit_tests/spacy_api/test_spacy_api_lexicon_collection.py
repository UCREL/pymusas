from collections.abc import Callable
from os import PathLike
from pathlib import Path

import spacy

from pymusas.spacy_api import lexicon_collection  # noqa: F401


DATA_DIR = Path(__file__, '..', '..', 'data', 'lexicon_collection').resolve()
LEXICON_FILE_PATH = Path(DATA_DIR, 'LexiconCollection', 'lexicon.tsv')
MINIMUM_LEXICON_FILE_PATH = Path(DATA_DIR, 'LexiconCollection',
                                 'minimum_lexicon.tsv')
MWE_LEXICON_FILE_PATH = Path(DATA_DIR, 'MWELexiconCollection', 'mwe_lexicon.tsv')
AUTOTAG_LEXICON_FILE_PATH = Path(DATA_DIR, 'AutotagLexiconCollection',
                                 'autotag_lexicon.tsv')


def test_lexicon_collection_from_tsv() -> None:
    lexicon_collection_from_tsv: Callable[[PathLike | str, bool],
                                          dict[str, list[str]]] \
        = spacy.util.registry.misc.get('pymusas.LexiconCollection.from_tsv')
    collection = lexicon_collection_from_tsv(LEXICON_FILE_PATH, True)
    assert isinstance(collection, dict)
    assert 19 == len(collection)
    assert collection['Laptop|noun'] == ['Z3', 'Z0']

    # Test `include_pos`
    minimum_lexicon_collection \
        = lexicon_collection_from_tsv(MINIMUM_LEXICON_FILE_PATH, True)
    assert lexicon_collection_from_tsv(LEXICON_FILE_PATH, False) \
        == minimum_lexicon_collection


def test_mwe_lexicon_collection_from_tsv() -> None:
    mwe_lexicon_collection_from_tsv: Callable[[PathLike | str],
                                              dict[str, list[str]]] \
        = spacy.util.registry.misc.get('pymusas.MWELexiconCollection.from_tsv')
    collection = mwe_lexicon_collection_from_tsv(MWE_LEXICON_FILE_PATH)
    assert isinstance(collection, dict)
    assert 9 == len(collection)
    assert collection['East_noun London_noun'] == ['Z2']


def test_autotag_lexicon_collection_from_tsv() -> None:
    autotag_lexicon_collection_from_tsv: Callable[[PathLike | str],
                                                  dict[str, list[str]]] \
        = spacy.util.registry.misc.get('pymusas.AutotagLexiconCollection.from_tsv')
    collection = autotag_lexicon_collection_from_tsv(AUTOTAG_LEXICON_FILE_PATH)
    assert isinstance(collection, dict)
    assert 4 == len(collection)
    assert collection['*MB|N*'] == ['N3.2', 'N5']
