from dataclasses import dataclass
from typing import Tuple

from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexical_match import LexicalMatch


@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class RankingMetaData:
    '''
    A RankingMetaData object contains all of the meta data about a lexicon
    entry match during the tagging process. This meta data can then be used
    to determine the ranking of the match compared to other matches within the
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
        What :class:`pymusas.rankers.lexical_match.LexicalMatch` the lexicon
        entry matched on.
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
