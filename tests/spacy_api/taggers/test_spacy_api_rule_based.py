import json
from pathlib import Path
import tempfile
from typing import Dict, List, Optional, Tuple, Union, cast

import pytest
import spacy
from spacy.language import Language
from spacy.tokens import Doc
from spacy.vocab import Vocab

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger


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


def tagger_attribute_tests(tagger: USASRuleBasedTagger,
                           lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                           lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                           pos_mapper: Optional[Dict[str, List[str]]] = None,
                           usas_tags_token_attr: str = 'usas_tags',
                           pos_attribute: str = 'pos_',
                           lemma_attribute: str = 'lemma_') -> None:
    if lexicon_lookup is None:
        assert {} == tagger.lexicon_lookup
    else:
        assert lexicon_lookup == tagger.lexicon_lookup
    if lemma_lexicon_lookup is None:
        assert {} == tagger.lemma_lexicon_lookup
    else:
        assert lemma_lexicon_lookup == tagger.lemma_lexicon_lookup
    if pos_mapper is None:
        assert tagger.pos_mapper is None
    else:
        assert pos_mapper == tagger.pos_mapper
    assert usas_tags_token_attr == tagger.usas_tags_token_attr
    assert pos_attribute == tagger.pos_attribute
    assert lemma_attribute == tagger.lemma_attribute

    expected_attributes = ['lexicon_lookup', 'lemma_lexicon_lookup',
                           'pos_mapper', '_usas_tags_token_attr',
                           '_pos_attribute', '_lemma_attribute']
    tagger_attributes = list(tagger.__dict__.keys())
    assert len(expected_attributes) == len(tagger_attributes)
    for expected_attribute in expected_attributes:
        assert expected_attribute in tagger_attributes


def tagger_meta_tests(usas_tags_token_attr: str,
                      pos_attribute: str, lemma_attribute: str) -> None:
    meta_assigns = [f'token._.{usas_tags_token_attr}']
    assert meta_assigns == Language.get_factory_meta('usas_tagger').assigns
    required_token_attributes = Language.get_factory_meta('usas_tagger').requires
    
    pos_required = pos_attribute
    if pos_required == 'pos_':
        pos_required = 'pos'
    if pos_required == 'tag_':
        pos_required = 'tag'
    lemma_required = lemma_attribute
    if lemma_required == 'lemma_':
        lemma_required = 'lemma'
    meta_required = [f'token.{lemma_required}', f'token.{pos_required}']

    number_attributes_in_required = 0
    for value in required_token_attributes:
        assert value in meta_required
        number_attributes_in_required += 1
    assert len(meta_required) == number_attributes_in_required


def create_USASRuleBasedTagger(empty_lexicon_lookup: bool,
                               empty_lemma_lexicon_lookup: bool,
                               empty_pos_mapper: bool,
                               custom_usas_tags_token_attr: bool,
                               custom_pos_attribute: bool,
                               custom_lemma_attribute: bool,
                               use_initialize: bool
                               ) -> Tuple[USASRuleBasedTagger,
                                          Dict[str, List[str]],
                                          Dict[str, List[str]],
                                          Union[Dict[str, List[str]], None],
                                          str, str, str]:
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

    tagger = USASRuleBasedTagger()
    if use_initialize:
        tagger.initialize(None, None, lexicon_lookup, lemma_lexicon_lookup,
                          pos_mapper, usas_tags_token_attr,
                          pos_attribute, lemma_attribute)
    else:
        tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup,
                                     pos_mapper, usas_tags_token_attr,
                                     pos_attribute, lemma_attribute)
    if lexicon_lookup is None:
        lexicon_lookup = {}
    if lemma_lexicon_lookup is None:
        lemma_lexicon_lookup = {}
    return (tagger, lexicon_lookup, lemma_lexicon_lookup, pos_mapper,
            usas_tags_token_attr, pos_attribute, lemma_attribute)
    

@pytest.mark.parametrize('empty_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_lemma_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_pos_mapper', [True, False])
@pytest.mark.parametrize('custom_usas_tags_token_attr', [True, False])
@pytest.mark.parametrize('custom_pos_attribute', [True, False])
@pytest.mark.parametrize('custom_lemma_attribute', [True, False])
@pytest.mark.parametrize('use_initialize', [True, False])
def test_USASRuleBasedTagger(empty_lexicon_lookup: bool,
                             empty_lemma_lexicon_lookup: bool,
                             empty_pos_mapper: bool,
                             custom_usas_tags_token_attr: bool,
                             custom_pos_attribute: bool,
                             custom_lemma_attribute: bool,
                             use_initialize: bool) -> None:
    (tagger, lexicon_lookup, lemma_lexicon_lookup, pos_mapper,
     usas_tags_token_attr, pos_attribute,
     lemma_attribute) = create_USASRuleBasedTagger(empty_lexicon_lookup, empty_lemma_lexicon_lookup,
                                                   empty_pos_mapper, custom_usas_tags_token_attr,
                                                   custom_pos_attribute, custom_lemma_attribute,
                                                   use_initialize)

    tagger_attribute_tests(tagger, lexicon_lookup, lemma_lexicon_lookup,
                           pos_mapper, usas_tags_token_attr,
                           pos_attribute, lemma_attribute)

    tagger_meta_tests(usas_tags_token_attr, pos_attribute, lemma_attribute)


def test_usas_tags_token_attr() -> None:
    default_usas_tags_token_attr = 'usas_tags'
    tagger = USASRuleBasedTagger()
    tagger_meta_tests(default_usas_tags_token_attr, 'pos_', 'lemma_')

    tagger.usas_tags_token_attr = 'semantic_tags'
    tagger_meta_tests('semantic_tags', 'pos_', 'lemma_')

    tagger.usas_tags_token_attr = 'semantic_tags'
    tagger_meta_tests('semantic_tags', 'pos_', 'lemma_')
    assert 'semantic_tags' == tagger.usas_tags_token_attr

    tagger.usas_tags_token_attr = 'usas_tags'
    assert 'usas_tags' == tagger.usas_tags_token_attr
    tagger_meta_tests('usas_tags', 'pos_', 'lemma_')


def test_pos_attribute() -> None:
    default_pos_attribute = 'pos_'
    tagger = USASRuleBasedTagger()
    tagger_meta_tests('usas_tags', default_pos_attribute, 'lemma_')
    assert tagger.pos_attribute == default_pos_attribute

    tagger.pos_attribute = 'test'
    tagger_meta_tests('usas_tags', 'test', 'lemma_')
    assert tagger.pos_attribute == 'test'

    tagger.pos_attribute = 'test'
    tagger_meta_tests('usas_tags', 'test', 'lemma_')
    assert tagger.pos_attribute == 'test'

    tagger.pos_attribute = 'pos_'
    tagger_meta_tests('usas_tags', 'pos_', 'lemma_')
    assert tagger.pos_attribute == 'pos_'

    tagger.pos_attribute = 'tag_'
    tagger_meta_tests('usas_tags', 'tag_', 'lemma_')
    assert tagger.pos_attribute == 'tag_'


def test_lemma_attribute() -> None:
    default_lemma_attribute = 'lemma_'
    tagger = USASRuleBasedTagger()
    tagger_meta_tests('usas_tags', 'pos_', default_lemma_attribute)
    assert tagger.lemma_attribute == default_lemma_attribute

    tagger.lemma_attribute = 'test'
    tagger_meta_tests('usas_tags', 'pos_', 'test')
    assert tagger.lemma_attribute == 'test'

    tagger.lemma_attribute = 'test'
    tagger_meta_tests('usas_tags', 'pos_', 'test')
    assert tagger.lemma_attribute == 'test'

    tagger.lemma_attribute = 'lemma_'
    tagger_meta_tests('usas_tags', 'pos_', 'lemma_')
    assert tagger.lemma_attribute == 'lemma_'


def test_call() -> None:
    test_data_file = Path(DATA_DIR, 'rule_based_input_output.json')
    lexicon_file = Path(DATA_DIR, 'lexicon.tsv')
    (test_doc, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(test_data_file, lexicon_file)
    
    usas_tagger_config = {'pos_attribute': 'tag_', 'lexicon_lookup': lexicon_lookup,
                          'lemma_lexicon_lookup': lemma_lexicon_lookup}
    nlp = Language(Vocab(), meta={"name": "example"})
    usas_tagger = nlp.add_pipe('usas_tagger', 'semantic tagger', config=usas_tagger_config)
    usas_tagger(test_doc)
    predicted_usas_tags = [token._.usas_tags for token in test_doc]
    assert expected_usas_tags == predicted_usas_tags

    # Tets that it works with a POS mapper
    pos_map_test_data_file = Path(DATA_DIR, 'rule_based_input_output_pos_mapped.json')
    (test_doc, lexicon_lookup,
     lemma_lexicon_lookup, expected_usas_tags) = generate_tag_test_data(pos_map_test_data_file, lexicon_file)
    nlp = Language(Vocab(), meta={"name": "example"})
    usas_tagger_config['pos_mapper'] = POS_MAPPER
    usas_tagger = nlp.add_pipe('usas_tagger', 'semantic tagger', config=usas_tagger_config)
    usas_tagger(test_doc)
    predicted_usas_tags = [token._.usas_tags for token in test_doc]
    assert expected_usas_tags == predicted_usas_tags


@pytest.mark.parametrize('empty_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_lemma_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_pos_mapper', [True, False])
@pytest.mark.parametrize('custom_usas_tags_token_attr', [True, False])
@pytest.mark.parametrize('custom_pos_attribute', [True, False])
@pytest.mark.parametrize('custom_lemma_attribute', [True, False])
@pytest.mark.parametrize('use_initialize', [True, False])
def test_load_and_save_bytes(empty_lexicon_lookup: bool,
                             empty_lemma_lexicon_lookup: bool,
                             empty_pos_mapper: bool,
                             custom_usas_tags_token_attr: bool,
                             custom_pos_attribute: bool,
                             custom_lemma_attribute: bool,
                             use_initialize: bool) -> None:
    (_, lexicon_lookup, lemma_lexicon_lookup, pos_mapper,
     usas_tags_token_attr, pos_attribute,
     lemma_attribute) = create_USASRuleBasedTagger(empty_lexicon_lookup, empty_lemma_lexicon_lookup,
                                                   empty_pos_mapper, custom_usas_tags_token_attr,
                                                   custom_pos_attribute, custom_lemma_attribute,
                                                   use_initialize)
    usas_config = {'lexicon_lookup': lexicon_lookup,
                   'lemma_lexicon_lookup': lemma_lexicon_lookup,
                   'pos_mapper': pos_mapper,
                   'usas_tags_token_attr': usas_tags_token_attr,
                   'pos_attribute': pos_attribute,
                   'lemma_attribute': lemma_attribute}
    # Default settings
    nlp = spacy.blank("en")
    nlp.add_pipe('usas_tagger', config=usas_config)
    data = nlp.to_bytes()
    config = nlp.config
    del nlp
    nlp = spacy.blank("en")
    nlp = nlp.from_config(config)
    nlp.from_bytes(data)
    loaded_tagger_pipe = nlp.get_pipe('usas_tagger')
    loaded_tagger = cast(USASRuleBasedTagger, loaded_tagger_pipe)
    tagger_attribute_tests(loaded_tagger, lexicon_lookup, lemma_lexicon_lookup,
                           pos_mapper, usas_tags_token_attr,
                           pos_attribute, lemma_attribute)

    tagger_meta_tests(usas_tags_token_attr, pos_attribute, lemma_attribute)


@pytest.mark.parametrize('empty_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_lemma_lexicon_lookup', [True, False])
@pytest.mark.parametrize('empty_pos_mapper', [True, False])
@pytest.mark.parametrize('custom_usas_tags_token_attr', [True, False])
@pytest.mark.parametrize('custom_pos_attribute', [True, False])
@pytest.mark.parametrize('custom_lemma_attribute', [True, False])
@pytest.mark.parametrize('use_initialize', [True, False])
def test_load_and_save_json(empty_lexicon_lookup: bool,
                            empty_lemma_lexicon_lookup: bool,
                            empty_pos_mapper: bool,
                            custom_usas_tags_token_attr: bool,
                            custom_pos_attribute: bool,
                            custom_lemma_attribute: bool,
                            use_initialize: bool) -> None:

    (_, lexicon_lookup, lemma_lexicon_lookup, pos_mapper,
     usas_tags_token_attr, pos_attribute,
     lemma_attribute) = create_USASRuleBasedTagger(empty_lexicon_lookup, empty_lemma_lexicon_lookup,
                                                   empty_pos_mapper, custom_usas_tags_token_attr,
                                                   custom_pos_attribute, custom_lemma_attribute,
                                                   use_initialize)
    usas_config = {'lexicon_lookup': lexicon_lookup,
                   'lemma_lexicon_lookup': lemma_lexicon_lookup,
                   'pos_mapper': pos_mapper,
                   'usas_tags_token_attr': usas_tags_token_attr,
                   'pos_attribute': pos_attribute,
                   'lemma_attribute': lemma_attribute}
    # Default settings
    nlp = spacy.blank("en")
    nlp.add_pipe('usas_tagger', config=usas_config)
    with tempfile.TemporaryDirectory() as temp_dir:
        nlp.to_disk(temp_dir)
        del nlp
        nlp = spacy.load(temp_dir)
        assert 'usas_tagger' in nlp.pipe_names
        loaded_tagger_pipe = nlp.get_pipe('usas_tagger')
        loaded_tagger = cast(USASRuleBasedTagger, loaded_tagger_pipe)
        tagger_attribute_tests(loaded_tagger, lexicon_lookup, lemma_lexicon_lookup,
                               pos_mapper, usas_tags_token_attr,
                               pos_attribute, lemma_attribute)

        tagger_meta_tests(usas_tags_token_attr, pos_attribute, lemma_attribute)
