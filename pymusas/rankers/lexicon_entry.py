from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from typing import List

from pymusas.lexicon_collection import LexiconType


class LexicalMatch(IntEnum):
    '''
    Descriptions of the lexical matches and their ordering in tagging priority
    during ranking. Lower the value and rank the higher the tagging priority.

    The `value` attribute of each instance attribute is of type `int`. For the
    best explanation see the example below.

    # Instance Attributes

    TOKEN : `int`
        The lexicon entry matched on the token text.
    LEMMA : `int`
        The lexicon entry matched on the lemma of the token.
    TOKEN_LOWER : `int`
        The lexicon entry matched on the lower cased token text.
    LEMMA_LOWER : `int`
        The lexicon entry matched on the lower cased lemma of the token.

    # Examples
    ``` python
    >>> from pymusas.rankers.lexicon_entry import LexicalMatch
    >>> assert 1 == LexicalMatch.TOKEN
    >>> assert 'TOKEN' == LexicalMatch.TOKEN.name
    >>> assert 1 == LexicalMatch.TOKEN.value
    ...
    >>> assert 2 == LexicalMatch.LEMMA
    >>> assert 3 == LexicalMatch.TOKEN_LOWER
    >>> assert 4 == LexicalMatch.LEMMA_LOWER
    ...
    >>> assert 2 < LexicalMatch.LEMMA_LOWER

    ```
    '''
    TOKEN = 1
    LEMMA = 2
    TOKEN_LOWER = 3
    LEMMA_LOWER = 4

    def __repr__(self) -> str:
        '''
        Machine readable string. When printed and run `eval()` over the string
        you should be able to recreate the object.
        '''
        return self.__str__()
    

@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class RankingMetaData:
    '''
    A RankingMetaData object contains all of the meta data about a lexicon
    entry match during the tagging process. This meta data can then be used
    to determine the ranking of the match comapred to other matches within the
    same text/sentence that is being tagged.

    # Instance Attributes

    lexicon_type : `LexiconType`
        Type associated to the lexicon entry.
    lexicon_n_gram_length : `int`
        The n-gram size of the lexicon entry, e.g. `*_noun boot*_noun` will be
        of length 2 and all single word lexicon entries will be of length 1.
    lexicon_wildcard_count : `int`
        Number of wildcards in the lexicon entry, e.g. `*_noun boot*_noun` will
        be 2 and `ski_noun boot_noun` will be 0.
    exclude_pos_information : `bool`
        Whether the POS information was excluded in the match. This is only `True`
        when the match ignores the POS information for single word lexicon entries.
        This is always `False` when used in a Multi Word Expression (MWE) lexicon
        entry match.
    lexical_match : `LexicalMatch`
        What :class:`LexicalMatch` the lexicon entry matched on.
    token_match_start_index : `int`
        Index of the first token in the lexicon entry match.
    token_match_end_index : `int`
        Index of the last token in the lexicon entry match.
    '''
    lexicon_type: LexiconType
    lexicon_n_gram_length: int
    lexicon_wildcard_count: int
    exclude_pos_information: bool
    lexical_match: LexicalMatch
    token_match_start_index: int
    token_match_end_index: int


class LexiconEntryRanker(ABC):
    '''
    An **abstract class** that defines the basic method, `__call__`, that is
    required for all :class:`LexiconEntryRanker`s.

    A LexcionEntryRanker when called, `__call__`, ranks the lexicon entry matches
    for each token, whereby each match is represented by a :class:`RankingMetaData`
    object.

    **Lower ranked lexicon entry matches should be given priority when making
    tagging decisions.**
    '''
    
    @abstractmethod
    def __call__(self, token_ranking_data: List[List[RankingMetaData]]
                 ) -> List[List[int]]:
        '''
        For each token it returns a `List` of rankings for each lexicon entry
        match.

        # Parameters

        token_ranking_data : `List[List[RankingMetaData]]`
            For each token a `List` of :class:`RankingMetaData` representing
            the lexicon entry match.

        # Returns
        
        `List[List[int]]`
        '''
        ...


class ContextualRuleBasedRanker(LexiconEntryRanker):
    '''
    The contextual rule based ranker creates ranks based on the rules stated below.
    
    These rankings are fully interpretable as each rank is a *n* digit integer,
    whereby the first 5 digit indexes corresponds to the first 5 ranking rules
    below, e.g. first digit index corresponds to the first rule. The last *m*
    digits correspond to the start index which relates to the sixth/last rule.
    For example the rank `12111020` the first 5 digits `12111` correspond to the
    first 5 rules below and `020` means that the start index was 20 for the
    lexicon match which relates to rule 6, the reason for the 0 before 20 was can
    be due to the text sequence containing start indexes of more than 99 and less
    than 1000.

    **Lower ranked lexicon entry matches should be given priority when making
    tagging decisions.** For example a rank of 0 is better than a rank of 1.

    **Ranking Rules:**

    The ranking of lexicon entires is based off the following rules, these rules
    are based on the 6 heuristic stated at the top of column 2 on page 4 of
    [Piao et al. 2003](https://aclanthology.org/W03-1807.pdf):

    First we create an initial ranking based on lexicon entry type:

    1. Multi Word Expression (MWE) entries ranked lower than single and Non-Special
    entries are ranked lower than wild card entires.

    Then within these rankings we further rank based on:
    
    2. Longer entries, based on n-gram length, are ranked lower.
    3. Entries with fewer wildcards are ranked lower.

    Then we apply the following contextual ranking rules:

    4. Whether the POS information was excluded in the match if so these are ranked
    higher. This is only `True` when the match ignores the POS information for
    single word lexicon entries. This is always `False` when used in a
    MWE lexicon entry match.
    5. Whether the lexicon entry was matched on Token < Lemma <
    Lower cased token < Lower cased lemma. Token is the lowest ranked and lower
    cased lemma is highest.
    6. The lexicon entry that first appears in the text is ranked lowest,
    this is required for matches that do not apply to the same sequence
    of tokens.

    In the case whereby the ranker has no more rules to apply and lexicon entry
    matches per token have joint ranks, then those joint ranks will be returned
    and the tagger will have to decide what to do with those joint ranked lexicon
    matches.
    '''

    def __call__(self, token_ranking_data: List[List[RankingMetaData]]
                 ) -> List[List[int]]:
        '''
        For each token it returns a `List` of rankings for each lexicon entry
        match. See the ranking rules in the class docstring for details on how
        each lexicon entry match is ranked.

        # Parameters

        token_ranking_data : `List[List[RankingMetaData]]`
            For each token a `List` of :class:`RankingMetaData` representing
            the lexicon entry match.

        # Returns
        
        `List[List[int]]`

        # Examples
        ```python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.rankers.lexicon_entry import RankingMetaData
        >>> from pymusas.rankers.lexicon_entry import LexiconType
        >>> from pymusas.rankers.lexicon_entry import LexicalMatch
        >>> token_ranking_data = [
        ...    [
        ...        RankingMetaData(LexiconType.MWE_WILDCARD, 2, 1, False, LexicalMatch.TOKEN, 2, 3),
        ...        RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0, False, LexicalMatch.LEMMA, 2, 3),
        ...    ],
        ...    [
        ...        RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0, True, LexicalMatch.TOKEN_LOWER, 21, 23),
        ...    ]
        ... ]
        >>> expected_rankings = [[2211102, 1201202], [4102321]]
        >>> ranker = ContextualRuleBasedRanker()
        >>> assert expected_rankings == ranker(token_ranking_data)

        ```
        '''
        
        lexicon_type_to_rank = {
            LexiconType.MWE_NON_SPECIAL: 1,
            LexiconType.MWE_WILDCARD: 2,
            LexiconType.MWE_CURLY_BRACES: 3,
            LexiconType.SINGLE_NON_SPECIAL: 4
        }

        exclude_pos_information_to_rank = {
            False: 1,
            True: 2
        }

        initial_rankings: List[List[str]] = []
        largest_token_index = 0
        for token in token_ranking_data:
            token_rankings: List[str] = []
            for ranking_data in token:
                lexicon_type_rank = lexicon_type_to_rank[ranking_data.lexicon_type]
                n_gram_rank = ranking_data.lexicon_n_gram_length
                wildcard_rank = ranking_data.lexicon_wildcard_count
                exclude_pos_information_rank = exclude_pos_information_to_rank[ranking_data.exclude_pos_information]
                lexical_match_rank = ranking_data.lexical_match.value
                rank_str = (f'{lexicon_type_rank}{n_gram_rank}{wildcard_rank}'
                            f'{exclude_pos_information_rank}{lexical_match_rank}')
                token_rankings.append(rank_str)

                if largest_token_index < ranking_data.token_match_start_index:
                    largest_token_index = ranking_data.token_match_start_index
                if largest_token_index < ranking_data.token_match_end_index:
                    largest_token_index = ranking_data.token_match_end_index
            initial_rankings.append(token_rankings)

        largest_token_index_str_length = len(str(largest_token_index))
        rankings: List[List[int]] = []
        for str_token_rankings, token in zip(initial_rankings, token_ranking_data):
            int_token_rankings: List[int] = []
            for str_ranking, ranking_data in zip(str_token_rankings, token):
                str_start_index = str(ranking_data.token_match_start_index)
                str_start_index_len = len(str_start_index)
                start_index_len_diff = (largest_token_index_str_length
                                        - str_start_index_len)
                start_index_prefix = '0' * start_index_len_diff
                str_start_index = f'{start_index_prefix}{str_start_index}'
                
                int_token_ranking = int(f'{str_ranking}{str_start_index}')
                int_token_rankings.append(int_token_ranking)
            rankings.append(int_token_rankings)

        if rankings == []:
            return [[]]
        
        return rankings
