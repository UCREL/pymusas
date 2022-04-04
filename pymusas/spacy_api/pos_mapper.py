'''
spaCy registered functions for loading Part Of Speech (POS) mappings.
'''

from typing import Dict, List

import spacy

from pymusas import pos_mapper


@spacy.util.registry.misc('pymusas.pos_mapper.UPOS_TO_USAS_COREv1')
def upos_to_usas_core() -> Dict[str, List[str]]:
    '''
    `pymusas.pos_mapper.UPOS_TO_USAS_COREv1` is a registered function under the
    `@misc` function register. It returns the
    :var:`pymusas.pos_mapper.UPOS_TO_USAS_CORE` mapping.

    # Returns

    `Dict[str, List[str]]`
    '''
    return pos_mapper.UPOS_TO_USAS_CORE


@spacy.util.registry.misc('pymusas.pos_mapper.USAS_CORE_TO_UPOSv1')
def usas_core_to_upos() -> Dict[str, List[str]]:
    '''
    `pymusas.pos_mapper.USAS_CORE_TO_UPOSv1` is a registered function under the
    `@misc` function register. It returns the
    :var:`pymusas.pos_mapper.USAS_CORE_TO_UPOS` mapping.

    # Returns

    `Dict[str, List[str]]`
    '''
    return pos_mapper.USAS_CORE_TO_UPOS


@spacy.util.registry.misc('pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_COREv1')
def penn_chinese_treebank_to_usas_core() -> Dict[str, List[str]]:
    '''
    `pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_COREv1` is a registered
    function under the `@misc` function register. It returns the
    :var:`pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_CORE` mapping.

    # Returns

    `Dict[str, List[str]]`
    '''
    return pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_CORE


@spacy.util.registry.misc('pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANKv1')
def usas_core_to_penn_chinese_treebank() -> Dict[str, List[str]]:
    '''
    `pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANKv1` is a registered
    function under the `@misc` function register. It returns the
    :var:`pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANK` mapping.

    # Returns

    `Dict[str, List[str]]`
    '''
    return pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANK


@spacy.util.registry.misc('pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_COREv1')
def basic_corcencc_to_usas_core() -> Dict[str, List[str]]:
    '''
    `pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_COREv1` is a registered
    function under the `@misc` function register. It returns the
    :var:`pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_CORE` mapping.

    # Returns

    `Dict[str, List[str]]`
    '''
    return pos_mapper.BASIC_CORCENCC_TO_USAS_CORE


@spacy.util.registry.misc('pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCCv1')
def usas_core_to_basic_corcencc() -> Dict[str, List[str]]:
    '''
    `pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCCv1` is a registered
    function under the `@misc` function register. It returns the
    :var:`pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCC` mapping.

    # Returns

    `Dict[str, List[str]]`
    '''
    return pos_mapper.USAS_CORE_TO_BASIC_CORCENCC
