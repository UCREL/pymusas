import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pytest

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.new_rule_based import RuleBasedTagger
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.single_word import SingleWordRule


DATA_DIR = Path(__file__, '..', '..', 'data').resolve()
TAGGER_DATA_DIR = Path(DATA_DIR, 'taggers', 'new_rule_based')


def generate_test_data(test_data_file: Path,
                       pos_mapper: Optional[Dict[str, str]] = None
                       ) -> Tuple[List[str],
                                  List[str],
                                  List[str],
                                  List[Tuple[List[str],
                                             List[Tuple[int, int]]]
                                       ]]:
    '''
    Given the test data stored at `test_data_file` it returns this data as a
    Tuple of length 4:

    1. A List of expected `token`s
    2. A list of expected `lemma`s
    3. A list of expected `POS tags`s
    4. A list of Tuples of length 2, each tuple corresponds to a token and
    contains the following:
      1. A list of expected semantic tags that should be generated based
    on the associated `token`, `lemma`, and `pos`.
      2. A List of tuples of length 2. each `Tuple` indicates the start and end
    token index of the associated Multi Word Expression (MWE). If the `List` contains
    more than one `Tuple` then the MWE is discontinuous. For single word
    expressions the `List` will only contain 1 `Tuple` which will only contain

    # Parameters

    test_data_file : `Path`
        A JSON file containing an Array of Objects. Each object must contain the
        following properties/keys:
        1. token
        2. lemma
        3. pos
        4. usas
        5. start_indexes
        6. end_indexes
    pos_mapper : `Dict[str, str]`, optional (default = `None`)
        If not `None` it will map the pos tags using this mapper.

    # Returns

    `Tuple[List[str], List[str], List[str], List[Tuple[List[str], List[Tuple[int, int]]]]]`
    '''
    tokens: List[str] = []
    lemmas: List[str] = []
    pos_tags: List[str] = []
    if pos_mapper is None:
        pos_mapper = {}
    
    expected_output: List[Tuple[List[str], List[Tuple[int, int]]]] = []
    with test_data_file.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            tokens.append(token_data['token'])
            lemmas.append(token_data['lemma'])
            pos = token_data['pos']
            pos = pos_mapper.get(pos, pos)
            pos_tags.append(pos)
            
            usas_tags = token_data['usas']
            mwe_indexes: List[Tuple[int, int]] = []
            for start, end in zip(token_data['start_indexes'],
                                  token_data['end_indexes']):
                mwe_indexes.append((int(start), int(end)))
            expected_output.append((usas_tags, mwe_indexes))
    
    return tokens, lemmas, pos_tags, expected_output


def single_word_rule(pos_mapper: Optional[Dict[str, List[str]]]
                     ) -> SingleWordRule:
    lexicon_file = Path(TAGGER_DATA_DIR, 'single_lexicon.tsv')
    single_lexicon = LexiconCollection.from_tsv(lexicon_file)
    single_lemma_lexicon = LexiconCollection.from_tsv(lexicon_file, include_pos=False)
    return SingleWordRule(single_lexicon, single_lemma_lexicon, pos_mapper)


def mwe_word_rule(pos_mapper: Optional[Dict[str, List[str]]]) -> MWERule:
    lexicon_file = Path(TAGGER_DATA_DIR, 'mwe_lexicon.tsv')
    mwe_lexicon = MWELexiconCollection.from_tsv(lexicon_file)
    return MWERule(mwe_lexicon, pos_mapper)


def test_rule_based_tagger__init__() -> None:
    single_word_rule = SingleWordRule({}, {})
    ranker = ContextualRuleBasedRanker(1, 0)
    tagger = RuleBasedTagger([single_word_rule], ranker)

    assert 1 == len(tagger.rules)
    assert isinstance(tagger.rules[0], SingleWordRule)
    assert isinstance(tagger.ranker, ContextualRuleBasedRanker)


def test_rule_based_tagger__call__() -> None:

    # Test the first case where we have no rules and it should tag everything as
    # Z99
    ranker = ContextualRuleBasedRanker(1, 0)
    tagger = RuleBasedTagger([], ranker)
    assert [] == tagger([], [], [])
    expected_output = [
        (['Z99'], [(0, 1)]),
        (['Z99'], [(1, 2)])
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

    # Test the case where we only use single word lexicon rules.
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_single_input_output.json')
    
    tagger = RuleBasedTagger([single_word_rule(None)], ranker)
    
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output

    # Test the case where we use the POS mapper on the single word lexicon rules.
    rule_pos_mapper = {'adj': ['noun'], 'noun': ['adj']}
    tagger = RuleBasedTagger([single_word_rule(rule_pos_mapper)], ranker)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output != tagger_output

    test_data_pos_mapper = {'adj': 'noun', 'noun': 'adj'}
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file, test_data_pos_mapper)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output

    # Test the MWE case
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_mwe_input_output.json')
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file)
    ranker = ContextualRuleBasedRanker(3, 0)
    tagger = RuleBasedTagger([mwe_word_rule(None)], ranker)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output

    # Test the MWE case with POS Mapper
    tagger = RuleBasedTagger([mwe_word_rule(rule_pos_mapper)], ranker)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output != tagger_output
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file, test_data_pos_mapper)
    assert expected_output != tagger_output

    # Test the case of Single and MWE
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_single_mwe_input_output.json')
    (test_tokens, test_lemmas, test_pos_tags, expected_output) = \
        generate_test_data(test_data_file)
    ranker = ContextualRuleBasedRanker(3, 0)
    tagger = RuleBasedTagger([single_word_rule(None),
                              mwe_word_rule(None)], ranker)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_output == tagger_output
