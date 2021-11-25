import json
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple

import pytest
from spacy.tokens import Token, Doc
from spacy.language import Language
from spacy.vocab import Vocab

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger, make_usas_rule_based_tagger


DATA_DIR = Path(__file__, '..', '..', '..', 'data').resolve()
POS_MAPPER = {'DET': ['det', 'art'], 'NOUN': ['noun'], 'SCONJ': ['conj'],
              'PUNCT': ['PUNCT'], 'obj': ['obj']}


def generate_tag_test_data(test_data_file: Path, lexicon_file: Path
                           ) -> Tuple[Doc,
                                      Dict[str, List[str]],
                                      Dict[str, List[str]],
                                      List[List[str]]]:
    '''
    Given the test data stored at `test_data_file`, and
    the semantic lexicon at `lexicon_file`, it returns this data as a
    Tuple of length 4:

    1. `Doc` object that contains the following Token attributes:
        * lemmas
        * tags
    2. The semantic lexicon including Part Of Speech tag information.
    3. The semantic lexicon excluding Part Of Speech tag information.
    4. A list of a list of expected semantic tags that should be generated based
    on the associated token text, `lemma`, and `pos` from the values in the `Doc`
    object given in the first value of the tuple and the semantic lexicons
    from the second and third tuple values.

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

    `Tuple[Doc, Dict[str, List[str]], Dict[str, List[str]], List[List[str]]]`
    '''
    
    test_words: List[str] = []
    test_spaces: List[bool] = []
    test_tags: List[str] = []
    test_lemmas: List[str] = []
    
    expected_usas_tags: List[List[str]] = []
    with test_data_file.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            test_words.append(token_data['token'])
            test_lemmas.append(token_data['lemma'])
            test_spaces.append(True)
            test_tags.append(token_data['pos'])
            
            expected_usas_tags.append([token_data['usas']])
    doc = Doc(Vocab(), test_words, test_spaces, tags=test_tags, lemmas=test_lemmas)
    lexicon_lookup = LexiconCollection.from_tsv(lexicon_file, include_pos=True)
    lemma_lexicon_lookup = LexiconCollection.from_tsv(lexicon_file, include_pos=False)
    
    return doc, lexicon_lookup, lemma_lexicon_lookup, expected_usas_tags


@pytest.mark.parametrize('empty_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_lemma_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_pos_mapper', [True, False])
@pytest.mark.parametrize('custom_usas_tags_token_attr', [True, False])
@pytest.mark.parametrize('custom_pos_attribute', [True, False])
@pytest.mark.parametrize('custom_lemma_attribute', [True, False])
def test_USASRuleBasedTagger(empty_lexicon_lookup: bool,
                             empty_lemma_lexicon_lookup: bool,
                             empty_pos_mapper: bool,
                             custom_usas_tags_token_attr: bool,
                             custom_pos_attribute: bool,
                             custom_lemma_attribute: bool) -> None:
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

    usas_tags_token_attr = 'usas_tags'
    if custom_usas_tags_token_attr:
        usas_tags_token_attr = 'custom_tags'
    
    pos_attribute = 'pos_'
    if custom_pos_attribute:
        pos_attribute = 'custom_pos'

    lemma_attribute = 'lemma_'
    if custom_lemma_attribute:
        lemma_attribute = 'custom_lemma'

    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup,
                                 pos_mapper, usas_tags_token_attr,
                                 pos_attribute, lemma_attribute)

    if lexicon_lookup is None:
        lexicon_lookup = {}
    if lemma_lexicon_lookup is None:
        lemma_lexicon_lookup = {}
    
    assert lexicon_lookup == tagger.lexicon_lookup
    assert lemma_lexicon_lookup == tagger.lemma_lexicon_lookup
    assert pos_mapper == tagger.pos_mapper
    assert usas_tags_token_attr == tagger.usas_tags_token_attr
    assert pos_attribute == tagger.pos_attribute
    assert lemma_attribute == tagger.lemma_attribute
    
    expected_attributes = ['lexicon_lookup', 'lemma_lexicon_lookup',
                           'pos_mapper', 'usas_tags_token_attr',
                           'pos_attribute', 'lemma_attribute']
    tagger_attributes = list(tagger.__dict__.keys())
    assert len(expected_attributes) == len(tagger_attributes)
    for expected_attribute in expected_attributes:
        assert expected_attribute in tagger_attributes

    meta_assigns = [f'token._.{usas_tags_token_attr}']
    assert meta_assigns == Language.get_factory_meta('usas_tagger').assigns
    required_token_attributes = Language.get_factory_meta('usas_tagger').requires
    
    pos_required = pos_attribute
    if pos_required == 'pos_':
        pos_required = 'pos'
    lemma_required = lemma_attribute
    if lemma_required == 'lemma_':
        lemma_required = 'lemma'
    meta_required = [f'token.{lemma_required}', f'token.{pos_required}']
    assert meta_required == required_token_attributes


def test_call() -> None:
    test_data_file = Path(DATA_DIR, 'rule_based_input_output.json')
    lexicon_file = Path(DATA_DIR, 'lexicon.tsv')
    (test_doc, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(test_data_file, lexicon_file)
    
    usas_tagger_config = {'pos_attribute': 'tag_', 'lexicon_lookup': lexicon_lookup,
                          'lemma_lexicon_lookup': lemma_lexicon_lookup}
    nlp = Language(Vocab(), meta={"name": "example"})
    usas_tagger = nlp.add_pipe('usas_tagger', 'semantic tagger', config=usas_tagger_config)
    assert isinstance(usas_tagger, USASRuleBasedTagger)
    usas_tagger(test_doc)
    predicted_usas_tags = [token._.usas_tags for token in test_doc]
    assert expected_usas_tags == predicted_usas_tags

'''
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
'''