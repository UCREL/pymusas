import json
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple

import pytest

from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.rule_based import USASRuleBasedTagger, _tag_token


DATA_DIR = Path(__file__, '..', '..', 'data').resolve()


def generate_tag_test_data() -> Tuple[List[Tuple[str, str, str]],
                                      Dict[str, List[str]],
                                      Dict[str, List[str]],
                                      List[List[str]]]:
    '''
    Given the test data stored at `../../data/rule_based_input_output.json`, and
    the semantic lexicon at `../../data/lexicon.tsv`, it returns this data as a
    Tuple of length 4:

    1. A List of expected `token`, `lemma`, and `pos`
    2. The semantic lexicon including Part Of Speech tag information.
    3. The semantic lexicon excluding Part Of Speech tag information.
    4. A list of a list of expected semantic tags that should be generated based
    on the associated `token`, `lemma`, and `pos` from the first argument and
    the semantic lexicons data from the second and thgiven in the second argument assuming you use the
    semantic lexicon with and without pos tag data.
    
    # Returns

    `Tuple[List[Tuple[str, str, str]], Path, List[List[str]]]`
    '''
    test_data_path = Path(DATA_DIR, 'rule_based_input_output.json')
    test_data: List[Tuple[str, str, str]] = []
    
    expected_usas_tags: List[List[str]] = []
    with test_data_path.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            token = token_data['token']
            lemma = token_data['lemma']
            pos = token_data['pos']
            test_data.append((token, lemma, pos))
            expected_usas_tags.append([token_data['usas']])
    
    lexicon_path = Path(DATA_DIR, 'lexicon.tsv')
    lexicon_lookup = LexiconCollection.from_tsv(lexicon_path, include_pos=True)
    lemma_lexicon_lookup = LexiconCollection.from_tsv(lexicon_path, include_pos=False)
    
    return test_data, lexicon_lookup, lemma_lexicon_lookup, expected_usas_tags


def test__tag_token() -> None:

    test_data, lexicon_lookup, lemma_lexicon_lookup, expected_usas_tags = generate_tag_test_data()
    for data, expected_tags in zip(test_data, expected_usas_tags):
        text, lemma, pos = data
        predicted_tags = _tag_token(text, lemma, pos, lexicon_lookup, lemma_lexicon_lookup)
        assert predicted_tags == expected_tags


@pytest.mark.parametrize('empty_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_lemma_lexicon_lookup', [True, False])
def test_USASRuleBasedTagger(empty_lexicon_lookup: bool,
                             empty_lemma_lexicon_lookup: bool) -> None:
    lexicon_path = Path(DATA_DIR, 'lexicon.tsv')
    lexicon_lookup: Optional[Dict[str, List[str]]] = LexiconCollection.from_tsv(lexicon_path, include_pos=True)
    if empty_lexicon_lookup:
        lexicon_lookup = None
    lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = LexiconCollection.from_tsv(lexicon_path, include_pos=False)
    if empty_lemma_lexicon_lookup:
        lemma_lexicon_lookup = None

    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
    if lexicon_lookup is None:
        lexicon_lookup = {}
    if lemma_lexicon_lookup is None:
        lemma_lexicon_lookup = {}

    assert lexicon_lookup == tagger.lexicon_lookup
    assert lemma_lexicon_lookup == tagger.lemma_lexicon_lookup
    
    expected_attributes = ['lexicon_lookup', 'lemma_lexicon_lookup']
    tagger_attributes = list(tagger.__dict__.keys())
    assert len(expected_attributes) == len(tagger_attributes)
    for expected_attribute in expected_attributes:
        assert expected_attribute in tagger_attributes


def test_tag_token() -> None:
    test_data, lexicon_lookup, lemma_lexicon_lookup, expected_usas_tags = generate_tag_test_data()
    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
    for data, expected_tags in zip(test_data, expected_usas_tags):
        predicted_tags = tagger.tag_token(data)
        assert predicted_tags == expected_tags


def test_tag_tokens() -> None:
    test_data, lexicon_lookup, lemma_lexicon_lookup, expected_usas_tags = generate_tag_test_data()
    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
    output_usas_tags = tagger.tag_tokens(test_data)
    assert isinstance(output_usas_tags, Generator)

    assert len(expected_usas_tags) == len(list(output_usas_tags))
    for expected, output, context in zip(expected_usas_tags,
                                         output_usas_tags,
                                         test_data):
        assert expected == output, context
