from collections.abc import Callable

import spacy

from pymusas.spacy_api.taggers import rules  # noqa: F401
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule


def test_single_word_rule() -> None:
    single_word_rule: Callable[[dict[str, list[str]], dict[str, list[str]],
                                dict[str, list[str]]], SingleWordRule] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.SingleWordRule.v1')
    assert isinstance(single_word_rule({}, {}, {}), SingleWordRule)


def test_single_word_rule_v2() -> None:
    single_word_rule: Callable[[dict[str, list[str]], dict[str, list[str]],
                                dict[str, list[str]] | None, dict[str, list[str]]],
                               SingleWordRule] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.SingleWordRule.v2')
    autotag_lexicon = {'*kg|NUM': ['N3.5']}
    rule = single_word_rule({'kg|NOUN': ['N3.5']}, {}, None, autotag_lexicon)
    assert isinstance(rule, SingleWordRule)
    assert SingleWordRule({'kg|NOUN': ['N3.5']}, {}, None, autotag_lexicon) == rule
    assert autotag_lexicon == rule.autotag_lexicon_collection.data


def test_mwe_rule() -> None:
    mwe_rule: Callable[[dict[str, list[str]], dict[str, list[str]]], MWERule] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.MWERule.v1')
    assert isinstance(mwe_rule({}, {}), MWERule)


def test_mwe_rule_v2() -> None:
    mwe_rule: Callable[[dict[str, list[str]], dict[str, list[str]],
                        SingleWordRule], MWERule] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.MWERule.v2')
    single_word_rule = SingleWordRule({'acting|ADJ': ['A1']}, {})
    rule = mwe_rule({}, {}, single_word_rule)
    assert isinstance(rule, MWERule)
    assert single_word_rule == rule.single_word_rule


def test_rule_list() -> None:
    rule_list_call: Callable[[Rule, Rule], list[Rule]] \
        = spacy.util.registry.misc.get('pymusas.taggers.rules.rule_list')
    single_rule = SingleWordRule({}, {})
    mwe_rule = MWERule({})
    list_of_rules = rule_list_call(*(single_rule, mwe_rule))
    assert isinstance(list_of_rules, list)
    assert [single_rule, mwe_rule] == list_of_rules
