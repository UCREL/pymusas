from pathlib import Path
from typing import cast

import pytest
import spacy
from spacy.lang.en import English
from spacy.language import Language
from spacy.tokens import Doc
from spacy.vocab import Vocab
import torch
from transformers import AutoTokenizer, PreTrainedTokenizerBase
from wsd_torch_models.bem import BEM

from pymusas.spacy_api.taggers.neural import NeuralTagger
from pymusas.spacy_api.utils import remove_custom_token_extension as remove_extension

from ...taggers.test_neural_tagger import EXPECTED_TAG_INDICIES, EXPECTED_TAG_OUTPUT, TEST_TOKENS
from ..utils import compare_output


def create_empty_tagger() -> Language:
    remove_extension('pymusas_tags')
    remove_extension('pymusas_mwe_indexes')
    return English()


def create_tagger() -> Language:
    remove_extension('pymusas_tags')
    remove_extension('pymusas_mwe_indexes')
    nlp = English()
    nlp.config["initialize"]["components"]["pymusas_neural_tagger"] = {
        "pretrained_model_name_or_path": "ucrelnlp/PyMUSAS-Neural-English-Small-BEM"
    }
    return nlp


def test_neural_tagger_token_extension_warning() -> None:
    '''
    A token extension warning should appear if two or more
    `pymusas_neural_tagger`s are added to a spaCy pipeline, as they will use
    the same Token extensions.
    '''
    nlp = create_tagger()
    nlp.add_pipe('pymusas_neural_tagger', name='test_1')
    with pytest.warns(UserWarning):
        nlp.add_pipe('pymusas_neural_tagger', name='test_2')
    remove_extension('pymusas_tags')
    remove_extension('pymusas_mwe_indexes')

    # If we use a different `pymusas_tags_token_attr` and
    # `pymusas_mwe_indexes_attr` in the config the warning should not be raised.
    nlp = create_tagger()
    nlp.add_pipe('pymusas_neural_tagger', name='test_1')
    nlp.add_pipe('pymusas_neural_tagger', name='test_2',
                 config={'pymusas_tags_token_attr': 'usas_tags',
                         'pymusas_mwe_indexes_attr': 'mwe_indexes'})
    remove_extension('pymusas_tags')
    remove_extension('pymusas_mwe_indexes')
    remove_extension('usas_tags')
    remove_extension('mwe_indexes')


def test_to_from_disk(tmp_path: Path) -> None:
    nlp = create_tagger()

    initialized_tagger = cast(NeuralTagger,
                              nlp.add_pipe('pymusas_neural_tagger'))
    nlp.initialize()

    empty_nlp = create_empty_tagger()
    empty_tagger = cast(NeuralTagger,
                        empty_nlp.add_pipe('pymusas_neural_tagger'))
    assert empty_tagger.wsd_model is None
    assert isinstance(initialized_tagger.wsd_model, BEM)
    assert empty_tagger.tokenizer is None
    assert isinstance(initialized_tagger.tokenizer, PreTrainedTokenizerBase)
    with pytest.raises(ValueError):
        empty_tagger._validate()

    nlp.to_disk(path=tmp_path / "test_1")
    empty_nlp = spacy.load(tmp_path / "test_1")
    empty_tagger = cast(NeuralTagger,
                        empty_nlp.get_pipe('pymusas_neural_tagger'))
    assert isinstance(empty_tagger.wsd_model, BEM)
    assert isinstance(empty_tagger.tokenizer, PreTrainedTokenizerBase)
    assert empty_tagger._tokenizer_kwargs is None
    empty_tagger._validate()

    assert initialized_tagger.tokenizer.add_prefix_space

    # Test that if we change the tokenizer_kwargs the model is
    # loaded with these changed tokenizer kwargs, by default the
    # add_prefix_space is True here we will load it with False
    # This is more of a side affect in that the tokenizer should be saved with
    # these kwargs.
    nlp = create_tagger()

    config = {
        'tokenizer_kwargs': {'add_prefix_space': False}
    }
    initialized_tagger = cast(NeuralTagger,
                              nlp.add_pipe('pymusas_neural_tagger', config=config))
    nlp.initialize()
    nlp.to_disk(path=tmp_path / "test_2")

    empty_nlp = spacy.load(tmp_path / "test_2")
    empty_tagger = cast(NeuralTagger,
                        empty_nlp.get_pipe('pymusas_neural_tagger'))
    assert isinstance(empty_tagger.wsd_model, BEM)
    assert isinstance(empty_tagger.tokenizer, PreTrainedTokenizerBase)
    assert empty_tagger.tokenizer.add_prefix_space == config["tokenizer_kwargs"]["add_prefix_space"]
    empty_tagger._validate()

    # Want to ensure that when loading a model from disk that it loads the model
    # to the correct device.
    empty_nlp = spacy.load(tmp_path / "test_2", config={"components.pymusas_neural_tagger.device": "meta"})
    empty_tagger = cast(NeuralTagger,
                        empty_nlp.get_pipe('pymusas_neural_tagger'))
    assert isinstance(empty_tagger.wsd_model, BEM)
    assert isinstance(empty_tagger.tokenizer, PreTrainedTokenizerBase)
    assert empty_tagger.tokenizer.add_prefix_space == config["tokenizer_kwargs"]["add_prefix_space"]
    assert empty_tagger.device.type == "meta"
    assert empty_tagger.wsd_model.base_model.device.type == "meta"
    empty_tagger._validate()


@pytest.mark.parametrize("pymusas_tags_token_attr,pymusas_mwe_indexes_attr",
                         [('pymusas_tags', 'pymusas_mwe_indexes'),
                          ('pym_tags', 'mwe_indexes')])
@pytest.mark.parametrize("top_n", [1, 2, 3, 4, 5])
def test__call__(top_n: int,
                 pymusas_tags_token_attr: str,
                 pymusas_mwe_indexes_attr: str) -> None:

    config = {
        "top_n": top_n,
        "pymusas_tags_token_attr": pymusas_tags_token_attr,
        "pymusas_mwe_indexes_attr": pymusas_mwe_indexes_attr,
        "tokenizer_kwargs": {"add_prefix_space": True}
    }
    nlp = English()
    tagger = cast(NeuralTagger,
                  nlp.add_pipe('pymusas_neural_tagger',
                               config=config))
    tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")

    test_doc = Doc(Vocab(), words=TEST_TOKENS, spaces=[True] * len(TEST_TOKENS))
    output_doc = tagger(test_doc)
    compare_output(list(zip(EXPECTED_TAG_OUTPUT, EXPECTED_TAG_INDICIES)),
                   output_doc,
                   pymusas_tags_token_attr,
                   pymusas_mwe_indexes_attr,
                   top_n=top_n)

    # Test empty whitespace tokens
    number_whitespace_tokens = 3
    expected_empty_tags = [['Z9']] * number_whitespace_tokens
    expected_tag_indicies = [[(0, 1)], [(1, 2)], [(2, 3)]]
    test_doc = Doc(Vocab(),
                   words=["\n", "\t", "\n"],
                   spaces=[True] * number_whitespace_tokens)
    output_doc = tagger(test_doc)
    compare_output(list(zip(expected_empty_tags, expected_tag_indicies)),
                   output_doc,
                   pymusas_tags_token_attr,
                   pymusas_mwe_indexes_attr,
                   top_n=None)


def test__init__() -> None:
    tagger = NeuralTagger()
    assert tagger.name == 'pymusas_neural_tagger'
    assert tagger._pymusas_tags_token_attr == 'pymusas_tags'
    assert tagger._pymusas_mwe_indexes_attr == 'pymusas_mwe_indexes'
    assert tagger.top_n == 5
    assert tagger._tokenizer_kwargs is None
    assert isinstance(tagger.device, torch.device)
    assert tagger.device.type == "cpu"

    test_doc = Doc(Vocab(), words=TEST_TOKENS, spaces=[True] * len(TEST_TOKENS))
    with pytest.raises(ValueError):
        tagger.initialize()
    with pytest.raises(ValueError):
        tagger(test_doc)

    tagger.wsd_model = BEM.from_pretrained("ucrelnlp/PyMUSAS-Neural-English-Small-BEM")

    with pytest.raises(ValueError):
        tagger.initialize()
    with pytest.raises(ValueError):
        tagger(test_doc)
 
    tagger.tokenizer = cast(PreTrainedTokenizerBase,
                            AutoTokenizer.from_pretrained("ucrelnlp/PyMUSAS-Neural-English-Small-BEM"))  # type: ignore[no-untyped-call]
    tagger.initialize()
    assert tagger.wsd_model.base_model.device.type == "cpu"
    assert tagger.device.type == "cpu"

    # Testing valid values of top-n
    with pytest.raises(ValueError):
        NeuralTagger(top_n=0)
    NeuralTagger(top_n=-1)
    with pytest.raises(ValueError):
        NeuralTagger(top_n=-2)

    # Testing with a non-default device
    tagger = NeuralTagger(device="meta")
    assert tagger.device.type == "meta"
    tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
    tagger_wsd_model = cast(BEM, tagger.wsd_model)
    assert tagger_wsd_model.base_model.device.type == "meta"

    # Testing that validate will move the wsd_model to the correct device
    tagger = NeuralTagger(device="cpu")
    tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
    tagger_wsd_model = cast(BEM, tagger.wsd_model)
    assert tagger_wsd_model.base_model.device.type == "cpu"
    tagger.device = torch.device("meta")
    tagger._validate()
    assert tagger_wsd_model.base_model.device.type == "meta"
