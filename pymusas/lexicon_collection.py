import collections
from collections.abc import MutableMapping
import csv
from dataclasses import dataclass
from enum import Enum, unique
from os import PathLike
import re
import typing
from typing import DefaultDict, Dict, Generator, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse

from . import file_utils


@unique
class LexiconType(Enum):
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

    **Note** that even though this a sub-class of a MutableMapping it has a
    time complexity of O(n) for deletion unlike the standard Python MutableMapping,
    see the [following dict time complexities](https://wiki.python.org/moin/TimeComplexity),
    this is due to keeping track of the `longest_non_special_mwe_template` and
    `longest_wildcard_mwe_template`.

    # Parameters

    data: `Dict[str, List[str]]`, optional (default = `None`)
        Dictionary where the keys are MWE templates, of any :class:`LexiconType`,
        and the values are a list of associated semantic tags.

    # Instance Attributes
    
    **Note** if the `data` parameter given was `None` then the value of all
    dictionary attributes will be an empty dictionary and all integer values will
    be `0`.
    
    meta_data: `Dict[str, Tuple[List[str], int, LexiconType]]`
        Dictionary where the keys are MWE templates, of any type, and the values
        are a Tuple of length 3 containing the following meta data on the MWE
        template:
        
        1. Semantic tags.
        2. Length of the MWE template, measured by n-gram size.
        3. Type of MWE as defined by the :class:`LexiconType`, e.g. `LexiconType.MWE_NON_SPECIAL`
    longest_non_special_mwe_template : `int`
        The longest MWE template with no special symbols measured by n-gram size.
        For example the MWE template `ski_noun boot_noun` will be of length 2.
    longest_wildcard_mwe_template : `int`
        The longest MWE template with at least one wildcard (`*`) measured by n-gram size.
        For example the MWE template `*_noun boot*_noun` will be of length 2.
    mwe_regular_expression_lookup: `Dict[int, Dict[str, Dict[str, re.Pattern]]]`
        A dictionary that can lookup all special syntax MWE templates and there
        regular expression pattern, only wildcard (`*`) symbols are supported, by
        there n-gram length and then there first character symbol. The regular
        expression pattern is used for quick matching within the :func:`mwe_match`.

    # Examples
    ``` python
    >>> import re
    >>> from pymusas.lexicon_collection import MWELexiconCollection, LexiconType
    >>> mwe_collection = MWELexiconCollection()
    >>> mwe_collection['*_noun boot*_noun'] = ['Z0', 'Z3']
    >>> semantic_tags, n_gram_length, mwe_type = mwe_collection['*_noun boot*_noun']
    >>> assert 2 == n_gram_length
    >>> assert LexiconType.MWE_WILDCARD == mwe_type
    >>> most_likely_tag = semantic_tags[0]
    >>> assert most_likely_tag == 'Z0'
    >>> least_likely_tag = semantic_tags[-1]
    >>> assert least_likely_tag == 'Z3'
    >>> # change defaultdict to dict so the dictionary is easier to read and understand
    >>> assert ({k: dict(v) for k, v in mwe_collection.mwe_regular_expression_lookup.items()}
    ...         == {2: {'*': {'*_noun boot*_noun': re.compile('[^\\s_]*_noun\\ boot[^\\s_]*_noun')}}})
    
    ```

    '''
    
    def __init__(self, data: Optional[Dict[str, List[str]]] = None) -> None:

        self.meta_data: Dict[str, Tuple[List[str], int, LexiconType]] = {}
        self.longest_non_special_mwe_template = 0
        self.longest_wildcard_mwe_template = 0
        self.mwe_regular_expression_lookup: DefaultDict[int, DefaultDict[str, Dict[str, re.Pattern]]]\
            = collections.defaultdict(lambda: collections.defaultdict(dict))
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
            `river_noun bank_noun` or `*_noun boot*_noun`
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
        mew_templates_matches: List[str] = []
        if mwe_type == LexiconType.MWE_NON_SPECIAL:
            potential_match = self.meta_data.get(mwe_template, None)
            if potential_match is not None:
                potential_match_type = potential_match[2]
                if LexiconType.MWE_NON_SPECIAL == potential_match_type:
                    mew_templates_matches.append(mwe_template)
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
                                mew_templates_matches.append(potential_mwe_match)
        
        return mew_templates_matches

    def to_dictionary(self) -> Dict[str, List[str]]:
        '''
        Returns a dictionary of all MWE templates, the keys, stored in the
        collection and their associated semantic tags, the values.

        This can then be used to re-create a :class:`MWELexiconCollection`.

        # Returns

        `Dict[str, List[str]]`

        # Examples
        ``` python
        >>> from pymusas.lexicon_collection import MWELexiconCollection, LexiconType
        >>> mwe_collection = MWELexiconCollection()
        >>> mwe_collection['*_noun boot*_noun'] = ['Z0', 'Z3']
        >>> assert (mwe_collection['*_noun boot*_noun']
        ... == (['Z0', 'Z3'], 2, LexiconType.MWE_WILDCARD))
        >>> assert (mwe_collection.to_dictionary()
        ... == {'*_noun boot*_noun': ['Z0', 'Z3']})
        
        ```
        '''
        
        return {key: value[0] for key, value in self.items()}

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

        with open(tsv_file_path, 'r', newline='') as fp:
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
        method, is that we apply the `re.escape` method to the MWE template and
        then replace `\*` with `[^\s_]*` so that the wildcards keep there original
        meaning with respect to the MWE special syntax rules.

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

        ```
        '''
        escaped_mwe_template = re.escape(mwe_template)
        escaped_mwe_template = escaped_mwe_template.replace(r'\*', r'[^\s_]*')
        return escaped_mwe_template
    
    def __setitem__(self, key: str, value: List[str]) -> None:
        semantic_tags = value
        key_n_gram_length = len(key.split())
        mwe_type: LexiconType = LexiconType.MWE_NON_SPECIAL
        
        if '*' in key:
            mwe_type = LexiconType.MWE_WILDCARD
            
            if key_n_gram_length > self.longest_wildcard_mwe_template:
                self.longest_wildcard_mwe_template = key_n_gram_length
            
            key_as_pattern = re.compile(self.escape_mwe(key))
            self.mwe_regular_expression_lookup[key_n_gram_length][key[0]][key] = key_as_pattern
        else:
            
            if key_n_gram_length > self.longest_non_special_mwe_template:
                self.longest_non_special_mwe_template = key_n_gram_length
        
        self.meta_data[key] = (semantic_tags, key_n_gram_length, mwe_type)

    def __getitem__(self, key: str) -> Tuple[List[str], int, LexiconType]:
        return self.meta_data[key]

    def __delitem__(self, key: str) -> None:
        
        def _get_new_longest_n_gram_lengths() -> Tuple[int, int]:
            '''
            Returns the `longest_non_special_mwe_template` and
            `longest_wildcard_mwe_template` in the `meta_data`. This is required
            after deleting an MWE as we do not know if we have just deleted the
            longest non-special or wildcard MWE.

            # Returns

            `Tuple[int, int]`
            '''
            longest_non_special_mwe_template = 0
            longest_wildcard_mwe_template = 0
            for value in self.values():
                mwe_type = value[2]
                key_n_gram_length = value[1]
                if mwe_type == LexiconType.MWE_NON_SPECIAL:
                    if key_n_gram_length > longest_non_special_mwe_template:
                        longest_non_special_mwe_template = key_n_gram_length
                elif mwe_type == LexiconType.MWE_WILDCARD:
                    if key_n_gram_length > longest_wildcard_mwe_template:
                        longest_wildcard_mwe_template = key_n_gram_length
            return longest_non_special_mwe_template, longest_wildcard_mwe_template
        
        _, key_n_gram_length, mwe_type = self[key]
        del self.meta_data[key]
        
        if mwe_type == LexiconType.MWE_WILDCARD:
            del self.mwe_regular_expression_lookup[key_n_gram_length][key[0]][key]
        
        (self.longest_non_special_mwe_template,
         self.longest_wildcard_mwe_template) = _get_new_longest_n_gram_lengths()

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
            semantic_tags, n_gram_length, mwe_type = item[1]
            object_str += (f"('{mwe_template}': "
                           f"({semantic_tags}, {n_gram_length}, {mwe_type})), ")
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

        return f'{self.__class__.__name__}(data={self.to_dictionary()})'
