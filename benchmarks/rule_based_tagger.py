import argparse
from collections.abc import Iterable
import logging
from pathlib import Path
import timeit
from resource import getrusage, RUSAGE_SELF
import sys

from pymusas.basic_tagger import RuleBasedTagger

RESOURCE_DIR = Path(__file__, '..', '..', 'resources', 'welsh').resolve()
BENCH_DATA_FILE = Path(RESOURCE_DIR, 'enhanced_gold_standard_data.txt')
LEXICON_FILE = Path(RESOURCE_DIR, 'semantic_lexicon_cy.usas.txt')

def iter_over_benchmark_data(benchmark_data_file: Path
                             ) -> Iterable[list[tuple[str, str, str]]]:
    bench_data: list[list[tuple[str, str, str]]] = []
    with benchmark_data_file.open('r') as data_fp:
        for line in data_fp:
            sentence_data = []
            tokens = line.split()
            for token in tokens:
                token, lemma, core_pos, basic_pos, rich_pos, gold_sem = token.split('|')
                sentence_data.append((token, lemma, core_pos))
            bench_data.append(sentence_data)
    for sentence_data in bench_data:
        yield sentence_data

def get_number_tokens(benchmark_data_file: Path) -> int:
    number_tokens = 0
    with benchmark_data_file.open('r') as data_fp:
        for line in data_fp:
            number_tokens += len(line.split())
    return number_tokens

def speed_test():
    tagger = RuleBasedTagger(LEXICON_FILE, True)
    
    for sentence_data in iter_over_benchmark_data(BENCH_DATA_FILE):
        tagged_data = tagger.tag_data(sentence_data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    description = '''
    Runs the rule based tagger `number_runs` * `number_repeats` times. 
    Prints the average time to run the code based on the best repeat 
    performance e.g. if the first repeat performance took 50 seconds to run and 
    the number of runs is 10 then the average time to run the code would be 
    5 seconds. Based on this time it also reports the average number of 
    Tokens Processed per Second (TPS).
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--number_runs', type=int, default=10,
                        help='Number of times to benchmark the rule based tagger per repeat')
    parser.add_argument('--number_repeats', type=int, default=3,
                        help='Number of times to repeat the runs')

    args = parser.parse_args()

    number_runs = args.number_runs
    number_repeats = args.number_repeats
    
    current_memory = 0.0
    if sys.platform == 'linux' or sys.platform == 'darwin':
        current_memory = getrusage(RUSAGE_SELF).ru_maxrss

    
    tagger = RuleBasedTagger(LEXICON_FILE, True)

    if sys.platform == 'linux':
        memory_used_to_load = getrusage(RUSAGE_SELF).ru_maxrss - current_memory
        mega_bytes_used_to_load = memory_used_to_load / 1024
        print(f'Number of {mega_bytes_used_to_load:.2f}MB used to load the '
              'rule based tagger.')
    elif sys.platform == 'darwin':
        memory_used_to_load = getrusage(RUSAGE_SELF).ru_maxrss - current_memory
        mega_bytes_used_to_load = memory_used_to_load / (1024 ** 2)
        print(f'Number of {mega_bytes_used_to_load:.2f}MB used to load the '
              'rule based tagger.')
    # no longer needed
    del tagger

    
    total_times: list[float] = timeit.repeat(stmt='speed_test()', 
                                             number=number_runs, 
                                             repeat=number_repeats, globals=globals())
    average_time = min(total_times) / number_runs
    tokens_per_second = get_number_tokens(BENCH_DATA_FILE) / average_time
    print(f'Average time to run the rule based tagger: {average_time:.4f} seconds')
    print(f'Number of Tokens Processed per Second (TPS): {tokens_per_second:.2f}')
    print(f'Average times based on the best performance across {number_repeats} '
          f'lots of {number_runs} runs.')
    
