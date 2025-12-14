import spacy


def test_spacy_factories_rule_based_tagger() -> None:
    nlp = spacy.blank("en")
    _ = nlp.add_pipe("pymusas_rule_based_tagger")


def test_spacy_factories_neural_tagger() -> None:
    nlp = spacy.blank("en")
    _ = nlp.add_pipe("pymusas_neural_tagger")


def test_spacy_factories_hybrid_tagger() -> None:
    nlp = spacy.blank("en")
    _ = nlp.add_pipe("pymusas_hybrid_tagger")
