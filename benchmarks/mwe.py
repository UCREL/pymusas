'''
This benchmarks the MWE rule based tagger with regards to direct lookup, therefore
does not test any of the special syntax rules like wildcards or curly braces.
'''
import argparse
import collections
import timeit
from typing import List, OrderedDict, Tuple
from random import randint

from pymusas.lexicon_collection import MWELexiconCollection


def run_mwe(sentences_to_tag: List[str], sentence_tokens_exist_in_lexicon: bool,
            mwe_lexicon: OrderedDict[str, List[str]]) -> List[Tuple[int, bool, int, float]]:
    '''
    # Parameters
    
    sentences_to_tag : `List[str]`
        A list of sentences to tag.
    sentence_tokens_exist_in_lexicon : `bool`
        Whether all of the tokens in each sentence exist in the `mwe_lexicon`
    mwe_lexicon : `OrderedDict[str, List[str]]`
        A MWE lexicon lookup that contains MWE templates as keys and a `List` of
        semantic tags as values. The Dictionary should be ordered based on the
        n-gram of the templates, whereby the order should be largest value of
        *n* first and smallest last.
    
    # Returns

    `List[Tuple[int, bool, int, float]]`
    '''
    time_data: List[Tuple[int, bool, int, float]] = []
    for mwe_test_n_gram in sentences_to_tag:
        mwe_test_n_gram = mwe_test_n_gram.strip()
        tokens = []
        lemmas = []
        pos_tags = []
        for mwe in mwe_test_n_gram.split():
            token, pos = mwe.split('_')
            tokens.append(token)
            lemmas.append(token)
            pos_tags.append(pos)
        total_times: list[float] = timeit.repeat(stmt='_tag_mwe(tokens, lemmas, pos_tags, mwe_lexicon)',
                                                 number=number_runs,
                                                 repeat=number_repeats,
                                                 setup='from pymusas.taggers.rule_based import _tag_mwe',
                                                 globals=locals())
        average_time = min(total_times) / number_runs
        mwe_lexicon_size = len(mwe_lexicon)
        data = (mwe_lexicon_size, sentence_tokens_exist_in_lexicon,
                len(tokens), average_time)
        time_data.append(data)
    return time_data


if __name__ == '__main__':
    description = '''
    Runs the MWE part of the rule based tagger `number_runs` * `number_repeats` times.
    Prints the average time to run the code based on the best repeat
    performance e.g. if the first repeat performance took 50 seconds to run and
    the number of runs is 10 then the average time to run the code would be
    5 seconds. Further it only runs it against sentences of length 50, 100,
    and 150 tokens that DO and DO NOT exist in the MWE lexicon. In addition we
    also vary the size of the MWE lexicon by using the whole lexicon and then
    roughly half the lexicon. Further more the MWE lexicon only contains direct
    lookup MWEs, e.g. contains no wildcard or curly braces MWE templates.
    '''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--number_runs', type=int, default=100,
                        help='Number of times to benchmark the rule based tagger per repeat')
    parser.add_argument('--number_repeats', type=int, default=5,
                        help='Number of times to repeat the runs')
    args = parser.parse_args()

    number_repeats = args.number_repeats
    number_runs = args.number_runs
    
    spanish_mwe_lexicon = MWELexiconCollection.from_tsv('https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Spanish/mwe-es.tsv')
    
    half_spanish_mwe_lexicon: OrderedDict[str, List[str]] = collections.OrderedDict()
    for mwe_template, semantic_tags in spanish_mwe_lexicon.items():
        if randint(0, 1):
            half_spanish_mwe_lexicon[mwe_template] = semantic_tags
    half_spanish_mwe_lexicon['A_pnoun Arnoia_pnoun'] = spanish_mwe_lexicon['A_pnoun Arnoia_pnoun']
    
    mwes_that_do_not_exist_in_the_lexicon = ['hello_noun ' * 50,
                                             'hello_noun ' * 100,
                                             'hello_noun ' * 150]
    mwes_that_do_exist_in_the_lexicon = ['A_pnoun Arnoia_pnoun ' * 25,
                                         'A_pnoun Arnoia_pnoun ' * 50,
                                         'A_pnoun Arnoia_pnoun ' * 75]
    
    time_data: List[Tuple[int, bool, int, float]] = []
    time_data.extend(run_mwe(mwes_that_do_not_exist_in_the_lexicon, False, spanish_mwe_lexicon))
    time_data.extend(run_mwe(mwes_that_do_not_exist_in_the_lexicon, False, half_spanish_mwe_lexicon))
    time_data.extend(run_mwe(mwes_that_do_exist_in_the_lexicon, True, spanish_mwe_lexicon))
    time_data.extend(run_mwe(mwes_that_do_exist_in_the_lexicon, True, half_spanish_mwe_lexicon))
    
    print('| MWE Lexicon Size (number MWE templates) '
          '| All sentence tokens exist in MWE lexicon '
          '| Sentence Length (tokens) | Time Taken (s) |')
    print('|---------------|----------------|---------------|----------------|')
    for lexicon_size, exist, sentence_length, time_taken in time_data:
        print(f'| {lexicon_size} | {exist} | {sentence_length} | {time_taken:.4f} |')
