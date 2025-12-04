from pathlib import Path
from typing import Iterator, Dict
import argparse
import sys
from resource import getrusage, RUSAGE_SELF
import timeit

from pymusas.taggers.rule_based import USASRuleBasedTagger
from pymusas.lexicon_collection import LexiconCollection


def iter_over_benchmark_data(benchmark_data_file: Path
                             ) -> Iterator[list[tuple[str, str, str]]]:
    '''
    :returns: A sentence of `token`, `lemma`, and `USAS core POS tag`
    '''
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


def iter_over_gold_tags(benchmark_data_file: Path) -> Iterator[list[str]]:
    '''
    :returns: A sentence of Gold Semantic Lexicons
    '''
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


def get_metric_scores(benchmark_data_file: Path, tagger: USASRuleBasedTagger) -> Dict[str, float]:
    '''
    :returns: The coverage and accuracy of the tagger given the benchmarking data
    '''
    gold_data = iter_over_gold_tags(benchmark_data_file)
    input_data = iter_over_benchmark_data(benchmark_data_file)
    total_tokens = get_number_tokens(benchmark_data_file)
    non_z99_tokens = 0
    correct_tags = 0
    for input_sentence, gold_tags in zip(input_data, gold_data):
        for tag_index, tags in enumerate(tagger.tag_tokens(input_sentence)):
            gold_tag = gold_tags[tag_index]
            predicted_tag = tags[0]
            if predicted_tag != 'Z99':
                non_z99_tokens += 1
            if gold_tag == predicted_tag:
                correct_tags += 1
    coverage = 100 * (float(non_z99_tokens) / float(total_tokens))
    accuracy = 100 * (float(correct_tags) / float(total_tokens))
    return {'accuracy': accuracy, 'coverage': coverage}


def speed_test(benchmark_data_file: Path, tagger: USASRuleBasedTagger) -> None:
    
    for sentence_data in iter_over_benchmark_data(benchmark_data_file):
        _ = tagger.tag_tokens(sentence_data)


if __name__ == "__main__":
    description = '''
    Runs the rule based tagger `number_runs` * `number_repeats` times.
    Prints the average time to run the code based on the best repeat
    performance e.g. if the first repeat performance took 50 seconds to run and
    the number of runs is 10 then the average time to run the code would be
    5 seconds. Based on this time it also reports the average number of
    Tokens processed Per Second (TPS)
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
    
    lexicon = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Welsh/semantic_lexicon_cy.tsv'
    lexicon_lookup = LexiconCollection.from_tsv(lexicon, include_pos=True)
    lemma_lexicon_lookup = LexiconCollection.from_tsv(lexicon, include_pos=False)
    tagger = USASRuleBasedTagger(lexicon_lookup=lexicon_lookup,
                                 lemma_lexicon_lookup=lemma_lexicon_lookup)

    memory_used_to_load = getrusage(RUSAGE_SELF).ru_maxrss - current_memory
    mega_bytes_used_to_load = 0.0
    if sys.platform == 'linux':
        mega_bytes_used_to_load = memory_used_to_load / 1024
    elif sys.platform == 'darwin':
        mega_bytes_used_to_load = memory_used_to_load / (1024 ** 2)

    RESOURCE_DIR = Path(__file__, '..', '..', 'resources', 'welsh').resolve()
    BENCH_DATA_FILE = Path(RESOURCE_DIR, 'enhanced_gold_standard_data.txt')

    total_times: list[float] = timeit.repeat(stmt='speed_test(BENCH_DATA_FILE, tagger)',
                                             number=number_runs,
                                             repeat=number_repeats, globals=globals())
    average_time = min(total_times) / number_runs
    tokens_per_second = get_number_tokens(BENCH_DATA_FILE) / average_time
    performance_results = get_metric_scores(BENCH_DATA_FILE, tagger)
    
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
        print('Evaluating the performance')
        print('-' * 40)
        print(f'Accuracy (%): {performance_results["accuracy"]:.2f}%')
        print(f'Coverage (%): {performance_results["coverage"]:.2f}%')
