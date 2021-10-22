from typing import Callable, Dict, Iterable, List, Optional

from spacy.language import Language
from spacy.tokens import Doc, Token
from spacy.training import Example

from ..taggers.rule_based import _tag_token
from ..config import LANG_LEXICON_RESOUCRE_MAPPER
from ..lexicon_collection import LexiconCollection


class RuleBasedTagger:

    def __init__(self, nlp: Language,
                 lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                 lexicon_lemma_lookup: Optional[Dict[str, List[str]]] = None,
                 usas_tags_token_attr: str = 'usas_tags'
                 ) -> None:

        self.lexicon_lookup: Dict[str, List[str]] = dict()
        self.lexicon_lemma_lookup: Dict[str, List[str]] = dict()
        if lexicon_lookup is not None:
            self.lexicon_lookup = lexicon_lookup
        if lexicon_lemma_lookup is not None:
            self.lexicon_lemma_lookup = lexicon_lemma_lookup

        self.usas_tags_token_attr = usas_tags_token_attr
        Token.set_extension(self.usas_tags_token_attr, default=None)

    def __call__(self, doc: Doc) -> Doc:
        for token in doc:
            text = token.text
            lemma = token.lemma_
            pos = token.pos_
            semantic_tags = _tag_token(text, lemma, pos,
                                       self.lexicon_lookup,
                                       self.lexicon_lemma_lookup)
            setattr(token._, self.usas_tags_token_attr, semantic_tags)
        return doc

    def initialize(self, get_examples: Optional[Callable[[], Iterable[Example]]] = None,
                   nlp: Optional[Language] = None,
                   lexicon_lookup_data: Optional[Dict[str, List[str]]] = None,
                   lexicon_lemma_lookup_data: Optional[Dict[str, List[str]]] = None,
                   ) -> None:

        def any_data(lexicon_data: List[Optional[Dict[str, List[str]]]]) -> bool:
            return any(lexicon_data)
        
        all_lexicon_data = [lexicon_lookup_data, lexicon_lemma_lookup_data]
        if not any_data(all_lexicon_data) and nlp is not None:
            nlp_language = nlp.lang
            if nlp_language in LANG_LEXICON_RESOUCRE_MAPPER:
                lang_lexicon_info = LANG_LEXICON_RESOUCRE_MAPPER[nlp_language]
                lexicon_lookup_data = LexiconCollection.from_tsv(lang_lexicon_info['lexicon'], include_pos=True)
                lexicon_lemma_lookup_data = LexiconCollection.from_tsv(lang_lexicon_info['lexicon_lemma'], include_pos=False)
        
        all_lexicon_data = [lexicon_lookup_data, lexicon_lemma_lookup_data]
        if lexicon_lookup_data is not None:
            self.lexicon_lookup = lexicon_lookup_data
        if lexicon_lemma_lookup_data is not None:
            self.lexicon_lemma_lookup = lexicon_lemma_lookup_data
        
        if not any_data(all_lexicon_data):
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
                                             lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                                             lexicon_lemma_lookup_data: Optional[Dict[str, List[str]]] = None,
                                             usas_tags_token_attr: str = 'usas_tags'
                                             ) -> RuleBasedTagger:
    return RuleBasedTagger(nlp, lexicon_lookup, lexicon_lemma_lookup_data,
                           usas_tags_token_attr)
