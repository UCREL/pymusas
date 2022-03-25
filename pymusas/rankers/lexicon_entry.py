from abc import abstractmethod
import collections
from typing import DefaultDict, Dict, List, Optional, Set, Tuple, cast

import srsly

from pymusas.base import Serialise
from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule


class LexiconEntryRanker(Serialise):
    '''
    An **abstract class** that defines the basic methods, `__call__`,
    `to_bytes`, and `from_bytes`, that is required for all
    :class:`LexiconEntryRanker`s.

    Each lexicon entry match is represented by a
    :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object.

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
        match and the optional :class:`pymusas.rankers.ranking_meta_data.RankingMetaData`
        object of the **global** lowest ranked match for each token.

        # Parameters

        token_ranking_data : `List[List[RankingMetaData]]`
            For each token a `List` of :class:`pymusas.rankers.ranking_meta_data.RankingMetaData`
            representing the lexicon entry match.

        # Returns
        
        `Tuple[List[List[int]], List[Optional[RankingMetaData]]]`
        '''
        ...  # pragma: no cover

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...  # pragma: no cover


class ContextualRuleBasedRanker(LexiconEntryRanker):
    '''
    The contextual rule based ranker creates ranks based on the rules stated below.
    
    Each lexicon entry match is represented by a
    :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object.

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

        self._maximum_n_gram_length = maximum_n_gram_length
        self._maximum_number_wildcards = maximum_number_wildcards
        
        self.n_gram_number_indexes = len(str(maximum_n_gram_length))
        self.wildcards_number_indexes = len(str(maximum_number_wildcards))

        self.n_gram_ranking_dictionary: Dict[int, int] = \
            dict(zip(range(1, maximum_n_gram_length + 1, 1),
                     range(maximum_n_gram_length, 0, -1)))

    def to_bytes(self) -> bytes:
        '''
        Serialises the :class:`ContextualRuleBasedRanker` to a bytestring.

        # Returns

        `bytes`
        '''
        serialise = {}
        serialise['maximum_n_gram_length'] = srsly.msgpack_dumps(self._maximum_n_gram_length)
        serialise['maximum_number_wildcards'] = srsly.msgpack_dumps(self._maximum_number_wildcards)
        return cast(bytes, srsly.msgpack_dumps(serialise))

    @staticmethod
    def from_bytes(bytes_data: bytes) -> "ContextualRuleBasedRanker":
        '''
        Loads :class:`ContextualRuleBasedRanker` from the given bytestring and
        returns it.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.
        
        # Returns

        :class:`ContextualRuleBasedRanker`
        '''
        serialise_data = srsly.msgpack_loads(bytes_data)
        maximum_n_gram_length = srsly.msgpack_loads(serialise_data['maximum_n_gram_length'])
        maximum_number_wildcards = srsly.msgpack_loads(serialise_data['maximum_number_wildcards'])
        return ContextualRuleBasedRanker(maximum_n_gram_length,
                                         maximum_number_wildcards)

    @staticmethod
    def get_construction_arguments(rules: List['Rule']) -> Tuple[int, int]:
        '''
        Given a `List` of rules it will return the `maximum_n_gram_length` and
        `maximum_number_wildcards` from the lexicon collections that those
        :class:`pymusas.taggers.rules.rule.Rule`(s) are based on. The output from
        this function can then be used as the arguments to the constructor of
        :class:`ContextualRuleBasedRanker`.

        # Parameters

        rules : `List[Rule]`
            A `List` of rules. This `List` is typically required when creating
            a :class:`pymusas.taggers.new_rule_based.RuleBasedTagger` tagger.
        
        # Returns

        `Tuple[int, int]`

        # Examples
        ``` python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.taggers.rules.mwe import MWERule
        >>> from pymusas.lexicon_collection import MWELexiconCollection
        >>> pt_mwe_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/mwe-pt.tsv"
        >>> mwe_dict = MWELexiconCollection.from_tsv(pt_mwe_lexicon_url)
        >>> mwe_rule = MWERule(mwe_dict)
        >>> ranker_construction_arguments = ContextualRuleBasedRanker.get_construction_arguments([mwe_rule])
        >>> ranker = ContextualRuleBasedRanker(*ranker_construction_arguments)

        ```
        '''
        maximum_n_gram_length = 0
        maximum_number_wildcards = 0
        for rule in rules:
            rule_max_n_gram_length = 0
            rule_max_number_wildcards = 0
            if isinstance(rule, SingleWordRule):
                rule_max_n_gram_length = 1
            elif isinstance(rule, MWERule):
                rule_max_n_gram_length = rule.mwe_lexicon_collection.longest_mwe_template
                rule_max_number_wildcards = rule.mwe_lexicon_collection.most_wildcards_in_mwe_template

            if rule_max_n_gram_length > maximum_n_gram_length:
                maximum_n_gram_length = rule_max_n_gram_length

            if rule_max_number_wildcards > maximum_number_wildcards:
                maximum_number_wildcards = rule_max_number_wildcards

        return (maximum_n_gram_length, maximum_number_wildcards)
        
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
            For each token a `List` of
            :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` representing
            the lexicon entry match.
        token_rankings : `List[List[int]]`
            For each token contains the ranks of the lexicon entry matches.
            **Note** that the `List` can be empty if a token has no lexicon
            entry matches.
        ranking_data_to_exclude : `Set[RankingMetaData]`, optional (default = `None`)
            Any :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` to
            exclude from the ranking selection, this can be useful when wanting
            to get the next best global rank for each token.

        # Raises

        `AssertionError`
            If the length of `token_ranking_data` is not equal to the length of
            `token_rankings`, for both the outer and inner `List`s.

        # Examples
        ``` python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.rankers.ranking_meta_data import RankingMetaData
        >>> from pymusas.lexicon_collection import LexiconType
        >>> from pymusas.rankers.lexical_match import LexicalMatch
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
        match and the optional :class:`pymusas.rankers.ranking_meta_data.RankingMetaData`
        object of the **global** lowest ranked match for each token.
        
        See the ranking rules in the class docstring for details on how
        each lexicon entry match is ranked.

        Time Complexity, given *N* is the number of tokens, *M* is the number
        of unique ranking data, and *P* is the number of ranking data (non-unique)
        then the time complexity is:
        
        O(3(N + P)) + O(M log M) + O(M)

        # Parameters

        token_ranking_data : `List[List[RankingMetaData]]`
            For each token a `List` of :class:`pymusas.rankers.ranking_meta_data.RankingMetaData`
            representing the lexicon entry match.

        # Returns
        
        `Tuple[List[List[int]], List[Optional[RankingMetaData]]]`

        # Examples
        ```python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.rankers.ranking_meta_data import RankingMetaData
        >>> from pymusas.lexicon_collection import LexiconType
        >>> from pymusas.rankers.lexical_match import LexicalMatch
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

    def __eq__(self, other: object) -> bool:
        '''
        Given another object to compare too it will return `True` if the other
        object is the same class and was initialised using with the same
        `maximum_n_gram_length` and `maximum_number_wildcards` values.

        # Parameters

        other : `object`
            The object to compare too.
        
        # Returns

        `True`
        '''
        if not isinstance(other, ContextualRuleBasedRanker):
            return False
        
        if self._maximum_n_gram_length != other._maximum_n_gram_length:
            return False

        if self._maximum_number_wildcards != other._maximum_number_wildcards:
            return False

        return True
