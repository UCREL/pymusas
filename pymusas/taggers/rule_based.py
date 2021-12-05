from typing import Dict, Iterable, Iterator, List, Optional, Tuple


def _tag_token(text: str, lemma: str, pos: List[str],
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
    pos : `List[str]`
        A list of the token's Part Of Speech e.g. `[Noun]`. Normally the list
        should be of length 1, if it is larger than 1 then we assume these are
        POS from a `pos_mapper`, therefore we follow the rules for the
        `pos_mapper` as stated in the :class:`USASRuleBasedTagger` class doc string.
    lexicon_lookup : `Dict[str, List[str]]`
        The lexicon data structure with both lemma and POS information mapped to
        a `List` of USAS semantic tags e.g. `{'cars_noun': ['Z2', 'Z1']}`
    lemma_lexicon_lookup : `Optional[List[str]]`, optional (default = `None`)
        The lexicon data structure with only lemma information mapped to
        a `List` of USAS semantic tags e.g. `{'car': ['Z2', 'Z1']}`
    
    # Returns
    
    `List[str]`
    '''
    if not isinstance(pos, list):
        raise TypeError(f'The Part Of Speech (pos) should be of type `List`, not {type(pos)},'
                        ' even if the List contains only 1 POS, which is expected'
                        f' in most cases. Value of the erroneous pos: {pos}')
    text_lower = text.lower()
    lemma_lower = lemma.lower()
    
    for pos_ in pos:
        if pos_ == 'punc':
            return ["PUNCT"]

        text_pos = f"{text}|{pos_}"
        if text_pos in lexicon_lookup:
            return lexicon_lookup[text_pos]

        lemma_pos = f"{lemma}|{pos_}"
        if lemma_pos in lexicon_lookup:
            return lexicon_lookup[lemma_pos]

        text_pos_lower = f"{text_lower}|{pos_}"
        if text_pos_lower in lexicon_lookup:
            return lexicon_lookup[text_pos_lower]

        lemma_pos_lower = f"{lemma_lower}|{pos_}"
        if lemma_pos_lower in lexicon_lookup:
            return lexicon_lookup[lemma_pos_lower]

        if pos_ == 'num':
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
    The Tagger uses two Lexicon like data structures, both in the format of
    `Dict[str, List[str]]`, this structure maps a lemma (with or without it's
    Part Of Speech (POS) ) to a `List` of USAS semantic tags.
    The first semantic tag in the `List` of tags is the most likely tag.
    
    The easiest way of producing the Lexicon like data structures is through
    :func:`pymusas.lexicon_collection.from_tsv`
    whereby the TSV file path would be to a USAS Semantic Lexicon.
    
    The optional POS mapper is used in this tagger when the POS tagset within
    the lexicons does not match the tagset used by the POS model that has
    been applied to the text. For instance a lot of the
    [USAS Semantic Lexicon(s).](https://github.com/UCREL/Multilingual-USAS)
    use the USAS core tagset which does not align with the Universal Part of Speech (UPOS)
    tagset that a lot of the [spaCy POS models](https://spacy.io/usage/linguistic-features#pos-tagging)
    have in common. Therefore, when using the UPOS tags from the spaCy POS model for tagging text using a USAS
    Semantic lexicon with this tagger a POS mapper is required to map UPOS to
    USAS core tags. The POS mapper is expected to map from the tagset of the POS model
    to the tagset of the lexicons, whereby the mapping is a `List`
    of tags, the first tag in the list is assumed to be the most relevant
    and the last to be the least. Some pre-compiled Dictionaries can be found in
    the :mod:`pymusas.pos_mapper` module, e.g. the UPOS to USAS core :var:`pymusas.pos_mapper.UPOS_TO_USAS_CORE`

    Using these lexicon lookups the following rules are applied to assign a
    `List` of USAS semantic tags from the lexicon lookups to the given tokens
    in the given text. The text given is assumed to have been tokenised,
    lemmatised, and POS tagged:

    **Rules:**

    1. **If `pos_mapper` is not `None`**, map the POS, from the POS model,
    to the first POS value in the `List` from the `pos_mapper`s `Dict`. **If** the
    `pos_mapper` cannot map the POS, from the POS model, go to step 9.
    2. If `POS==punc` label as `PUNCT`
    3. Lookup token and POS tag
    4. Lookup lemma and POS tag
    5. Lookup lower case token and POS tag
    6. Lookup lower case lemma and POS tag
    7. if `POS==num` label as `N1`
    8. **If there is another POS value in the `pos_mapper`** go back to step 2
    with this new POS value else carry on to step 9.
    9. Lookup token with any POS tag and choose first entry in lexicon.
    10. Lookup lemma with any POS tag and choose first entry in lexicon.
    11. Lookup lower case token with any POS tag and choose first entry in lexicon.
    12. Lookup lower case lemma with any POS tag and choose first entry in lexicon.
    13. Label as `Z99`, this is the unmatched semantic tag.

    **NOTE** this tagger has been designed to be flexible with the amount of
    resources avaliable, if you do not have a POS tagger then assign
    the POS tag an empty string e.g. `''`. If you do not have a lexicon with
    POS information then `lexicon_lookup` can be `None`. However, the fewer
    resources avaliable, less rules, stated above, will be applied making the
    tagger less effective.

    # Parameters

    lexicon_lookup : `Dict[str, List[str]]`, optional (default = `None`)
        The lexicon data structure with both lemma and POS information mapped to
        a `List` of USAS semantic tags e.g. `{'car_noun': ['Z2', 'Z1']}`
    lemma_lexicon_lookup : `Dict[str, List[str]]`, optional (default = `None`)
        The lexicon data structure with only lemma information mapped to
        a `List` of USAS semantic tags e.g. `{'car': ['Z2', 'Z1']}`
    pos_mapper : `Dict[str, List[str]]`, optional (default = `None`)
        If not `None`, maps from the POS model tagset to the lexicon data
        POS tagset, whereby the mapping is a `List` of tags, the first tag in
        the list is assumed to be the most relevant and the last to be the least.

    # Instance Attributes

    lexicon_lookup : `Dict[str, List[str]]`
        The given `lexicon_lookup` data, if that was `None` then this becomes
        an empty dictionary e.g. `{}`
    lemma_lexicon_lookup : `Dict[str, List[str]]`
        The given `lemma_lexicon_lookup` data, if that was `None` then this
        becomes an empty dictionary e.g. `{}`
    pos_mapper : `Dict[str, List[str]]`, optional (default = `None`)
        The given `pos_mapper`.

    # Examples
    ``` python
    >>> from pymusas.lexicon_collection import LexiconCollection
    >>> from pymusas.taggers.rule_based import USASRuleBasedTagger
    >>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
    >>> lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
    >>> lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
    >>> tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)

    ```
    '''

    def __init__(self, lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                 lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                 pos_mapper: Optional[Dict[str, List[str]]] = None
                 ) -> None:

        self.lexicon_lookup: Dict[str, List[str]] = {}
        if lexicon_lookup is not None:
            self.lexicon_lookup = lexicon_lookup

        self.lemma_lexicon_lookup: Dict[str, List[str]] = {}
        if lemma_lexicon_lookup is not None:
            self.lemma_lexicon_lookup = lemma_lexicon_lookup
        
        self.pos_mapper = pos_mapper

    def tag_token(self, token: Tuple[str, str, str]) -> List[str]:
        '''
        Given a tokens with the relevant lingustic information it returns
        a list of USAS semantic tags, tagged according
        to the tagger's rules (see the class's doc string for tagger's rules).
        The first semantic tag in the `List` of tags is the most likely tag.
        
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
        initial_pos = token[2]
        pos = [initial_pos]
        if self.pos_mapper is not None:
            pos = self.pos_mapper.get(initial_pos, [])

        return _tag_token(token_text, lemma, pos, self.lexicon_lookup,
                          self.lemma_lexicon_lookup)

    def tag_tokens(self, tokens: Iterable[Tuple[str, str, str]]
                   ) -> Iterator[List[str]]:
        '''
        Given a list/iterable of tokens with the relevant lingustic
        information it returns for each token a list of USAS semantic
        tags, tagged according to the tagger's rules (see the class's doc string for
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
