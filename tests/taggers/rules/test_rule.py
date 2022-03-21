from typing import List

from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.taggers.rules.rule import Rule


def test_rule() -> None:
    
    class TestRule(Rule):

        def __call__(self, tokens: List[str], lemmas: List[str],
                     pos_tags: List[str]) -> List[List[RankingMetaData]]:
            ranking_meta_data: List[List[RankingMetaData]] = [[]]
            return ranking_meta_data

        def to_bytes(self) -> bytes:
            return b'test'

        @staticmethod
        def from_bytes(bytes_data: bytes) -> 'TestRule':
            return TestRule()

    concrete_rule = TestRule()
    assert [[]] == concrete_rule([], [], [])
    assert isinstance(concrete_rule, Rule)

    assert b'test' == concrete_rule.to_bytes()
    assert isinstance(TestRule.from_bytes(b'test'), TestRule)
