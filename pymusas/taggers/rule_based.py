import logging
from typing import Dict, Iterable, Iterator, List, Optional, Tuple


logger = logging.getLogger(__name__)


def _tag_token(text: str, lemma: str, pos: str,
               lexicon_lookup: Dict[str, List[str]],
               lemma_lexicon_lookup: Dict[str, List[str]]
               ) -> List[str]:
    '''
    Given the token's lingustic information and the lexicon lookup information
    it returns a `List` of USAS semantic tags, whereby the most likely tag is
    the first tag in the `List`. The `List` of tags returned are based on the
    set of Rules specified in the :class:`USASRuleBasedTagger` class doc string.
    
    # Parameters

    text : `str`
        The token's full text form e.g. `cars`
    lemma : `str`
        The token's lemma/base form e.g. `car`
    pos : `str`
        The token's Part Of Speech e.g. `Noun`
    lexicon_lookup : `Dict[str, List[str]]`
        The lexicon data structure with both lemma and POS information mapped to
        a `List` of USAS semantic tags e.g. `{'cars_noun': ['Z2', 'Z1']}`
    lemma_lexicon_lookup : `Optional[List[str]]`, optional (default = `None`)
        The lexicon data structure with only lemma information mapped to
        a `List` of USAS semantic tags e.g. `{'car': ['Z2', 'Z1']}`
    
    # Returns
    
    `List[str]`
    '''
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


class USASRuleBasedTagger():
    '''
    The USAS Rule Based Tagger is based around the
    [USAS Semantic Lexicon(s).](https://github.com/UCREL/Multilingual-USAS)
    The Tagger expects two Lexicon like data structure, both in the format of
    `Dict[str, List[str]]`, this structure maps a lemma (with or without it's
    Part Of Speech (POS)) to a `List` of USAS semantic tags. The easiest way
    of producing such a data structure is through
    :func:`pymusas.lexicon_collection.from_tsv`
    whereby the TSV file path would be to a USAS Semantic Lexicon.
    
    The class requires two Lexicon data structure the first, `lexicon_lookup`,
    requires both the lemma and POS, whereas the second, `lemma_lexicon_lookup`,
    only requires the lemma.

    Using these lexicon lookups the following rules are applied to assign a
    `List` of USAS semantic tags from the lexicon lookups to the given tokens
    in the given text. The text given is assumed to have been tokenised,
    lemmatised, and POS tagged:

    **Rules:**

    1. If `POS==punc` label as `PUNCT`
    2. Lookup token and POS tag
    3. Lookup lemma and POS tag
    4. Lookup lower case token and POS tag
    5. Lookup lower case lemma and POS tag
    6. if `POS==num` label as `N1`
    7. Lookup token with any POS tag and choose first entry in lexicon.
    8. Lookup lemma with any POS tag and choose first entry in lexicon.
    9. Lookup lower case token with any POS tag and choose first entry in lexicon.
    10. Lookup lower case lemma with any POS tag and choose first entry in lexicon.
    11. Label as `Z99`, this is the unmatched semantic tag.

    # Parameters

    lexicon_lookup : `Optional[List[str]]`, optional (default = `None`)
        The lexicon data structure with both lemma and POS information mapped to
        a `List` of USAS semantic tags e.g. `{'car_noun': ['Z2', 'Z1']}`
    lemma_lexicon_lookup : `Optional[List[str]]`, optional (default = `None`)
        The lexicon data structure with only lemma information mapped to
        a `List` of USAS semantic tags e.g. `{'car': ['Z2', 'Z1']}`

    # Attributes

    lexicon_lookup : `Dict[str, List[str]]`
        The given `lexicon_lookup` data, if that was `None` then this becomes
        an empty dictionary e.g. `{}`
    lemma_lexicon_lookup : `Dict[str, List[str]]`
        The given `lemma_lexicon_lookup` data, if that was `None` then this
        becomes an empty dictionary e.g. `{}`

    # Examples
    ``` python
    >>> from pymusas.lexicon_collection import LexiconCollection
    >>> from pymusas.taggers.rule_base import USASRuleBasedTagger
    >>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
    >>> lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
    >>> lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
    >>> tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
    ```
    '''

    def __init__(self, lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                 lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None
                 ) -> None:

        self.lexicon_lookup: Dict[str, List[str]] = {}
        if lexicon_lookup is not None:
            self.lexicon_lookup = lexicon_lookup

        self.lemma_lexicon_lookup: Dict[str, List[str]] = {}
        if lemma_lexicon_lookup is not None:
            self.lemma_lexicon_lookup = lemma_lexicon_lookup

    def tag_token(self, token: Tuple[str, str, str]) -> List[str]:
        '''
        Given a tokens with the relevant lingustic information it returns
        a list of possible USAS semantic tags, tagged according
        to the tagger's rules (see class doc string for tagger's rules). The
        first semantic tag in the `List` of tags is the most likely tag.
        
        # Parameters

        tokens : `List[Tuple[str, str, str]]`
            Each tuple represents a token. The tuple must contain the
            following lingustic information per token;
            1. Full text form e.g. `cars`
            2. Lemma/base form e.g. `car`
            3. Part Of Speech e.g. `Noun`
        
        # Returns

        `List[str]`
        '''

        token_text = token[0]
        lemma = token[1]
        pos = token[2]

        return _tag_token(token_text, lemma, pos, self.lexicon_lookup,
                          self.lemma_lexicon_lookup)

    def tag_tokens(self, tokens: Iterable[Tuple[str, str, str]]
                   ) -> Iterator[List[str]]:
        '''
        Given a list/iterable of tokens with the relevant lingustic
        information it returns for each token a list of possible USAS semantic
        tags, tagged according to the tagger's rules (see class doc string for
        tagger's rules). The first semantic tag in the `List` of tags is the
        most likely tag.
        
        # Parameters

        tokens : `Iterable[Tuple[str, str, str]]`
            Each tuple represents a token. The tuple must contain the
            following lingustic information per token;
            1. Full text form e.g. `cars`
            2. Lemma/base form e.g. `car`
            3. Part Of Speech e.g. `Noun`
        
        # Returns

        `Iterator[List[str]]`
        '''
        
        for token in tokens:
            token_sem_tags = self.tag_token(token)
            yield token_sem_tags
