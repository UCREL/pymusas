from typing import Dict, List, Set

import pytest

from pymusas.pos_mapper import (
    BASIC_CORCENCC_TO_USAS_CORE,
    PENN_CHINESE_TREEBANK_TO_USAS_CORE,
    UPOS_TO_USAS_CORE,
    USAS_CORE_TO_BASIC_CORCENCC,
    USAS_CORE_TO_PENN_CHINESE_TREEBANK,
    USAS_CORE_TO_UPOS,
    upos_to_usas_core,
)


@pytest.fixture(scope='module')
def upos_tags() -> Set[str]:
    return set(
        ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN',
         'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM',
         'VERB', 'X']
    )


@pytest.fixture(scope='module')
def usas_tags() -> Set[str]:
    return set(
        ['adj', 'prep', 'adv', 'verb', 'conj', 'det', 'art', 'intj',
         'noun', 'num', 'part', 'pron', 'pnoun', 'punc', 'code',
         'fw', 'xx']
    )


@pytest.fixture(scope='module')
def basic_corcencc_tags() -> Set[str]:
    return set(
        ['E', 'YFB', 'Ar', 'Cys', 'Rhi', 'Ans', 'Adf', 'B',
         'Rha', 'U', 'Ebych', 'Gw', 'Atd']
    )


@pytest.fixture(scope='module')
def penn_chinese_treebank_tags() -> Set[str]:
    return set(
        ['AS', 'DEC', 'DEG', 'DER', 'DEV', 'ETC', 'LC', 'MSP', 'SP',
         'BA', 'FW', 'IJ', 'LB', 'ON', 'SB', 'X', 'URL', 'INF', 'NN', 'NR',
         'NT', 'VA', 'VC', 'VE', 'VV', 'CD', 'M', 'OD', 'DT', 'CC',
         'CS', 'AD', 'JJ', 'P', 'PN', 'PU']
    )


def tags_in_tagsets(pos_mapping: Dict[str, List[str]],
                    tagset_1: Set[str], tagset_2: Set[str]) -> None:
    for tag_1, tags_2 in pos_mapping.items():
        assert tag_1 in tagset_1
        for tag_2 in tags_2:
            assert tag_2 in tagset_2
    assert tagset_1 == set(list(pos_mapping))


def test_upos_to_usas_core(upos_tags: Set[str], usas_tags: Set[str]) -> None:
    assert upos_to_usas_core('CCONJ') == ['conj']
    assert upos_to_usas_core('X') == ['fw', 'xx']
    assert upos_to_usas_core('Unknown') == []

    for upos_tag in upos_tags:
        tags = upos_to_usas_core(upos_tag)
        assert tags != []
        for tag in tags:
            assert tag in usas_tags
    
    tags_in_tagsets(UPOS_TO_USAS_CORE, upos_tags, usas_tags)


def test_usas_core_to_upos(usas_tags: Set[str], upos_tags: Set[str]) -> None:
    assert 17 == len(USAS_CORE_TO_UPOS)
    tags_in_tagsets(USAS_CORE_TO_UPOS, usas_tags, upos_tags)


def test_penn_chinese_to_usas_core(penn_chinese_treebank_tags: Set[str],
                                   usas_tags: Set[str]) -> None:
    assert len(PENN_CHINESE_TREEBANK_TO_USAS_CORE) == 36
    tags_in_tagsets(PENN_CHINESE_TREEBANK_TO_USAS_CORE, penn_chinese_treebank_tags,
                    usas_tags)


def test_usas_core_to_penn_chinese(penn_chinese_treebank_tags: Set[str],
                                   usas_tags: Set[str]) -> None:
    assert len(USAS_CORE_TO_PENN_CHINESE_TREEBANK) == 17
    tags_in_tagsets(USAS_CORE_TO_PENN_CHINESE_TREEBANK, usas_tags,
                    penn_chinese_treebank_tags)


def test_basic_corcencc_to_usas_core(basic_corcencc_tags: Set[str],
                                     usas_tags: Set[str]) -> None:
    assert 13 == len(BASIC_CORCENCC_TO_USAS_CORE)
    tags_in_tagsets(BASIC_CORCENCC_TO_USAS_CORE, basic_corcencc_tags,
                    usas_tags)


def test_usas_core_to_basic_corcencc(usas_tags: Set[str],
                                     basic_corcencc_tags: Set[str]) -> None:
    assert 17 == len(USAS_CORE_TO_BASIC_CORCENCC)
    tags_in_tagsets(USAS_CORE_TO_BASIC_CORCENCC, usas_tags, basic_corcencc_tags)
