import spacy

from pymusas import lexicon_collection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules import mwe, single_word


TEST_TOKENS = ['Sporting', 'community', 'hack', 'had', '.', '49557282']
TEST_POS = ['NOUN', 'NOUN', 'NOUN', 'DET', 'PUNCT', 'NUM']
TEST_SPACES = [True] * len(TEST_TOKENS)


def test_single_and_mwe_spacy_tagger() -> None:
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

    doc = spacy.tokens.Doc(spacy.vocab.Vocab(), words=TEST_TOKENS,
                           spaces=TEST_SPACES, pos=TEST_POS)
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
