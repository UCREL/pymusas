from typing import Callable, Dict, List

import spacy

from pymusas.spacy_api import pos_mapper  # noqa: F401


def test_UPOS_TO_USAS_CORE() -> None:
    UPOS_TO_USAS_CORE: Callable[[],
                                Dict[str, List[str]]] \
        = spacy.util.registry.misc.get('pymusas.pos_mapper.UPOS_TO_USAS_COREv1')
    mapping = UPOS_TO_USAS_CORE()
    assert 17 == len(mapping)
    assert 'ADJ' in mapping
    assert ['adj'] == mapping['ADJ']


def test_USAS_CORE_TO_UPOS() -> None:
    USAS_CORE_TO_UPOS: Callable[[],
                                Dict[str, List[str]]] \
        = spacy.util.registry.misc.get('pymusas.pos_mapper.USAS_CORE_TO_UPOSv1')
    mapping = USAS_CORE_TO_UPOS()
    assert 17 == len(mapping)
    assert 'adj' in mapping
    assert ['ADJ'] == mapping['adj']


def test_PENN_CHINESE_TREEBANK_TO_USAS_CORE() -> None:
    PENN_CHINESE_TREEBANK_TO_USAS_CORE: Callable[[],
                                                 Dict[str, List[str]]] \
        = spacy.util.registry.misc.get('pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_COREv1')
    mapping = PENN_CHINESE_TREEBANK_TO_USAS_CORE()
    assert 36 == len(mapping)
    assert 'AS' in mapping
    assert ['part'] == mapping['AS']


def test_USAS_CORE_TO_PENN_CHINESE_TREEBANK() -> None:
    USAS_CORE_TO_PENN_CHINESE_TREEBANK: Callable[[],
                                                 Dict[str, List[str]]] \
        = spacy.util.registry.misc.get('pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANKv1')
    mapping = USAS_CORE_TO_PENN_CHINESE_TREEBANK()
    assert 17 == len(mapping)
    assert 'part' in mapping
    assert ['NN', 'NT'] == mapping['noun']


def test_BASIC_CORCENCC_TO_USAS_CORE() -> None:
    BASIC_CORCENCC_TO_USAS_CORE: Callable[[],
                                          Dict[str, List[str]]] \
        = spacy.util.registry.misc.get('pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_COREv1')
    mapping = BASIC_CORCENCC_TO_USAS_CORE()
    assert 13 == len(mapping)
    assert 'E' in mapping
    assert ['noun'] == mapping['E']


def test_USAS_CORE_TO_BASIC_CORCENCC() -> None:
    USAS_CORE_TO_BASIC_CORCENCC: Callable[[],
                                          Dict[str, List[str]]] \
        = spacy.util.registry.misc.get('pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCCv1')
    mapping = USAS_CORE_TO_BASIC_CORCENCC()
    assert 17 == len(mapping)
    assert 'noun' in mapping
    assert ['E'] == mapping['noun']
