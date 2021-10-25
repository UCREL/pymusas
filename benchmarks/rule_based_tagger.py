import argparse
from collections.abc import Iterable
import logging
from pathlib import Path
import timeit
from resource import getrusage, RUSAGE_SELF
import sys
from typing import Union

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

def iter_over_gold_tags(benchmark_data_file: Path) -> Iterable[list[str]]:
    bench_data: list[list[str]] = []
    with benchmark_data_file.open('r') as data_fp:
        for line in data_fp:
            sentence_data = []
            tokens = line.split()
            for token in tokens:
                token, lemma, core_pos, basic_pos, rich_pos, gold_sem = token.split('|')
                sentence_data.append(gold_sem)
            bench_data.append(sentence_data)
    for sentence_data in bench_data:
        yield sentence_data

def get_number_tokens(benchmark_data_file: Path) -> int:
    number_tokens = 0
    with benchmark_data_file.open('r') as data_fp:
        for line in data_fp:
            number_tokens += len(line.split())
    return number_tokens

def speed_test() -> None:
    tagger = RuleBasedTagger(LEXICON_FILE, True)
    
    for sentence_data in iter_over_benchmark_data(BENCH_DATA_FILE):
        _ = tagger.tag_data(sentence_data)

def performance_test() -> dict[str, float]:
    '''
    coverage is the number of tokens that have been tagged, that are not tagged 
    with the unmatched tag (the `Z99` tag).

    :returns: A dictionary of coverage and accuracy results as a percentage.
    '''
    tagger = RuleBasedTagger(LEXICON_FILE, True)
    sentence_data = list(iter_over_benchmark_data(BENCH_DATA_FILE))
    sentence_gold_tags = list(iter_over_gold_tags(BENCH_DATA_FILE))
    
    total_count = 0
    correct = 0
    coverage = 0
    for data, gold_tags in zip(sentence_data, sentence_gold_tags):
        most_likely_tags = tagger.tag_data(data)
        for most_likely_tag, gold_tag in zip(most_likely_tags, gold_tags):
            most_likely_tag = most_likely_tag[0]
            if most_likely_tag == gold_tag:
                correct += 1
            if most_likely_tag != 'Z99':
                coverage += 1
            total_count += 1
    accuracy = (correct / total_count) * 100
    coverage = (coverage / total_count) * 100
    return {'accuracy': accuracy, 'coverage': coverage}


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    description = '''
    Runs the rule based tagger `number_runs` * `number_repeats` times. 
    Prints the average time to run the code based on the best repeat 
    performance e.g. if the first repeat performance took 50 seconds to run and 
    the number of runs is 10 then the average time to run the code would be 
    5 seconds. Based on this time it also reports the average number of 
    Tokens processed Per Second (TPS).
    '''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--number_runs', type=int, default=10,
                        help='Number of times to benchmark the rule based tagger per repeat')
    parser.add_argument('--number_repeats', type=int, default=3,
                        help='Number of times to repeat the runs')
    parser.add_argument('--markdown', action='store_true')

    args = parser.parse_args()

    valid_operating_systems = ['darwin', 'linux']
    if sys.platform not in valid_operating_systems:
        raise OSError('Can only run the benchmarks on Mac or '
                      'Linux operating systems')

    number_runs = args.number_runs
    number_repeats = args.number_repeats
    
    current_memory = getrusage(RUSAGE_SELF).ru_maxrss
    
    tagger = RuleBasedTagger(LEXICON_FILE, True)

    memory_used_to_load = getrusage(RUSAGE_SELF).ru_maxrss - current_memory
    mega_bytes_used_to_load = 0.0
    if sys.platform == 'linux':
        mega_bytes_used_to_load = memory_used_to_load / 1024
    elif sys.platform == 'darwin':
        mega_bytes_used_to_load = memory_used_to_load / (1024 ** 2)
    # no longer needed
    del tagger

    
    total_times: list[float] = timeit.repeat(stmt='speed_test()', 
                                             number=number_runs, 
                                             repeat=number_repeats, globals=globals())
    average_time = min(total_times) / number_runs
    tokens_per_second = get_number_tokens(BENCH_DATA_FILE) / average_time
    performance_results = performance_test()
    
    if args.markdown:
        print('| Memory (MB) | Tokens Per Second | Accuracy (%) | Coverage (%) |')
        print('|-------------|-------------------|--------------|--------------|')
        print(f'| {mega_bytes_used_to_load:.2f}  | {tokens_per_second:,.0f}  |'
              f' {performance_results["accuracy"]:.2f} | '
              f'{performance_results["coverage"]:.2f} |')
    else:
        print('-' * 40)
        print('Evaluating the resource usage')
        print('-' * 40)
        print(f'Number of {mega_bytes_used_to_load:.2f}MB used to load the '
              'rule based tagger.')
        print(f'Average time to run the rule based tagger: {average_time:.4f} seconds')
        print(f'Number of Tokens processed Per Second (TPS): {tokens_per_second:,.0f}')
        print(f'Average times based on the best performance across {number_repeats} '
              f'lots of {number_runs} runs.')

        print('-' * 40)
        print(f'Evaluating the performance')
        print('-' * 40)
        print(f'Accuracy (%): {performance_results["accuracy"]:.2f}%')
        print(f'Coverage (%): {performance_results["coverage"]:.2f}%')

