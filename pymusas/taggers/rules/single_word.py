from typing import cast

import srsly

from pymusas.lexicon_collection import AutotagLexiconCollection, LexiconCollection, LexiconType
from pymusas.rankers.lexical_match import LexicalMatch
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.rankers.single_word import SingleWordRanker
from pymusas.taggers.rules.rule import Rule


class SingleWordRule(Rule):
    '''
    A single word rule match, is a rule that matches on single word lexicon
    entries. Entires can be matched on:
    
    1. Token and the token's Part Of Speech (POS) tag, e.g. `driving|adj`
    2. Lemma and the lemma's POS tag, e.g. `drive|adj`
    3. Token, e.g. `driving`
    4. Lemma, e.g. `drive`

    In all cases matches are found based on the original token/lemma and lower
    cased versions of the token/lemma. These matches are found through searching
    the `lexicon_collection` and `lemma_lexicon_collection` attributes.

    If a token has no matches from the above, and an
    `autotag_lexicon_collection` is given, then the token is matched against
    the `autotag` patterns, e.g. `*kg|NUM`, see
    :class:`pymusas.lexicon_collection.AutotagLexiconCollection`. An `autotag`
    entry only matches when its lemma pattern matches the token, lemma, lower
    cased token, or lower cased lemma **and** its POS pattern matches the
    token's POS tag, there is no match that ignores the POS tag. The patterns
    are case sensitive. If more than one `autotag` entry matches a token, only
    the entry that comes first in the `autotag_lexicon_collection` is used,
    therefore the order of the `autotag` lexicon sets the priority of its
    entries. Lexicon order takes priority over what the entry matched on,
    e.g. an earlier entry that only matches the lower cased token is used
    instead of a later entry that matches the token itself. Lexicon order also
    takes priority over the order of the POS tags in a `pos_mapper` mapping,
    e.g. with the mapping `{'CD': ['noun', 'num']}` and the entries `*kg|num`
    then `*kg|noun`, the token `15kg` with the POS tag `CD` matches both
    entries but uses `*kg|num`, as it comes first in the lexicon. These
    matches have the lexicon type
    `SINGLE_AUTOTAG` from :class:`pymusas.lexicon_collection.LexiconType`.


    # Parameters

    lexicon_collection : `dict[str, list[str]]`
        The data to create `lexicon_collection` instance attribute. A
        Dictionary where the keys are a combination of
        lemma/token and POS in the following format: `{lemma}|{POS}` and the
        values are a list of associated semantic tags.
    lemma_lexicon_collection : `dict[str, list[str]]`
        The data to create `lemma_lexicon_collection` instance attribute. A
        Dictionary where the keys are either just a lemma/token
        in the following format: `{lemma}` and the
        values are a list of associated semantic tags.
    pos_mapper : `dict[str, list[str]]`, optional (default = `None`)
        If not `None`, maps from the given token's POS tagset to the desired
        POS tagset, whereby the mapping is a `list` of tags, at the moment there
        is no preference order in this list of POS tags. The POS mapping is
        useful in situtation whereby the token's POS tagset is different to
        those used in the lexicons. **Note** the longer the `list[str]` for
        each POS mapping the slower the tagger, a one to one mapping will have
        no speed impact on the tagger. A selection of POS mappers can be found in
        :mod:`pymusas.pos_mapper`.
    autotag_lexicon_collection : `dict[str, list[str]]`, optional (default = `None`)
        The data to create the `autotag_lexicon_collection` instance
        attribute. A dictionary where the keys are a combination of lemma
        pattern and POS pattern in the following format: `{lemma}|{POS}` and
        the values are a list of associated semantic tags.

    # Instance Attributes

    lexicon_collection : `pymusas.lexicon_collection.LexiconCollection`
        A :class:`pymusas.lexicon_collection.LexiconCollection` instance that
        has been initialised using the `lexicon_collection` parameter.
    lemma_lexicon_collection : `pymusas.lexicon_collection.LexiconCollection`
        A :class:`pymusas.lexicon_collection.LexiconCollection` instance that
        has been initialised using the `lemma_lexicon_collection` parameter.
    pos_mapper : `dict[str, list[str]]`, optional (default = `None`)
        The given `pos_mapper`.
    autotag_lexicon_collection : `pymusas.lexicon_collection.AutotagLexiconCollection`
        A :class:`pymusas.lexicon_collection.AutotagLexiconCollection` instance
        that has been initialised using the `autotag_lexicon_collection`
        parameter, it is empty if that parameter is `None`.

    # Examples
    ``` python
    >>> from pymusas.taggers.rules.single_word import SingleWordRule
    >>> rule = SingleWordRule({'kg|NOUN': ['N3.5']}, {},
    ...                       autotag_lexicon_collection={'*kg|NUM': ['N3.5'],
    ...                                                   '*|PUNCT': ['PUNCT']})
    >>> matches = rule(['15kg', '15kg', '!'], ['15kg', '15kg', '!'],
    ...                ['NUM', 'NOUN', 'PUNCT'])
    >>> assert [match.lexicon_entry_match for match in matches[0]] == ['*kg|NUM'] * 4
    >>> assert matches[1] == []
    >>> assert matches[2][0].semantic_tags == ('PUNCT',)

    ```
    '''
    def __init__(self, lexicon_collection: dict[str, list[str]],
                 lemma_lexicon_collection: dict[str, list[str]],
                 pos_mapper: dict[str, list[str]] | None = None,
                 autotag_lexicon_collection: dict[str, list[str]] | None = None
                 ) -> None:

        self.lexicon_collection = LexiconCollection(lexicon_collection)
        self.lemma_lexicon_collection = LexiconCollection(lemma_lexicon_collection)
        self.pos_mapper = pos_mapper
        self.autotag_lexicon_collection = AutotagLexiconCollection(autotag_lexicon_collection)

    def __call__(self, tokens: list[str], lemmas: list[str], pos_tags: list[str]
                 ) -> list[list[RankingMetaData]]:
        '''
        Given the tokens, lemmas, and POS tags for each word in a text,
        it returns for each token a `list` of rules matches defined by
        the :class:`pymusas.rankers.ranking_meta_data.RankingMetaData`
        object based on the rule matches stated in the class docstring above.

        # Parameters

        tokens : `list[str]`
            The tokens that are within the text.
        lemmas : `list[str]`
            The lemmas of the tokens.
        pos_tags : `list[str]`
            The Part Of Speech tags of the tokens.

        # Returns

        `list[list[RankingMetaData]]`

        # Raises

        `ValueError`
            If the length of the `tokens`, `lemmas`, and `pos_tags` are not of
            the same length.
        '''

        def find_match_and_add_to_ranking_data(lexicon_entry: str,
                                               exclude_pos_information: bool,
                                               lexical_match: LexicalMatch,
                                               start_index: int, end_index: int,
                                               token_ranking_meta_data: list[list[RankingMetaData]]
                                               ) -> None:
            collection = self.lexicon_collection
            if exclude_pos_information:
                collection = self.lemma_lexicon_collection
            if lexicon_entry in collection:
                semantic_tags = tuple(collection[lexicon_entry])
                ranking_data = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL,
                                               1, 0, exclude_pos_information,
                                               lexical_match,
                                               start_index, end_index,
                                               lexicon_entry, semantic_tags)
                token_ranking_meta_data[start_index].append(ranking_data)

        token_ranking_meta_data: list[list[RankingMetaData]] \
            = [[] for _ in range(len(tokens))]
        
        index = 0

        for token, lemma, initial_pos in zip(tokens, lemmas, pos_tags, strict=True):

            token_lower = token.lower()
            lemma_lower = lemma.lower()

            start_index = index
            end_index = start_index + 1
            
            token_pos_tags = [initial_pos]
            if self.pos_mapper is not None:
                token_pos_tags = self.pos_mapper.get(initial_pos, [])
            
            # All of these use POS information
            for pos in token_pos_tags:
                token_pos = f'{token}|{pos}'
                find_match_and_add_to_ranking_data(token_pos, False,
                                                   LexicalMatch.TOKEN,
                                                   start_index, end_index,
                                                   token_ranking_meta_data)
                
                lemma_pos = f'{lemma}|{pos}'
                find_match_and_add_to_ranking_data(lemma_pos, False,
                                                   LexicalMatch.LEMMA,
                                                   start_index, end_index,
                                                   token_ranking_meta_data)
                
                token_lower_pos = f'{token_lower}|{pos}'
                find_match_and_add_to_ranking_data(token_lower_pos, False,
                                                   LexicalMatch.TOKEN_LOWER,
                                                   start_index, end_index,
                                                   token_ranking_meta_data)
                
                lemma_lower_pos = f'{lemma_lower}|{pos}'
                find_match_and_add_to_ranking_data(lemma_lower_pos, False,
                                                   LexicalMatch.LEMMA_LOWER,
                                                   start_index, end_index,
                                                   token_ranking_meta_data)
                
            # All of these do not use POS information
            lexical_value_type = [(token, LexicalMatch.TOKEN),
                                  (lemma, LexicalMatch.LEMMA),
                                  (token_lower, LexicalMatch.TOKEN_LOWER),
                                  (lemma_lower, LexicalMatch.LEMMA_LOWER)]
            for lexical_value, lexical_type in lexical_value_type:
                find_match_and_add_to_ranking_data(lexical_value, True, lexical_type,
                                                   start_index, end_index,
                                                   token_ranking_meta_data)

            # Autotag patterns are only used when there is no exact match.
            if self.autotag_lexicon_collection and not token_ranking_meta_data[start_index]:
                autotag_matches: list[tuple[str, LexicalMatch]] = []
                for pos in token_pos_tags:
                    for lexical_value, lexical_type in lexical_value_type:
                        for autotag_entry in self.autotag_lexicon_collection.match(lexical_value, pos):
                            autotag_matches.append((autotag_entry, lexical_type))

                # Only the matching entry that comes first in the autotag
                # lexicon is used, so the lexicon order sets the priority.
                matched_entries = {autotag_entry for autotag_entry, _ in autotag_matches}
                first_entry = next((autotag_entry for autotag_entry in self.autotag_lexicon_collection
                                    if autotag_entry in matched_entries), None)
                for autotag_entry, lexical_type in autotag_matches:
                    if autotag_entry != first_entry:
                        continue
                    semantic_tags = tuple(self.autotag_lexicon_collection[autotag_entry])
                    ranking_data = RankingMetaData(LexiconType.SINGLE_AUTOTAG,
                                                   1, 0, False,
                                                   lexical_type,
                                                   start_index, end_index,
                                                   autotag_entry, semantic_tags)
                    token_ranking_meta_data[start_index].append(ranking_data)

            index += 1

        return token_ranking_meta_data

    def best_match(self, token: str, lemma: str, pos_tag: str
                   ) -> RankingMetaData | None:
        '''
        Returns the best single word rule match for the given token, lemma, and
        POS tag, or `None` if there is no match. The matches are found using
        :func:`__call__` and ranked using
        :class:`pymusas.rankers.single_word.SingleWordRanker`.

        `autotag` matches are included, but as they are only found when the
        token has no exact single word lexicon match, an exact match is always
        returned before an `autotag` match. This method is used by
        :class:`pymusas.taggers.rules.mwe.MWERule` to resolve default (`Df`)
        semantic tags in Multi Word Expressions, therefore a `Df` tag can be
        resolved using an `autotag` match.

        # Parameters

        token : `str`
            The token.
        lemma : `str`
            The lemma of the token.
        pos_tag : `str`
            The Part Of Speech tag of the token.

        # Returns

        `RankingMetaData | None`

        # Examples
        ``` python
        >>> from pymusas.taggers.rules.single_word import SingleWordRule
        >>> rule = SingleWordRule({'act|ADJ': ['A1']}, {'acting': ['A2']})
        >>> best_match = rule.best_match('acting', 'act', 'ADJ')
        >>> assert best_match is not None
        >>> assert ('A1',) == best_match.semantic_tags
        >>> assert rule.best_match('style', 'style', 'NOUN') is None
        >>> autotag_rule = SingleWordRule({'5kg|NUM': ['N1']}, {},
        ...                               autotag_lexicon_collection={'*kg|NUM': ['N3.5']})
        >>> best_match = autotag_rule.best_match('15kg', '15kg', 'NUM')
        >>> assert best_match is not None
        >>> assert ('N3.5',) == best_match.semantic_tags
        >>> best_match = autotag_rule.best_match('5kg', '5kg', 'NUM')
        >>> assert best_match is not None
        >>> assert ('N1',) == best_match.semantic_tags

        ```
        '''
        return SingleWordRanker.best_match(self([token], [lemma], [pos_tag])[0])

    def to_bytes(self) -> bytes:
        '''
        Serialises the :class:`SingleWordRule` to a bytestring.

        # Returns

        `bytes`
        '''
        serialise = {}
        serialise['lexicon_collection'] = self.lexicon_collection.to_bytes()
        serialise['lemma_lexicon_collection'] \
            = self.lemma_lexicon_collection.to_bytes()
        serialise['pos_mapper'] = srsly.msgpack_dumps(self.pos_mapper)
        serialise['autotag_lexicon_collection'] \
            = self.autotag_lexicon_collection.to_bytes()
        return cast(bytes, srsly.msgpack_dumps(serialise))

    @staticmethod
    def from_bytes(bytes_data: bytes) -> "SingleWordRule":
        '''
        Loads :class:`SingleWordRule` from the given bytestring and returns it.

        Bytestrings created before `autotag` support was added, which do not
        contain an `autotag_lexicon_collection`, can still be loaded and will
        have an empty `autotag_lexicon_collection`.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.
        
        # Returns

        :class:`SingleWordRule`
        '''
        serialise_data = srsly.msgpack_loads(bytes_data)
        lexicon_collection \
            = LexiconCollection.from_bytes(serialise_data['lexicon_collection'])
        lemma_lexicon_collection \
            = LexiconCollection.from_bytes(serialise_data['lemma_lexicon_collection'])
        pos_mapper = srsly.msgpack_loads(serialise_data['pos_mapper'])
        autotag_lexicon_collection = AutotagLexiconCollection()
        if 'autotag_lexicon_collection' in serialise_data:
            autotag_lexicon_collection \
                = AutotagLexiconCollection.from_bytes(serialise_data['autotag_lexicon_collection'])

        single_word_rule = SingleWordRule({}, {}, None)
        single_word_rule.lexicon_collection = lexicon_collection
        single_word_rule.lemma_lexicon_collection = lemma_lexicon_collection
        single_word_rule.pos_mapper = pos_mapper
        single_word_rule.autotag_lexicon_collection = autotag_lexicon_collection
        return single_word_rule

    def __eq__(self, other: object) -> bool:
        '''
        Given another object to compare too it will return `True` if the other
        object is the same class and initialised using with the same argument
        values.

        # Parameters

        other : `object`
            The object to compare too.
        
        # Returns

        `True`
        '''
        if not isinstance(other, SingleWordRule):
            return False
        
        if self.pos_mapper != other.pos_mapper:
            return False
        
        if self.lexicon_collection != other.lexicon_collection:
            return False

        if self.lemma_lexicon_collection != other.lemma_lexicon_collection:
            return False

        if self.autotag_lexicon_collection != other.autotag_lexicon_collection:
            return False

        return True
