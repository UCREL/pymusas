from os import PathLike
from typing import Optional, Dict, List, Union

import spacy

from .lexicon_collection import LexiconCollection



@spacy.util.registry.misc('lexicon_collection')
def lexicon_collection(data: Optional[Dict[str, List[str]]] = None,
                       tsv_file_path: Optional[Union[PathLike, str]] = None
                       ) -> LexiconCollection:
    if data is not None:
        return LexiconCollection(data)
    else:
        return LexiconCollection.from_tsv(tsv_file_path)