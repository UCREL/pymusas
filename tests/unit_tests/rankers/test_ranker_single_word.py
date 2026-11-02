from pymusas.lexicon_collection import LexiconType
from pymusas.rankers.lexical_match import LexicalMatch
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.rankers.single_word import SingleWordRanker


def _match(exclude_pos_information: bool, lexical_match: LexicalMatch,
           semantic_tag: str = 'Z1',
           lexicon_type: LexiconType = LexiconType.SINGLE_NON_SPECIAL
           ) -> RankingMetaData:
    return RankingMetaData(lexicon_type, 1, 0,
                           exclude_pos_information, lexical_match, 0, 1,
                           'entry', (semantic_tag,))


def _ordered_matches() -> list[RankingMetaData]:
    '''
    All kinds of single word match of one token, from best to worst ranked.
    Exact matches that use POS information, then exact matches that do not,
    then `autotag` matches, which always use POS information. Within each
    of these Token < Lemma < Lower token < Lower lemma.
    '''
    ordered_matches = [_match(exclude_pos, lexical_match)
                       for exclude_pos in [False, True]
                       for lexical_match in LexicalMatch]
    ordered_matches += [_match(False, lexical_match,
                               lexicon_type=LexiconType.SINGLE_AUTOTAG)
                        for lexical_match in LexicalMatch]
    return ordered_matches


def test_sort_key() -> None:
    assert (False, False, 1) == SingleWordRanker.sort_key(_match(False, LexicalMatch.TOKEN))
    assert (False, True, 4) == SingleWordRanker.sort_key(_match(True, LexicalMatch.LEMMA_LOWER))
    autotag_match = _match(False, LexicalMatch.LEMMA, lexicon_type=LexiconType.SINGLE_AUTOTAG)
    assert (True, False, 2) == SingleWordRanker.sort_key(autotag_match)


def test_best_match() -> None:
    assert SingleWordRanker.best_match([]) is None

    ordered_matches = _ordered_matches()
    for index, expected_match in enumerate(ordered_matches):
        worse_matches = ordered_matches[index + 1:]
        assert expected_match == SingleWordRanker.best_match(worse_matches + [expected_match])
        assert expected_match == SingleWordRanker.best_match([expected_match] + worse_matches)


def test_best_match_joint_ranked() -> None:
    first = _match(False, LexicalMatch.TOKEN, 'A1')
    second = _match(False, LexicalMatch.TOKEN, 'A2')
    assert first is SingleWordRanker.best_match([first, second])
    assert second is SingleWordRanker.best_match([second, first])


def test_sort_key_agrees_with_contextual_rule_based_ranker() -> None:
    '''
    Single word matches of one token only differ in their lexicon type,
    whether they use POS information, and their lexical match. Sorting all
    12 kinds of match with `sort_key` must give the same order as the
    `ContextualRuleBasedRanker`, which means both rankers agree on every pair
    of matches.
    '''
    matches = list(reversed(_ordered_matches()))
    contextual_ranks = ContextualRuleBasedRanker(1, 0)([matches])[0][0]
    contextual_order = [match for _, match in sorted(zip(contextual_ranks, matches),
                                                     key=lambda rank_match: rank_match[0])]
    assert contextual_order == sorted(matches, key=SingleWordRanker.sort_key)
    assert contextual_order == _ordered_matches()
