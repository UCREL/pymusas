import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from _pytest.fixtures import SubRequest
import pytest

from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexicon_entry import LexicalMatch, RankingMetaData
from pymusas.taggers.rules.mwe import MWERule
from pymusas.utils import token_pos_tags_in_lexicon_entry


DATA_DIR = Path(__file__, '..', '..', '..', 'data').resolve()
TAGGER_DATA_DIR = Path(DATA_DIR, 'taggers', 'rules', 'mwe')


def compare_token_ranking_meta_data(token_ranking_meta_data_1: List[List[RankingMetaData]],
                                    token_ranking_meta_data_2: List[List[RankingMetaData]]
                                    ) -> None:
    '''
    This tests if the two token ranking meta data lists are equal to each other.

    # Raises

    `AssertionError`
        If the two lists are not of same length.
    `AssertionError`
        If each inner list is not of same length.
    `AssertionError`
        If each inner list when converted to a set are not equal to each other.
    '''
    assert len(token_ranking_meta_data_1) == len(token_ranking_meta_data_2)

    index = 0
    for ranking_meta_data_1, ranking_meta_data_2 in zip(token_ranking_meta_data_1,
                                                        token_ranking_meta_data_2):
        assert len(ranking_meta_data_1) == len(ranking_meta_data_2), index
        assert set(ranking_meta_data_1) == set(ranking_meta_data_2), index


def generate_tag_test_data(test_data_file: Path,
                           pos_mapper: Optional[Dict[str, str]]
                           ) -> Tuple[List[str],
                                      List[str],
                                      List[str],
                                      List[List[RankingMetaData]]
                                      ]:
    '''
    Given the test data stored at `test_data_file` it returns this data as a
    Tuple of length 4:

    1. A List of `tokens`, from the `test_data_file`.
    2. A List of `lemmas`, from the `test_data_file`.
    3. A List of `POS tags`, from the `test_data_file`.
    4. A list of a list of expected
    :class:`pymusas.rankers.lexicon_entry.RankingMetaData` objects.

    # Parameters

    test_data_file : `Path`
        A JSON file containing an Array of Objects. Each object must contain the
        following properties/keys:
        1. token, type str
        2. lemma, type str
        3. pos, type str
        4. ranking_meta_data_objects, type List[List[RankingMetaData]] - This
        has to be written as a JSON object that is then converted to a
        RankingMetaData object in Python.
    pos_mapper : `Dict[str, str]`, optional (default `None`)
        If not `None` it will map each POS value in the `lexicon_entry_match`,
        that is within the `test_data_file`.
    
    # Returns

    `Tuple[List[str], List[str], List[str], List[List[RankingMetaData]]]`
    '''
    def json_to_ranking_meta_data(json_object: Dict[str, Union[str, int,
                                                               bool, List[str]]]
                                  ) -> RankingMetaData:
        
        assert isinstance(json_object['lexicon_type'], str)
        lexicon_type = getattr(LexiconType, json_object['lexicon_type'])
        assert isinstance(lexicon_type, LexiconType)

        n_gram_length = json_object['lexicon_n_gram_length']
        assert isinstance(n_gram_length, int)

        wildcard_count = json_object['wildcard_count']
        assert isinstance(wildcard_count, int)

        exclude_pos_information = json_object['exclude_pos_information']
        assert isinstance(exclude_pos_information, bool)

        assert isinstance(json_object['lexical_match'], str)
        lexical_match = getattr(LexicalMatch, json_object['lexical_match'])
        assert isinstance(lexical_match, LexicalMatch)

        start_index = json_object['token_match_start_index']
        assert isinstance(start_index, int)

        end_index = json_object['token_match_end_index']
        assert isinstance(end_index, int)

        lexicon_entry_match = json_object['lexicon_entry_match']
        assert isinstance(lexicon_entry_match, str)
        if pos_mapper is not None:
            mapped_lexicon_entry_match: List[str] = []
            for token, pos in token_pos_tags_in_lexicon_entry(lexicon_entry_match):
                mapped_pos = pos_mapper.get(pos, pos)
                mapped_lexicon_entry_match.append(f'{token}_{mapped_pos}')
            lexicon_entry_match = ' '.join(mapped_lexicon_entry_match)

        semantic_tags_list = json_object['semantic_tags']
        assert isinstance(semantic_tags_list, list)
        for value in semantic_tags_list:
            assert isinstance(value, str)
        semantic_tags = tuple(semantic_tags_list)

        return RankingMetaData(lexicon_type, n_gram_length, wildcard_count,
                               exclude_pos_information, lexical_match,
                               start_index, end_index, lexicon_entry_match,
                               semantic_tags)
    
    test_tokens: List[str] = []
    test_lemmas: List[str] = []
    test_pos_tags: List[str] = []
    test_ranking_meta_data: List[List[RankingMetaData]] = []
    
    with test_data_file.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            test_tokens.append(token_data['token'])
            test_lemmas.append(token_data['lemma'])
            test_pos_tags.append(token_data['pos'])
            
            token_ranking_meta_data: List[RankingMetaData] = []
            ranking_meta_data_objects = token_data['ranking_meta_data_objects']
            for ranking_object in ranking_meta_data_objects:
                ranking_object = json_to_ranking_meta_data(ranking_object)
                token_ranking_meta_data.append(ranking_object)
            test_ranking_meta_data.append(token_ranking_meta_data)
    
    return (test_tokens, test_lemmas, test_pos_tags, test_ranking_meta_data)


@pytest.fixture(scope="module", params=[None, {'NN': 'noun'}])
def non_special_data(request: SubRequest) -> Tuple[Tuple[List[str],
                                                         List[str],
                                                         List[str],
                                                         List[List[RankingMetaData]]
                                                         ],
                                                   Dict[str, List[str]],
                                                   Optional[Dict[str, List[str]]]]:
    
    non_special_data_file = Path(TAGGER_DATA_DIR,
                                 'rule_based_mwe_non_special_input_output.json')
    pos_mapper: Optional[Dict[str, str]] = request.param
    if pos_mapper is None:
        test_data = generate_tag_test_data(non_special_data_file, pos_mapper)
        lexicon = {
            "North_noun East_noun London_noun": ['Z1'],
            "east_noun london_noun": ['Z2']
        }
        return (test_data, lexicon, pos_mapper)
    else:
        assert isinstance(pos_mapper, dict)
        
    pos_mapped_lexicon = {
        "North_NN East_NN London_NN": ['Z1'],
        "east_NN london_NN": ['Z2']
    }
    noun_mapper = {'NN': ['noun']}
    reverse_noun_mapper = {'noun': 'NN'}
    test_data = generate_tag_test_data(non_special_data_file, reverse_noun_mapper)

    return (test_data, pos_mapped_lexicon, noun_mapper)


@pytest.fixture(scope="module", params=[None, {'NN': 'noun'}])
def wildcard_data(request: SubRequest) -> Tuple[Tuple[List[str],
                                                      List[str],
                                                      List[str],
                                                      List[List[RankingMetaData]]
                                                      ],
                                                Dict[str, List[str]],
                                                Optional[Dict[str, List[str]]]]:
    wildcard_data_file = Path(TAGGER_DATA_DIR,
                              'rule_based_mwe_wildcard_input_output.json')
    pos_mapper: Optional[Dict[str, str]] = request.param
    if pos_mapper is None:
        test_data = generate_tag_test_data(wildcard_data_file, pos_mapper)
        lexicon = {
            "North_noun East_noun London_*": ['Z1'],
            "North_* East**_noun London_noun": ['Z2'],
            "East_* London_noun": ['Z3'],
            "East_* London_*": ['Z4'],
            "*as*_noun London_*": ['Z5']
        }
        return (test_data, lexicon, pos_mapper)
    else:
        assert isinstance(pos_mapper, dict)
    
    pos_mapped_lexicon = {
        "North_NN East_NN London_*": ['Z1'],
        "North_* East**_NN London_NN": ['Z2'],
        "East_* London_NN": ['Z3'],
        "East_* London_*": ['Z4'],
        "*as*_NN London_*": ['Z5']
    }
    noun_mapper = {'NN': ['noun']}
    reverse_noun_mapper = {'noun': 'NN'}
    test_data = generate_tag_test_data(wildcard_data_file, reverse_noun_mapper)

    return (test_data, pos_mapped_lexicon, noun_mapper)


def test_mwe_rule__NON_SPECIAL_CASES(non_special_data: Tuple[Tuple[List[str],
                                                                   List[str],
                                                                   List[str],
                                                                   List[List[RankingMetaData]]],
                                                             Dict[str, List[str]],
                                                             Optional[Dict[str, List[str]]]]
                                     ) -> None:
    '''
    This tests MWE Rule when using only NON SPECIAL CASES, which are direct
    matches, e.g. `ski_noun boot_noun`, i.e. does not use any special syntax
    like wildcards.
    '''
    data, lexicon, pos_mapper = non_special_data
    tokens, lemmas, pos_tags, expected_ranking_meta_data = data
    
    # Test that it returns a list of empty lists.
    mwe_rule = MWERule({})
    empty_list: List[List[RankingMetaData]] = [[] for _ in tokens]
    assert empty_list == mwe_rule(tokens, lemmas, pos_tags)

    # Test that it returns a list of one empty list, as we have no tokens to
    # tag
    assert [] == mwe_rule([], [], [])

    # Test that in the case of only tagging one token we have an empty list,
    # as one token is not enough to create a MWE
    assert [[]] == mwe_rule(['test'], ['test'], ['det'])

    # Test that it covers all of the non special syntax cases, e.g. all of the
    # cases that do not contain a wildcard or curly braces.
    mwe_rule = MWERule(lexicon, pos_mapper)
    compare_token_ranking_meta_data(expected_ranking_meta_data,
                                    mwe_rule(tokens, lemmas, pos_tags))


def test_mwe_rules_WILDCARD_CASES(wildcard_data: Tuple[Tuple[List[str],
                                                             List[str],
                                                             List[str],
                                                             List[List[RankingMetaData]]],
                                                       Dict[str, List[str]],
                                                       Optional[Dict[str, List[str]]]]
                                  ) -> None:
    '''
    This tests MWE Rule when using only WILDCARD cases, e.g. `ski_noun *_noun`
    '''
    data, lexicon, pos_mapper = wildcard_data
    tokens, lemmas, pos_tags, expected_ranking_meta_data = data
    
    mwe_rule = MWERule(lexicon, pos_mapper)
    compare_token_ranking_meta_data(expected_ranking_meta_data,
                                    mwe_rule(tokens, lemmas, pos_tags))
