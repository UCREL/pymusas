import json
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple

import pytest

from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.rule_based import USASRuleBasedTagger, _tag_token


DATA_DIR = Path(__file__, '..', '..', 'data').resolve()
POS_MAPPER = {'DET': ['det', 'art'], 'NOUN': ['noun'], 'SCONJ': ['conj'],
              'PUNCT': ['PUNCT'], 'obj': ['obj']}


def generate_tag_test_data(test_data_file: Path, lexicon_file: Path
                           ) -> Tuple[List[Tuple[str, str, str]],
                                      Dict[str, List[str]],
                                      Dict[str, List[str]],
                                      List[List[str]]]:
    '''
    Given the test data stored at `test_data_file`, and
    the semantic lexicon at `lexicon_file`, it returns this data as a
    Tuple of length 4:

    1. A List of expected `token`, `lemma`, and `pos`. From the `test_data_file`.
    2. The semantic lexicon including Part Of Speech tag information.
    3. The semantic lexicon excluding Part Of Speech tag information.
    4. A list of a list of expected semantic tags that should be generated based
    on the associated `token`, `lemma`, and `pos` from the first value of the tuple and
    the semantic lexicons data from the second and third tuple values.

    # Parameters

    test_data_file : `Path`
        A JSON file containing an Array of Objects. Each object must contain the
        following properties/keys:
        1. token
        2. lemma
        3. pos
        4. usas

    lexicon_file : `Path`
        A TSV file that can be converted into a :class:`pymusas.lexicon_collection.LexiconCollection`
        by using the class method :func:`pymusas.lexicon_collection.LexiconCollection.from_tsv`
    
    # Returns

    `Tuple[List[Tuple[str, str, str]], Dict[str, List[str]], Dict[str, List[str]], List[List[str]]]`
    '''
    test_data: List[Tuple[str, str, str]] = []
    
    expected_usas_tags: List[List[str]] = []
    with test_data_file.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            token = token_data['token']
            lemma = token_data['lemma']
            pos = token_data['pos']
            test_data.append((token, lemma, pos))
            expected_usas_tags.append([token_data['usas']])
    
    lexicon_lookup = LexiconCollection.from_tsv(lexicon_file, include_pos=True)
    lemma_lexicon_lookup = LexiconCollection.from_tsv(lexicon_file, include_pos=False)
    
    return test_data, lexicon_lookup, lemma_lexicon_lookup, expected_usas_tags


def test__tag_token() -> None:

    test_data_file = Path(DATA_DIR, 'rule_based_input_output.json')
    lexicon_file = Path(DATA_DIR, 'lexicon.tsv')
    (test_data, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(test_data_file, lexicon_file)
    for data, expected_tags in zip(test_data, expected_usas_tags):
        text, lemma, pos = data
        predicted_tags = _tag_token(text, lemma, [pos], lexicon_lookup, lemma_lexicon_lookup)
        assert predicted_tags == expected_tags

    # Test that it works with a POS mapper
    pos_map_test_data_file = Path(DATA_DIR, 'rule_based_input_output_pos_mapped.json')
    (test_data, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(pos_map_test_data_file, lexicon_file)
    for data, expected_tags in zip(test_data, expected_usas_tags):
        text, lemma, pos = data
        mapped_pos = POS_MAPPER.get(pos, [])
        predicted_tags = _tag_token(text, lemma, mapped_pos, lexicon_lookup, lemma_lexicon_lookup,)
        assert predicted_tags == expected_tags

    # Raise TypeError due to not converting a POS tag into a List rather than
    # being kept as a String
    with pytest.raises(TypeError):
        _tag_token('example', 'example', 'pos', {}, {})  # type: ignore


@pytest.mark.parametrize('empty_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_lemma_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_pos_mapper', [True, False])
def test_USASRuleBasedTagger(empty_lexicon_lookup: bool,
                             empty_lemma_lexicon_lookup: bool,
                             empty_pos_mapper: bool) -> None:
    lexicon_path = Path(DATA_DIR, 'lexicon.tsv')
    lexicon_lookup: Optional[Dict[str, List[str]]] = LexiconCollection.from_tsv(lexicon_path, include_pos=True)
    if empty_lexicon_lookup:
        lexicon_lookup = None
    lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = LexiconCollection.from_tsv(lexicon_path, include_pos=False)
    if empty_lemma_lexicon_lookup:
        lemma_lexicon_lookup = None
    pos_mapper: Optional[Dict[str, List[str]]] = POS_MAPPER
    if empty_pos_mapper:
        pos_mapper = None

    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup, pos_mapper)
    if lexicon_lookup is None:
        lexicon_lookup = {}
    if lemma_lexicon_lookup is None:
        lemma_lexicon_lookup = {}

    assert lexicon_lookup == tagger.lexicon_lookup
    assert lemma_lexicon_lookup == tagger.lemma_lexicon_lookup
    assert pos_mapper == tagger.pos_mapper
    
    expected_attributes = ['lexicon_lookup', 'lemma_lexicon_lookup', 'pos_mapper']
    tagger_attributes = list(tagger.__dict__.keys())
    assert len(expected_attributes) == len(tagger_attributes)
    for expected_attribute in expected_attributes:
        assert expected_attribute in tagger_attributes


def test_tag_token() -> None:
    test_data_file = Path(DATA_DIR, 'rule_based_input_output.json')
    lexicon_file = Path(DATA_DIR, 'lexicon.tsv')
    (test_data, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(test_data_file, lexicon_file)
    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
    for data, expected_tags in zip(test_data, expected_usas_tags):
        predicted_tags = tagger.tag_token(data)
        assert predicted_tags == expected_tags

    # Test that it works with a POS mapper
    pos_map_test_data_file = Path(DATA_DIR, 'rule_based_input_output_pos_mapped.json')
    (test_data, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(pos_map_test_data_file, lexicon_file)
    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup, POS_MAPPER)
    for data, expected_tags in zip(test_data, expected_usas_tags):
        predicted_tags = tagger.tag_token(data)
        assert predicted_tags == expected_tags


def test_tag_tokens() -> None:
    test_data_file = Path(DATA_DIR, 'rule_based_input_output.json')
    lexicon_file = Path(DATA_DIR, 'lexicon.tsv')
    (test_data, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(test_data_file, lexicon_file)
    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
    output_usas_tags = tagger.tag_tokens(test_data)
    assert isinstance(output_usas_tags, Generator)

    assert len(expected_usas_tags) == len(list(output_usas_tags))
    for expected, output, context in zip(expected_usas_tags,
                                         output_usas_tags,
                                         test_data):
        assert expected == output, context
