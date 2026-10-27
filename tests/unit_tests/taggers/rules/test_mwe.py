import json
from pathlib import Path

from _pytest.fixtures import SubRequest
import pytest

from pymusas.lexicon_collection import LexiconType, MWELexiconCollection
from pymusas.rankers.lexical_match import LexicalMatch
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.utils import token_pos_tags_in_lexicon_entry


DATA_DIR = Path(__file__, '..', '..', '..', 'data').resolve()
TAGGER_DATA_DIR = Path(DATA_DIR, 'taggers', 'rules', 'mwe')


def compare_token_ranking_meta_data(token_ranking_meta_data_1: list[list[RankingMetaData]],
                                    token_ranking_meta_data_2: list[list[RankingMetaData]]
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
                           pos_mapper: dict[str, str] | None
                           ) -> tuple[list[str],
                                      list[str],
                                      list[str],
                                      list[list[RankingMetaData]]
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
        4. ranking_meta_data_objects, type list[list[RankingMetaData]] - This
        has to be written as a JSON object that is then converted to a
        RankingMetaData object in Python.
    pos_mapper : `dict[str, str]`, optional (default `None`)
        If not `None` it will map each POS value in the `lexicon_entry_match`,
        that is within the `test_data_file`.
    
    # Returns

    `tuple[list[str], list[str], list[str], list[list[RankingMetaData]]]`
    '''
    def json_to_ranking_meta_data(json_object: dict[str, str | int | bool | list[str]]
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
            mapped_lexicon_entry_match: list[str] = []
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
    
    test_tokens: list[str] = []
    test_lemmas: list[str] = []
    test_pos_tags: list[str] = []
    test_ranking_meta_data: list[list[RankingMetaData]] = []
    
    with test_data_file.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            test_tokens.append(token_data['token'])
            test_lemmas.append(token_data['lemma'])
            test_pos_tags.append(token_data['pos'])
            
            token_ranking_meta_data: list[RankingMetaData] = []
            ranking_meta_data_objects = token_data['ranking_meta_data_objects']
            for ranking_object in ranking_meta_data_objects:
                ranking_object = json_to_ranking_meta_data(ranking_object)
                token_ranking_meta_data.append(ranking_object)
            test_ranking_meta_data.append(token_ranking_meta_data)
    
    return (test_tokens, test_lemmas, test_pos_tags, test_ranking_meta_data)


@pytest.fixture(scope="module", params=[None, {'NN': 'noun'}])
def non_special_data(request: SubRequest) -> tuple[tuple[list[str],
                                                         list[str],
                                                         list[str],
                                                         list[list[RankingMetaData]]
                                                         ],
                                                   dict[str, list[str]],
                                                   dict[str, list[str]] | None]:
    
    non_special_data_file = Path(TAGGER_DATA_DIR,
                                 'rule_based_mwe_non_special_input_output.json')
    pos_mapper: dict[str, str] | None = request.param
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
def wildcard_data(request: SubRequest) -> tuple[tuple[list[str],
                                                      list[str],
                                                      list[str],
                                                      list[list[RankingMetaData]]
                                                      ],
                                                dict[str, list[str]],
                                                dict[str, list[str]] | None]:
    wildcard_data_file = Path(TAGGER_DATA_DIR,
                              'rule_based_mwe_wildcard_input_output.json')
    pos_mapper: dict[str, str] | None = request.param
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


@pytest.mark.parametrize('from_bytes', [False, True])
def test_mwe_rule__NON_SPECIAL_CASES(non_special_data: tuple[tuple[list[str],
                                                                   list[str],
                                                                   list[str],
                                                                   list[list[RankingMetaData]]],
                                                             dict[str, list[str]],
                                                             dict[str, list[str]] | None],
                                     from_bytes: bool
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
    empty_list: list[list[RankingMetaData]] = [[] for _ in tokens]
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
    if from_bytes:
        mwe_rule = MWERule.from_bytes(mwe_rule.to_bytes())

    compare_token_ranking_meta_data(expected_ranking_meta_data,
                                    mwe_rule(tokens, lemmas, pos_tags))


@pytest.mark.parametrize('from_bytes', [False, True])
def test_mwe_rules_WILDCARD_CASES(wildcard_data: tuple[tuple[list[str],
                                                             list[str],
                                                             list[str],
                                                             list[list[RankingMetaData]]],
                                                       dict[str, list[str]],
                                                       dict[str, list[str]] | None],
                                  from_bytes: bool
                                  ) -> None:
    '''
    This tests MWE Rule when using only WILDCARD cases, e.g. `ski_noun *_noun`
    '''
    data, lexicon, pos_mapper = wildcard_data
    tokens, lemmas, pos_tags, expected_ranking_meta_data = data
    
    mwe_rule = MWERule(lexicon, pos_mapper)
    if from_bytes:
        mwe_rule = MWERule.from_bytes(mwe_rule.to_bytes())

    compare_token_ranking_meta_data(expected_ranking_meta_data,
                                    mwe_rule(tokens, lemmas, pos_tags))


def test_to_from_bytes() -> None:
    lexicon = {
        "North_noun East_noun London_*": ['Z1'],
        "North_* East**_noun London_noun": ['Z2'],
        "East_* London_noun": ['Z3'],
        "East_* London_*": ['Z4'],
        "*as*_noun London_*": ['Z5']
    }
    pos_mapper = {'NN': ['noun']}
    mwe_rule = MWERule(lexicon, pos_mapper)
    mwe_rule_from_bytes = MWERule.from_bytes(mwe_rule.to_bytes())

    assert len(mwe_rule_from_bytes.mwe_lexicon_collection) \
        == len(mwe_rule.mwe_lexicon_collection)
    
    assert mwe_rule.mwe_lexicon_collection.pos_mapper \
        == mwe_rule_from_bytes.mwe_lexicon_collection.pos_mapper
    
    assert mwe_rule.mwe_lexicon_collection.meta_data \
        == mwe_rule_from_bytes.mwe_lexicon_collection.meta_data


def test__eq__() -> None:
    lexicon = {
        "North_noun East_noun London_*": ['Z1'],
        "North_* East**_noun London_noun": ['Z2'],
        "East_* London_noun": ['Z3'],
        "East_* London_*": ['Z4'],
        "*as*_noun London_*": ['Z5']
    }
    pos_mapper = {'NN': ['noun']}

    empty_rule = MWERule({}, None)
    assert 1 != empty_rule

    assert empty_rule != MWERule(lexicon, None)
    assert empty_rule != MWERule({}, pos_mapper)
    
    empty_rule = MWERule(lexicon, None)
    assert empty_rule == MWERule(lexicon, None)
    assert empty_rule != MWERule(lexicon, pos_mapper)

    empty_rule = MWERule(lexicon, pos_mapper)
    assert empty_rule == MWERule(lexicon, pos_mapper)


def _mwe_semantic_tags(mwe_rule: MWERule, tokens: list[str], lemmas: list[str],
                       pos_tags: list[str]) -> dict[str, tuple[str, ...]]:
    '''
    Returns a dictionary of the MWE template matched to its semantic tags for
    all MWE matches found by the `mwe_rule`.
    '''
    template_tags: dict[str, tuple[str, ...]] = {}
    for token_ranking_meta_data in mwe_rule(tokens, lemmas, pos_tags):
        for ranking_meta_data in token_ranking_meta_data:
            template_tags[ranking_meta_data.lexicon_entry_match] = ranking_meta_data.semantic_tags
    return template_tags


@pytest.mark.parametrize("mwe_semantic_tags, expected", [
    (['Df'], ('A1',)),
    (['C1/Df'], ('C1/A1',)),
    (['Df++'], ('A1++',)),
    (['Dfc', 'Df/O2'], ('A1c', 'A1/O2')),
])
def test_mwe_rule_default_tags(mwe_semantic_tags: list[str],
                               expected: tuple[str, ...]) -> None:
    single_word_rule = SingleWordRule({'acting|ADJ': ['A1+/Z3', 'B1']}, {})
    mwe_rule = MWERule({'*_ADJ style_NOUN': mwe_semantic_tags},
                       single_word_rule=single_word_rule)
    tokens = ['The', 'acting', 'style']
    pos_tags = ['DET', 'ADJ', 'NOUN']
    token_ranking_meta_data = mwe_rule(tokens, tokens, pos_tags)
    assert [] == token_ranking_meta_data[0]
    for token_index in [1, 2]:
        # A token and lemma match, the lower cased matches also lower case
        # the POS tags and therefore do not match.
        assert 2 == len(token_ranking_meta_data[token_index])
        for ranking_meta_data in token_ranking_meta_data[token_index]:
            assert (1, 3) == (ranking_meta_data.token_match_start_index,
                              ranking_meta_data.token_match_end_index)
            assert expected == ranking_meta_data.semantic_tags


def test_mwe_rule_default_tags_token_position() -> None:
    single_word_rule = SingleWordRule({'the|DET': ['Z5'], 'dark|ADJ': ['W2-']}, {})
    mwe_rule = MWERule({'on_ADP the_DET *_ADJ side_NOUN': ['Df'],
                        'half_DET a*_DET *_NOUN': ['Df']},
                       single_word_rule=single_word_rule)
    tokens = ['on', 'the', 'dark', 'side']
    template_tags = _mwe_semantic_tags(mwe_rule, tokens, tokens,
                                       ['ADP', 'DET', 'ADJ', 'NOUN'])
    assert {'on_ADP the_DET *_ADJ side_NOUN': ('W2',)} == template_tags

    single_word_rule = SingleWordRule({'an|DET': ['Z5'], 'hour|NOUN': ['T1.3']}, {})
    mwe_rule.single_word_rule = single_word_rule
    tokens = ['half', 'an', 'hour']
    template_tags = _mwe_semantic_tags(mwe_rule, tokens, tokens,
                                       ['DET', 'DET', 'NOUN'])
    assert {'half_DET a*_DET *_NOUN': ('T1.3',)} == template_tags


def test_mwe_rule_default_tags_single_word_match_priority() -> None:
    tokens = ['Acting', 'style']
    lemmas = ['act', 'style']
    pos_tags = ['ADJ', 'NOUN']
    mwe_lexicon = {'*_ADJ style_NOUN': ['Df']}

    # POS information is preferred over no POS information, and within those
    # Token < Lemma < Lower cased token < Lower cased lemma.
    single_word_lexicon = {'Acting|ADJ': ['A1'], 'act|ADJ': ['A2'],
                           'acting|ADJ': ['A3'], 'Act|ADJ': ['A4']}
    lemma_lexicon = {'Acting': ['B1']}
    ordered_expected = [('Acting|ADJ', 'A1'), ('act|ADJ', 'A2'),
                        ('acting|ADJ', 'A3')]
    for lexicon_entry, expected_tag in ordered_expected:
        single_word_rule = SingleWordRule(single_word_lexicon, lemma_lexicon)
        mwe_rule = MWERule(mwe_lexicon, single_word_rule=single_word_rule)
        template_tags = _mwe_semantic_tags(mwe_rule, tokens, lemmas, pos_tags)
        assert {'*_ADJ style_NOUN': (expected_tag,)} == template_tags
        del single_word_lexicon[lexicon_entry]

    # With no POS information both `act` (lemma match) and `acting` (lower
    # cased token match) match, of which the lemma match is preferred.
    single_word_rule = SingleWordRule({}, {'act': ['C1'], 'acting': ['C2']})
    mwe_rule = MWERule(mwe_lexicon, single_word_rule=single_word_rule)
    template_tags = _mwe_semantic_tags(mwe_rule, tokens, lemmas, pos_tags)
    assert {'*_ADJ style_NOUN': ('C1',)} == template_tags


def test_mwe_rule_default_tags_uses_single_word_pos_mapper() -> None:
    '''
    The text, MWE lexicon, and single word lexicon all use different POS
    tagsets, `JJ`, `ADJ`, and `adj` respectively. The `Df` tag must be
    resolved by giving the single word rule the text's POS tag, which it maps
    using its own POS mapper, and not the MWE lexicon's POS tag.
    '''
    tokens = ['acting', 'style']
    text_pos_tags = ['JJ', 'NN1']
    mwe_lexicon = {'*_ADJ style_NOUN': ['Df']}
    # Maps from the MWE lexicon's POS tagset to the text's POS tagset.
    mwe_pos_mapper = {'ADJ': ['JJ'], 'NOUN': ['NN1']}
    single_word_lexicon = {'acting|adj': ['A1']}
    # Maps from the text's POS tagset to the single word lexicon's POS tagset.
    single_word_pos_mapper = {'JJ': ['adj']}

    single_word_rule = SingleWordRule(single_word_lexicon, {},
                                      pos_mapper=single_word_pos_mapper)
    mwe_rule = MWERule(mwe_lexicon, pos_mapper=mwe_pos_mapper,
                       single_word_rule=single_word_rule)
    template_tags = _mwe_semantic_tags(mwe_rule, tokens, tokens, text_pos_tags)
    assert {'*_ADJ style_NOUN': ('A1',)} == template_tags

    # Without the single word POS mapper `acting|JJ` is looked up, which is
    # not in the single word lexicon, and so the `Df` tag becomes `Z99`.
    mwe_rule.single_word_rule = SingleWordRule(single_word_lexicon, {})
    template_tags = _mwe_semantic_tags(mwe_rule, tokens, tokens, text_pos_tags)
    assert {'*_ADJ style_NOUN': ('Z99',)} == template_tags


def test_mwe_rule_default_tags_no_single_word_match() -> None:
    mwe_lexicon = {'*_ADJ style_NOUN': ['C1/Df', 'Df+']}
    tokens = ['acting', 'style']
    pos_tags = ['ADJ', 'NOUN']
    expected = {'*_ADJ style_NOUN': ('C1/Z99', 'Z99')}

    single_word_rule = SingleWordRule({'style|NOUN': ['A4.1']}, {})
    mwe_rule = MWERule(mwe_lexicon, single_word_rule=single_word_rule)
    assert expected == _mwe_semantic_tags(mwe_rule, tokens, tokens, pos_tags)

    mwe_rule = MWERule(mwe_lexicon)
    assert expected == _mwe_semantic_tags(mwe_rule, tokens, tokens, pos_tags)


def test_to_from_bytes_single_word_rule() -> None:
    lexicon = {"*_ADJ style_NOUN": ['Df'], "East_* London_*": ['Z4']}
    pos_mapper = {'NN': ['noun']}
    single_word_rule = SingleWordRule({'acting|ADJ': ['A1']}, {'acting': ['A2']},
                                      {'JJ': ['ADJ']})

    mwe_rule = MWERule(lexicon, pos_mapper, single_word_rule)
    mwe_rule_from_bytes = MWERule.from_bytes(mwe_rule.to_bytes())
    assert mwe_rule == mwe_rule_from_bytes
    assert single_word_rule == mwe_rule_from_bytes.single_word_rule

    mwe_rule = MWERule(lexicon, pos_mapper)
    mwe_rule_from_bytes = MWERule.from_bytes(mwe_rule.to_bytes())
    assert mwe_rule == mwe_rule_from_bytes
    assert mwe_rule_from_bytes.single_word_rule is None


def test_from_bytes_legacy_format() -> None:
    '''
    Before the `single_word_rule` was added `MWERule.to_bytes` only serialised
    the `mwe_lexicon_collection`.
    '''
    lexicon = {"*_ADJ style_NOUN": ['Df'], "East_* London_*": ['Z4']}
    pos_mapper = {'NN': ['noun']}
    legacy_bytes = MWELexiconCollection(lexicon, pos_mapper).to_bytes()
    mwe_rule_from_bytes = MWERule.from_bytes(legacy_bytes)
    assert MWERule(lexicon, pos_mapper) == mwe_rule_from_bytes
    assert mwe_rule_from_bytes.single_word_rule is None


def test__eq__single_word_rule() -> None:
    lexicon = {"*_ADJ style_NOUN": ['Df']}
    single_word_rule = SingleWordRule({'acting|ADJ': ['A1']}, {})
    mwe_rule = MWERule(lexicon, None, single_word_rule)
    assert mwe_rule == MWERule(lexicon, None, SingleWordRule({'acting|ADJ': ['A1']}, {}))
    assert mwe_rule != MWERule(lexicon, None)
    assert mwe_rule != MWERule(lexicon, None, SingleWordRule({'acting|ADJ': ['A2']}, {}))


def test_mwe_rule_default_tags_autotag() -> None:
    '''
    Default (`Df`) tags are resolved using `autotag` pattern matches when the
    token has no exact single word lexicon match.
    '''
    mwe_lexicon = {'*_NUM weight_NOUN': ['Df', 'C1/Df+']}
    tokens = ['15kg', 'weight']
    pos_tags = ['NUM', 'NOUN']
    autotag_lexicon = {'*kg|NUM': ['N3.5']}

    single_word_rule = SingleWordRule({}, {}, autotag_lexicon_collection=autotag_lexicon)
    mwe_rule = MWERule(mwe_lexicon, single_word_rule=single_word_rule)
    assert ({'*_NUM weight_NOUN': ('N3.5', 'C1/N3.5+')}
            == _mwe_semantic_tags(mwe_rule, tokens, tokens, pos_tags))

    # An exact single word lexicon match is used instead of an `autotag` match.
    single_word_rule = SingleWordRule({'15kg|NUM': ['N1']}, {},
                                      autotag_lexicon_collection=autotag_lexicon)
    mwe_rule = MWERule(mwe_lexicon, single_word_rule=single_word_rule)
    assert ({'*_NUM weight_NOUN': ('N1', 'C1/N1+')}
            == _mwe_semantic_tags(mwe_rule, tokens, tokens, pos_tags))

    # No exact or `autotag` match, as the POS pattern does not match.
    mwe_lexicon = {'*_ADJ weight_NOUN': ['Df']}
    single_word_rule = SingleWordRule({}, {}, autotag_lexicon_collection=autotag_lexicon)
    mwe_rule = MWERule(mwe_lexicon, single_word_rule=single_word_rule)
    assert ({'*_ADJ weight_NOUN': ('Z99',)}
            == _mwe_semantic_tags(mwe_rule, tokens, tokens, ['ADJ', 'NOUN']))


def test_mwe_rule_mismatched_lengths() -> None:
    '''
    Tests that mismatched `tokens`, `lemmas`, and `pos_tags` lengths raise a
    `ValueError` rather than being silently truncated.
    '''
    rule = MWERule({'ski_noun boot_noun': ['Z2']})
    with pytest.raises(ValueError):
        rule(['ski', 'boot'], ['ski', 'boot'], ['noun'])
