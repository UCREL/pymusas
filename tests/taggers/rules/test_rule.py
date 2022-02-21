from typing import List

from pymusas.rankers.lexicon_entry import RankingMetaData
from pymusas.taggers.rules.rule import Rule


def test_rule() -> None:
    
    class TestRule(Rule):

        def __call__(self, tokens: List[str], lemmas: List[str],
                     pos_tags: List[str]) -> List[List[RankingMetaData]]:
            ranking_meta_data: List[List[RankingMetaData]] = [[]]
            return ranking_meta_data
    concrete_rule = TestRule()
    assert [[]] == concrete_rule([], [], [])
    assert isinstance(concrete_rule, Rule)
