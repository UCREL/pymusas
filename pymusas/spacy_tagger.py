from typing import Optional, List, Iterable, Callable, Dict

from spacy.training import Example
from spacy.language import Language
from spacy.tokens import Token, Doc

from .config import LANG_LEXICON_RESOUCRE_MAPPER
from .lexicon_collection import LexiconCollection


class RuleBasedTagger:

    def __init__(self, nlp: Language,
                 lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                 lexicon_lemma_lookup: Optional[Dict[str, List[str]]] = None,
                 usas_tags_token_attr: str = 'usas_tags'
                 ) -> None:
        print(nlp.pipe_names)
        self.lexicon_lookup: Dict[str, List[str]] = dict()
        self.lexicon_lemma_lookup: Dict[str, List[str]] = dict()
        if lexicon_lookup is not None:
            self.lexicon_lookup = lexicon_lookup
        if lexicon_lemma_lookup is not None:
            self.lexicon_lemma_lookup = lexicon_lemma_lookup

        self.usas_tags_token_attr = usas_tags_token_attr
        Token.set_extension(self.usas_tags_token_attr, default=None)

    @staticmethod
    def tag_token(text: str, lemma: str, pos: str,
                  lexicon_lookup: Dict[str, List[str]],
                  lemma_lexicon_lookup: Dict[str, List[str]]) -> List[str]:
        if pos == 'punc':
            return ["PUNCT"]

        text_pos = f"{text}|{pos}"
        if text_pos in lexicon_lookup:
            return lexicon_lookup[text_pos]

        lemma_pos = f"{lemma}|{pos}"
        if lemma_pos in lexicon_lookup:
            return lexicon_lookup[lemma_pos]

        text_lower = text.lower()
        text_pos_lower = f"{text_lower}|{pos}"
        if text_pos_lower in lexicon_lookup:
            return lexicon_lookup[text_pos_lower]

        lemma_lower = lemma.lower()
        lemma_pos_lower = f"{lemma_lower}|{pos}"
        if lemma_pos_lower in lexicon_lookup:
            return lexicon_lookup[lemma_pos_lower]

        if pos == 'num':
            return ['N1']

        if text in lemma_lexicon_lookup:
            return lemma_lexicon_lookup[text]

        if lemma in lemma_lexicon_lookup:
            return lemma_lexicon_lookup[lemma]

        if text_lower in lemma_lexicon_lookup:
            return lemma_lexicon_lookup[text_lower]

        if lemma_lower in lemma_lexicon_lookup:
            return lemma_lexicon_lookup[lemma_lower]

        return ['Z99']

    def __call__(self, doc: Doc) -> Doc:
        for token in doc:
            text = token.text
            lemma = token.lemma_
            pos = token.pos_
            semantic_tags = self.tag_token(text, lemma, pos,
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
