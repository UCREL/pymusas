from pathlib import Path
import pickle
from typing import Callable, Dict, List, Optional, cast

import pytest
import spacy
from spacy import registry
from spacy.lang.en import English
from spacy.language import Language

from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
from pymusas.taggers.rules.single_word import SingleWordRule

from ..utils import remove_extension


def non_standard_config() -> Dict[str, str]:
    return {
        'pymusas_tags_token_attr': 'usas_tags',
        'pymusas_mwe_indexes_attr': 'mwe_indexes',
        'pos_attribute': '_.claws',
        'lemma_attribute': '_.stem'
    }


def create_non_valid_tagger(remove_extension_if_exists: bool = True,
                            pymusas_tags_token_attr: str = 'pymusas_tags',
                            pymusas_mwe_indexes_attr: str = 'pymusas_mwe_indexes'
                            ) -> Language:
    if remove_extension_if_exists:
        remove_extension(pymusas_tags_token_attr)
        remove_extension(pymusas_mwe_indexes_attr)
    nlp = English()
    return nlp


@registry.misc("rules")
def rules() -> List[SingleWordRule]:
    return [SingleWordRule({'': ['']}, {'': ['']})]
    

@registry.misc("rankers")
def rankers() -> ContextualRuleBasedRanker:
    return ContextualRuleBasedRanker(0, 0)


def create_non_valid_no_ranker_tagger(remove_extension_if_exists: bool = True,
                                      pymusas_tags_token_attr: str = 'pymusas_tags',
                                      pymusas_mwe_indexes_attr: str = 'pymusas_mwe_indexes'
                                      ) -> Language:
    if remove_extension_if_exists:
        remove_extension(pymusas_tags_token_attr)
        remove_extension(pymusas_mwe_indexes_attr)
    nlp = English()
    nlp.config["initialize"]["components"]["pymusas_rule_based_tagger"] = {
        "rules": {"@misc": "rules"}
    }
    return nlp


def create_tagger(remove_extension_if_exists: bool = True,
                  pymusas_tags_token_attr: str = 'pymusas_tags',
                  pymusas_mwe_indexes_attr: str = 'pymusas_mwe_indexes'
                  ) -> Language:
    if remove_extension_if_exists:
        remove_extension(pymusas_tags_token_attr)
        remove_extension(pymusas_mwe_indexes_attr)
    nlp = English()
    nlp.config["initialize"]["components"]["pymusas_rule_based_tagger"] = {
        "rules": {"@misc": "rules"},
        "ranker": {"@misc": "rankers"},
        "default_punctuation_tags": ['grammar'],
        "default_number_tags": ['digits']
    }
    return nlp


@pytest.mark.parametrize("name", [None, 'test'])
@pytest.mark.parametrize("config", [{}, non_standard_config()])
@pytest.mark.parametrize("nlp_callable", [create_non_valid_tagger,
                                          create_tagger])
def test_rule_based_tagger__init__(nlp_callable: Callable[[bool, str, str], Language],
                                   config: Dict[str, str],
                                   name: Optional[str]
                                   ) -> None:
    nlp = nlp_callable(True,
                       config.get("pymusas_tags_token_attr", "pymusas_tags"),
                       config.get("pymusas_mwe_indexes_attr", "pymusas_mwe_indexes"))
    tagger = cast(RuleBasedTagger,
                  nlp.add_pipe('pymusas_rule_based_tagger', name=name,
                               config=config))
    
    expected_name = 'pymusas_rule_based_tagger' if name is None else name
    assert expected_name == tagger.name
    
    assert tagger.rules is None
    assert tagger.ranker is None
    assert set(['punc']) == tagger.default_punctuation_tags
    assert set(['num']) == tagger.default_number_tags
    pos_attribute = 'pos_' if not config else config['pos_attribute']
    lemma_attribute = 'lemma_' if not config else config['lemma_attribute']
    pymusas_tags_token_attr = 'pymusas_tags' \
        if not config else config['pymusas_tags_token_attr']
    pymusas_mwe_indexes_attr = 'pymusas_mwe_indexes' \
        if not config else config['pymusas_mwe_indexes_attr']
    
    assert pos_attribute == tagger.pos_attribute
    assert lemma_attribute == tagger.lemma_attribute
    assert pymusas_tags_token_attr == tagger.pymusas_tags_token_attr
    assert pymusas_mwe_indexes_attr == tagger.pymusas_mwe_indexes_attr

    factory_meta_data = nlp.get_pipe_meta(expected_name)
    assert set(factory_meta_data.requires) == set(['token.lemma',
                                                   'token.pos'])
    assert set(factory_meta_data.assigns) == set(['token._.pymusas_tags',
                                                  'token._.pymusas_mwe_indexes'])


def test_rule_based_tagger_token_extension_warning() -> None:
    '''
    A token extension warning should appear if two or more
    `pymusas_rule_based_tagger`s are added to a spaCy pipeline, as they will use
    the same Token extensions.
    '''
    nlp = create_tagger(False)
    nlp.add_pipe('pymusas_rule_based_tagger', name='test_1')
    with pytest.warns(UserWarning):
        nlp.add_pipe('pymusas_rule_based_tagger', name='test_2')
    remove_extension('pymusas_tags')
    remove_extension('pymusas_mwe_indexes')

    # If we use a different `pymusas_tags_token_attr` and
    # `pymusas_mwe_indexes_attr` in the config the warning should not be raised.
    nlp = create_tagger(False)
    nlp.add_pipe('pymusas_rule_based_tagger', name='test_1')
    nlp.add_pipe('pymusas_rule_based_tagger', name='test_2',
                 config={'pymusas_tags_token_attr': 'usas_tags',
                         'pymusas_mwe_indexes_attr': 'mwe_indexes'})
    remove_extension('pymusas_tags')
    remove_extension('pymusas_mwe_indexes')
    remove_extension('usas_tags')
    remove_extension('mwe_indexes')


def test_rule_based_tagger_initializer() -> None:
    for non_valid_tagger in [create_non_valid_tagger(),
                             create_non_valid_no_ranker_tagger()]:
        with pytest.raises(ValueError):
            non_valid_tagger.add_pipe('pymusas_rule_based_tagger')
            non_valid_tagger.initialize()
    
    nlp = create_tagger()
    tagger = cast(RuleBasedTagger, nlp.add_pipe('pymusas_rule_based_tagger'))
    assert set(['num']) == tagger.default_number_tags
    assert set(['punc']) == tagger.default_punctuation_tags
    nlp.initialize()
    assert tagger.rules is not None
    assert tagger.ranker is not None
    assert isinstance(tagger.rules[0], SingleWordRule)
    assert isinstance(tagger.ranker, ContextualRuleBasedRanker)
    assert set(['digits']) == tagger.default_number_tags
    assert set(['grammar']) == tagger.default_punctuation_tags


def compare_initializer_taggers(tagger_1: RuleBasedTagger,
                                tagger_2: RuleBasedTagger,
                                are_different: bool) -> None:
    assert are_different == (tagger_1.rules != tagger_2.rules)
    assert are_different == (tagger_1.ranker != tagger_2.ranker)
    assert are_different == (tagger_1.default_punctuation_tags
                             != tagger_2.default_punctuation_tags)
    assert are_different == (tagger_1.default_number_tags
                             != tagger_2.default_number_tags)


def test_to_from_bytes() -> None:
    nlp = create_tagger()
    initialized_tagger = cast(RuleBasedTagger,
                              nlp.add_pipe('pymusas_rule_based_tagger'))
    nlp.initialize()

    empty_nlp = create_non_valid_tagger()
    empty_tagger = cast(RuleBasedTagger,
                        empty_nlp.add_pipe('pymusas_rule_based_tagger'))
    compare_initializer_taggers(empty_tagger, initialized_tagger, True)

    empty_nlp = create_non_valid_tagger()
    empty_nlp.add_pipe('pymusas_rule_based_tagger')
    empty_nlp.from_bytes(nlp.to_bytes())
    empty_tagger = cast(RuleBasedTagger,
                        empty_nlp.get_pipe('pymusas_rule_based_tagger'))
    compare_initializer_taggers(empty_tagger, initialized_tagger, False)
    empty_tagger._validate()

    # Test that it raises a ValueError if saving a model that cannot be
    # validated
    empty_nlp = create_non_valid_tagger()
    empty_nlp.add_pipe('pymusas_rule_based_tagger')
    with pytest.raises(ValueError):
        empty_nlp.to_bytes()


def test_to_from_disk(tmp_path: Path) -> None:
    tmp_folder_1 = Path(tmp_path, 'folder_1')
    nlp = create_tagger()
    initialized_tagger = cast(RuleBasedTagger,
                              nlp.add_pipe('pymusas_rule_based_tagger'))
    nlp.initialize()
    
    nlp.to_disk(tmp_folder_1)
    nlp_2 = spacy.load(tmp_folder_1)
    loaded_tagger = cast(RuleBasedTagger,
                         nlp_2.get_pipe('pymusas_rule_based_tagger'))
    compare_initializer_taggers(initialized_tagger, loaded_tagger, False)
    loaded_tagger._validate()

    # Test that it raises a ValueError if saving a model that cannot be
    # validated
    empty_nlp = create_non_valid_tagger()
    empty_nlp.add_pipe('pymusas_rule_based_tagger')
    with pytest.raises(ValueError):
        tmp_folder_2 = Path(tmp_path, 'folder_2')
        empty_nlp.to_disk(tmp_folder_2)


def test_can_pickle() -> None:
    nlp = create_tagger()
    initialized_tagger = cast(RuleBasedTagger,
                              nlp.add_pipe('pymusas_rule_based_tagger'))
    nlp.initialize()
    
    pickle_tagger = cast(RuleBasedTagger,
                         pickle.loads(pickle.dumps(initialized_tagger)))
    compare_initializer_taggers(initialized_tagger, pickle_tagger, False)
    pickle_tagger._validate()
