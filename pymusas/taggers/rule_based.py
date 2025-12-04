from typing import List, Optional, Set, Tuple

from pymusas.rankers.lexicon_entry import LexiconEntryRanker, RankingMetaData
from pymusas.taggers.rules.rule import Rule


class RuleBasedTagger():
    '''
    The tagger when called, through :func:`__call__`, and given a sequence of
    tokens and their associated lingustic data (lemma, Part Of Speech (POS))
    will apply one or more :class:`pymusas.taggers.rules.rule.Rule`s
    to create a list of possible candidate tags for each token in the sequence.
    Each candidate, represented as a
    :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object, for each
    token is then Ranked using a
    :class:`pymusas.rankers.lexicon_entry.LexiconEntryRanker` ranker. The best
    candidate and it's associated tag(s) for each token are then returned along
    with a `List` of token indexes indicating if the token is part of a Multi
    Word Expression (MWE).

    If we cannot tag a token then the following process will happen:
    1. If the token's POS tag is in `default_punctuation_tags` then it will assign the
    tag `PUNCT`.
    2. If the token's POS tag is in `default_number_tags` then it will assign the tag
    `N1`.
    3. Assign the default tag `Z99`.

    # Parameters

    rules : `List[pymusas.taggers.rules.rule.Rule]`
        A list of rules to apply to the sequence of tokens in the
        :func:`__call__`. The output from each rule is concatendated and given
        to the `ranker`.
    ranker : `pymusas.rankers.lexicon_entry.LexiconEntryRanker`
        A ranker to rank the output from all of the `rules`.
    default_punctuation_tags : `Set[str]`, optional (default = `None`)
        The POS tags that represent punctuation. If `None` then we will use
        the `Set`: `set(['punc'])`.
    default_number_tags : `Set[str]`, optional (default = `None`)
        The POS tags that represent numbers. If `None` then we will use
        the `Set`: `set(['num'])`.
    
    # Instance Attributes

    rules : `List[pymusas.taggers.rules.rule.Rule]`
        The given `rules`.
    ranker : `pymusas.rankers.lexicon_entry.LexiconEntryRanker`
        The given `ranker`.
    default_punctuation_tags : `Set[str]`
        The given `default_punctuation_tags`
    default_number_tags : `Set[str]`
        The given `default_number_tags`

    # Examples
    ``` python
    >>> from pymusas.lexicon_collection import LexiconCollection
    >>> from pymusas.taggers.rule_based import RuleBasedTagger
    >>> from pymusas.taggers.rules.single_word import SingleWordRule
    >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
    >>> from pymusas.pos_mapper import BASIC_CORCENCC_TO_USAS_CORE
    >>> welsh_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Welsh/semantic_lexicon_cy.tsv'
    >>> lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
    >>> lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
    >>> single_word_rule = SingleWordRule(lexicon_lookup, lemma_lexicon_lookup,
    ...                                   BASIC_CORCENCC_TO_USAS_CORE)
    >>> ranker = ContextualRuleBasedRanker(1, 0)
    >>> tagger = RuleBasedTagger([single_word_rule], ranker)

    ```
    '''

    def __init__(self, rules: List[Rule], ranker: LexiconEntryRanker,
                 default_punctuation_tags: Optional[Set[str]] = None,
                 default_number_tags: Optional[Set[str]] = None) -> None:

        self.rules = rules
        self.ranker = ranker

        self.default_punctuation_tags = set(['punc'])
        if default_punctuation_tags is not None:
            self.default_punctuation_tags = default_punctuation_tags
        
        self.default_number_tags = set(['num'])
        if default_number_tags is not None:
            self.default_number_tags = default_number_tags

    def __call__(self, tokens: List[str], lemmas: List[str],
                 pos_tags: List[str]) -> List[Tuple[List[str],
                                                    List[Tuple[int, int]]
                                                    ]]:
        '''
        Given a `List` of tokens, their associated lemmas and
        Part Of Speech (POS) tags it returns for each token:
        
        1. A `List` of tags. The first tag in the `List` of tags is the most likely tag.
        2. A `List` of `Tuples` whereby each `Tuple` indicates the start and end
        token index of the associated Multi Word Expression (MWE). If the `List` contains
        more than one `Tuple` then the MWE is discontinuous. For single word
        expressions the `List` will only contain 1 `Tuple` which will be
        (token_start_index, token_start_index + 1).
    
        All the generated tags and MWEs are based on the rules and ranker given
        to this model.

        **NOTE** this tagger has been designed to be flexible with the amount of
        resources avaliable, if you do not have POS or lemma information assign
        them a `List` of empty strings.
        
        # Parameters

        tokens : `List[str]`
            A List of full text form of the tokens to be tagged.
        lemmas : `List[str]`
            The List of lemma/base form of the tokens to be tagged.
        pos_tags : `List[str]`
            The List of POS tags of the tokens to be tagged.
        
        # Returns

        `List[Tuple[List[str], List[Tuple[int, int]]]]`

        # Raises

        `ValueError`
            If the length of the `tokens`, `lemmas`, and `pos_tags` are not of
            the same legnth.
        '''

        tokens_length = len(tokens)
        pos_tags_length = len(pos_tags)
        lemmas_length = len(lemmas)
        length_error_msg = ('The `tokens`, `lemmas`, or `pos_tags` are not '
                            'of the the same length, their lengths respectively:'
                            f' {tokens_length}, {pos_tags_length}, {lemmas_length}')
        if (tokens_length != pos_tags_length) or (tokens_length != lemmas_length):
            raise ValueError(length_error_msg)
            
        token_ranking_meta_data: List[List[RankingMetaData]] \
            = [[] for _ in range(len(tokens))]
        for rule in self.rules:
            rule_ranking_meta_data = rule(tokens, lemmas, pos_tags)
            for token_index, ranking_meta_data in enumerate(rule_ranking_meta_data):
                token_ranking_meta_data[token_index].extend(ranking_meta_data)

        token_ranks, token_best_rank = self.ranker(token_ranking_meta_data)
        
        tags_indexes: List[Tuple[List[str], List[Tuple[int, int]]]] = []
        for token_index, best_rank in enumerate(token_best_rank):
            if best_rank is None:
                pos_tag = pos_tags[token_index]
                if pos_tag in self.default_punctuation_tags:
                    tags_indexes.append((['PUNCT'],
                                         [(token_index, token_index + 1)]))
                elif pos_tag in self.default_number_tags:
                    tags_indexes.append((['N1'],
                                         [(token_index, token_index + 1)]))
                else:
                    tags_indexes.append((['Z99'],
                                         [(token_index, token_index + 1)]))
                continue
            tags = list(best_rank.semantic_tags)
            indexes = [(best_rank.token_match_start_index,
                        best_rank.token_match_end_index)]
            tags_indexes.append((tags, indexes))
        
        return tags_indexes
