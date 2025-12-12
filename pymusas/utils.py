"""
This module contains various helper functions that are used in other modules.

# Attributes

NEURAL_EXTRA_PACKAGES: `list[str]`
    The Python packages that are required for the `pymusas[neural]` extra.
"""

import importlib.util
from typing import Iterable, Set, Tuple


NEURAL_EXTRA_PACKAGES: list[str] = ['transformers', 'wsd_torch_models', 'torch']


def token_pos_tags_in_lexicon_entry(lexicon_entry: str
                                    ) -> Iterable[Tuple[str, str]]:
    '''
    Yields the token and associated POS tag in the given `lexicon_entry`.

    # Parameters

    lexicon_entry : `str`
        Either a Multi Word Expression template or single word lexicon entry,
        which is a sequence of words/tokens and Part Of Speech (POS) tags
        joined together by an underscore and separated by a single whitespace,
        e.g. `word1_POS1 word2_POS2 word3_POS3`. For a single word lexicon it
        would be `word1_POS1`.

    # Returns

    `Iterable[Tuple[str, str]]`

    # Raises

    `ValueError`
        If the lexicon entry when split on whitespace and then split by `_`
        does not create a `Iterable[Tuple[str, str]]` whereby the tuple contains
        the `token text` and it's associated `POS tag`.

    # Examples
    ``` python
    >>> from pymusas.utils import token_pos_tags_in_lexicon_entry
    >>> mwe_template = 'East_noun London_noun is_det great_adj'
    >>> assert ([('East', 'noun'), ('London', 'noun'), ('is', 'det'), ('great', 'adj')]
    ...         == list(token_pos_tags_in_lexicon_entry(mwe_template)))
    >>> single_word_lexicon = 'East_noun'
    >>> assert ([('East', 'noun')]
    ...         == list(token_pos_tags_in_lexicon_entry(single_word_lexicon)))

    ```
    '''
    split_error_msg = ('The lexicon entry when split on whitespace and then by'
                       ' `_` does not create a `List[Tuple[str, str]]`. '
                       f'lexicon entry: {lexicon_entry}')
    for token_pos in lexicon_entry.split():
        token_pos_split = token_pos.split('_')
        if len(token_pos_split) != 2:
            raise ValueError(split_error_msg)
        token, pos_tag = token_pos_split
        yield token, pos_tag


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
    unique_pos_tags: Set[str] = set()
    for _, pos_tag in token_pos_tags_in_lexicon_entry(lexicon_entry):
        unique_pos_tags.add(pos_tag)
    return unique_pos_tags


def are_packages_installed(packages: list[str]) -> bool:
    """
    Returns True if all packages are installed, False otherwise.

    # Parameters

    packages : `list[str]`
        A list of package names to check if they are installed.

    # Returns

    `bool`
    """
    def is_package_installed(package_name: str) -> bool:
        """
        Returns True if the package is installed, False otherwise.

        # Parameters

        package_name : `str`
            The name of the package to check if it is installed.
        
        # Returns

        `bool`
        """
        return importlib.util.find_spec(package_name) is not None
    
    are_installed = [is_package_installed(package) for package in packages]
    return all(are_installed)


def neural_extra_installed() -> None:
    """
    Checks if the `pymusas[neural]` extra is installed by checking if the
    packages required for the `neural` extra are installed.

    # Raises

    `ImportError`
        If `pymusas[neural]` is not installed.
    """

    if not are_packages_installed(NEURAL_EXTRA_PACKAGES):
        import_error_message = (
            "To use the NeuralTagger you need to install the "
            "pymusas package with the `neural` extra installed, like so "
            "pip install pymusas[neural] or uv add pymusas[neural]"
        )
        raise ImportError(import_error_message)
