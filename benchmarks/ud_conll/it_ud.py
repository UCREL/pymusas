from typing import Callable, Dict, Union, List, Tuple
import time

import datasets
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.new_rule_based import RuleBasedTagger
from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.pos_mapper import USAS_CORE_TO_UPOS, UPOS_TO_USAS_CORE


def dataset_statistics(dataset: datasets.arrow_dataset.Dataset,
                       ) -> Dict[str, Union[str, int, float]]:
    statistics: Dict[str, Union[str, int, float]] = {}
    statistics['Universal Dependencies version'] = dataset.info.version
    statistics['Dataset Split'] = dataset.split
    statistics['Download Size'] = f'{dataset.info.download_size / (1024 ** 2):.2f} MB'
    statistics['Dataset Size'] = f'{dataset.info.size_in_bytes / (1024 ** 2):.2f} MB'
    statistics['Number of sentences'] = len(dataset)
    token_count = 0
    for sentence in dataset:
        token_count += len(sentence['tokens'])
    statistics['Number of tokens'] = token_count
    return statistics


single_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Italian/semantic_lexicon_ita.tsv"
mwe_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Italian/mwe-ita.tsv"

single_lexicon = LexiconCollection.from_tsv(single_lexicon_url)
single_lemma_lexicon = LexiconCollection.from_tsv(single_lexicon_url,
                                                  include_pos=False)

single_rule = SingleWordRule(single_lexicon, single_lemma_lexicon, pos_mapper=UPOS_TO_USAS_CORE)

import copy
a = copy.deepcopy(USAS_CORE_TO_UPOS)
a['verb'] = ['VERB']
a['conj'] = ['SCONJ']
print(a)
print(USAS_CORE_TO_UPOS)
mwe_lexicon = MWELexiconCollection.from_tsv(mwe_lexicon_url)
mwe_rule = MWERule(mwe_lexicon, pos_mapper=a)

rules = [single_rule, mwe_rule]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))

tagger = RuleBasedTagger(rules, ranker, set('PUNCT'), set(['NUM']))



dataset = datasets.load_dataset('universal_dependencies', 'it_isdt', split='test')
assert isinstance(dataset, datasets.arrow_dataset.Dataset)

upos_int_2_str: Callable[[int], str] = dataset.features['upos'].feature.int2str

t = time.time()
usas_tags_count = 0
raw_token_count = 0
number_mwe = 0
mwe_words = set()
for sentence_index, sentence in enumerate(dataset):
    text = sentence['text']
    idx = sentence['idx']
    raw_tokens = sentence['tokens']
    raw_lemmas = sentence['lemmas']
    raw_upos_tags = upos_int_2_str(sentence['upos'])
    
    tokens = []
    lemmas = []
    upos_tags = []
    for token, lemma, upos_tag in zip(raw_tokens, raw_lemmas, raw_upos_tags):
        if upos_tag != '_':
            tokens.append(token)
            lemmas.append(lemma)
            upos_tags.append(upos_tag)
    usas_tags_mwe_indexes = tagger(tokens, lemmas, upos_tags)
    
    mwe_indexes: List[Tuple[int, int]] = []
    for tags, indexes in usas_tags_mwe_indexes:
        if tags == ['Z99']:
            continue
        usas_tags_count += 1
        assert len(indexes) == 1
        if (indexes[0][1] - indexes[0][0]) > 1:
            mwe_indexes.append(indexes[0])
    for mwe_index in mwe_indexes:
        mwe_words.add(' '.join(tokens[mwe_index[0]: mwe_index[1]]))
    number_mwe += len(set(mwe_indexes))
    raw_token_count += len(tokens)

print(len(mwe_words))
print(mwe_words)
print(number_mwe)
print(raw_token_count)
print(usas_tags_count)
print(float(usas_tags_count) / float(raw_token_count))
print(time.time() - t)