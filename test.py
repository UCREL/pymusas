import spacy

from pymusas.lexicon_collection import LexiconCollection, LexiconEntry
from pymusas.spacy_tagger import create_spacy_rule_based_tagger_component
from pymusas.spacy_lexicon_collection import lexicon_collection
'''
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
'''
# Add the component to the pipeline and configure it
a_collection = lexicon_collection(data={'London|PROPN': ['Z2']}).data
print(a_collection)
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("usas_tagger", last=True, config={'lexicon_lookup':a_collection})
doc = nlp('London is great today')
for token in doc:
    print(f'{token.text} {token._.usas_tags}')