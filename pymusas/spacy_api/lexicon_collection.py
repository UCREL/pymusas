'''
spaCy registered functions for reading in a
:class:`pymusas.lexicon_collection.LexiconCollection`,
:class:`pymusas.lexicon_collection.MWELexiconCollection`, or
:class:`pymusas.lexicon_collection.AutotagLexiconCollection` from a TSV file.
'''

from os import PathLike

import spacy

from ..lexicon_collection import AutotagLexiconCollection, LexiconCollection, MWELexiconCollection


@spacy.util.registry.misc('pymusas.LexiconCollection.from_tsv')
def lexicon_collection_from_tsv(tsv_file_path: PathLike | str,
                                include_pos: bool = True
                                ) -> dict[str, list[str]]:
    '''
    `pymusas.LexiconCollection.from_tsv` is a registered function under the
    `@misc` function register. Given a `tsv_file_path` it will return a
    dictionary object that can be used to create a
    :class:`pymusas.lexicon_collection.LexiconCollection`.

    # Parameters

    tsv_file_path: `PathLike | str`
        A file path or URL to a TSV file that contains at least two
        fields, with an optional third, with the following headings:
        
        1. `lemma`,
        2. `semantic_tags`
        3. `pos` (Optional)
        
        All other fields will be ignored.
    include_pos: `bool`, optional (default = `True`)
        Whether to include the POS information, if the information is available,
        or not. See :func:`pymusas.lexicon_collection.add_lexicon_entry`
        for more information on this parameter.

    # Returns
    
    `dict[str, list[str]]`
    '''
    return LexiconCollection.from_tsv(tsv_file_path, include_pos)


@spacy.util.registry.misc('pymusas.MWELexiconCollection.from_tsv')
def mwe_lexicon_collection_from_tsv(tsv_file_path: PathLike | str
                                    ) -> dict[str, list[str]]:
    '''
    `pymusas.MWELexiconCollection.from_tsv` is a registered function under the
    `@misc` function register. Given a `tsv_file_path` it will return a
    dictionary object that can be used to create a
    :class:`pymusas.lexicon_collection.MWELexiconCollection`.

    # Parameters

    tsv_file_path: `PathLike | str`
        A file path or URL to a TSV file that contains at least these two
        fields:
        
        1. `mwe_template`,
        2. `semantic_tags`
        
        All other fields will be ignored.

    # Returns
    
    `dict[str, list[str]]`
    '''
    return MWELexiconCollection.from_tsv(tsv_file_path)


@spacy.util.registry.misc('pymusas.AutotagLexiconCollection.from_tsv')
def autotag_lexicon_collection_from_tsv(tsv_file_path: PathLike | str
                                        ) -> dict[str, list[str]]:
    '''
    `pymusas.AutotagLexiconCollection.from_tsv` is a registered function under
    the `@misc` function register. Given a `tsv_file_path` to an `autotag`
    lexicon file it will return a dictionary object that can be used to create
    a :class:`pymusas.lexicon_collection.AutotagLexiconCollection`.

    # Parameters

    tsv_file_path: `PathLike | str`
        A file path or URL to a TSV file that contains at least these three
        fields:
        
        1. `lemma`,
        2. `pos`,
        3. `semantic_tags`
        
        All other fields will be ignored.

    # Returns
    
    `dict[str, list[str]]`

    # Raises

    `ValueError`
        See the `from_tsv` method of :class:`pymusas.lexicon_collection.AutotagLexiconCollection`.
    '''
    return AutotagLexiconCollection.from_tsv(tsv_file_path)
