from __future__ import annotations
from collections.abc import Iterable, MutableMapping
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=True)
class LexiconEntry:
    '''
    As frozen is true no values can be assigned after creation of an instance of 
    this class.
    '''

    lemma: str
    semantic_tags: list[str]
    pos: str = None


class LexiconCollection(MutableMapping):
    '''
    This is a dictionary object that will hold LexiconEntry data in a fast to 
    access object. The keys of the dictionary are expected to be either just a 
    lemma or a combination of lemma and pos in the following format:
    {lemma}|{pos}

    The value to each key is the associated semantic tags, whereby the semantic 
    tags are in rank order, the most likely tag is the first tag in the list. 
    For example in the collection below, for the lemma London_noun the most 
    likely semantic tag is Z3 and the least likely tag is A1:

    ```
    from pymusas.lexicon_collection import LexiconEntry, LexiconCollection
    lexicon_entry = LexiconEntry('London', ['Z3', 'Z1', 'A1'], 'noun')
    collection = LexiconCollection([lexicon_entry])
    most_likely_tag = collection['London|noun'][0]
    least_likely_tag = collection['London|noun'][-1]
    ```
    '''
    
    def __init__(self, data: Optional[dict[str, list[str]]] = None) -> None:

        self.data: dict[str, list[str]] = {}
        if data is not None:
            self.data = data

    def __setitem__(self, key: str, value: list[str]) -> None:
        self.data[key] = value

    def __getitem__(self, key: str) -> list[str]:
        return self.data[key]

    def __delitem__(self, key: str) -> None:
        del self.data[key]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterable[str]:
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
        Machine readable string. When printed and run eval() over the string 
        you should be able to recreate the object.
        '''
        return f'{self.__class__.__name__}(data={self.data})'

    def add_lexicon_entry(self, value: LexiconEntry, 
                          include_pos: bool = True) -> None:
        '''
        Will add the LexiconEntry to the collection, whereby the key is the 
        combination of the lemma and pos and the value is the semantic tags. 
        
        The lemma and pos are combined as follows:
        {lemma}|{pos}

        If the pos value is None then then only the lemma is used, e.g.:
        {lemma}

        :param value: A LexiconEntry.
        :param include_pos: Whether to include the POS tag within the key.
        '''
        lemma = value.lemma
        if value.pos is not None and include_pos:
            lemma += f'|{value.pos}'
        self[lemma] = value.semantic_tags

    @staticmethod
    def from_tsv(tsv_file_path: Path, include_pos: bool = True
                 ) -> type['LexiconCollection']:
        '''
        **NOTE** if `include_pos` is True and the TSV file does not contain a 
        `pos` field heading then this will return a LexiconCollection that is 
        identical to a collection that ran this method with `include_pos` equal 
        to False.

        :param tsv_file_path: A path to a TSV file that contains at least two 
                              fields with the following headings: 1. `lemma`, 
                              and 2. `semantic_tags`. With an optional field 
                              `pos`. All other fields will be ignored. 
                              Each row will be used to create a `LexiconEntry` 
                              which will then be added to the returned 
                              `LexiconCollection`
        :param include_pos: Whether to include the POS tag in the key when 
                            adding the `LexiconEntry` into the returned 
                            `LexiconCollection`. For more information on this 
                            see the `add_lexicon_entry` method.
        :returns: A `LexiconCollection` that has been created from the data 
                  within the TSV file.
        :raises: ValueError if the minimum field headings, lemma and 
                 semantic_tags, do not exist in the given TSV file.
        '''
        minimum_field_names = {'lemma', 'semantic_tags'}
        extra_field_names = ['pos']
        field_names_to_extract = []

        collection_from_tsv = LexiconCollection()

        with tsv_file_path.open('r', newline='') as fp:
            csv_reader = csv.DictReader(fp, delimiter='\t')
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
                row_data = {}
                for field_name in field_names_to_extract:
                    if field_name == 'semantic_tags':
                        row_data[field_name] = row[field_name].split()
                    else:
                        row_data[field_name] = row[field_name]
                collection_from_tsv.add_lexicon_entry(LexiconEntry(**row_data), 
                                                      include_pos=include_pos)
        
        return collection_from_tsv