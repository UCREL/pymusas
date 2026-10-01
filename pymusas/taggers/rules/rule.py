from abc import abstractmethod

from pymusas.base import Serialise
from pymusas.rankers.ranking_meta_data import RankingMetaData


class Rule(Serialise):
    '''
    An **abstract class** that defines the basic method, `__call__`, that is
    required for all :class:`Rule`s.

    A Rule when called, `__call__`, creates a `list` of rules matches for each
    token, whereby each rule matched is defined by the
    :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object. These
    rules matches per token can then be, optionally, combined with other rule
    matches per token from other :class:`Rule` classes to then be ranked by a
    :class:`pymusas.rankers.lexicon_entry.LexiconEntryRanker`.
    '''

    @abstractmethod
    def __call__(self, tokens: list[str], lemmas: list[str],
                 pos_tags: list[str]) -> list[list[RankingMetaData]]:
        '''
        For each token it returns a `list` of rules matches defined by the
        :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object.

        Each `list` of `tokens`, `lemmas`, and `pos_tags` are assumed to be of
        equal length.

        # Parameters

        tokens : `list[str]`
            The tokens that are within the text.
        lemmas : `list[str]`
            The lemmas of the tokens.
        pos_tags : `list[str]`
            The Part Of Speech tags of the tokens.

        # Returns

        `list[list[RankingMetaData]]`
        '''
        ...  # pragma: no cover

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        ...  # pragma: no cover
