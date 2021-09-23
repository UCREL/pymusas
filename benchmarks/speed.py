from pathlib import Path

from pymusas.basic_tagger import RuleBasedTagger

RESOURCE_DIR = Path(__file__, '..', 'resources', 'welsh').resolve()

def speed_test():
    lexicon = Path(RESOURCE_DIR, 'semantic_lexicon_cy.usas.txt')
    bench_data_file = Path(RESOURCE_DIR, 'enhanced_gold_standard_data.txt')
    bench_data = []
    with bench_data_file.open('r') as data_fp:
        for line in data_fp:
            tokens = line.split()
            for token in tokens:
                token, lemma, core_pos, basic_pos, rich_pos, gold_sem = token.split('|')
                bench_data.append((token, lemma, core_pos))
    print(f"Number of tokens to benchmark the tagger: {len(bench_data)}")
    
    tagger = RuleBasedTagger(lexicon, True)
    tagged_data = tagger.tag_data(bench_data)

if __name__ == "__main__":
    speed_test()