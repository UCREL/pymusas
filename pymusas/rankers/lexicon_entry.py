from abc import ABC, abstractmethod
import collections
from dataclasses import dataclass
from enum import IntEnum
from typing import DefaultDict, Dict, List, Optional, Set, Tuple

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
    lexicon_entry_match : `str`
        The lexicon entry match, which can be either a single word or MWE entry
        match. In the case for single word this could be `Car|noun` and in the
        case for a MWE it would be it's template, e.g. `snow_noun boots_noun`.
    semantic_tags : `Tuple[str, ...]`
        The semantic tags associated with the lexicon entry. The semantic tags
        are in rank order, the most likely tag is the first tag in the tuple.
        The Tuple can be of variable length hence the `...` in the
        type annotation.
    '''
    lexicon_type: LexiconType
    lexicon_n_gram_length: int
    lexicon_wildcard_count: int
    exclude_pos_information: bool
    lexical_match: LexicalMatch
    token_match_start_index: int
    token_match_end_index: int
    lexicon_entry_match: str
    semantic_tags: Tuple[str, ...]


class LexiconEntryRanker(ABC):
    '''
    An **abstract class** that defines the basic method, `__call__`, that is
    required for all :class:`LexiconEntryRanker`s.

    Each lexicon entry match is represented by a :class:`RankingMetaData` object.

    **Lower ranked lexicon entry matches should be given priority when making
    tagging decisions. A rank of 0 is better than a rank of 1.**

    A LexcionEntryRanker when called, `__call__`, returns a tuple of two `List`s
    whereby each entry in the list corresponds to a token:

    1. Contains the ranks of the lexicon entry matches as a `List[int]`.
    **Note** that the `List` can be empty if a token has no lexicon entry matches.
    2. An `Optional[RankingMetaData]` that is the global lowest ranked entry
    match for that token. If the value is `None` then no global lowest ranked
    entry can be found for that token. If the `RankingMetaData` represents more
    than one token, like a Multi Word Expression (MWE) match, then those associated tokens
    will have the same `RankingMetaData` object as the global lowest ranked entry match.
    
    **The tagger will have to make a decision how to handle global lowest ranked
    matches of value `None`, a suggested approach would be to assign an
    unmatched/unknown semantic tag to those tokens.**

    The reason for the adding the second list is that the **global** lowest
    ranked match is not the same as the local/token lowest ranked match, this is
    due to the potential of overlapping matches, e.g. `North East London brewery`
    can have a match of `North East`, `North`, and `East London brewery` in this
    case the lowest rank for `North` would be `North East`, but as we have a
    lower match that uses `East` which is `East London brewery` then the
    **global** lowest rank for `North` would be `North`.
    '''
    
    @abstractmethod
    def __call__(self, token_ranking_data: List[List[RankingMetaData]]
                 ) -> Tuple[List[List[int]], List[Optional[RankingMetaData]]]:
        '''
        For each token it returns a `List` of rankings for each lexicon entry
        match and the optional :class:`RankingMetaData` object of the **global**
        lowest ranked match for each token.

        # Parameters

        token_ranking_data : `List[List[RankingMetaData]]`
            For each token a `List` of :class:`RankingMetaData` representing
            the lexicon entry match.

        # Returns
        
        `Tuple[List[List[int]], List[Optional[RankingMetaData]]]`
        '''
        ...


class ContextualRuleBasedRanker(LexiconEntryRanker):
    '''
    The contextual rule based ranker creates ranks based on the rules stated below.
    
    Each lexicon entry match is represented by a :class:`RankingMetaData` object.

    **Lower ranked lexicon entry matches should be given priority when making
    tagging decisions. See the :class:`LexiconEntryRanker` class docstring for
    more details on the returned value of the `__call__` method.**

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

    In the case whereby the global lowest ranked lexicon entry match is joint
    ranked with another entry then it is random which lexicon entry match is chosen.

    # Parameters

    maximum_n_gram_length : `int`
        The largest n_gram rule match that will be encountered, e.g. a match
        of `ski_noun boot_noun` will have a n-gram length of 2.
    maximum_number_wildcards : `int`
        The number of wildcards in the rule that contains the most wildcards, e.g.
        the rule `ski_* *_noun` would contain 2 wildcards. This can be 0 if you
        have no wildcard rules.

    # Instance Attributes

    n_gram_number_indexes : `int`
        The number of indexes that each n-gram length value should have when
        converting the n-gram length to a string using
        `pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.int_2_str`.
    wildcards_number_indexes : `int`
        The number of indexes that each wildcard count value should have when
        converting the wildcard count value to a string using
        `pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker.int_2_str`.
    n_gram_ranking_dictionary : `Dict[int, int]`
        Maps the n-gram length to it's rank value, as the n-gram length is
        inverse to it's rank, as the larger the n-gram length the lower it's
        rank.
    '''

    def __init__(self, maximum_n_gram_length: int,
                 maximum_number_wildcards: int) -> None:

        self.n_gram_number_indexes = len(str(maximum_n_gram_length))
        self.wildcards_number_indexes = len(str(maximum_number_wildcards))

        self.n_gram_ranking_dictionary: Dict[int, int] = \
            dict(zip(range(1, maximum_n_gram_length + 1, 1),
                     range(maximum_n_gram_length, 0, -1)))

    @staticmethod
    def int_2_str(int_value: int, number_indexes: int) -> str:
        '''
        Converts the integer, `int_value`, to a string with `number_indexes`,
        e.g. `10` and `05` both have `number_indexes` of 2 and `001`, `020`,
        and `211` have `number_indexes` of 3.

        # Parameters

        int_value : `int`
            The integer to converts to a string with the given `number_indexes`.
        number_indexes : `int`
            The number of indexes the `int_value` should have in the returned
            string.
        
        # Returns
        
        `str`

        # Raises

        ValueError
            If the `number_indexes` of the `int_value` when converted to a
            string is greater than the given `number_indexes`.
        '''
        str_value = str(int_value)
        str_value_number_indexes = len(str_value)
        if str_value_number_indexes > number_indexes:
            error_msg = (f"Cannot convert int ({int_value}) to a ranked"
                         f" string as the maximum number of indexes it can be"
                         f" is {number_indexes}.")
            raise ValueError(error_msg)
        
        number_prefix_zeros_to_add = number_indexes - str_value_number_indexes
        prefix_zeros = '0' * number_prefix_zeros_to_add
        return f'{prefix_zeros}{str_value}'

    @staticmethod
    def get_global_lowest_ranks(token_ranking_data: List[List[RankingMetaData]],
                                token_rankings: List[List[int]],
                                ranking_data_to_exclude: Optional[Set[RankingMetaData]] = None
                                ) -> List[Optional[RankingMetaData]]:
        '''
        Returns the global lowest ranked entry match for each token. If the value
        is `None` then no global lowest ranked entry can be found for that token.
        If the `RankingMetaData` represents more than one token, like a Multi
        Word Expression (MWE) match, then those associated tokens will have the
        same `RankingMetaData` object as the global lowest ranked entry match.

        Time Complexity, given *N* is the number of tokens, *M* is the number
        of unique ranking data, and *P* is the number of ranking data (non-unique)
        then the time complexity is:
        
        O(N + P) + O(M log M) + O(M)
        
        # Parameters

        token_ranking_data : `List[List[RankingMetaData]]`
            For each token a `List` of :class:`RankingMetaData` representing
            the lexicon entry match.
        token_rankings : `List[List[int]]`
            For each token contains the ranks of the lexicon entry matches.
            **Note** that the `List` can be empty if a token has no lexicon
            entry matches.
        ranking_data_to_exclude : `Set[RankingMetaData]`, optional (default = `None`)
            Any :class:`RankingMetaData` to exclude from the ranking selection, this can
            be useful when wanting to get the next best global rank for each token.

        # Raises

        `AssertionError`
            If the length of `token_ranking_data` is not equal to the length of
            `token_rankings`, for both the outer and inner `List`s.

        # Examples
        ``` python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.rankers.lexicon_entry import RankingMetaData
        >>> from pymusas.rankers.lexicon_entry import LexiconType
        >>> from pymusas.rankers.lexicon_entry import LexicalMatch
        >>> north_east = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0,
        ...                              False, LexicalMatch.TOKEN, 0, 2,
        ...                              'North_noun East_noun', ('Z1',))
        >>> east_london_brewery = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 3, 0,
        ...                                       False, LexicalMatch.TOKEN, 1, 4,
        ...                                       'East_noun London_noun brewery_noun', ('Z1',))
        >>> token_ranking_data = [
        ...     [
        ...         north_east
        ...     ],
        ...     [
        ...         north_east,
        ...         east_london_brewery
        ...     ],
        ...     [
        ...         east_london_brewery
        ...     ],
        ...     [
        ...         east_london_brewery
        ...     ]
        ... ]
        >>> token_rankings = [[120110], [120110, 110111], [110111], [110111]]
        >>> expected_lowest_ranked_matches = [None, east_london_brewery,
        ...                                   east_london_brewery, east_london_brewery]
        >>> assert (ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data, token_rankings, None)
        ...         == expected_lowest_ranked_matches)

        ```

        Following on from the previous example, we now want to find the next best
        global match for each token so we exclude the current best global match
        for each token which is the `east_london_brewery` match:
        
        ``` python
        >>> expected_lowest_ranked_matches = [north_east, north_east, None, None]
        >>> ranking_data_to_exclude = {east_london_brewery}
        >>> assert (ContextualRuleBasedRanker.get_global_lowest_ranks(token_ranking_data, token_rankings,
        ...                                                          ranking_data_to_exclude)
        ...         == expected_lowest_ranked_matches)

        ```
        '''
        if ranking_data_to_exclude is None:
            ranking_data_to_exclude = set()
        
        assert len(token_ranking_data) == len(token_rankings), 'Lengths should be equal'

        ranking_meta_data: DefaultDict[int, Set[RankingMetaData]] = collections.defaultdict(set)
        for token_data, token_ranking in zip(token_ranking_data, token_rankings):
            assert len(token_data) == len(token_ranking), 'Lengths should be equal'
            
            for data, rank in zip(token_data, token_ranking):
                if data in ranking_data_to_exclude:
                    continue
                ranking_meta_data[rank].add(data)
        
        global_lowest_ranks: List[Optional[RankingMetaData]] = \
            [None for _ in token_ranking_data]
        
        ordered_ranking_meta_data = sorted(ranking_meta_data.items(),
                                           key=lambda x: x[0])
        for rank, meta_data in ordered_ranking_meta_data:
            for data in meta_data:
                start, end = data.token_match_start_index, data.token_match_end_index
                if any(global_lowest_ranks[start: end]):
                    continue

                for index in range(start, end):
                    global_lowest_ranks[index] = data

        return global_lowest_ranks

    def __call__(self, token_ranking_data: List[List[RankingMetaData]]
                 ) -> Tuple[List[List[int]], List[Optional[RankingMetaData]]]:
        '''
        For each token it returns a `List` of rankings for each lexicon entry
        match and the optional :class:`RankingMetaData` object of the **global**
        lowest ranked match for each token.
        
        See the ranking rules in the class docstring for details on how
        each lexicon entry match is ranked.

        Time Complexity, given *N* is the number of tokens, *M* is the number
        of unique ranking data, and *P* is the number of ranking data (non-unique)
        then the time complexity is:
        
        O(3(N + P)) + O(M log M) + O(M)

        # Parameters

        token_ranking_data : `List[List[RankingMetaData]]`
            For each token a `List` of :class:`RankingMetaData` representing
            the lexicon entry match.

        # Returns
        
        `Tuple[List[List[int]], List[Optional[RankingMetaData]]]`

        # Examples
        ```python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.rankers.lexicon_entry import RankingMetaData
        >>> from pymusas.rankers.lexicon_entry import LexiconType
        >>> from pymusas.rankers.lexicon_entry import LexicalMatch
        >>> north_east = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 2, 0,
        ...                              False, LexicalMatch.TOKEN, 0, 2,
        ...                              'North_noun East_noun', ('Z1',))
        >>> east_london_brewery = RankingMetaData(LexiconType.MWE_NON_SPECIAL, 3, 0,
        ...                                       False, LexicalMatch.TOKEN, 1, 4,
        ...                                       'East_noun London_noun brewery_noun', ('Z1',))
        >>> token_ranking_data = [
        ...     [
        ...         north_east
        ...     ],
        ...     [
        ...         north_east,
        ...         east_london_brewery
        ...     ],
        ...     [
        ...         east_london_brewery
        ...     ],
        ...     [
        ...         east_london_brewery
        ...     ]
        ... ]
        >>> expected_ranks = [[120110], [120110, 110111], [110111], [110111]]
        >>> expected_lowest_ranked_matches = [None, east_london_brewery,
        ...                                   east_london_brewery, east_london_brewery]
        >>> ranker = ContextualRuleBasedRanker(3, 0)
        >>> assert ((expected_ranks, expected_lowest_ranked_matches)
        ...         == ranker(token_ranking_data))

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
                n_gram_rank = self.n_gram_ranking_dictionary[ranking_data.lexicon_n_gram_length]
                n_gram_str_rank = self.int_2_str(n_gram_rank, self.n_gram_number_indexes)
                wildcard_str_rank = self.int_2_str(ranking_data.lexicon_wildcard_count,
                                                   self.wildcards_number_indexes)
                exclude_pos_information_rank = exclude_pos_information_to_rank[ranking_data.exclude_pos_information]
                lexical_match_rank = ranking_data.lexical_match.value
                rank_str = (f'{lexicon_type_rank}{n_gram_str_rank}{wildcard_str_rank}'
                            f'{exclude_pos_information_rank}{lexical_match_rank}')
                token_rankings.append(rank_str)

                if largest_token_index < ranking_data.token_match_start_index:
                    largest_token_index = ranking_data.token_match_start_index
                if largest_token_index < ranking_data.token_match_end_index:
                    largest_token_index = ranking_data.token_match_end_index
            initial_rankings.append(token_rankings)

        # Add to each token ranking where it first appears in the text, rule 6.
        largest_token_index_number_indexes = len(str(largest_token_index))
        rankings: List[List[int]] = []
        for str_token_rankings, token in zip(initial_rankings, token_ranking_data):
            int_token_rankings: List[int] = []
            for str_ranking, ranking_data in zip(str_token_rankings, token):
                start_index_str_rank = self.int_2_str(ranking_data.token_match_start_index,
                                                      largest_token_index_number_indexes)
                int_token_ranking = int(f'{str_ranking}{start_index_str_rank}')
                int_token_rankings.append(int_token_ranking)
            rankings.append(int_token_rankings)
        global_lowest_rank_indexes = self.get_global_lowest_ranks(token_ranking_data,
                                                                  rankings, None)

        return (rankings, global_lowest_rank_indexes)
