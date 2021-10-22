import json
from pathlib import Path
from typing import Generator, List, Tuple

from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.rule_based import USASRuleBasedTagger


DATA_DIR = Path(__file__, '..', '..', 'data').resolve()


def test_tag_data() -> None:
    test_data_path = Path(DATA_DIR, 'rule_based_input_output.json')
    test_data: List[Tuple[str, str, str]] = []
    
    expected_usas_tags: List[List[str]] = []
    with test_data_path.open('r') as test_data_fp:
        for token_data in json.load(test_data_fp):
            token = token_data['token']
            lemma = token_data['lemma']
            pos = token_data['pos']
            test_data.append((token, lemma, pos))
            expected_usas_tags.append([token_data['usas']])

    lexicon_path = Path(DATA_DIR, 'lexicon.tsv')
    lexicon_lookup = LexiconCollection.from_tsv(lexicon_path, include_pos=True)
    lemma_lexicon_lookup = LexiconCollection.from_tsv(lexicon_path, include_pos=False)
    tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)
    output_usas_tags = tagger.tag_tokens(test_data)
    assert isinstance(output_usas_tags, Generator)

    assert len(expected_usas_tags) == len(list(output_usas_tags))
    for expected, output, context in zip(expected_usas_tags,
                                         output_usas_tags,
                                         test_data):
        assert expected == output, context
