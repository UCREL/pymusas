import logging
from typing import Callable, Dict, Iterable, List, Optional

from spacy.language import Language
from spacy.pipe_analysis import validate_attrs
from spacy.tokens import Doc, Token
from spacy.training import Example

from ...config import LANG_LEXICON_RESOUCRE_MAPPER
from ...lexicon_collection import LexiconCollection
from ...taggers.rule_based import _tag_token


logger = logging.getLogger(__name__)


class USASRuleBasedTagger:

    def __init__(self,
                 lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                 lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                 pos_mapper: Optional[Dict[str, List[str]]] = None,
                 usas_tags_token_attr: str = 'usas_tags',
                 pos_attribute: str = 'pos_',
                 lemma_attribute: str = 'lemma_'
                 ) -> None:
        self.lexicon_lookup: Dict[str, List[str]] = {}
        if lexicon_lookup is not None:
            self.lexicon_lookup = lexicon_lookup
        
        self.lemma_lexicon_lookup: Dict[str, List[str]] = {}
        if lemma_lexicon_lookup is not None:
            self.lemma_lexicon_lookup = lemma_lexicon_lookup

        self.usas_tags_token_attr = usas_tags_token_attr
        self.pos_mapper = pos_mapper
        self.pos_attribute = pos_attribute
        self.lemma_attribute = lemma_attribute
        
        if Token.has_extension(self.usas_tags_token_attr):
            old_extension = Token.get_extension(self.usas_tags_token_attr)
            Token.set_extension(self.usas_tags_token_attr, default=None, force=True)
            log_message = (f' Overwritten the spaCy Token extension `{self.usas_tags_token_attr}`'
                           ' which currently has the following (default, method, getter, setter):'
                           f'`{old_extension}`. And replacing it with the following:'
                           f'`{Token.get_extension(self.usas_tags_token_attr)}`'
                           '. This would only become a problem if the the two Tuples'
                           ' of four are different, if they are the same there is'
                           ' no problem.')
            logger.debug(log_message)
        else:
            Token.set_extension(self.usas_tags_token_attr, default=None)
        
        # Dynamically assigns the token attribute this spaCy component
        # creates and requires. This is normally done in the
        # `spacy.language.Language.factory` decoration function.
        usas_factory_meta = Language.get_factory_meta('usas_tagger')
        usas_factory_meta.assigns = validate_attrs([f'token._.{self.usas_tags_token_attr}'])
        
        pos_required = self.pos_attribute
        if pos_required in ['pos_', 'tag_']:
            pos_required = pos_required[:-1]
        lemma_required = lemma_attribute
        if lemma_required == 'lemma_':
            lemma_required = 'lemma'
        usas_factory_meta.requires = [f'token.{lemma_required}',
                                      f'token.{pos_required}']

    def __call__(self, doc: Doc) -> Doc:
        for token in doc:
            text = token.text
            lemma = getattr(token, self.lemma_attribute)
            initital_pos = getattr(token, self.pos_attribute)
            pos = [initital_pos]
            if self.pos_mapper is not None:
                pos = self.pos_mapper[initital_pos]
            semantic_tags = _tag_token(text, lemma, pos,
                                       self.lexicon_lookup,
                                       self.lemma_lexicon_lookup)
            setattr(token._, self.usas_tags_token_attr, semantic_tags)
        return doc

    def initialize(self, get_examples: Optional[Callable[[], Iterable[Example]]] = None,
                   nlp: Optional[Language] = None,
                   lexicon_lookup_data: Optional[Dict[str, List[str]]] = None,
                   lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                   ) -> None:

        def any_data(lexicon_data: List[Optional[Dict[str, List[str]]]]) -> bool:
            return any(lexicon_data)
        
        all_lexicon_data = [lexicon_lookup_data, lemma_lexicon_lookup]
        if not any_data(all_lexicon_data) and nlp is not None:
            nlp_language = nlp.lang
            if nlp_language in LANG_LEXICON_RESOUCRE_MAPPER:
                lang_lexicon_info = LANG_LEXICON_RESOUCRE_MAPPER[nlp_language]
                lexicon_lookup_data = LexiconCollection.from_tsv(lang_lexicon_info['lexicon'], include_pos=True)
                lemma_lexicon_lookup = LexiconCollection.from_tsv(lang_lexicon_info['lexicon_lemma'], include_pos=False)
        
        all_lexicon_data = [lexicon_lookup_data, lemma_lexicon_lookup]
        if lexicon_lookup_data is not None:
            self.lexicon_lookup = lexicon_lookup_data
        if lemma_lexicon_lookup is not None:
            self.lexicon_lemma_lookup = lemma_lexicon_lookup
        
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
def make_usas_rule_based_tagger(nlp: Language, name: str,
                                lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                                lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                                pos_mapper: Optional[Dict[str, List[str]]] = None,
                                usas_tags_token_attr: str = 'usas_tags',
                                pos_attribute: str = 'pos_',
                                lemma_attribute: str = 'lemma_'
                                ) -> USASRuleBasedTagger:
    return USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup,
                               pos_mapper, usas_tags_token_attr,
                               pos_attribute, lemma_attribute)
