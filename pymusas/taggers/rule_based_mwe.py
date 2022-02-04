from typing import Dict, Iterator, List, Tuple, Any, Sequence


def n_gram_indexes(sequence: Sequence[Any], min_n: int, max_n: int
                   ) -> Iterator[Tuple[int, int]]:
    '''
    Returns n-grams as indexes of the `sequence`,
    in the range from `max_n` to `min_n`, in
    order of largest n-grams first. If you only want one n-gram size then set
    `min_n` equal to `max_n`, for example to get bi-grams indexes set both
    `min_n` and `max_n` to `2`.

    # Parameters

    sequence : `Sequence[Any]`
        The sequence to generate n-gram indexes from.
    min_n : `int`
        Minimum size n-gram. Has to be greater than `0`.
    max_n : `int`
        Maximim size n-gram. This has to be equal to or greater than `min_n`.
        If this is greater than the length of the `sequence` then it is set to
        length of the `sequence`.

    # Returns

    `Iterator[Sequence[Any]]`

    # Raises

    `ValueError`
        If `min_n` is less than `1` or `max_n` is less than `min_n`.

    # Examples

    ``` python
    >>> from pymusas.taggers.rule_based_mwe import n_gram_indexes
    >>> tokens = ['hello', 'how', 'are', 'you', ',']
    >>> token_n_gram_indexes = n_gram_indexes(tokens, 2, 3)
    >>> expected_n_grams_indexes = [(0, 3), (1, 4), (2, 5), (0, 2), (1, 3), (2, 4), (3, 5)]
    >>> assert expected_n_grams_indexes == token_n_gram_indexes

    ```
    '''
    if min_n < 1:
        raise ValueError(f'`min_n` has to be greater than 0. Value given {min_n}')
    if min_n > max_n:
        raise ValueError(f'`max_n` ({max_n}) cannot be less than `min_n` ({min_n})')
    
    sequence_size = len(sequence)
    max_n = sequence_size if max_n > sequence_size else max_n
    
    for n_gram_size in range(max_n, min_n - 1, -1):
        for sequence_index in range(sequence_size):
            last_n_gram_index = sequence_index + n_gram_size
            if last_n_gram_index > sequence_size:
                break
            yield (sequence_index, last_n_gram_index)


def n_grams(sequence: Sequence[Any], min_n: int, max_n: int) -> Iterator[Sequence[Any]]:
    '''
    Returns n-grams, in the range from `max_n` to `min_n`, of the `sequence` in
    order of largest n-grams first. If you only want one n-gram size then set
    `min_n` equal to `max_n`, for example to get bi-grams set both `min_n` and
    `max_n` to `2`.

    # Parameters

    sequence : `Sequence[Any]`
        The sequence to generate n-grams from.
    min_n : `int`
        Minimum size n-gram. Has to be greater than `0`.
    max_n : `int`
        Maximim size n-gram. This has to be equal to or greater than `min_n`.
        If this is greater than the length of the `sequence` then it is set to
        length of the `sequence`.

    # Returns

    `Iterator[Sequence[Any]]`

    # Raises

    `ValueError`
        If `min_n` is less than `1` or `max_n` is less than `min_n`.

    # Examples

    ``` python
    >>> from pymusas.taggers.rule_based_mwe import n_grams
    >>> tokens = ['hello', 'how', 'are', 'you', ',']
    >>> token_n_grams = n_grams(tokens, 2, 3)
    >>> expected_n_grams = [['hello', 'how', 'are'], ['how', 'are', 'you'], ['are', 'you', ','],
    ...                     ['hello', 'how'], ['how', 'are'], ['are', 'you'], ['you', ',']]
    >>> assert expected_n_grams == token_n_grams

    ```
    '''
    for n_gram_index in n_gram_indexes(sequence, min_n, max_n):
        start_index, end_index = n_gram_index
        yield sequence[start_index: end_index]


def _tag_mwe(tokens: List[str], lemmas: List[str], pos_tags: List[str],
             mwe_lexicon_lookup: Dict[str, List[str]], largest_mwe_in_lexicon: int
             ) -> Tuple[List[List[str]], List[int]]:
    '''
    We want to:
    1. Find the longest n-grams
    2. Search through those n-grams in the following order:
        1. Match on tokens and POS tags.
        2. Match on lemma and POS tags.
        3. Match on lower cased tokens and POS tags.
        4. Match on lower cased lemmas and POS tags.
    3. Each time we have a match record the match with the following data:
        1. Matched MWE template. This MWE template should then correspond to a
        lookup table in the MWELexiconCollection defining the following attributes:
            1. Type of MWE template, e.g. wildcard, direct, or curly braces.
            2. Number of tokens in the template.
            3. Number of wildcards in the tokens/lemmas
            4. Number of wildcard in the POS tags
        2. The number of tokens in the match
        3. Matched on token or lemma
        4. Matched on lower cased
    

    Given the tokens, lemmas, and POS tags for each word in a text along with a
    Multi Word Expression lexicon lookup, it will return a `Tuple` of length 2
    containing:
    
    1. `List` of USAS semantic tags for each token, whereby the most likely tag is the first tag
    in the `List`. The `List` of tags returned are based on the MWE rules below.
    2. `List` of ids, each id defines which MWE a token belongs too, an id of `0`
    represents a token that is not part of an MWE.

    # MWE Rules
    
    The MWE lexicon lookup contains a MWE template as it's key and a
    `List` of semantic tags as it's value. Given this:

    Starting with the longest n-gram templates assign semantic tags to matching
    tokens in the following priority order, this priority order also determines
    which MWE is chosen over another if they are overlapping, if the level of
    priority is the same then the left most match takes priority:

        1. Match on tokens and POS tags.
        2. Match on lemma and POS tags.
        3. Match on lower cased tokens and POS tags.
        4. Match on lower cased lemmas and POS tags.
    
    Then repeat this process for `n = n-1`. Stop when `n==2`, e.g. a
    MWE has to have at last 2 tokens.

    **Note** that the MWE rules may not cover all tokens, therefore for any
    token not covered it will return the `Z99` semantic tag. For example
    if the semantic tags returned from this function are:
    `[[A1], [A1], [Z2, Z3], [Z2, Z3], [Z99]]` then the last token was not
    covered by any of the MWE rules, hence why it returned `[Z99]`.
    
    # Parameters

    tokens : `List[str]`
        The tokens that are within the text.
    lemmas : `List[str]`
        The lemmas of the tokens.
    pos_tags : `List[str]`
        The Part Of Speech tags of the tokens.
    mwe_lexicon_lookup : `Dict[str, List[str]]`
        A MWE lexicon lookup that contains MWE templates as keys and a `List` of
        semantic tags as values.
    largest_mwe_in_lexicon : `int`
        The largest n-gram MWE template in the `mwe_lexicon_lookup`. For instance
        the MWE template `land_noun rover_noun discovery_noun` would be a 3-gram
        template, and if the all other MWE templates within the `mwe_lexicon_lookup`
        are 2-gram then the `largest_mwe_in_lexicon` would be equal to `3`.
    
    # Returns

    `Tuple[List[List[str]], List[int]]`
    '''

    def tag_n_gram_indexes(_n_gram_indexes: List[Tuple[int, int]],
                           token_pos: List[str], lemma_pos: List[str],
                           token_lower_pos: List[str], lemma_lower_pos: List[str],
                           mwe_semantic_tags: List[List[str]],
                           mwe_ids: List[int], current_mwe_id: int) -> int:
        '''
        Given a `List` of n gram indexes whereby all grams have the same value
        of *n* it will tag the tokens in the priority order defined in the
        MWE Rules, stated in the top level function doc string. All semantic tags
        and their associated ids will be added to the `mwe_semantic_tags` and
        `mwe_ids` lists respectively.
        
        The return value is the `current_mwe_id` which is incremented each time
        an MWE is tagged.
        '''
        token_priority_list = [token_pos, lemma_pos, token_lower_pos, lemma_lower_pos]
        for token_list in token_priority_list:
            for n_gram_index in _n_gram_indexes:
                start_index, end_index = n_gram_index
                mwe_template = ''
                for token_index in range(start_index, end_index):
                    if (token_index + 1) == end_index:
                        mwe_template += f'{token_list[token_index]}'
                        continue
                    mwe_template += f'{token_list[token_index]} '
                semantic_tags = mwe_lexicon_lookup.get(mwe_template, None)
                if semantic_tags is None:
                    continue
                if any(mwe_ids[start_index: end_index]):
                    continue
                for token_index in range(start_index, end_index):
                    mwe_ids[token_index] = current_mwe_id
                    mwe_semantic_tags[token_index] = semantic_tags
                current_mwe_id += 1
        return current_mwe_id
                
    token_pos: List[str] = []
    token_lower_pos: List[str] = []
    lemma_pos: List[str] = []
    lemma_lower_pos: List[str] = []
    for token, lemma, pos in zip(tokens, lemmas, pos_tags):
        token_pos.append(f'{token}_{pos}')
        token_lower_pos.append(f'{token}_{pos}'.lower())
        lemma_pos.append(f'{lemma}_{pos}')
        lemma_lower_pos.append(f'{lemma}_{pos}'.lower())
    
    number_tokens = len(tokens)
    mwe_semantic_tags = [['Z99'] for _ in range(number_tokens)]
    mwe_ids = [0 for _ in range(number_tokens)]
    current_mwe_id = 1
    
    largest_n_gram = largest_mwe_in_lexicon + 1
    largest_n_gram_indexes: List[Tuple[int, int]] = []

    for n_gram_index in n_gram_indexes(token_pos, 2, largest_mwe_in_lexicon):
        start_index, end_index = n_gram_index
        n_gram_size = end_index - start_index
        if largest_n_gram > n_gram_size:
            largest_n_gram = n_gram_size
            current_mwe_id = tag_n_gram_indexes(largest_n_gram_indexes, token_pos,
                                                lemma_pos, token_lower_pos,
                                                lemma_lower_pos, mwe_semantic_tags,
                                                mwe_ids, current_mwe_id)
            largest_n_gram_indexes = []

        largest_n_gram_indexes.append(n_gram_index)
    
    tag_n_gram_indexes(largest_n_gram_indexes, token_pos,
                       lemma_pos, token_lower_pos,
                       lemma_lower_pos, mwe_semantic_tags,
                       mwe_ids, current_mwe_id)

    return mwe_semantic_tags, mwe_ids
