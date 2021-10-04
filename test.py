from __future__ import annotations
from spacy.language import Language
from spacy.tokens import Doc
from spacy.matcher import PhraseMatcher
import spacy

DICTIONARY = {"lol": "laughing out loud", "brb": "be right back"}
DICTIONARY.update({value: key for key, value in DICTIONARY.items()})

@Language.factory("ucrel")
def create_spacy_rule_based_tagger_component(nlp: Language, name: str):
    return SpacyRuleBasedTagger(nlp)

class SpacyRuleBasedTagger:
    def __init__(self, nlp: Language):
        pass

# Add the component to the pipeline and configure it
nlp = spacy.blank("en")
nlp.add_pipe("ucrel")