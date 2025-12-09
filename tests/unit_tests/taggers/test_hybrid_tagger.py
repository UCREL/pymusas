from pathlib import Path

import pytest

from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.hybrid import HybridTagger
from pymusas.taggers.neural import NeuralTagger
from pymusas.taggers.rules.single_word import SingleWordRule

from .test_rule_based import generate_test_data, mwe_word_rule, single_word_rule


DATA_DIR = Path(__file__, '..', '..', 'data').resolve()
TAGGER_DATA_DIR = Path(DATA_DIR, 'taggers', 'rule_based')


@pytest.fixture
def neural_tagger() -> NeuralTagger:
    return NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
                        device="cpu",
                        top_n=2)


def test_hybrid_based_tagger__init__(neural_tagger: NeuralTagger) -> None:
    single_word_rule = SingleWordRule({}, {})
    ranker = ContextualRuleBasedRanker(1, 0)
    tagger = HybridTagger([single_word_rule], ranker, neural_tagger)

    assert 1 == len(tagger.rules)
    assert isinstance(tagger.rules[0], SingleWordRule)
    assert isinstance(tagger.ranker, ContextualRuleBasedRanker)
    assert isinstance(tagger.neural_tagger, NeuralTagger)


def test_rule_based_tagger__call__(neural_tagger: NeuralTagger) -> None:

    # Test the first case where we have no rules and it should tag everything as
    # Z99
    ranker = ContextualRuleBasedRanker(1, 0)
    tagger = HybridTagger([], ranker, neural_tagger)
    assert [] == tagger([], [], [])
    expected_output = [
        (['Z2', 'Z3'], [(0, 1)]),
        (['A3', 'Z5'], [(1, 2)])
    ]
    assert expected_output == tagger(['London', 'is'], ['', ''], ['', ''])

    # Ensure that the ValueError is raised when the length of tokens, lemmas,
    # and POS tags are not the same
    with pytest.raises(ValueError):
        tagger([''], ['', ''], [''])
    with pytest.raises(ValueError):
        tagger(['', ''], ['', ''], [''])
    with pytest.raises(ValueError):
        tagger(['', '', ''], ['', ''], [''])

    # Test the default punctutation and number POS tags
    expected_output = [
        (['PUNCT'], [(0, 1)]),
        (['N1'], [(1, 2)])
    ]
    assert expected_output == tagger(['test', 'test'], ['', ''], ['punc', 'num'])
    
    # Test the punctutation and number POS tags when set by the user
    tagger = HybridTagger([], ranker, neural_tagger, set(['pu', 'pc']), set(['nu', 'st']))
    assert expected_output == tagger(['test', 'test'], ['', ''], ['pc', 'st'])
    assert expected_output == tagger(['test', 'test'], ['', ''], ['pu', 'nu'])
    assert expected_output != tagger(['test', 'test'], ['', ''], ['punc', 'num'])

    # Test the case where we only use single word lexicon rules.
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_single_input_output.json')
    
    tagger = HybridTagger([single_word_rule(None)], ranker, neural_tagger)
    
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file)
    expected_output[1] = (["Z5", "Z3"], [(1, 2)])
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output

    # Test the case where we use the POS mapper on the single word lexicon rules.
    rule_pos_mapper = {'adj': ['noun'], 'noun': ['adj']}
    tagger = HybridTagger([single_word_rule(rule_pos_mapper)], ranker, neural_tagger)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    expected_output[0] = (["Z5"], [(0, 1)])
    expected_output[2] = (["D3"], [(2, 3)])
    assert expected_output == tagger_output

    test_data_pos_mapper = {'adj': 'noun', 'noun': 'adj'}
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file, test_data_pos_mapper)
    expected_output[1] = (["Z5", "Z3"], [(1, 2)])
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output

    # Test the MWE case
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_mwe_input_output.json')
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file)
    ranker = ContextualRuleBasedRanker(3, 0)
    tagger = HybridTagger([mwe_word_rule(None)], ranker, neural_tagger)
    expected_output[2] = (["X2.4", "P1"], [(2, 3)])
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output

    # Test the MWE case with POS Mapper, this ends up using the Neural Tagger
    # for everything.
    tagger = HybridTagger([mwe_word_rule(rule_pos_mapper)], ranker, neural_tagger)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output != tagger_output
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file, test_data_pos_mapper)
    expected_output = [(['M6', 'Z2'], [(0, 1)]), (['Z2', 'Z3'], [(1, 2)]),
                       (['X2.4', 'P1'], [(2, 3)]), (['Z2', 'M6'], [(3, 4)]),
                       (['M6', 'Z2'], [(4, 5)]), (['Z2', 'Z3'], [(5, 6)])]
    assert expected_output == tagger_output

    # Test the case of Single and MWE
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_single_mwe_input_output.json')
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file)
    ranker = ContextualRuleBasedRanker(3, 0)
    tagger = HybridTagger([single_word_rule(None),
                           mwe_word_rule(None)], ranker, neural_tagger)
    expected_output[3] = (["X2.4", "P1"], [(3, 4)])
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output
