from collections.abc import MutableMapping
import csv
from dataclasses import dataclass
from os import PathLike
import typing
from typing import Dict, Generator, List, Optional, Set, Union
from urllib.parse import urlparse

from . import file_utils


@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class LexiconEntry:
    '''
    A LexiconEntry contains the `semantic_tags` that are associated with a
    `lemma` and optionally the lemma's `POS`.

    As frozen is true, the attributes cannot be assigned another value.

    **Note** the parameters to the `__init__` are the same as the Instance
    Attributes.

    # Instance Attributes

    lemma: `str`
        The lemma of a token or the token itself.
    semantic_tags: `List[str]`
        The semantic tags associated with the `lemma` and optional `POS`.
        The semantic tags are in rank order, the most likely tag associated
        tag is the first tag in the list.
    pos: `str`, optional (default = `None`)
        The Part Of Speech (POS) to be associated with the `lemma`.
    '''

    lemma: str
    semantic_tags: List[str]
    pos: Optional[str] = None


class LexiconCollection(MutableMapping):
    '''
    This is a dictionary object that will hold :class:`LexiconEntry` data in a fast to
    access object. The keys of the dictionary are expected to be either just a
    lemma or a combination of lemma and pos in the following format:
    `{lemma}|{pos}` e.g. `Car|Noun`.

    The value to each key is the associated semantic tags, whereby the semantic
    tags are in rank order, the most likely tag is the first tag in the list.
    
    **Note** that the `lemma` can be the token
    itself rather than just it's base form, e.g. can be `Cars` rather than `Car`.

    # Parameters

    data: `Dict[str, List[str]]`, optional (default = `None`)

    # Instance Attributes

    data: `Dict[str, List[str]]`
        Dictionary where the keys are `{lemma}|{pos}` and the values are
        a list of associated semantic tags. If the `data` parameter given was
        `None` then the value of this attribute will be an empty dictionary.

    # Examples
    ``` python
    >>> from pymusas.lexicon_collection import LexiconEntry, LexiconCollection
    >>> lexicon_entry = LexiconEntry('London', ['Z3', 'Z1', 'A1'], 'noun')
    >>> collection = LexiconCollection()
    >>> collection.add_lexicon_entry(lexicon_entry)
    >>> most_likely_tag = collection['London|noun'][0]
    >>> assert most_likely_tag == 'Z3'
    >>> least_likely_tag = collection['London|noun'][-1]
    >>> assert least_likely_tag == 'A1'

    ```

    '''
    
    def __init__(self, data: Optional[Dict[str, List[str]]] = None) -> None:

        self.data: Dict[str, List[str]] = {}
        if data is not None:
            self.data = data

    def add_lexicon_entry(self, value: LexiconEntry,
                          include_pos: bool = True) -> None:
        '''
        Will add the :class:`LexiconEntry` to the collection, whereby the key is the
        combination of the lemma and pos and the value are the semantic tags.
        
        The lemma and pos are combined as follows: `{lemma}|{pos}`, e.g.
        `Car|Noun`

        If the pos value is None then then only the lemma is used: `{lemma}`,
        e.g. `Car`

        # Parameters

        value: `LexiconEntry`
            Lexicon Entry to add to the collection.
        include_pos: `bool`, optional (default = `True`)
            Whether to include the POS tag within the key.
        '''
        lemma = value.lemma
        if value.pos is not None and include_pos:
            lemma += f'|{value.pos}'
        self[lemma] = value.semantic_tags

    def to_dictionary(self) -> Dict[str, List[str]]:
        '''
        Returns the `data` instance attribute.

        # Returns

        `Dict[str, List[str]]`
        '''

        return self.data

    @staticmethod
    def from_tsv(tsv_file_path: Union[PathLike, str], include_pos: bool = True
                 ) -> Dict[str, List[str]]:
        '''
        Given a `tsv_file_path` it will return a dictionary object that can
        be used to create a :class:`LexiconCollection`.

        Each line in the TSV file will be read in as a :class:`LexiconEntry`
        and added to a temporary :class:`LexiconCollection`, once all lines
        in the TSV have been parsed the return value is the `data` attribute of
        the temporary :class:`LexiconCollection`.

        If the file path is a URL, the file will be downloaded and cached using
        :func:`pymusas.file_utils.download_url_file`.
        
        If `include_pos` is True and the TSV file does not contain a
        `pos` field heading then this will return a LexiconCollection that is
        identical to a collection that ran this method with `include_pos` equal
        to False.

        Code reference, the identification of a URL and the idea to do this has
        come from the [AllenNLP library](https://github.com/allenai/allennlp/blob/main/allennlp/common/file_utils.py#L205)

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
        
        # Raises
        
        `ValueError`
            If the minimum field headings, `lemma` and `semantic_tags`, do not
            exist in the given TSV file.

        # Examples

        `include_pos` = `True`
        ``` python
        >>> from pymusas.lexicon_collection import LexiconCollection
        >>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
        >>> welsh_lexicon_dict = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
        >>> welsh_lexicon_collection = LexiconCollection(welsh_lexicon_dict)
        >>> assert welsh_lexicon_dict['ceir|noun'][0] == 'M3fn'
        >>> assert welsh_lexicon_dict['ceir|verb'][0] == 'A9+'

        ```

        `include_pos` = `False`
        ``` python
        >>> from pymusas.lexicon_collection import LexiconCollection
        >>> welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
        >>> welsh_lexicon_dict = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
        >>> welsh_lexicon_collection = LexiconCollection(welsh_lexicon_dict)
        >>> assert welsh_lexicon_dict['ceir'][0] == 'M3fn'

        ```
        '''
        minimum_field_names = {'lemma', 'semantic_tags'}
        extra_field_names = ['pos']
        field_names_to_extract = []

        collection_from_tsv = LexiconCollection()

        if not isinstance(tsv_file_path, str):
            tsv_file_path = str(tsv_file_path)

        parsed = urlparse(tsv_file_path)
        if parsed.scheme in ("http", "https", "s3", "hf", "gs"):
            tsv_file_path = file_utils.download_url_file(tsv_file_path)

        with open(tsv_file_path, 'r', newline='') as fp:
            csv_reader = csv.DictReader(fp, delimiter='\t')
            file_field_names: Set[str] = set()
            if csv_reader.fieldnames:
                file_field_names = set(csv_reader.fieldnames)
            if minimum_field_names.issubset(file_field_names):
                field_names_to_extract.extend(list(minimum_field_names))
            else:
                error_msg = ("The TSV file given should contain a header that"
                             " has at minimum the following fields "
                             f"{minimum_field_names}. The field names found "
                             f"were {file_field_names}")
                raise ValueError(error_msg)
            
            for extra_field_name in extra_field_names:
                if extra_field_name in file_field_names:
                    field_names_to_extract.append(extra_field_name)
            
            for row in csv_reader:
                row_data: typing.MutableMapping[str, Union[str, List[str]]] = {}
                for field_name in field_names_to_extract:
                    if field_name == 'semantic_tags':
                        row_data[field_name] = row[field_name].split()
                    else:
                        row_data[field_name] = row[field_name]
                collection_from_tsv.add_lexicon_entry(LexiconEntry(**row_data),
                                                      include_pos=include_pos)
        
        return collection_from_tsv.to_dictionary()

    def __setitem__(self, key: str, value: List[str]) -> None:
        self.data[key] = value

    def __getitem__(self, key: str) -> List[str]:
        return self.data[key]

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Generator[str, None, None]:
        for key in self.data:
            yield key

    def __str__(self) -> str:
        '''
        Human readable string.
        '''
        object_str = 'LexiconCollection('
        for index, item in enumerate(self.items()):
            object_str += f"('{item[0]}': {item[1]}), "
            if index == 1:
                object_str += '... '
                break
        object_str += f') ({len(self)} entires in the collection)'
        return object_str

    def __repr__(self) -> str:
        '''
        Machine readable string. When printed and run `eval()` over the string
        you should be able to recreate the object.
        '''
        return f'{self.__class__.__name__}(data={self.data})'
