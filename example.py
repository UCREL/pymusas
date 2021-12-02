from typing import cast
from pathlib import Path

import spacy

from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger, make_usas_rule_based_tagger # noqa
from pymusas.lexicon_collection import LexiconCollection
from pymusas.pos_mapper import UD_TO_USAS_CORE

# Before running this enure that you have downloaded the spaCy `fr_core_news_sm`
# model, this can be done using the following command:
# `python -m spacy download fr_core_news_sm`
nlp = spacy.load("fr_core_news_sm")

usas_french_lexicon = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.tsv'
french_lexicon_lookup = LexiconCollection.from_tsv(usas_french_lexicon, include_pos=True)
french_lemma_lexicon_lookup = LexiconCollection.from_tsv(usas_french_lexicon, include_pos=False)

usas_tagger = cast(USASRuleBasedTagger, nlp.add_pipe('usas_tagger'))
usas_tagger.lexicon_lookup = french_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = french_lemma_lexicon_lookup
usas_tagger.pos_mapper = UD_TO_USAS_CORE
nlp.analyze_pipes(pretty=True)
# Taken from the French Wikipedia page of the Marvel Cinematic Universe
# https://fr.wikipedia.org/wiki/Univers_cin%C3%A9matographique_Marvel
example_data = '''
L'univers cinématographique Marvel (en anglais : Marvel Cinematic Universe,
parfois abrégé en MCU) est une franchise cinématographique produite par Marvel
Studios mettant en scène des personnages de bandes dessinées de l'éditeur
Marvel Comics, imaginée et mise en route par Kevin Feige à partir de 2008.
Marvel Studios est la propriété de The Walt Disney Company.
'''

for token in nlp(example_data):
    print(f'{token.text} {token._.usas_tags}')

# Save to a directory
example_dir = Path(__file__, '..', 'spacy_data_dir').resolve()
example_dir.mkdir(exist_ok=True)
nlp.to_disk(example_dir)


# Load and run from that directory
usas_nlp = spacy.load(example_dir)
print(usas_nlp.pipe_names)
for token in usas_nlp(example_data):
    print(f'{token.text} {token._.usas_tags}')
