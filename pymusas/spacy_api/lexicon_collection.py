from os import PathLike
from typing import Dict, List, Union

import spacy

from ..lexicon_collection import LexiconCollection


@spacy.util.registry.misc('lexicon_collection_from_tsv')
def lexicon_collection(tsv_file_path: Union[PathLike, str]
                       ) -> Dict[str, List[str]]:
    return LexiconCollection.from_tsv(tsv_file_path)
