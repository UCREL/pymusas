from typing import Dict, List, Optional

from pymusas.lexicon_collection import LexiconCollection, LexiconType
from pymusas.rankers.lexicon_entry import LexicalMatch, RankingMetaData
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


    # Parameters

    lexicon_collection : `Dict[str, List[str]]`
        The data to create `lexicon_collection` instance attribute. A
        Dictionary where the keys are a combination of
        lemma/token and POS in the following format: `{lemma}|{POS}` and the
        values are a list of associated semantic tags.
    lemma_lexicon_collection : `Dict[str, List[str]]`
        The data to create `lemma_lexicon_collection` instance attribute. A
        Dictionary where the keys are either just a lemma/token
        in the following format: `{lemma}` and the
        values are a list of associated semantic tags.
    pos_mapper : `Dict[str, List[str]]`, optional (default = `None`)
        If not `None`, maps from the given token's POS tagset to the desired
        POS tagset, whereby the mapping is a `List` of tags, at the moment there
        is no preference order in this list of POS tags. The POS mapping is
        useful in situtation whereby the token's POS tagset is different to
        those used in the lexicons. **Note** the longer the `List[str]` for
        each POS mapping the slower the tagger, a one to one mapping will have
        no speed impact on the tagger. A selection of POS mappers can be found in
        :mod:`pymusas.pos_mapper`.

    # Instance Attributes

    lexicon_collection : `pymusas.lexicon_collection.LexiconCollection`
        A :class:`pymusas.lexicon_collection.LexiconCollection` instance that
        has been initialised using the `lexicon_collection` parameter.
    lemma_lexicon_collection : `pymusas.lexicon_collection.LexiconCollection`
        A :class:`pymusas.lexicon_collection.LexiconCollection` instance that
        has been initialised using the `lemma_lexicon_collection` parameter.
    pos_mapper : `Dict[str, List[str]]`, optional (default = `None`)
        The given `pos_mapper`.
    '''
    def __init__(self, lexicon_collection: Dict[str, List[str]],
                 lemma_lexicon_collection: Dict[str, List[str]],
                 pos_mapper: Optional[Dict[str, List[str]]] = None):

        self.lexicon_collection = LexiconCollection(lexicon_collection)
        self.lemma_lexicon_collection = LexiconCollection(lemma_lexicon_collection)
        self.pos_mapper = pos_mapper

    def __call__(self, tokens: List[str], lemmas: List[str], pos_tags: List[str]
                 ) -> List[List[RankingMetaData]]:
        '''
        Given the tokens, lemmas, and POS tags for each word in a text,
        it returns for each token a `List` of rules matches defined by
        the :class:`pymusas.rankers.lexicon_entry.RankingMetaData` object based on
        the rule matches stated in the class docstring above.
        
        # Parameters

        tokens : `List[str]`
            The tokens that are within the text.
        lemmas : `List[str]`
            The lemmas of the tokens.
        pos_tags : `List[str]`
            The Part Of Speech tags of the tokens.
        
        # Returns

        `List[List[RankingMetaData]]`
        '''

        def find_match_and_add_to_ranking_data(lexicon_entry: str,
                                               exclude_pos_information: bool,
                                               lexical_match: LexicalMatch,
                                               start_index: int, end_index: int,
                                               token_ranking_meta_data: List[List[RankingMetaData]]
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

        token_ranking_meta_data: List[List[RankingMetaData]] \
            = [[] for _ in range(len(tokens))]
        
        index = 0

        for token, lemma, initial_pos in zip(tokens, lemmas, pos_tags):

            token_lower = token.lower()
            lemma_lower = lemma.lower()

            start_index = index
            end_index = start_index + 1
            
            pos_tags = [initial_pos]
            if self.pos_mapper is not None:
                pos_tags = self.pos_mapper.get(initial_pos, [])
            
            # All of these use POS information
            for pos in pos_tags:
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

            index += 1

        return token_ranking_meta_data
