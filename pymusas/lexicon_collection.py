import collections
from collections.abc import MutableMapping
import csv
from dataclasses import dataclass
from enum import Enum, unique
from os import PathLike
import re
import typing
from typing import DefaultDict, Dict, Generator, List, Optional, Set, Tuple, Union, cast
from urllib.parse import urlparse
import warnings

import srsly

from . import file_utils, utils


@unique
class LexiconType(str, Enum):
    '''
    Descriptions of the type associated to single and Multi Word Expression (MWE)
    lexicon entires and templates. Any type with the word `NON_SPECIAL` means
    that it does not use any special syntax, for example does not use wildcards
    or curly braces.

    The `value` attribute of each instance attribute is of type `str` describing
    the type associated with that attribute. For the best explanation see the
    example below.
    
    # Instance Attributes

    SINGLE_NON_SPECIAL : `LexiconType`
        Single word lexicon lookup.
    MWE_NON_SPECIAL : `LexiconType`
        MWE lexicon lookup.
    MWE_WILDCARD : `LexiconType`
        MWE lexicon lookup using a wildcard.
    MWE_CURLY_BRACES : `LexiconType`
        MWE lexicon lookup using curly braces.

    # Examples
    ```python
    >>> from pymusas.lexicon_collection import LexiconType
    >>> assert 'Single Non Special' == LexiconType.SINGLE_NON_SPECIAL
    >>> assert 'Single Non Special' == LexiconType.SINGLE_NON_SPECIAL.value
    >>> assert 'SINGLE_NON_SPECIAL' == LexiconType.SINGLE_NON_SPECIAL.name
    >>> all_possible_values = {'Single Non Special', 'MWE Non Special',
    ... 'MWE Wildcard', 'MWE Curly Braces'}
    >>> assert all_possible_values == {lexicon_type.value for lexicon_type in LexiconType}
    
    ```
    '''
    SINGLE_NON_SPECIAL = 'Single Non Special'
    MWE_NON_SPECIAL = 'MWE Non Special'
    MWE_WILDCARD = 'MWE Wildcard'
    MWE_CURLY_BRACES = 'MWE Curly Braces'

    def __repr__(self) -> str:
        '''
        Machine readable string. When printed and run `eval()` over the string
        you should be able to recreate the object.
        '''
        return self.__str__()


@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class LexiconEntry:
    '''
    A LexiconEntry contains the `semantic_tags` that are associated with a
    `lemma` and optionally the lemma's `POS`.

    As frozen is true, the attributes cannot be assigned another value.

    This data type is mainly used for single word lexicons, rather than
    Multi Word Expression (MWE).

    **Note** the parameters to the `__init__` are the same as the Instance
    Attributes.

    # Instance Attributes

    lemma: `str`
        The lemma of a token or the token itself.
    semantic_tags: `List[str]`
        The semantic tags associated with the `lemma` and optional `POS`.
        The semantic tags are in rank order, the most likely tag
        is the first tag in the list.
    pos: `str`, optional (default = `None`)
        The Part Of Speech (POS) to be associated with the `lemma`.
    '''

    lemma: str
    semantic_tags: List[str]
    pos: Optional[str] = None


@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class LexiconMetaData:
    '''
    A LexiconMetaData object contains all of the meta data about a given
    single word or Multi Word Expression (MWE) lexicon entry. This meta data can
    be used to help rank single and MWE entries when tagging.

    As frozen is true, the attributes cannot be assigned another value.

    **Note** the parameters to the `__init__` are the same as the Instance
    Attributes.

    # Instance Attributes

    semantic_tags : `List[str]`
        The semantic tags associated with the lexicon entry.
        The semantic tags are in rank order, the most likely tag
        is the first tag in the list.
    n_gram_length : `int`
        The n-gram size of the lexicon entry, e.g. `*_noun boot*_noun` will be
        of length 2 and all single word lexicon entries will be of length 1.
    lexicon_type : `LexiconType`
        Type associated to the lexicon entry.
    wildcard_count : `int`
        Number of wildcards in the lexicon entry, e.g. `*_noun boot*_noun` will
        be 2 and `ski_noun boot_noun` will be 0.
    '''

    semantic_tags: List[str]
    n_gram_length: int
    lexicon_type: LexiconType
    wildcard_count: int


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

    This data type is used for single word lexicons, to store Multi Word
    Expression (MWE) see the :class:`MWELexiconCollection`.

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

    def to_bytes(self) -> bytes:
        '''
        Serialises the :class:`LexiconCollection` to a bytestring.

        # Returns

        `bytes`
        '''
        return cast(bytes, srsly.msgpack_dumps(self.data))

    @staticmethod
    def from_bytes(bytes_data: bytes) -> "LexiconCollection":
        '''
        Loads :class:`LexiconCollection` from the given bytestring and
        returns it.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.
        
        # Returns

        :class:`LexiconCollection`
        '''
        return LexiconCollection(srsly.msgpack_loads(bytes_data))

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

        with open(tsv_file_path, 'r', newline='', encoding='utf-8') as fp:
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

    def __eq__(self, other: object) -> bool:
        '''
        Given another object to compare too it will return `True` if the other
        object is the same class and contains the same `data` instance attribute.

        # Parameters

        other : `object`
            The object to compare too.
        
        # Returns

        `True`
        '''
        if not isinstance(other, LexiconCollection):
            return False
        
        if len(self) != len(other):
            return False
        
        if self.data != other.data:
            return False
        
        return True


class MWELexiconCollection(MutableMapping):
    r'''
    A collection that stores Multi Word Expression (MWE) templates and their
    associated meta data.
    
    This collection allows users to:

    1. Easily load MWE templates from a single TSV file.
    2. Find strings that match MWE templates taking into account
    any special syntax rules that should be applied, e.g. wildcards allow zero
    or more characters to appear after the word token and/or Part Of Speech (POS) tag.
    For more information on the MWE special syntax rules see the following notes.
    3. POS mapping, it can find strings that match MWE templates while taking
    into account mapping from one POS tagset to another in both a one to one and
    one to many mapping.

    **Note** that even though this a sub-class of a MutableMapping it has a
    time complexity of O(n) for deletion unlike the standard Python MutableMapping,
    see the [following dict time complexities](https://wiki.python.org/moin/TimeComplexity),
    this is due to keeping track of the `longest_non_special_mwe_template` and
    `longest_wildcard_mwe_template`.

    As we do not currently support curly braces MWE template syntax, therefore
    any MWE templates that contain a `{` or `}` will be ignored and will not be
    added to this collection, in addition a `UserWarning` will be raised stating
    this.

    # Parameters

    data: `Dict[str, List[str]]`, optional (default = `None`)
        Dictionary where the keys are MWE templates, of any :class:`LexiconType`,
        and the values are a list of associated semantic tags.
    pos_mapper : `Dict[str, List[str]]`, optional (default = `None`)
        If not `None`, maps from the lexicon's POS tagset to the desired
        POS tagset, whereby the mapping is a `List` of tags, at the moment there
        is no preference order in this list of POS tags. The POS mapping is
        useful in situtation whereby the leixcon's POS tagset is different to
        the token's. **Note** that the longer the `List[str]` for each POS
        mapping the longer it will take to match MWE templates. A one to one
        mapping will have no speed impact on the tagger. A selection of POS
        mappers can be found in :mod:`pymusas.pos_mapper`.

    # Instance Attributes
    
    **Note** if the `data` parameter given was `None` then the value of all
    dictionary attributes will be an empty dictionary and all integer values will
    be `0`. If `pos_mapper` parameter was `None` then the `pos_mapper` attribute
    will be an empty dictionary.
    
    meta_data: `Dict[str, LexiconMetaData]`
        Dictionary where the keys are MWE templates, of any type, and the values
        are their associated meta data stored in a :class:`LexiconMetaData` object.
    longest_non_special_mwe_template : `int`
        The longest MWE template with no special symbols measured by n-gram size.
        For example the MWE template `ski_noun boot_noun` will be of length 2.
    longest_wildcard_mwe_template : `int`
        The longest MWE template with at least one wildcard (`*`) measured by n-gram size.
        For example the MWE template `*_noun boot*_noun` will be of length 2.
    longest_mwe_template : `int`
        The longest MWE template regardless of type measured by n-gram size.
    most_wildcards_in_mwe_template : `int`
        The number of wildcards in the MWE template that contains the
        most wildcards, e.g. the MWE template `ski_* *_noun` would contain 2
        wildcards. This can be 0 if you have no wildcard MWE templates.
    mwe_regular_expression_lookup: `Dict[int, Dict[str, Dict[str, re.Pattern]]]`
        A dictionary that can lookup all special syntax MWE templates there
        regular expression pattern. These templates are found first by
        their n-gram length and then their first character symbol. The regular
        expression pattern is used for quick matching within the :func:`mwe_match`.
        From the special syntax only wildcard (`*`) symbols are supported at the
        moment.
    pos_mapper : `Dict[str, List[str]]`
        The given `pos_mapper`.
    one_to_many_pos_tags : `Set[str]`
        A set of POS tags that have a one to many mapping, this is created based
        on the `pos_mapper`. This is empty if `pos_mapper` is `None`
    pos_mapping_lookup : `Dict[str, str]`
        Only used if `pos_mapper` is not `None`. For all one-to-one POS mappings
        will store the mapped POS MWE template as keys and the original non-mapped
        (original) MWE templates as values, which can be used to lookup the meta
        data from `meta_data`.
    pos_mapping_regular_expression_lookup : `Dict[LexiconType, Dict[int, Dict[str, Dict[str, re.Pattern]]]]`
        Only used if `pos_mapper` is not `None` and will result in
        `mwe_regular_expression_lookup` being empty as it replaces it
        functionality and extends it and by handlining the one-to-many POS
        mapping cases. When we have a one-to-many POS mapping case this requires
        a regular expression mapping even for non special syntax MWE templates.
        Compared to the `mwe_regular_expression_lookup` the first set of keys
        represent the lexicon entry match type.

    # Examples
    ``` python
    >>> import re
    >>> from pymusas.lexicon_collection import MWELexiconCollection, LexiconType
    >>> mwe_collection = MWELexiconCollection()
    >>> mwe_collection['*_noun boot*_noun'] = ['Z0', 'Z3']
    >>> meta_data = mwe_collection['*_noun boot*_noun']
    >>> assert 2 == meta_data.n_gram_length
    >>> assert LexiconType.MWE_WILDCARD == meta_data.lexicon_type
    >>> assert 2 == meta_data.wildcard_count
    >>> most_likely_tag = meta_data.semantic_tags[0]
    >>> assert most_likely_tag == 'Z0'
    >>> least_likely_tag = meta_data.semantic_tags[-1]
    >>> assert least_likely_tag == 'Z3'
    >>> # change defaultdict to dict so the dictionary is easier to read and understand
    >>> assert ({k: dict(v) for k, v in mwe_collection.mwe_regular_expression_lookup.items()}
    ...         == {2: {'*': {'*_noun boot*_noun': re.compile('[^\\s_]*_noun\\ boot[^\\s_]*_noun')}}})
    
    ```

    '''
    
    def __init__(self, data: Optional[Dict[str, List[str]]] = None,
                 pos_mapper: Optional[Dict[str, List[str]]] = None) -> None:

        self.meta_data: Dict[str, LexiconMetaData] = {}
        self.longest_non_special_mwe_template = 0
        self.longest_wildcard_mwe_template = 0
        self.longest_mwe_template = 0
        self.most_wildcards_in_mwe_template = 0
        self.mwe_regular_expression_lookup: DefaultDict[int, DefaultDict[str, Dict[str, re.Pattern]]]\
            = collections.defaultdict(lambda: collections.defaultdict(dict))

        self.pos_mapper: Dict[str, List[str]] = {}
        self.one_to_many_pos_tags: Set[str] = set()
        self.pos_mapping_lookup: Dict[str, str] = {}
        self.pos_mapping_regular_expression_lookup: DefaultDict[LexiconType, DefaultDict[int, DefaultDict[str, Dict[str, re.Pattern]]]]\
            = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(dict)))
        
        if pos_mapper is not None:
            self.pos_mapper = pos_mapper
            for from_pos, to_pos in pos_mapper.items():
                if len(to_pos) > 1:
                    self.one_to_many_pos_tags.add(from_pos)
        
        if data is not None:
            for key, value in data.items():
                self[key] = value

    def mwe_match(self, mwe_template: str, mwe_type: LexiconType
                  ) -> List[str]:
        '''
        Returns a `List` of MWE templates, with the given `mwe_type`, that match
        the given `mwe_template`. If there are no matches the returned `List`
        will be empty.
        
        This method applies all of the special syntax rules that should be applied
        e.g. wildcards allow zero or more characters to appear after the word
        token and/or Part Of Speech (POS) tag. For more information on the MWE
        special syntax rules see the following notes.

        # Parameters
        
        mwe_template : `str`
            The MWE template that you want to match against, e.g.
            `river_noun bank_noun` or `ski_noun boots_noun`
        mwe_type : `LexiconType`
            The type of MWE templates that you want to return.

        # Returns

        `Optional[List[str]]`

        # Examples
        ``` python
        >>> from pymusas.lexicon_collection import MWELexiconCollection, LexiconType
        >>> collection = MWELexiconCollection({'walking_noun boot_noun': ['Z2'], 'ski_noun boot_noun': ['Z2'], '*_noun boot_noun': ['Z2'], '*_noun *_noun': ['Z2']})
        >>> assert [] == collection.mwe_match('river_noun bank_noun', LexiconType.MWE_NON_SPECIAL)
        >>> assert ['walking_noun boot_noun'] == collection.mwe_match('walking_noun boot_noun', LexiconType.MWE_NON_SPECIAL)
        >>> assert ['*_noun boot_noun', '*_noun *_noun'] == collection.mwe_match('walking_noun boot_noun', LexiconType.MWE_WILDCARD)
        
        ```
        '''
        mwe_templates_matches: List[str] = []
        if self.pos_mapper:
            if mwe_type == LexiconType.MWE_NON_SPECIAL:
                mwe_mapped_template = self.pos_mapping_lookup.get(mwe_template, None)
                if mwe_mapped_template is not None:
                    potential_match = self.meta_data.get(mwe_mapped_template, None)
                    if potential_match is not None:
                        potential_match_type = potential_match.lexicon_type
                        if LexiconType.MWE_NON_SPECIAL == potential_match_type:
                            mwe_templates_matches.append(mwe_mapped_template)
            
            requires_regular_expression_matching = False
            if mwe_type == LexiconType.MWE_WILDCARD:
                requires_regular_expression_matching = True
            if not mwe_templates_matches and self.one_to_many_pos_tags:
                requires_regular_expression_matching = True
            if requires_regular_expression_matching:
                n_gram_length = len(mwe_template.split())
                mwe_template_length = len(mwe_template)
                if mwe_template_length > 0:
                    for character_lookup in ['*', mwe_template[0]]:
                        regular_expression_lookup = self.pos_mapping_regular_expression_lookup[mwe_type][n_gram_length]
                        if character_lookup not in regular_expression_lookup:
                            continue

                        for (potential_mwe_match,
                             mwe_pattern) in regular_expression_lookup[character_lookup].items():
                            match = mwe_pattern.match(mwe_template)
                            if match is not None:
                                if (match.start() == 0
                                   and match.end() == mwe_template_length):
                                    mwe_templates_matches.append(potential_mwe_match)
        else:
            if mwe_type == LexiconType.MWE_NON_SPECIAL:
                potential_match = self.meta_data.get(mwe_template, None)
                if potential_match is not None:
                    potential_match_type = potential_match.lexicon_type
                    if LexiconType.MWE_NON_SPECIAL == potential_match_type:
                        mwe_templates_matches.append(mwe_template)
            elif mwe_type == LexiconType.MWE_WILDCARD:
                n_gram_length = len(mwe_template.split())
                mwe_template_length = len(mwe_template)
                if mwe_template_length > 0:
                    # By default all MWE matches can start with a * as it covers all characters.
                    for character_lookup in ['*', mwe_template[0]]:
                        regular_expression_lookup = self.mwe_regular_expression_lookup[n_gram_length]
                        if character_lookup not in regular_expression_lookup:
                            continue

                        for (potential_mwe_match,
                             mwe_pattern) in regular_expression_lookup[character_lookup].items():
                            match = mwe_pattern.match(mwe_template)
                            if match is not None:
                                if (match.start() == 0
                                   and match.end() == mwe_template_length):
                                    mwe_templates_matches.append(potential_mwe_match)

        return mwe_templates_matches

    def to_dictionary(self) -> Dict[str, List[str]]:
        '''
        Returns a dictionary of all MWE templates, the keys, stored in the
        collection and their associated semantic tags, the values.

        This can then be used to re-create a :class:`MWELexiconCollection`.

        # Returns

        `Dict[str, List[str]]`

        # Examples
        ``` python
        >>> from pymusas.lexicon_collection import (MWELexiconCollection,
        ... LexiconType, LexiconMetaData)
        >>> mwe_collection = MWELexiconCollection()
        >>> mwe_collection['*_noun boot*_noun'] = ['Z0', 'Z3']
        >>> assert (mwe_collection['*_noun boot*_noun']
        ... == LexiconMetaData(['Z0', 'Z3'], 2, LexiconType.MWE_WILDCARD, 2))
        >>> assert (mwe_collection.to_dictionary()
        ... == {'*_noun boot*_noun': ['Z0', 'Z3']})
        
        ```
        '''
        
        return {key: value.semantic_tags for key, value in self.items()}

    def to_bytes(self) -> bytes:
        '''
        Serialises the :class:`MWELexiconCollection` to a bytestring.

        # Returns

        `bytes`
        '''
        serialise = {}
        data: Dict[str, List[str]] = {key: value.semantic_tags
                                      for key, value in self.meta_data.items()}
        serialise['data'] = srsly.msgpack_dumps(data)
        serialise['pos_mapper'] = srsly.msgpack_dumps(self.pos_mapper)
        return cast(bytes, srsly.msgpack_dumps(serialise))

    @staticmethod
    def from_bytes(bytes_data: bytes) -> "MWELexiconCollection":
        '''
        Loads :class:`MWELexiconCollection` from the given bytestring and
        returns it.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.
        
        # Returns

        :class:`MWELexiconCollection`
        '''
        serialise_data = srsly.msgpack_loads(bytes_data)
        data = srsly.msgpack_loads(serialise_data['data'])
        pos_mapper = srsly.msgpack_loads(serialise_data['pos_mapper'])
        return MWELexiconCollection(data, pos_mapper)

    @staticmethod
    def from_tsv(tsv_file_path: Union[PathLike, str]
                 ) -> Dict[str, List[str]]:
        '''
        Given a `tsv_file_path` it will return a dictionary object
        that can be used to create a :class:`MWELexiconCollection`.

        Each line in the TSV file will be read in and added to a temporary
        :class:`MWELexiconCollection`, once all lines
        in the TSV have been parsed, the return value is the `data` attribute of
        the temporary :class:`MWELexiconCollection`.

        If the file path is a URL, the file will be downloaded and cached using
        :func:`pymusas.file_utils.download_url_file`.

        Code reference, the identification of a URL and the idea to do this has
        come from the [AllenNLP library](https://github.com/allenai/allennlp/blob/main/allennlp/common/file_utils.py#L205)

        # Parameters

        tsv_file_path: `Union[PathLike, str]`
            A file path or URL to a TSV file that contains at least these two
            fields:
            
            1. `mwe_template`,
            2. `semantic_tags`
            
            All other fields will be ignored.

        # Returns
        
        `Dict[str, List[str]]`
        
        # Raises
        
        `ValueError`
            If the minimum field headings, `mwe_template` and `semantic_tags`,
            do not exist in the given TSV file.

        # Examples

        ``` python
        >>> from pymusas.lexicon_collection import MWELexiconCollection
        >>> portuguese_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/mwe-pt.tsv'
        >>> mwe_lexicon_dict = MWELexiconCollection.from_tsv(portuguese_lexicon_url)
        >>> mwe_lexicon_collection = MWELexiconCollection(mwe_lexicon_dict)
        >>> assert mwe_lexicon_dict['abaixo_adv de_prep'][0] == 'M6'
        >>> assert mwe_lexicon_dict['arco_noun e_conj flecha_noun'][0] == 'K5.1'

        ```

        '''
        minimum_field_names = {'mwe_template', 'semantic_tags'}

        collection_from_tsv = MWELexiconCollection()

        if not isinstance(tsv_file_path, str):
            tsv_file_path = str(tsv_file_path)

        parsed = urlparse(tsv_file_path)
        if parsed.scheme in ("http", "https", "s3", "hf", "gs"):
            tsv_file_path = file_utils.download_url_file(tsv_file_path)

        with open(tsv_file_path, 'r', newline='', encoding='utf-8') as fp:
            csv_reader = csv.DictReader(fp, delimiter='\t')
            file_field_names: Set[str] = set()
            if csv_reader.fieldnames:
                file_field_names = set(csv_reader.fieldnames)
            if not minimum_field_names.issubset(file_field_names):
                error_msg = (f"The TSV file, {tsv_file_path}, given should "
                             "contain a header that"
                             " has at minimum the following fields "
                             f"{minimum_field_names}. The field names found "
                             f"were {file_field_names}")
                raise ValueError(error_msg)
            
            for row in csv_reader:
                mwe_template = ''
                semantic_tags: List[str] = []
                for field_name in minimum_field_names:
                    if field_name == 'semantic_tags':
                        semantic_tags = row[field_name].split()
                    elif field_name == 'mwe_template':
                        mwe_template = row[field_name]
                collection_from_tsv[mwe_template] = semantic_tags
        
        return collection_from_tsv.to_dictionary()

    @staticmethod
    def escape_mwe(mwe_template: str) -> str:
        r'''
        Returns the MWE template escaped so that it can be used in a regular
        expression.
        
        The difference between this and the normal `re.escape`
        method, is that we apply the `re.escape` method to the tokens in the
        MWE template and then replace `\*` with `[^\s_]*` so that the wildcards
        keep there original meaning with respect to the MWE special syntax rules.
        Furthermore, the POS tags in the MWE template replace the `*` with
        `[^\s_]*`.

        # Parameters

        mwe_template : `str`
            The MWE template that you want to escape, e.g.
            `river_noun bank_noun` or `*_noun boot*_noun`

        # Returns

        `str`

        # Examples
        ``` python
        >>> from pymusas.lexicon_collection import MWELexiconCollection
        >>> mwe_escaped = MWELexiconCollection.escape_mwe('ano*_prep carta_noun')
        >>> assert r'ano[^\s_]*_prep\ carta_noun' == mwe_escaped
        >>> mwe_escaped = MWELexiconCollection.escape_mwe('ano_prep carta_*')
        >>> assert r'ano_prep\ carta_[^\s_]*' == mwe_escaped

        ```
        '''
        
        escaped_mwe_template_list: List[str] = []
        for token, pos in utils.token_pos_tags_in_lexicon_entry(mwe_template):
            escaped_token = re.escape(token).replace(r'\*', r'[^\s_]*')
            escaped_pos = pos.replace(r'*', r'[^\s_]*')
            escaped_mwe_template_list.append(f'{escaped_token}_{escaped_pos}')
        escaped_mwe_template = r'\ '.join(escaped_mwe_template_list)
        return escaped_mwe_template
    
    def __setitem__(self, key: str, value: List[str]) -> None:
        '''
        # Raises

        `ValueError`
            If using a `pos_mapper` all POS tags within a MWE template cannot
            contain any wildcards or the POS tags can only be a wildcard, if
            this is not the case a `ValueError` will be raised.
        '''
        if '{' in key or '}' in key:
            warnings.warn('We do not currently support Curly Braces expressions'
                          ' within Multi Word Expression (MWE) lexicons and '
                          'therefore any MWE template that contains a `{` '
                          'or `}` will be ignored.')
            return None

        semantic_tags = value
        key_n_gram_length = len(key.split())
        mwe_type: LexiconType = LexiconType.MWE_NON_SPECIAL
        wildcard_count = 0
        
        if not self.pos_mapper:
            if '*' in key:
                mwe_type = LexiconType.MWE_WILDCARD
                wildcard_count += key.count('*')

                if wildcard_count > self.most_wildcards_in_mwe_template:
                    self.most_wildcards_in_mwe_template = wildcard_count
                
                if key_n_gram_length > self.longest_wildcard_mwe_template:
                    self.longest_wildcard_mwe_template = key_n_gram_length
                
                key_as_pattern = re.compile(self.escape_mwe(key))
                self.mwe_regular_expression_lookup[key_n_gram_length][key[0]][key] = key_as_pattern
            else:
                
                if key_n_gram_length > self.longest_non_special_mwe_template:
                    self.longest_non_special_mwe_template = key_n_gram_length
        else:
            contains_one_to_many_pos_tag = False
            pos_mapped_key_list: List[str] = []
            for token, pos in utils.token_pos_tags_in_lexicon_entry(key):
                if '*' in pos:
                    pos_error = ('When using a POS mapper a POS tag within '
                                 'a lexicon entry cannot contain a wildcard'
                                 ' unless the POS tag is only a wildcard '
                                 'and no other characters. Leixcon entry '
                                 'and POS tag in that entry that caused '
                                 f'this error: {key} {pos}')
                    if set(pos.strip()) != set('*'):
                        raise ValueError(pos_error)

                mapped_pos_list = self.pos_mapper.get(pos, [pos])
                if len(mapped_pos_list) > 1:
                    contains_one_to_many_pos_tag = True
                    mapped_pos = '|'.join(mapped_pos_list)
                    mapped_pos = '(?:' + mapped_pos + ')'
                    pos_mapped_key_list.append(f'{token}_{mapped_pos}')
                else:
                    mapped_pos = mapped_pos_list[0]
                    pos_mapped_key_list.append(f'{token}_{mapped_pos}')
            pos_mapped_key = ' '.join(pos_mapped_key_list)
            
            if '*' in pos_mapped_key:
                mwe_type = LexiconType.MWE_WILDCARD
                wildcard_count += key.count('*')

                if wildcard_count > self.most_wildcards_in_mwe_template:
                    self.most_wildcards_in_mwe_template = wildcard_count
                
                if key_n_gram_length > self.longest_wildcard_mwe_template:
                    self.longest_wildcard_mwe_template = key_n_gram_length
                
                key_as_pattern = re.compile(self.escape_mwe(pos_mapped_key))
                self.pos_mapping_regular_expression_lookup[mwe_type][key_n_gram_length][key[0]][key] = key_as_pattern
            elif contains_one_to_many_pos_tag:
                key_as_pattern = re.compile(self.escape_mwe(pos_mapped_key))
                self.pos_mapping_regular_expression_lookup[mwe_type][key_n_gram_length][key[0]][key] = key_as_pattern
                
                if key_n_gram_length > self.longest_non_special_mwe_template:
                    self.longest_non_special_mwe_template = key_n_gram_length
            else:
                self.pos_mapping_lookup[pos_mapped_key] = key
                if key_n_gram_length > self.longest_non_special_mwe_template:
                    self.longest_non_special_mwe_template = key_n_gram_length

        self.longest_mwe_template = max(self.longest_non_special_mwe_template,
                                        self.longest_wildcard_mwe_template)
        self.meta_data[key] = LexiconMetaData(semantic_tags, key_n_gram_length,
                                              mwe_type, wildcard_count)

    def __getitem__(self, key: str) -> LexiconMetaData:
        return self.meta_data[key]

    def __delitem__(self, key: str) -> None:
        
        def _get_lexicon_statistics() -> Tuple[int, int, int]:
            '''
            Returns the `longest_non_special_mwe_template`,
            `longest_wildcard_mwe_template`, and `most_wildcards_in_mwe_template`
            in the `meta_data` as a `Tuple`. This is required as after deleting
            an MWE we do not know if it has affected any of these statistics.

            # Returns

            `Tuple[int, int, int]`
            '''
            longest_non_special_mwe_template = 0
            longest_wildcard_mwe_template = 0
            wildcard_count = 0
            for value in self.values():
                mwe_type = value.lexicon_type
                key_n_gram_length = value.n_gram_length
                if mwe_type == LexiconType.MWE_NON_SPECIAL:
                    if key_n_gram_length > longest_non_special_mwe_template:
                        longest_non_special_mwe_template = key_n_gram_length
                elif mwe_type == LexiconType.MWE_WILDCARD:
                    if key_n_gram_length > longest_wildcard_mwe_template:
                        longest_wildcard_mwe_template = key_n_gram_length
                if value.wildcard_count > wildcard_count:
                    wildcard_count = value.wildcard_count
            return (longest_non_special_mwe_template,
                    longest_wildcard_mwe_template,
                    wildcard_count)
        
        lexicon_meta_data = self[key]
        del self.meta_data[key]
        
        lexicon_type = lexicon_meta_data.lexicon_type
        n_gram_length = lexicon_meta_data.n_gram_length
        if self.pos_mapper:
            if lexicon_type == LexiconType.MWE_WILDCARD:
                del self.pos_mapping_regular_expression_lookup[lexicon_type][n_gram_length][key[0]][key]
            if lexicon_type == LexiconType.MWE_NON_SPECIAL:
                unique_pos_tags_in_key = utils.unique_pos_tags_in_lexicon_entry(key)
                if self.one_to_many_pos_tags.intersection(unique_pos_tags_in_key):
                    del self.pos_mapping_regular_expression_lookup[lexicon_type][n_gram_length][key[0]][key]
                else:
                    _key_to_delete = ''
                    for _key, value in self.pos_mapping_lookup.items():
                        if value == key:
                            _key_to_delete = _key
                    if _key_to_delete:
                        del self.pos_mapping_lookup[_key_to_delete]
        else:
            if lexicon_type == LexiconType.MWE_WILDCARD:
                del self.mwe_regular_expression_lookup[n_gram_length][key[0]][key]
        
        (self.longest_non_special_mwe_template,
         self.longest_wildcard_mwe_template,
         self.most_wildcards_in_mwe_template) = _get_lexicon_statistics()
        self.longest_mwe_template = max(self.longest_non_special_mwe_template,
                                        self.longest_wildcard_mwe_template)

    def __len__(self) -> int:
        return len(self.meta_data)

    def __iter__(self) -> Generator[str, None, None]:
        for key in self.meta_data:
            yield key

    def __str__(self) -> str:
        '''
        Human readable string.
        '''

        object_str = f'{self.__class__.__name__}('
        for index, item in enumerate(self.items()):
            mwe_template = item[0]
            meta_data = item[1]
            object_str += f"('{mwe_template}': {meta_data}), "
            if index == 1:
                object_str += '... '
                break
        object_str += f') ({len(self)} entires in the collection)'
        if self.pos_mapper:
            object_str += ' (Using a POS Mapper)'
        return object_str

    def __repr__(self) -> str:
        '''
        Machine readable string. When printed and run `eval()` over the string
        you should be able to recreate the object.
        '''

        return (f'{self.__class__.__name__}(data={self.to_dictionary()}, '
                f'pos_mapper={self.pos_mapper})')

    def __eq__(self, other: object) -> bool:
        '''
        Given another object to compare too it will return `True` if the other
        object is the same class and contains the same `meta_data` and
        `pos_mapper` instance attributes.

        # Parameters

        other : `object`
            The object to compare too.
        
        # Returns

        `True`
        '''
        if not isinstance(other, MWELexiconCollection):
            return False
        
        if len(self) != len(other):
            return False

        if self.pos_mapper != other.pos_mapper:
            return False

        if self.meta_data != other.meta_data:
            return False
        
        return True
