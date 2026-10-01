"""
This module contains various helper functions that are used in other modules.

# Attributes

NEURAL_EXTRA_PACKAGES: `list[str]`
    The Python packages that are required for the `pymusas[neural]` extra.
DEFAULT_TAG_RE: `re.Pattern[str]`
    Matches a default (`Df`) semantic tag, e.g. `Df`, `Df+++`, `Dfc`, `Df-m%`,
    or `Dfm+`. The `suffix` group captures everything after `Df`, which can be
    any combination, in any order, of `+`/`-` affixes, lower case markers,
    e.g. gender markers, and rarity markers (`%` and `@`).
"""

from collections.abc import Iterable
import importlib.util
import re


NEURAL_EXTRA_PACKAGES: list[str] = ['transformers', 'wsd_torch_models', 'torch']
DEFAULT_TAG_RE: re.Pattern[str] = re.compile(r'^Df(?P<suffix>[+\-a-z%@]*)$')


def token_pos_tags_in_lexicon_entry(lexicon_entry: str
                                    ) -> Iterable[tuple[str, str]]:
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

    `Iterable[tuple[str, str]]`

    # Raises

    `ValueError`
        If the lexicon entry when split on whitespace and then split by `_`
        does not create a `Iterable[tuple[str, str]]` whereby the tuple contains
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
                       ' `_` does not create a `list[tuple[str, str]]`. '
                       f'lexicon entry: {lexicon_entry}')
    for token_pos in lexicon_entry.split():
        token_pos_split = token_pos.split('_')
        if len(token_pos_split) != 2:
            raise ValueError(split_error_msg)
        token, pos_tag = token_pos_split
        yield token, pos_tag


def unique_pos_tags_in_lexicon_entry(lexicon_entry: str) -> set[str]:
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

    `set[str]`

    # Raises

    `ValueError`
        If the lexicon entry when split on whitespace and then split by `_`
        does not create a `list[tuple[str, str]]` whereby the tuple contains
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
    unique_pos_tags: set[str] = set()
    for _, pos_tag in token_pos_tags_in_lexicon_entry(lexicon_entry):
        unique_pos_tags.add(pos_tag)
    return unique_pos_tags


def contains_default_tag(semantic_tags: list[str]) -> bool:
    '''
    Returns `True` if any of the given `semantic_tags`, including any part of
    a slash (`/`) tag, is a default (`Df`) tag, see :var:`DEFAULT_TAG_RE`.

    # Parameters

    semantic_tags : `list[str]`
        The semantic tags of a lexicon entry, e.g. `['C1/Df', 'Z3']`.

    # Returns

    `bool`

    # Examples
    ``` python
    >>> from pymusas.utils import contains_default_tag
    >>> assert contains_default_tag(['Z3', 'C1/Df+'])
    >>> assert contains_default_tag(['Dfc'])
    >>> assert contains_default_tag(['Df%'])
    >>> assert contains_default_tag(['Dfm+'])
    >>> assert not contains_default_tag(['Z3', 'A1/B2'])

    ```
    '''
    for semantic_tag in semantic_tags:
        for tag_part in semantic_tag.split('/'):
            if DEFAULT_TAG_RE.match(tag_part):
                return True
    return False


def default_token_index(mwe_template: str) -> int | None:
    '''
    Returns the index of the first token in the `mwe_template` whose token
    text starts with a wildcard (`*`). This is the token that a default (`Df`)
    semantic tag refers to. `None` is returned if no token starts with a
    wildcard.

    # Parameters

    mwe_template : `str`
        A Multi Word Expression template, e.g. `half_DET a*_DET *_NOUN`.

    # Returns

    `int | None`

    # Raises

    `ValueError`
        If the `mwe_template` is not in the format expected by
        :func:`token_pos_tags_in_lexicon_entry`.

    # Examples
    ``` python
    >>> from pymusas.utils import default_token_index
    >>> assert 2 == default_token_index('half_DET a*_DET *_NOUN')
    >>> assert 0 == default_token_index('*ing_NOUN job*_*')
    >>> assert default_token_index('ski_NOUN boot*_NOUN') is None

    ```
    '''
    for index, (token, _) in enumerate(token_pos_tags_in_lexicon_entry(mwe_template)):
        if token.startswith('*'):
            return index
    return None


def resolve_default_tags(semantic_tags: list[str], replacement: str | None
                         ) -> list[str]:
    '''
    Returns the `semantic_tags` whereby every default (`Df`) tag, including
    those within a slash (`/`) tag, has been replaced using the `replacement`
    semantic tag.

    Only the first part of a slash `replacement` tag is used and all of its
    affixes, lower case markers, and rarity markers (`%` and `@`) are removed,
    e.g. `A5.1+++mfn@/Z3` becomes `A5.1`. Any affixes, lower case markers, and
    rarity markers on the `Df` tag are then added to it in the same order,
    e.g. `Df++` with the replacement `A1-` becomes `A1++`, `Df-m%` becomes
    `A1-m%`, and `Dfm+` becomes `A1m+`. If the
    `replacement` is `None` the `Df` tag is replaced with `Z99` with no suffixes
    even if the Df tag contains suffixes.

    # Parameters

    semantic_tags : `list[str]`
        The semantic tags that may contain `Df` tags, e.g. `['C1/Df']`.
    replacement : `str | None`
        The semantic tag to replace the `Df` tags with, this would be the
        single word semantic tag of the token the `Df` tag refers to.

    # Returns

    `list[str]`

    # Examples
    ``` python
    >>> from pymusas.utils import resolve_default_tags
    >>> assert ['A1'] == resolve_default_tags(['Df'], 'A1/Z3')
    >>> assert ['C1/A1'] == resolve_default_tags(['C1/Df'], 'A1')
    >>> assert ['N3.8+++'] == resolve_default_tags(['Df+++'], 'N3.8+')
    >>> assert ['I2.1c', 'B1'] == resolve_default_tags(['Dfc', 'B1'], 'I2.1mf')
    >>> assert ['A1-m%'] == resolve_default_tags(['Df-m%'], 'A1+@')
    >>> assert ['A1m+'] == resolve_default_tags(['Dfm+'], 'A1')
    >>> assert ['C1/Z99'] == resolve_default_tags(['C1/Df'], None)

    ```
    '''
    replacement_core_tag = 'Z99'
    if replacement is not None:
        first_tag_part = replacement.split('/')[0]
        replacement_core_tag = re.sub(r'[^A-Z0-9.]', '', first_tag_part)

    resolved_tags: list[str] = []
    for semantic_tag in semantic_tags:
        resolved_parts: list[str] = []
        for tag_part in semantic_tag.split('/'):
            default_match = DEFAULT_TAG_RE.match(tag_part)
            if default_match is None:
                resolved_parts.append(tag_part)
            elif replacement is None:
                resolved_parts.append(replacement_core_tag)
            else:
                resolved_parts.append(f'{replacement_core_tag}'
                                      f'{default_match.group("suffix")}')
        resolved_tags.append('/'.join(resolved_parts))
    return resolved_tags


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
