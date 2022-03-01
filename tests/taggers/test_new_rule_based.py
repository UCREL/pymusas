import json
from pathlib import Path
from typing import List, Tuple

import pytest

from pymusas.lexicon_collection import LexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.new_rule_based import RuleBasedTagger
from pymusas.taggers.rules.single_word import SingleWordRule


DATA_DIR = Path(__file__, '..', '..', 'data').resolve()
TAGGER_DATA_DIR = Path(DATA_DIR, 'taggers', 'new_rule_based')


def generate_test_data(test_data_file: Path
                       ) -> Tuple[List[str],
                                  List[str],
                                  List[str],
                                  List[List[str]]]:
    '''
    Given the test data stored at `test_data_file` it returns this data as a
    Tuple of length 4:

    1. A List of expected `token`s
    2. A list of expected `lemma`s
    3. A list of expected `POS tags`s
    4. A list of a list of expected semantic tags that should be generated based
    on the associated `token`, `lemma`, and `pos`.

    # Parameters

    test_data_file : `Path`
        A JSON file containing an Array of Objects. Each object must contain the
        following properties/keys:
        1. token
        2. lemma
        3. pos
        4. usas

    # Returns

    `Tuple[List[str], List[str], List[str], List[List[str]]]`
    '''
    tokens: List[str] = []
    lemmas: List[str] = []
    pos_tags: List[str] = []
    
    expected_usas_tags: List[List[str]] = []
    with test_data_file.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            tokens.append(token_data['token'])
            lemmas.append(token_data['lemma'])
            pos_tags.append(token_data['pos'])
            expected_usas_tags.append([token_data['usas']])
    
    return tokens, lemmas, pos_tags, expected_usas_tags


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
    assert [['Z99'], ['Z99']] == tagger(['London', 'is'], ['', ''], ['', ''])

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
    lexicon_file = Path(TAGGER_DATA_DIR, 'single_lexicon.tsv')
    single_lexicon = LexiconCollection.from_tsv(lexicon_file)
    single_lemma_lexicon = LexiconCollection.from_tsv(lexicon_file, include_pos=False)
    single_rule = SingleWordRule(single_lexicon, single_lemma_lexicon)
    tagger = RuleBasedTagger([single_rule], ranker)
    
    (test_tokens, test_lemmas, test_pos_tags, expected_usas_tags) = \
        generate_test_data(test_data_file)
    assert expected_usas_tags == tagger(test_tokens, test_lemmas, test_pos_tags)

    # Test the case where we use the POS mapper on the single word lexicon rules.
    pos_mapper = {'noun': ['adj']}
    single_rule = SingleWordRule(single_lexicon, single_lemma_lexicon, pos_mapper)
    tagger = RuleBasedTagger([single_rule], ranker)
    tagger_output = tagger(test_tokens, test_lemmas, test_pos_tags)
    assert expected_usas_tags != tagger_output
    assert [['Z5'], ['Z99'], ['D3']] == tagger_output
