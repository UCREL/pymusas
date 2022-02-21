from typing import Dict, List, Tuple

from pymusas.lexicon_collection import LexiconType, MWELexiconCollection
from pymusas.rankers.lexicon_entry import LexicalMatch, RankingMetaData
from pymusas.taggers.rules import util
from pymusas.taggers.rules.rule import Rule


class MWERule(Rule):
    '''
    A Multi Word Expression (MWE) rule match can be one of the following matches:

    1. `MWE_NON_SPECIAL` match - whereby the combined token/lemma and POS
    is found within the given MWE Lexicon Collection (`self.mwe_lexicon_collection`).
    2. `MWE_WILDCARD` match - whereby the combined token/lemma and POS matches
    a wildcard MWE template that is within the MWE Lexicon Collection
    (`self.mwe_lexicon_collection`).

    All rule matches use the
    `pymusas.lexicon_collection.MWELexiconCollection.mwe_match`
    method for matching. Matches are found based on the original token/lemma and
    lower cased versions of the token/lemma.

    # Parameters

    mwe_lexicon_lookup : `Dict[str, List[str]]`
        The data to create `mwe_lexicon_collection` instance attribute. A
        Dictionary where the keys are MWE templates, of any
        :class:`pymusas.lexicon_collection.LexiconType`,
        and the values are a list of associated semantic tags.

    # Instance Attributes

    mwe_lexicon_collection : `pymusas.lexicon_collection.MWELexiconCollection`
        A :class:`pymusas.lexicon_collection.MWELexiconCollection` instance that
        has been initialised using the `data` parameter. This collection is used
        to find MWE rule matches.
    '''

    def __init__(self, mwe_lexicon_lookup: Dict[str, List[str]]) -> None:
        
        self.mwe_lexicon_collection = MWELexiconCollection(mwe_lexicon_lookup)

    def __call__(self, tokens: List[str], lemmas: List[str], pos_tags: List[str]
                 ) -> List[List[RankingMetaData]]:
        '''
        Given the tokens, lemmas, and POS tags for each word in a text,
        it returns for each token a `List` of rules matches defined by
        the :class:`pymusas.rankers.lexicon_entry.RankingMetaData` object based on
        the rule matches states in the class docstring above.
        
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

        def tag_n_gram_indexes(_n_gram_indexes: List[Tuple[int, int]],
                               mwe_type: LexiconType,
                               token_pos: List[str], lemma_pos: List[str],
                               token_lower_pos: List[str], lemma_lower_pos: List[str],
                               token_ranking_meta_data: List[List[RankingMetaData]]
                               ) -> None:
            '''
            Given a `List` of n gram indexes, whereby all grams have the same value
            of *n*, it will find all MWE rule matches of type `mwe_type` for those
            n-grams in the four token `List`s (`token_pos`, `lemma_pos`,
            `token_lower_pos`, `lemma_lower_pos`). All rule matches will crate a
            `RankingMetaData` object for each token in the match, of which these
            objects are appended to the relevant token indexes within the
            `token_ranking_meta_data` object.

            Nothing is returned but the `token_ranking_meta_data` object will have
            been updated if at least one rule match has been found.
            '''
            token_list_type: List[Tuple[List[str], LexicalMatch]]
            token_list_type = [(token_pos, LexicalMatch.TOKEN),
                               (lemma_pos, LexicalMatch.LEMMA),
                               (token_lower_pos, LexicalMatch.TOKEN_LOWER),
                               (lemma_lower_pos, LexicalMatch.LEMMA_LOWER)]
            
            for token_list, token_type in token_list_type:
                for n_gram_index in _n_gram_indexes:
                    start_index, end_index = n_gram_index
                    mwe_template = ''
                    for token_index in range(start_index, end_index):
                        if (token_index + 1) == end_index:
                            mwe_template += f'{token_list[token_index]}'
                            continue
                        mwe_template += f'{token_list[token_index]} '
                    matched_mwe_templates = self.mwe_lexicon_collection.mwe_match(mwe_template,
                                                                                  mwe_type)
                    if not matched_mwe_templates:
                        continue

                    for matched_mwe_template in matched_mwe_templates:
                        mwe_meta_data = self.mwe_lexicon_collection[matched_mwe_template]
                        ranking_meta_data = RankingMetaData(mwe_type,
                                                            mwe_meta_data.n_gram_length,
                                                            mwe_meta_data.wildcard_count,
                                                            False, token_type, start_index,
                                                            end_index,
                                                            matched_mwe_template)
                        for token_index in range(start_index, end_index):
                            token_ranking_meta_data[token_index].append(ranking_meta_data)
                
        def tag_n_gram_based_MWE(mwe_type: LexiconType,
                                 token_pos: List[str], lemma_pos: List[str],
                                 token_lower_pos: List[str], lemma_lower_pos: List[str],
                                 token_ranking_meta_data: List[List[RankingMetaData]]
                                 ) -> None:
            '''
            Any type of rule match that uses n-grams should use this function.
            At the moment only the `MWE_NON_SPECIAL` and `MWE_WILDCARD` matches
            are supported.
            
            The function for each token list () creates n-grams, up to the size
            of the maximum n-gram for the match type requested, of these tokens
            and then matches those n-grams using the
            `pymusas.lexicon_collection.MWELexiconCollection.mwe_match`
            method.

            Nothing is returned but the `token_ranking_meta_data` object will have
            been updated if at least one rule match has been found.
            '''
            largest_mwe_in_lexicon = 0
            if mwe_type == LexiconType.MWE_NON_SPECIAL:
                largest_mwe_in_lexicon = self.mwe_lexicon_collection.longest_non_special_mwe_template
            elif mwe_type == LexiconType.MWE_WILDCARD:
                largest_mwe_in_lexicon = self.mwe_lexicon_collection.longest_wildcard_mwe_template
            
            # If we do not have any MWE lexicons that are at least 2 grams
            # then return
            if largest_mwe_in_lexicon < 2:
                return
            
            largest_n_gram = largest_mwe_in_lexicon + 1
            largest_n_gram_indexes: List[Tuple[int, int]] = []

            for n_gram_index in util.n_gram_indexes(token_pos, 2, largest_mwe_in_lexicon):
                start_index, end_index = n_gram_index
                n_gram_size = end_index - start_index
                if largest_n_gram > n_gram_size:
                    largest_n_gram = n_gram_size
                    tag_n_gram_indexes(largest_n_gram_indexes, mwe_type,
                                       token_pos, lemma_pos, token_lower_pos,
                                       lemma_lower_pos,
                                       token_ranking_meta_data)
                    largest_n_gram_indexes = []

                largest_n_gram_indexes.append(n_gram_index)
            
            tag_n_gram_indexes(largest_n_gram_indexes, mwe_type, token_pos,
                               lemma_pos, token_lower_pos,
                               lemma_lower_pos, token_ranking_meta_data)
        
        token_pos: List[str] = []
        token_lower_pos: List[str] = []
        lemma_pos: List[str] = []
        lemma_lower_pos: List[str] = []
        for token, lemma, pos in zip(tokens, lemmas, pos_tags):
            token_pos.append(f'{token}_{pos}')
            token_lower_pos.append(f'{token}_{pos}'.lower())
            lemma_pos.append(f'{lemma}_{pos}')
            lemma_lower_pos.append(f'{lemma}_{pos}'.lower())
        
        number_tokens = len(tokens)
        token_ranking_meta_data: List[List[RankingMetaData]] \
            = [[] for _ in range(number_tokens)]
        
        if number_tokens < 2:
            return token_ranking_meta_data

        # First match on `MWE_NON_SPECIAL`
        tag_n_gram_based_MWE(LexiconType.MWE_NON_SPECIAL, token_pos, lemma_pos,
                             token_lower_pos, lemma_lower_pos,
                             token_ranking_meta_data)

        # Second match on `MWE_WILDCARD`
        tag_n_gram_based_MWE(LexiconType.MWE_WILDCARD, token_pos, lemma_pos,
                             token_lower_pos, lemma_lower_pos,
                             token_ranking_meta_data)

        return token_ranking_meta_data
