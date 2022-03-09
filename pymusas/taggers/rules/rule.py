from abc import ABC, abstractmethod
from typing import List

from pymusas.rankers.ranking_meta_data import RankingMetaData


class Rule(ABC):
    '''
    An **abstract class** that defines the basic method, `__call__`, that is
    required for all :class:`Rule`s.

    A Rule when called, `__call__`, creates a `List` of rules matches for each
    token, whereby each rule matched is defined by the
    :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object. These
    rules matches per token can then be, optionally, combined with other rule
    matches per token from other :class:`Rule` classes to then be ranked by a
    :class:`pymusas.rankers.lexicon_entry.LexiconEntryRanker`.
    '''

    @abstractmethod
    def __call__(self, tokens: List[str], lemmas: List[str],
                 pos_tags: List[str]) -> List[List[RankingMetaData]]:
        '''
        For each token it returns a `List` of rules matches defined by the
        :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object.

        Each `List` of `tokens`, `lemmas`, and `pos_tags` are assumed to be of
        equal length.

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
        ...
