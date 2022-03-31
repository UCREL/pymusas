from typing import Callable, Dict, List

import spacy

from pymusas.spacy_api.taggers import rules  # noqa: F401
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.single_word import SingleWordRule


def test_single_word_rule() -> None:
    single_word_rule: Callable[[Dict[str, List[str]], Dict[str, List[str]],
                                Dict[str, List[str]]], SingleWordRule] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.SingleWordRule.v1')
    assert isinstance(single_word_rule({}, {}, {}), SingleWordRule)


def test_mwe_rule() -> None:
    mwe_rule: Callable[[Dict[str, List[str]], Dict[str, List[str]]], MWERule] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.MWERule.v1')
    assert isinstance(mwe_rule({}, {}), MWERule)


def test_rule_list() -> None:
    rule_list_call: Callable[[Rule, Rule], List[Rule]] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.rule_list')
    single_rule = SingleWordRule({}, {})
    mwe_rule = MWERule({})
    list_of_rules = rule_list_call(*(single_rule, mwe_rule))
    assert isinstance(list_of_rules, List)
    assert [single_rule, mwe_rule] == list_of_rules
