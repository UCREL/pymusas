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
EXPECTED_TAG_INDICIES: list[tuple[int,int]] = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)
]


def test_neural_tagger__call__() -> None:

    tagger = NeuralTagger()
    for index, tags_and_indicies in enumerate(tagger(TEST_TOKENS)):
        tags, tag_indicies = tags_and_indicies
        assert EXPECTED_TAG_OUTPUT[index] == tags
        assert EXPECTED_TAG_INDICIES[index] == tag_indicies

    # Test empty whitespace tokens
    for tags, tag_indicies in enumerate(tagger(["", "   ", " "])):
        assert ["Z9"] == tags
        assert [(index, index + 1)] == tag_indicies
