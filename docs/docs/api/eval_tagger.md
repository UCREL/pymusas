<div className="source-div">
 <p><i>pymusas</i><strong>.eval_tagger</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/eval_tagger.py">[SOURCE]</a></p>
</div>
<div></div>

---

from pathlib import Path

from .lexicon_collection import LexiconCollection
from .taggers.rule_based import USASRuleBasedTagger


resource_dir = Path(__file__, '..', 'resources', 'welsh').resolve()
gold_path = Path(resource_dir, 'enhanced_gold_standard_data.txt')
lexicon_path = Path(resource_dir, 'semantic_lexicon_cy.usas.txt')

lexicon_lookup = LexiconCollection.from_tsv(lexicon_path, include_pos=True)
lemma_lexicon_lookup = LexiconCollection.from_tsv(lexicon_path, include_pos=False)
tagger = USASRuleBasedTagger(lexicon_lookup, lemma_lexicon_lookup)

total_tokens = 0
total_can_be_tagged = 0
correct = 0
line_count = 0
with gold_path.open('r') as gold_data:
    for line in gold_data:
        line_count += 1
        gold_tokens = line.split()
        gold_input_tokens = []
        gold_sem_tokens = []
        for gold_token in gold_tokens:
            token, lemma, core_pos, basic_pos, rich_pos, gold_sem = gold_token.split('|')
            gold_input_tokens.append((token, lemma, core_pos))
            gold_sem_tokens.append(gold_sem)

        predicted_sem_tokens = list(tagger.tag_tokens(gold_input_tokens))
        for gold, pred in zip(gold_sem_tokens, predicted_sem_tokens):
            if pred[0] == gold:
                correct += 1
        total_tokens += len(predicted_sem_tokens)
        total_can_be_tagged += len([token for token in predicted_sem_tokens if token != ['Z99']])
print(f'Coverage {(total_can_be_tagged / total_tokens) * 100:.2f}')
print(f'Accuracy {(correct / total_tokens) * 100}')
print(f'Line count: {line_count}')

