from typing import Set


def unique_pos_tags_in_lexicon_entry(lexicon_entry: str) -> Set[str]:
    '''
    Returns the unique POS tag values in the given `lexicon_entry`.

    # Parameters

    lexicon_entry : `str`
        Either a Multi Word Expression template or single word lexicon entry,
        which is a sequence of words/tokens and Part Of Speech (POS) tags
        joined together by an underscore and separated by a single whitespace,
        e.g. `word1_POS1 word2_POS2 word3_POS3`. For a single word lexicon it
        would be `word1_POS1`.

    # Returns

    `Set[str]`

    # Raises

    `ValueError`
        If the lexicon entry when split on whitespace and then split by `_`
        does not create a `List[Tuple[str, str]]` whereby the tuple contains
        the `token text` and it's associated `POS tag`.

    # Examples
    ``` python
    >>> from pymusas.utils import unique_pos_tags_in_lexicon_entry
    >>> mwe_template = 'East_noun London_noun is_det great_adj'
    >>> assert ({'noun', 'adj', 'det'}
    ...         == unique_pos_tags_in_lexicon_entry(mwe_template))
    >>> single_word_lexicon = 'East_noun'
    >>> assert {'noun'} == unique_pos_tags_in_lexicon_entry(single_word_lexicon)

    ```
    '''
    split_error_msg = ('The lexicon entry when split on whitespace and then by'
                       ' `_` does not create a `List[Tuple[str, str]]`. '
                       f'lexicon entry: {lexicon_entry}')
    unique_pos_tags: Set[str] = set()
    for token_pos in lexicon_entry.split():
        token_pos_split = token_pos.split('_')
        if len(token_pos_split) != 2:
            raise ValueError(split_error_msg)
        pos_tag = token_pos_split[1]
        unique_pos_tags.add(pos_tag)
    return unique_pos_tags
