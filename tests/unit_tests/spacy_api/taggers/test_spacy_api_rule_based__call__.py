import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pytest
from spacy.tokens import Doc
from spacy.vocab import Vocab

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule

from ..utils import compare_output, remove_extension


DATA_DIR = Path(__file__, '..', '..', '..', 'data').resolve()
TAGGER_DATA_DIR = Path(DATA_DIR, 'taggers', 'rule_based')


def generate_test_data(test_data_file: Path,
                       pos_mapper: Optional[Dict[str, str]] = None
                       ) -> Tuple[Doc,
                                  List[Tuple[List[str],
                                             List[Tuple[int, int]]]
                                       ]]:
    '''
    Given the test data stored at `test_data_file` it returns this data as a
    Tuple of length 2:

    1. `Doc` object that contains the following Token attributes:
        * lemmas
        * tags
    2. A list of Tuples of length 2, each tuple corresponds to a token and
    contains the following:
      1. A list of expected semantic tags that should be generated based
    on the associated `token`, `lemma`, and `pos` from the values in the `Doc`.
      2. A List of tuples of length 2. each `Tuple` indicates the start and end
    token index of the associated Multi Word Expression (MWE). If the `List` contains
    more than one `Tuple` then the MWE is discontinuous. For single word
    expressions the `List` will only contain 1 `Tuple` which will be
    (token_start_index, token_start_index + 1).

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

    `Tuple[Doc, List[Tuple[List[str], List[Tuple[int, int]]]]]`
    '''
    tokens: List[str] = []
    lemmas: List[str] = []
    pos_tags: List[str] = []
    spaces: List[bool] = []
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
            spaces.append(True)
            
            usas_tags = token_data['usas']
            mwe_indexes: List[Tuple[int, int]] = []
            for start, end in zip(token_data['start_indexes'],
                                  token_data['end_indexes']):
                mwe_indexes.append((int(start), int(end)))
            expected_output.append((usas_tags, mwe_indexes))
    
    doc = Doc(Vocab(), tokens, spaces, tags=pos_tags, lemmas=lemmas)
    return doc, expected_output


def empty_word_rule() -> SingleWordRule:
    '''An empty rule'''
    return SingleWordRule({'ignore': ['']}, {'ignore': ['']})


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


def create_tagger(pymusas_tags_token_attr: str,
                  pymusas_mwe_indexes_attr: str,
                  default_punctuation_tags: List[str],
                  default_number_tags: List[str],
                  rules: List[Rule],
                  pos_attribute: str = 'tag_'
                  ) -> RuleBasedTagger:
    remove_extension(pymusas_tags_token_attr)
    remove_extension(pymusas_mwe_indexes_attr)
    ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
    
    tagger = RuleBasedTagger(pymusas_tags_token_attr=pymusas_tags_token_attr,
                             pymusas_mwe_indexes_attr=pymusas_mwe_indexes_attr,
                             pos_attribute=pos_attribute)
    tagger.initialize(rules=rules, ranker=ranker,
                      default_punctuation_tags=default_punctuation_tags,
                      default_number_tags=default_number_tags)
    return tagger


def create_non_valid_tagger(pymusas_tags_token_attr: str,
                            pymusas_mwe_indexes_attr: str,) -> RuleBasedTagger:
    remove_extension(pymusas_tags_token_attr)
    remove_extension(pymusas_mwe_indexes_attr)
    tagger = RuleBasedTagger(pymusas_tags_token_attr=pymusas_tags_token_attr,
                             pymusas_mwe_indexes_attr=pymusas_mwe_indexes_attr,
                             pos_attribute='tag_')
    return tagger


@pytest.mark.parametrize("pymusas_tags_token_attr,pymusas_mwe_indexes_attr",
                         [('pymusas_tags', 'pymusas_mwe_indexes'),
                          ('pym_tags', 'mwe_indexes')])
def test_rule_based_tagger__call__(pymusas_tags_token_attr: str,
                                   pymusas_mwe_indexes_attr: str
                                   ) -> None:
    # Test the first case where we have no rules and it should tag everything as
    # Z99
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['punc'], ['num'], [empty_word_rule()])
    empty_doc = Doc(Vocab(), words=[' ', ' '], spaces=[True, True])
    expected_output = [
        (['Z99'], [(0, 1)]),
        (['Z99'], [(1, 2)])
    ]
    compare_output(expected_output, tagger(empty_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)

    # Test the default punctuation and number POS tags
    expected_output = [
        (['PUNCT'], [(0, 1)]),
        (['N1'], [(1, 2)])
    ]
    punctuation_doc = Doc(Vocab(), words=[' ', ' '], spaces=[True, True],
                          tags=['punc', 'num'])
    compare_output(expected_output, tagger(punctuation_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)
    
    # Test the punctuation and number POS tags when set by the user
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['grammer'], ['digit'], [empty_word_rule()])
    punctuation_doc = Doc(Vocab(), words=[' ', ' '], spaces=[True, True],
                          tags=['grammer', 'digit'])
    compare_output(expected_output, tagger(punctuation_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)

    # Test the case where we only use single word lexicon rules.
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_single_input_output.json')
    
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['punc'], ['num'], [single_word_rule(None)])
    test_doc, expected_output = generate_test_data(test_data_file)
    compare_output(expected_output, tagger(test_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)

    # Test the case where we use the POS mapper on the single word lexicon rules.
    rule_pos_mapper = {'adj': ['noun'], 'noun': ['adj']}
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['punc'], ['num'],
                           [single_word_rule(rule_pos_mapper)])
    with pytest.raises(AssertionError):
        compare_output(expected_output, tagger(test_doc),
                       pymusas_tags_token_attr, pymusas_mwe_indexes_attr)

    test_data_pos_mapper = {'adj': 'noun', 'noun': 'adj'}
    test_doc, expected_output = generate_test_data(test_data_file,
                                                   test_data_pos_mapper)
    compare_output(expected_output, tagger(test_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)

    # Test the MWE case
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_mwe_input_output.json')
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['punc'], ['num'], [mwe_word_rule(None)])
    test_doc, expected_output = generate_test_data(test_data_file)
    compare_output(expected_output, tagger(test_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)

    # Test the MWE case with POS Mapper
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['punc'], ['num'],
                           [mwe_word_rule(rule_pos_mapper)])
    test_doc, expected_output = generate_test_data(test_data_file,
                                                   test_data_pos_mapper)
    compare_output(expected_output, tagger(test_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)

    # Test the case of Single and MWE
    test_data_file = Path(TAGGER_DATA_DIR, 'rule_based_single_mwe_input_output.json')
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['punc'], ['num'],
                           [single_word_rule(None), mwe_word_rule(None)])
    test_doc, expected_output = generate_test_data(test_data_file)
    compare_output(expected_output, tagger(test_doc),
                   pymusas_tags_token_attr, pymusas_mwe_indexes_attr)
    
    # Test the error cases:
    # Error case 1: Non validated tagger
    tagger = create_non_valid_tagger(pymusas_tags_token_attr,
                                     pymusas_mwe_indexes_attr)
    with pytest.raises(ValueError):
        tagger(test_doc)
    
    # Error case 2: error occur during tagging as the token does not contain
    # the `pos` attribute.
    tagger = create_tagger(pymusas_tags_token_attr, pymusas_mwe_indexes_attr,
                           ['punc'], ['num'],
                           [single_word_rule(None), mwe_word_rule(None)],
                           pos_attribute='custom_pos')
    with pytest.raises(AttributeError):
        tagger(test_doc)
    
