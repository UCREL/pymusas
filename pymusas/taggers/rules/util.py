from typing import Any, Iterator, Sequence, Tuple


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

    `Iterator[Tuple[int, int]]`

    # Raises

    `ValueError`
        If `min_n` is less than `1` or `max_n` is less than `min_n`.

    # Examples

    ``` python
    >>> from pymusas.taggers.rules.util import n_gram_indexes
    >>> tokens = ['hello', 'how', 'are', 'you', ',']
    >>> token_n_gram_indexes = n_gram_indexes(tokens, 2, 3)
    >>> expected_n_grams_indexes = [(0, 3), (1, 4), (2, 5), (0, 2), (1, 3), (2, 4), (3, 5)]
    >>> assert expected_n_grams_indexes == list(token_n_gram_indexes)

    ```
    '''
    if min_n < 1:
        raise ValueError(f'`min_n` has to be greater than 0. Value given {min_n}')
    if min_n > max_n:
        raise ValueError(f'`max_n` ({max_n}) cannot be less than `min_n` ({min_n})')
    
    sequence_size = len(sequence)
    max_n = sequence_size if max_n > sequence_size else max_n
    
    for n_gram_size in range(max_n, min_n - 1, -1):
        for sequence_index in range(sequence_size - n_gram_size + 1):
            last_n_gram_index = sequence_index + n_gram_size
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
    >>> from pymusas.taggers.rules.util import n_grams
    >>> tokens = ['hello', 'how', 'are', 'you', ',']
    >>> token_n_grams = n_grams(tokens, 2, 3)
    >>> expected_n_grams = [['hello', 'how', 'are'], ['how', 'are', 'you'], ['are', 'you', ','],
    ...                     ['hello', 'how'], ['how', 'are'], ['are', 'you'], ['you', ',']]
    >>> assert expected_n_grams == list(token_n_grams)

    ```
    '''
    for n_gram_index in n_gram_indexes(sequence, min_n, max_n):
        start_index, end_index = n_gram_index
        yield sequence[start_index: end_index]
