
from pymusas.rankers.ranking_meta_data import RankingMetaData


class SingleWordRanker:
    '''
    A stateless ranker that ranks the single word lexicon entry matches of
    **one** token, represented by a `list` of
    :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` objects, e.g. the
    matches returned by :class:`pymusas.taggers.rules.single_word.SingleWordRule`
    for one token.

    Matches are ranked using the single word ranking rules of
    :class:`pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker`, as the other
    rules are the same for all single word matches of one token:

    1. Matches that use POS information are ranked lower than those that do not. (Contextual Rule Based Ranker rule 4).
    2. Matches on Token < Lemma < Lower cased token < Lower cased lemma. (Contextual Rule Based Ranker rule 5).

    **Lower ranked matches should be given priority.** As the ranker has no
    state it does not need to be created or serialised, all methods are static.

    # Examples
    ``` python
    >>> from pymusas.rankers.single_word import SingleWordRanker
    >>> from pymusas.rankers.ranking_meta_data import RankingMetaData
    >>> from pymusas.lexicon_collection import LexiconType
    >>> from pymusas.rankers.lexical_match import LexicalMatch
    >>> lemma_pos = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
    ...                             False, LexicalMatch.LEMMA, 0, 1,
    ...                             'act|ADJ', ('A1',))
    >>> token_no_pos = RankingMetaData(LexiconType.SINGLE_NON_SPECIAL, 1, 0,
    ...                                True, LexicalMatch.TOKEN, 0, 1,
    ...                                'acting', ('A2',))
    >>> assert lemma_pos == SingleWordRanker.best_match([token_no_pos, lemma_pos])
    >>> assert SingleWordRanker.best_match([]) is None

    ```
    '''

    @staticmethod
    def sort_key(match: RankingMetaData) -> tuple[bool, int]:
        '''
        Returns the key used to rank the given single word `match`, a lower key
        is a better ranked match. It can be used as the `key` argument of
        `sorted`, `min`, etc.

        # Parameters

        match : `RankingMetaData`
            A single word lexicon entry match.

        # Returns

        `tuple[bool, int]`
        '''
        return (match.exclude_pos_information, match.lexical_match.value)

    @staticmethod
    def best_match(matches: list[RankingMetaData]) -> RankingMetaData | None:
        '''
        Returns the lowest ranked, best, single word match from the given
        `matches` of one token, or `None` if `matches` is empty. When matches
        are joint ranked the first of those matches in `matches` is returned.

        # Parameters

        matches : `list[RankingMetaData]`
            The single word lexicon entry matches of one token.

        # Returns

        `RankingMetaData | None`
        '''
        if not matches:
            return None
        return min(matches, key=SingleWordRanker.sort_key)
