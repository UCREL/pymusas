import spacy


def test_spacy_factories() -> None:
    nlp = spacy.blank("en")
    _ = nlp.add_pipe("pymusas_rule_based_tagger")
