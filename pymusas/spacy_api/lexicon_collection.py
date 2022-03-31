'''
spaCy registered functions for reading in a
:class:`pymusas.lexicon_collection.LexiconCollection` or
:class:`pymusas.lexicon_collection.MWELexiconCollection` from a TSV file.
'''

from os import PathLike
from typing import Dict, List, Union

import spacy

from ..lexicon_collection import LexiconCollection, MWELexiconCollection


@spacy.util.registry.readers('pymusas.LexiconCollection.from_tsv')
def lexicon_collection_from_tsv(tsv_file_path: Union[PathLike, str],
                                include_pos: bool = True
                                ) -> Dict[str, List[str]]:
    '''
    `pymusas.LexiconCollection.from_tsv` is a registered function under the
    `@readers` function register. Given a `tsv_file_path` it will return a
    dictionary object that can be used to create a
    :class:`pymusas.lexicon_collection.LexiconCollection`.

    # Parameters

    tsv_file_path: `Union[PathLike, str]`
        A file path or URL to a TSV file that contains at least two
        fields, with an optional third, with the following headings:
        
        1. `lemma`,
        2. `semantic_tags`
        3. `pos` (Optional)
        
        All other fields will be ignored.
    include_pos: `bool`, optional (default = `True`)
        Whether to include the POS information, if the information is avaliable,
        or not. See :func:`add_lexicon_entry` for more information on this
        parameter.

    # Returns
    
    `Dict[str, List[str]]`
    '''
    return LexiconCollection.from_tsv(tsv_file_path, include_pos)


@spacy.util.registry.readers('pymusas.MWELexiconCollection.from_tsv')
def mwe_lexicon_collection_from_tsv(tsv_file_path: Union[PathLike, str]
                                    ) -> Dict[str, List[str]]:
    '''
    `pymusas.MWELexiconCollection.from_tsv` is a registered function under the
    `@readers` function register. Given a `tsv_file_path` it will return a
    dictionary object that can be used to create a
    :class:`pymusas.lexicon_collection.MWELexiconCollection`.

    # Parameters

    tsv_file_path: `Union[PathLike, str]`
        A file path or URL to a TSV file that contains at least these two
        fields:
        
        1. `mwe_template`,
        2. `semantic_tags`
        
        All other fields will be ignored.

    # Returns
    
    `Dict[str, List[str]]`
    '''
    return MWELexiconCollection.from_tsv(tsv_file_path)
