from collections.abc import Iterable, Callable
from typing import Optional

from spacy.training import Example
from spacy.language import Language

from .config import LANG_LEXICON_RESOUCRE_MAPPER
from .lexicon_collection import LexiconCollection

class SpacyRuleBasedTagger:

    def __init__(self, lexicon_lookup: Optional[LexiconCollection] = None, 
                 lexicon_lemma_lookup: Optional[LexiconCollection] = None
                 ) -> None:
        if lexicon_lookup is None:
            self.lexicon_lookup: LexiconCollection = LexiconCollection()
        if lexicon_lemma_lookup is None:
            self.lexicon_lemma_lookup: LexiconCollection = LexiconCollection()

    def __call__(self, doc):
        for token in doc:
            # Overwrite the token.norm_ if there's an entry in the data
            token.norm_ = self.norm_table.get(token.text, token.norm_)
        return doc

    def initialize(self, get_examples: Optional[Callable[[], Iterable[Example]]] = None, 
                   nlp: Optional[Language] = None,
                   lexicon_lookup_data: Optional[LexiconCollection] = None,
                   lexicon_lemma_lookup_data: Optional[LexiconCollection] = None
                   ) -> None:
        
        any_data = lambda: any([lexicon_lookup_data, lexicon_lemma_lookup_data])
        if not any_data() and nlp is not None:
            nlp_language = nlp.lang
            if nlp_language in LANG_LEXICON_RESOUCRE_MAPPER:
                lang_lexicon_info = LANG_LEXICON_RESOUCRE_MAPPER[nlp_language]
                lexicon_lookup_data = LexiconCollection.from_tsv(lang_lexicon_info['lexicon'], include_pos=True)
                lexicon_lookup_data = LexiconCollection.from_tsv(lang_lexicon_info['lexicon_lemma'], include_pos=False)
        
        if any_data:
            self.lexicon_lookup = lexicon_lookup_data
            self.lexicon_lemma_lookup = lexicon_lemma_lookup_data
        else:
            error_msg = ('Missing data for initialisation. No data has '
                         'been explicitly passed.')
            if nlp is not None:
                supported_languages = '\n'.join(LANG_LEXICON_RESOUCRE_MAPPER.keys())
                error_msg += (' In addition the Spacy language you are using '
                              'is not supported by our list of pre-complied '
                              f'lexicons:\n{supported_languages}')
            raise ValueError(error_msg)

@Language.factory("usas_tagger")
def create_spacy_rule_based_tagger_component(nlp: Language, name: str, 
                                             lexicon_lookup: LexiconCollection, 
                                             lexicon_lemma_lookup: LexiconCollection):
    return SpacyRuleBasedTagger(lexicon_lookup, lexicon_lemma_lookup)