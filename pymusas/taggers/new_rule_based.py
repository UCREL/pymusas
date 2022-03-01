from typing import List

from pymusas.rankers.lexicon_entry import LexiconEntryRanker, RankingMetaData
from pymusas.taggers.rules.rule import Rule


class RuleBasedTagger():
    '''
    The tagger when called, through :func:`__call__`, and given a sequence of
    tokens and their associated lingustic data (lemma, Part Of Speech (POS))
    to tag will apply one or more :class:`pymusas.taggers.rules.rule.Rule`s
    to create a list of possible candidate tags for each token in the sequence.
    Each candidate, represented as a
    :class:`pymusas.rankers.lexicon_entry.RankingMetaData` object, for each
    token is then Ranked using a
    `:class:`pymusas.rankers.lexicon_entry.LexiconEntryRanker` ranker. The best
    candidate and it's associated tag(s) for each token are then returned.

    If we cannot tag a token the default assigned tag is `Z99`.

    # Parameters

    rules : `List[pymusas.taggers.rules.rule.Rule]`
        A list of rules to apply to the sequence of tokens in the
        :func:`__call__`. The output from each rule is concatendated and given
        to the `ranker`.
    ranker : `pymusas.rankers.lexicon_entry.LexiconEntryRanker`
        A ranker to rank the output from all of the `rules`.

    # Instance Attributes

    rules : `List[pymusas.taggers.rules.rule.Rule]`
        The given `rules`.
    ranker : `pymusas.rankers.lexicon_entry.LexiconEntryRanker`
        The given `ranker`.

    # Examples
    ``` python
    >>> from pymusas.lexicon_collection import LexiconCollection
    >>> from pymusas.taggers.new_rule_based import RuleBasedTagger
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

    def __init__(self, rules: List[Rule], ranker: LexiconEntryRanker
                 ) -> None:

        self.rules = rules
        self.ranker = ranker

    def __call__(self, tokens: List[str], lemmas: List[str],
                 pos_tags: List[str]) -> List[List[str]]:
        '''
        Given a `List` of tokens, their associated lemmas and Part Of Speech tags
        it returns for each token a list of tags. These tags are generated based
        on the rules and ranker given to this model.
        
        The first tag in the `List` of tags is the most likely tag.

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

        `List[List[str]]`

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
        
        tags: List[List[str]] = []
        for best_rank in token_best_rank:
            if best_rank is None:
                tags.append(['Z99'])
                continue
            tags.append(list(best_rank.semantic_tags))
        
        return tags
