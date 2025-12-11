import pytest
import spacy

from pymusas import lexicon_collection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules import mwe, single_word
from pymusas.utils import NEURAL_EXTRA_PACKAGES, are_packages_installed


TEST_TOKENS = ['Sporting', 'community', 'hack', 'had', '.', '49557282']
TEST_POS = ['NOUN', 'NOUN', 'NOUN', 'DET', 'PUNCT', 'NUM']
TEST_SPACES = [True] * len(TEST_TOKENS)

EXPECTED_NEURAL_TAG_OUTPUT: list[list[str]] = [
    ['K5.1', 'G2.2', 'A6.2', 'S2', 'A5.4'],
    ['S5', 'S1.1.1', 'S2', 'K1', 'O2'],
    ['Y2', 'A1.1.1', 'O2', 'S2', 'L2'],
    ['S4', 'A2.2', 'A9', 'Z5', 'S6'],
    ['S2', 'N3.2', 'Z5', 'T1.2', 'O3'],
    ['N1', 'N3.2', 'T1.2', 'T1.3', 'T3']
]

def cuda_available() -> bool:
    """
    Check if CUDA is available.
    
    # Returns

    `bool`
    """
    try:
        import torch
        return torch.cuda.is_available()
    except:
        return False


def test_rule_base_single_and_mwe_spacy_tagger() -> None:
    """
    Based off the PyMUSAS English MWE spaCy model test, this tests the spaCy
    API rule based tagger with both single and mwe English lexicons.

    Reference:
    https://github.com/UCREL/pymusas-models/blob/
    90918461322281aa89e659c252c2999194bd03ab/
    model_function_tests/en/test_rule_based_tagger.py#L29C1-L47C83
    """
    nlp = spacy.blank('en')
    en_single_lexicon_url = ("https://raw.githubusercontent.com/UCREL/Multilingual-USAS/"
                             "7ccc8baaea36f3fd249e77671db5638c1cba6136/English/semantic_lexicon_en.tsv")
    en_mwe_lexicon_url = ("https://raw.githubusercontent.com/UCREL/Multilingual-USAS/"
                          "7ccc8baaea36f3fd249e77671db5638c1cba6136/English/mwe-en.tsv")
    single_lexicon = lexicon_collection.LexiconCollection.from_tsv(en_single_lexicon_url, include_pos=True)
    single_lemma_lexicon = lexicon_collection.LexiconCollection.from_tsv(en_single_lexicon_url, include_pos=False)
    mwe_lexicon = lexicon_collection.MWELexiconCollection.from_tsv(en_mwe_lexicon_url)

    single_rule = single_word.SingleWordRule(single_lexicon, single_lemma_lexicon,
                                             pos_mapper=None)
    mwe_rule = mwe.MWERule(mwe_lexicon, pos_mapper=None)

    rules = [single_rule, mwe_rule]
    ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
    tagger = nlp.add_pipe('pymusas_rule_based_tagger')
    tagger.rules = rules  # type: ignore
    tagger.ranker = ranker  # type: ignore
    tagger.default_punctuation_tags = set(['PUNCT'])  # type: ignore
    tagger.default_number_tags = set(['NUM'])  # type: ignore

    doc = spacy.tokens.Doc(spacy.vocab.Vocab(),
                           words=TEST_TOKENS,
                           spaces=TEST_SPACES,
                           pos=TEST_POS)
    output = nlp(doc)
    expected_output = [
        ['Df/S5+c'],
        ['Df/S5+c'],
        ['Q4.2/S2mf', 'Y2', 'K5.1'],
        ['A9+', 'Z5', 'A2.2', 'S4'],
        ['PUNCT'],
        ['N1']
    ]

    assert len(expected_output) == len(output)
    for token_index, token in enumerate(output):
        assert expected_output[token_index] == token._.pymusas_tags
        if token_index == 0 or token_index == 1:
            assert [(0, 2)] == token._.pymusas_mwe_indexes
        else:
            assert [(token_index, token_index + 1)] == token._.pymusas_mwe_indexes


@pytest.mark.parametrize("with_spacy_gpu", [True, False])
@pytest.mark.parametrize("device", ["cpu", "cuda"])
@pytest.mark.parametrize("with_gpu", [True, False])
def test_neural_spacy_tagger(with_gpu: bool, device: str, with_spacy_gpu: bool) -> None:
    """
    Test the spaCy neural tagger.
    """
    
    if not cuda_available() and (with_gpu or device == "cuda"):
        pytest.skip("CUDA not available")

    if cuda_available():
        # GPU should work with or without spacy gpu enabled
        if with_spacy_gpu:
            spacy.prefer_gpu()

    nlp = spacy.blank('en')
    config = {
        "top_n": 5,
        "tokenizer_kwargs": {"add_prefix_space": True},
        "device": device
    }
    if not are_packages_installed(NEURAL_EXTRA_PACKAGES):
        with pytest.raises(ImportError):
            nlp.add_pipe('pymusas_neural_tagger')
    else:
        tagger = nlp.add_pipe('pymusas_neural_tagger', config=config)
        tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")  # type: ignore[attr-defined]
        output_doc = nlp(" ".join(TEST_TOKENS))
        assert len(output_doc) == len(TEST_TOKENS)
        for token_index, token in enumerate(output_doc):
            assert EXPECTED_NEURAL_TAG_OUTPUT[token_index] == token._.pymusas_tags
            assert [(token_index, token_index + 1)] == token._.pymusas_mwe_indexes


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_neural_tagger(device: str) -> None:
    """
    Test the neural tagger.
    """
    if not cuda_available() and device == "cuda":
        pytest.skip("CUDA not available")

    if not are_packages_installed(NEURAL_EXTRA_PACKAGES):
        with pytest.raises(ImportError):
            from pymusas.taggers.neural import NeuralTagger
    else:
        from pymusas.taggers.neural import NeuralTagger
        tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
                              top_n=5,
                              tokenizer_kwargs={"add_prefix_space": True},
                              device=device)
        output_tag_indicies = tagger(TEST_TOKENS)
        assert len(output_tag_indicies) == len(TEST_TOKENS)
        for token_index, tag_indicies in enumerate(output_tag_indicies):
            tags = tag_indicies[0]
            indicies = tag_indicies[1]
            assert EXPECTED_NEURAL_TAG_OUTPUT[token_index] == tags
            assert [(token_index, token_index + 1)] == indicies


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_hybrid_tagger(device: str) -> None:
    """
    Test the hybrid tagger.
    """
    if not cuda_available() and device == "cuda":
        pytest.skip("CUDA not available")

    if not are_packages_installed(NEURAL_EXTRA_PACKAGES):
        with pytest.raises(ImportError):
            from pymusas.taggers.hybrid import HybridTagger
    else:
        from pymusas.taggers.hybrid import HybridTagger
        from pymusas.taggers.neural import NeuralTagger
        en_single_lexicon_url = ("https://raw.githubusercontent.com/UCREL/Multilingual-USAS/"
                                 "7ccc8baaea36f3fd249e77671db5638c1cba6136/English/semantic_lexicon_en.tsv")
        en_mwe_lexicon_url = ("https://raw.githubusercontent.com/UCREL/Multilingual-USAS/"
                              "7ccc8baaea36f3fd249e77671db5638c1cba6136/English/mwe-en.tsv")
        single_lexicon = lexicon_collection.LexiconCollection.from_tsv(en_single_lexicon_url, include_pos=True)
        single_lemma_lexicon = lexicon_collection.LexiconCollection.from_tsv(en_single_lexicon_url, include_pos=False)
        mwe_lexicon = lexicon_collection.MWELexiconCollection.from_tsv(en_mwe_lexicon_url)

        single_rule = single_word.SingleWordRule(single_lexicon, single_lemma_lexicon,
                                                 pos_mapper=None)
        mwe_rule = mwe.MWERule(mwe_lexicon, pos_mapper=None)

        rules = [single_rule, mwe_rule]
        ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
        neural_tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
                                     top_n=5,
                                     tokenizer_kwargs={"add_prefix_space": True},
                                     device=device)
        tagger = HybridTagger(rules, ranker, neural_tagger, set(), set())
        output_tag_indicies = tagger(tokens=TEST_TOKENS, lemmas=TEST_TOKENS, pos_tags=TEST_POS)
        assert len(output_tag_indicies) == len(TEST_TOKENS)

        expected_output = [
            ['Df/S5+c'],
            ['Df/S5+c'],
            ['Q4.2/S2mf', 'Y2', 'K5.1'],
            ['A9+', 'Z5', 'A2.2', 'S4'],
            ['S2', 'N3.2', 'Z5', 'T1.2', 'O3'],
            ['N1', 'N3.2', 'T1.2', 'T1.3', 'T3']
        ]
        
        for token_index, tag_indicies in enumerate(output_tag_indicies):
            tags = tag_indicies[0]
            indicies = tag_indicies[1]
            assert expected_output[token_index] == tags
            if token_index == 0 or token_index == 1:
                assert [(0, 2)] == indicies
            else:
                assert [(token_index, token_index + 1)] == indicies
