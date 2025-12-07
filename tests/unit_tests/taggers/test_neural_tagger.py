import pytest

from pymusas.taggers.neural import NeuralTagger


TEST_TOKENS: list[str] = ['Sporting', 'community', 'hack', 'had', '.', '49557282']
EXPECTED_TAG_OUTPUT: list[list[str]] = [
    ['K5.1', 'G2.2', 'A6.2', 'S2', 'A5.4'],
    ['S5', 'S1.1.1', 'S2', 'K1', 'O2'],
    ['Y2', 'A1.1.1', 'O2', 'S2', 'L2'],
    ['S4', 'A2.2', 'A9', 'Z5', 'S6'],
    ['S2', 'N3.2', 'Z5', 'T1.2', 'O3'],
    ['N1', 'N3.2', 'T1.2', 'T1.3', 'T3']
]
EXPECTED_TAG_INDICIES: list[list[tuple[int, int]]] = [
    [(0, 1)], [(1, 2)], [(2, 3)], [(3, 4)], [(4, 5)], [(5, 6)]
]


def test_neural_tagger__init__() -> None:
    tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
    # Tests that the model is in eval mode
    assert not tagger.wsd_model.training
    assert tagger.device.type == "cpu"
    assert tagger.tokenizer.add_prefix_space

    tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
                          device="meta",
                          tokenizer_kwargs={"add_prefix_space": False})
    # Tests that the model is in eval mode
    assert not tagger.wsd_model.training
    # Test that we can change device
    assert tagger.device.type == "meta"
    # Test that we can change the tokenizer kwargs
    assert not tagger.tokenizer.add_prefix_space

    with pytest.raises(ValueError):
        NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM", top_n=0)
    with pytest.raises(ValueError):
        NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM", top_n=-2)


@pytest.mark.parametrize("top_n", [1, 2, 3, 4, 5])
def test_neural_tagger__call__(top_n: int) -> None:

    tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM", device="cpu", top_n=top_n)
    for index, tags_and_indicies in enumerate(tagger(TEST_TOKENS)):
        tags, tag_indicies = tags_and_indicies
        assert EXPECTED_TAG_OUTPUT[index][:top_n] == tags
        assert EXPECTED_TAG_INDICIES[index] == tag_indicies

    # Test empty whitespace tokens
    for index, tags_and_indicies in enumerate(tagger(["", "  \n ", " \t "])):
        tags, tag_indicies = tags_and_indicies
        assert ["Z9"] == tags
        assert [(index, index + 1)] == tag_indicies
