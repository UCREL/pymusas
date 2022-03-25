from typing import List
import pytest

from pymusas.base import Serialise
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule


@pytest.fixture
def single_word_rule() -> SingleWordRule:
    pos_mapper = {'NN': ['adv', 'noun']}
    return SingleWordRule({'Car|noun': ['Z2']}, {'Car': ['Z1']}, pos_mapper)


@pytest.fixture
def mwe_rule() -> MWERule:
    pos_mapper = {'NN': ['adv', 'noun']}
    return MWERule({'fast_adj car_noun': ['Z1']}, pos_mapper)


def test_serialise_object_list_to_from_bytes(single_word_rule: SingleWordRule,
                                             mwe_rule: MWERule) -> None:
    rule_list: List[Rule] = []
    serialised = Serialise.serialise_object_list_to_bytes(rule_list)
    assert rule_list == Serialise.serialise_object_list_from_bytes(serialised)

    rule_list = [single_word_rule, mwe_rule]
    serialised = Serialise.serialise_object_list_to_bytes(rule_list)
    assert rule_list == Serialise.serialise_object_list_from_bytes(serialised)