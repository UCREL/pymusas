from typing import List, Optional, Set, Tuple


class NeuralTagger():
    '''
    The tagger when called, through :func:`__call__`, and given a sequence of
    tokens, to create a list of possible candidate tags for each token in the sequence.
    
    The number of possible candidate tags for each token is determined by the
    `top_n` parameter, of which this is then stored in the `top_n` attribute.

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
    >>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
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

    def __call__(self, tokens: List[str]
                 ) -> List[Tuple[List[str], List[Tuple[int, int]]]]:
        '''
        Given a `List` of tokens it returns for each token:
        
        1. A `List` of tags. The first tag in the `List` of tags is the most likely tag.
        2. A `List` of `Tuples` whereby each `Tuple` indicates the start and end
        token index of the associated Multi Word Expression (MWE). If the `List` contains
        more than one `Tuple` then the MWE is discontinuous. For single word
        expressions the `List` will only contain 1 `Tuple` which will be
        (token_start_index, token_start_index + 1).

        NOTE: Currently the Neural Tagger is limited to only tagging single word
        expressions.
        
        # Parameters

        tokens : `List[str]`
            A List of full text form of the tokens to be tagged.
 
        # Returns

        `List[Tuple[List[str], List[Tuple[int, int]]]]`
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
