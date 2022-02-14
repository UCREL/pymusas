<div className="source-div">
 <p><i>pymusas</i><strong>.lexicon_collection</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/lexicon_collection.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.lexicon_collection.LexiconType"></a>

## LexiconType

```python
@unique
class LexiconType(Enum)
```

Descriptions of the type associated to single and Multi Word Expression (MWE)
lexicon entires and templates. Any type with the word `NON_SPECIAL` means
that it does not use any special syntax, for example does not use wildcards
or curly braces.

The `value` attribute of each instance attribute is of type `str` describing
the type associated with that attribute. For the best explanation see the
example below.

<h4 id="lexicontype.instance_attributes">Instance Attributes<a className="headerlink" href="#lexicontype.instance_attributes" title="Permanent link">&para;</a></h4>


- __SINGLE\_NON\_SPECIAL__ : `LexiconType` <br/>
    Single word lexicon lookup.
- __MWE\_NON\_SPECIAL__ : `LexiconType` <br/>
    MWE lexicon lookup.
- __MWE\_WILDCARD__ : `LexiconType` <br/>
    MWE lexicon lookup using a wildcard.
- __MWE\_CURLY\_BRACES__ : `LexiconType` <br/>
    MWE lexicon lookup using curly braces.

<h4 id="lexicontype.examples">Examples<a className="headerlink" href="#lexicontype.examples" title="Permanent link">&para;</a></h4>

```python
from pymusas.lexicon_collection import LexiconType
assert 'Single Non Special' == LexiconType.SINGLE_NON_SPECIAL.value
assert 'SINGLE_NON_SPECIAL' == LexiconType.SINGLE_NON_SPECIAL.name
all_possible_values = {'Single Non Special', 'MWE Non Special',
'MWE Wildcard', 'MWE Curly Braces'}
assert all_possible_values == {lexicon_type.value for lexicon_type in LexiconType}
```

<a id="pymusas.lexicon_collection.LexiconType.SINGLE_NON_SPECIAL"></a>

#### SINGLE\_NON\_SPECIAL

```python
class LexiconType(Enum):
 | ...
 | SINGLE_NON_SPECIAL = 'Single Non Special'
```

<a id="pymusas.lexicon_collection.LexiconType.MWE_NON_SPECIAL"></a>

#### MWE\_NON\_SPECIAL

```python
class LexiconType(Enum):
 | ...
 | MWE_NON_SPECIAL = 'MWE Non Special'
```

<a id="pymusas.lexicon_collection.LexiconType.MWE_WILDCARD"></a>

#### MWE\_WILDCARD

```python
class LexiconType(Enum):
 | ...
 | MWE_WILDCARD = 'MWE Wildcard'
```

<a id="pymusas.lexicon_collection.LexiconType.MWE_CURLY_BRACES"></a>

#### MWE\_CURLY\_BRACES

```python
class LexiconType(Enum):
 | ...
 | MWE_CURLY_BRACES = 'MWE Curly Braces'
```

<a id="pymusas.lexicon_collection.LexiconType.__repr__"></a>

### \_\_repr\_\_

```python
class LexiconType(Enum):
 | ...
 | def __repr__() -> str
```

Machine readable string. When printed and run `eval()` over the string
you should be able to recreate the object.

<a id="pymusas.lexicon_collection.LexiconEntry"></a>

## LexiconEntry

```python
@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class LexiconEntry
```

A LexiconEntry contains the `semantic_tags` that are associated with a
`lemma` and optionally the lemma's `POS`.

As frozen is true, the attributes cannot be assigned another value.

This data type is mainly used for single word lexicons, rather than
Multi Word Expression (MWE).

**Note** the parameters to the `__init__` are the same as the Instance
Attributes.

<h4 id="lexiconentry.instance_attributes">Instance Attributes<a className="headerlink" href="#lexiconentry.instance_attributes" title="Permanent link">&para;</a></h4>


- __lemma__ : `str` <br/>
    The lemma of a token or the token itself.
- __semantic\_tags__ : `List[str]` <br/>
    The semantic tags associated with the `lemma` and optional `POS`.
    The semantic tags are in rank order, the most likely tag
    is the first tag in the list.
- __pos__ : `str`, optional (default = `None`) <br/>
    The Part Of Speech (POS) to be associated with the `lemma`.

<a id="pymusas.lexicon_collection.LexiconEntry.lemma"></a>

#### lemma

```python
class LexiconEntry:
 | ...
 | lemma: str = None
```

<a id="pymusas.lexicon_collection.LexiconEntry.semantic_tags"></a>

#### semantic\_tags

```python
class LexiconEntry:
 | ...
 | semantic_tags: List[str] = None
```

<a id="pymusas.lexicon_collection.LexiconEntry.pos"></a>

#### pos

```python
class LexiconEntry:
 | ...
 | pos: Optional[str] = None
```

<a id="pymusas.lexicon_collection.LexiconMetaData"></a>

## LexiconMetaData

```python
@dataclass(init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=True)
class LexiconMetaData
```

A LexiconMetaData object contains all of the meta data about a given
single word or Multi Word Expression (MWE) lexicon entry. This meta data can
be used to help rank single and MWE entries when tagging.

As frozen is true, the attributes cannot be assigned another value.

**Note** the parameters to the `__init__` are the same as the Instance
Attributes.

<h4 id="lexiconmetadata.instance_attributes">Instance Attributes<a className="headerlink" href="#lexiconmetadata.instance_attributes" title="Permanent link">&para;</a></h4>


- __semantic\_tags__ : `List[str]` <br/>
    The semantic tags associated with the lexicon entry.
    The semantic tags are in rank order, the most likely tag
    is the first tag in the list.
- __n\_gram\_length__ : `int` <br/>
    The n-gram size of the lexicon entry, e.g. `*_noun boot*_noun` will be
    of length 2 and all single word lexicon entries will be of length 1.
- __lexicon\_type__ : `LexiconType` <br/>
    Type associated to the lexicon entry.
- __wildcard\_count__ : `int` <br/>
    Number of wildcards in the lexicon entry, e.g. `*_noun boot*_noun` will
    be 2 and `ski_noun boot_noun` will be 0.

<a id="pymusas.lexicon_collection.LexiconMetaData.semantic_tags"></a>

#### semantic\_tags

```python
class LexiconMetaData:
 | ...
 | semantic_tags: List[str] = None
```

<a id="pymusas.lexicon_collection.LexiconMetaData.n_gram_length"></a>

#### n\_gram\_length

```python
class LexiconMetaData:
 | ...
 | n_gram_length: int = None
```

<a id="pymusas.lexicon_collection.LexiconMetaData.lexicon_type"></a>

#### lexicon\_type

```python
class LexiconMetaData:
 | ...
 | lexicon_type: LexiconType = None
```

<a id="pymusas.lexicon_collection.LexiconMetaData.wildcard_count"></a>

#### wildcard\_count

```python
class LexiconMetaData:
 | ...
 | wildcard_count: int = None
```

<a id="pymusas.lexicon_collection.LexiconCollection"></a>

## LexiconCollection

```python
class LexiconCollection(MutableMapping):
 | ...
 | def __init__(
 |     self,
 |     data: Optional[Dict[str, List[str]]] = None
 | ) -> None
```

This is a dictionary object that will hold [`LexiconEntry`](#lexiconentry) data in a fast to
access object. The keys of the dictionary are expected to be either just a
lemma or a combination of lemma and pos in the following format:
`{lemma}|{pos}` e.g. `Car|Noun`.

The value to each key is the associated semantic tags, whereby the semantic
tags are in rank order, the most likely tag is the first tag in the list.

**Note** that the `lemma` can be the token
itself rather than just it's base form, e.g. can be `Cars` rather than `Car`.

This data type is used for single word lexicons, to store Multi Word
Expression (MWE) see the [`MWELexiconCollection`](#mwelexiconcollection).

<h4 id="lexiconcollection.parameters">Parameters<a className="headerlink" href="#lexiconcollection.parameters" title="Permanent link">&para;</a></h4>


- __data__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>

<h4 id="lexiconcollection.instance_attributes">Instance Attributes<a className="headerlink" href="#lexiconcollection.instance_attributes" title="Permanent link">&para;</a></h4>


- __data__ : `Dict[str, List[str]]` <br/>
    Dictionary where the keys are `{lemma}|{pos}` and the values are
    a list of associated semantic tags. If the `data` parameter given was
    `None` then the value of this attribute will be an empty dictionary.

<h4 id="lexiconcollection.examples">Examples<a className="headerlink" href="#lexiconcollection.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.lexicon_collection import LexiconEntry, LexiconCollection
lexicon_entry = LexiconEntry('London', ['Z3', 'Z1', 'A1'], 'noun')
collection = LexiconCollection()
collection.add_lexicon_entry(lexicon_entry)
most_likely_tag = collection['London|noun'][0]
assert most_likely_tag == 'Z3'
least_likely_tag = collection['London|noun'][-1]
assert least_likely_tag == 'A1'
```

<a id="pymusas.lexicon_collection.LexiconCollection.add_lexicon_entry"></a>

### add\_lexicon\_entry

```python
class LexiconCollection(MutableMapping):
 | ...
 | def add_lexicon_entry(
 |     self,
 |     value: LexiconEntry,
 |     include_pos: bool = True
 | ) -> None
```

Will add the [`LexiconEntry`](#lexiconentry) to the collection, whereby the key is the
combination of the lemma and pos and the value are the semantic tags.

The lemma and pos are combined as follows: `{lemma}|{pos}`, e.g.
`Car|Noun`

If the pos value is None then then only the lemma is used: `{lemma}`,
e.g. `Car`

<h4 id="add_lexicon_entry.parameters">Parameters<a className="headerlink" href="#add_lexicon_entry.parameters" title="Permanent link">&para;</a></h4>


- __value__ : `LexiconEntry` <br/>
    Lexicon Entry to add to the collection.
- __include\_pos__ : `bool`, optional (default = `True`) <br/>
    Whether to include the POS tag within the key.

<a id="pymusas.lexicon_collection.LexiconCollection.to_dictionary"></a>

### to\_dictionary

```python
class LexiconCollection(MutableMapping):
 | ...
 | def to_dictionary() -> Dict[str, List[str]]
```

Returns the `data` instance attribute.

<h4 id="to_dictionary.returns">Returns<a className="headerlink" href="#to_dictionary.returns" title="Permanent link">&para;</a></h4>


- `Dict[str, List[str]]` <br/>

<a id="pymusas.lexicon_collection.LexiconCollection.from_tsv"></a>

### from\_tsv

```python
class LexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def from_tsv(
 |     tsv_file_path: Union[PathLike, str],
 |     include_pos: bool = True
 | ) -> Dict[str, List[str]]
```

Given a `tsv_file_path` it will return a dictionary object that can
be used to create a [`LexiconCollection`](#lexiconcollection).

Each line in the TSV file will be read in as a [`LexiconEntry`](#lexiconentry)
and added to a temporary [`LexiconCollection`](#lexiconcollection), once all lines
in the TSV have been parsed the return value is the `data` attribute of
the temporary [`LexiconCollection`](#lexiconcollection).

If the file path is a URL, the file will be downloaded and cached using
[`pymusas.file_utils.download_url_file`](/pymusas/api/file_utils/#download_url_file).

If `include_pos` is True and the TSV file does not contain a
`pos` field heading then this will return a LexiconCollection that is
identical to a collection that ran this method with `include_pos` equal
to False.

Code reference, the identification of a URL and the idea to do this has
come from the [AllenNLP library](https://github.com/allenai/allennlp/blob/main/allennlp/common/file_utils.py#L205)

<h4 id="from_tsv.parameters">Parameters<a className="headerlink" href="#from_tsv.parameters" title="Permanent link">&para;</a></h4>


- __tsv\_file\_path__ : `Union[PathLike, str]` <br/>
    A file path or URL to a TSV file that contains at least two
    fields, with an optional third, with the following headings:

    1. `lemma`,
    2. `semantic_tags`
    3. `pos` (Optional)

    All other fields will be ignored.
- __include\_pos__ : `bool`, optional (default = `True`) <br/>
    Whether to include the POS information, if the information is avaliable,
    or not. See [`add_lexicon_entry`](#add_lexicon_entry) for more information on this
    parameter.

<h4 id="from_tsv.returns">Returns<a className="headerlink" href="#from_tsv.returns" title="Permanent link">&para;</a></h4>


- `Dict[str, List[str]]` <br/>

<h4 id="from_tsv.raises">Raises<a className="headerlink" href="#from_tsv.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the minimum field headings, `lemma` and `semantic_tags`, do not
    exist in the given TSV file.

<h4 id="from_tsv.examples">Examples<a className="headerlink" href="#from_tsv.examples" title="Permanent link">&para;</a></h4>


`include_pos` = `True`
``` python
from pymusas.lexicon_collection import LexiconCollection
welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
welsh_lexicon_dict = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
welsh_lexicon_collection = LexiconCollection(welsh_lexicon_dict)
assert welsh_lexicon_dict['ceir|noun'][0] == 'M3fn'
assert welsh_lexicon_dict['ceir|verb'][0] == 'A9+'
```

`include_pos` = `False`
``` python
from pymusas.lexicon_collection import LexiconCollection
welsh_lexicon_url = 'https://raw.githubusercontent.com/apmoore1/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
welsh_lexicon_dict = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=False)
welsh_lexicon_collection = LexiconCollection(welsh_lexicon_dict)
assert welsh_lexicon_dict['ceir'][0] == 'M3fn'
```

<a id="pymusas.lexicon_collection.LexiconCollection.__str__"></a>

### \_\_str\_\_

```python
class LexiconCollection(MutableMapping):
 | ...
 | def __str__() -> str
```

Human readable string.

<a id="pymusas.lexicon_collection.LexiconCollection.__repr__"></a>

### \_\_repr\_\_

```python
class LexiconCollection(MutableMapping):
 | ...
 | def __repr__() -> str
```

Machine readable string. When printed and run `eval()` over the string
you should be able to recreate the object.

<a id="pymusas.lexicon_collection.MWELexiconCollection"></a>

## MWELexiconCollection

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def __init__(
 |     self,
 |     data: Optional[Dict[str, List[str]]] = None
 | ) -> None
```

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

<h4 id="mwelexiconcollection.parameters">Parameters<a className="headerlink" href="#mwelexiconcollection.parameters" title="Permanent link">&para;</a></h4>


- __data__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>
    Dictionary where the keys are MWE templates, of any [`LexiconType`](#lexicontype),
    and the values are a list of associated semantic tags.

<h4 id="mwelexiconcollection.instance_attributes">Instance Attributes<a className="headerlink" href="#mwelexiconcollection.instance_attributes" title="Permanent link">&para;</a></h4>


**Note** if the `data` parameter given was `None` then the value of all
dictionary attributes will be an empty dictionary and all integer values will
be `0`.

- __meta\_data__ : `Dict[str, LexiconMetaData]` <br/>
    Dictionary where the keys are MWE templates, of any type, and the values
    are their associated meta data stored in a [`LexiconMetaData`](#lexiconmetadata) object.
- __longest\_non\_special\_mwe\_template__ : `int` <br/>
    The longest MWE template with no special symbols measured by n-gram size.
    For example the MWE template `ski_noun boot_noun` will be of length 2.
- __longest\_wildcard\_mwe\_template__ : `int` <br/>
    The longest MWE template with at least one wildcard (`*`) measured by n-gram size.
    For example the MWE template `*_noun boot*_noun` will be of length 2.
- __mwe\_regular\_expression\_lookup__ : `Dict[int, Dict[str, Dict[str, re.Pattern]]]` <br/>
    A dictionary that can lookup all special syntax MWE templates and there
    regular expression pattern, only wildcard (`*`) symbols are supported, by
    there n-gram length and then there first character symbol. The regular
    expression pattern is used for quick matching within the [`mwe_match`](#mwe_match).

<h4 id="mwelexiconcollection.examples">Examples<a className="headerlink" href="#mwelexiconcollection.examples" title="Permanent link">&para;</a></h4>

``` python
import re
from pymusas.lexicon_collection import MWELexiconCollection, LexiconType
mwe_collection = MWELexiconCollection()
mwe_collection['*_noun boot*_noun'] = ['Z0', 'Z3']
meta_data = mwe_collection['*_noun boot*_noun']
assert 2 == meta_data.n_gram_length
assert LexiconType.MWE_WILDCARD == meta_data.lexicon_type
assert 2 == meta_data.wildcard_count
most_likely_tag = meta_data.semantic_tags[0]
assert most_likely_tag == 'Z0'
least_likely_tag = meta_data.semantic_tags[-1]
assert least_likely_tag == 'Z3'
# change defaultdict to dict so the dictionary is easier to read and understand
assert ({k: dict(v) for k, v in mwe_collection.mwe_regular_expression_lookup.items()}
        == {2: {'*': {'*_noun boot*_noun': re.compile('[^\\s_]*_noun\\ boot[^\\s_]*_noun')}}})
```

<a id="pymusas.lexicon_collection.MWELexiconCollection.mwe_match"></a>

### mwe\_match

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def mwe_match(
 |     self,
 |     mwe_template: str,
 |     mwe_type: LexiconType
 | ) -> List[str]
```

Returns a `List` of MWE templates, with the given `mwe_type`, that match
the given `mwe_template`. If there are no matches the returned `List`
will be empty.

This method applies all of the special syntax rules that should be applied
e.g. wildcards allow zero or more characters to appear after the word
token and/or Part Of Speech (POS) tag. For more information on the MWE
special syntax rules see the following notes.

<h4 id="mwe_match.parameters">Parameters<a className="headerlink" href="#mwe_match.parameters" title="Permanent link">&para;</a></h4>


- __mwe\_template__ : `str` <br/>
    The MWE template that you want to match against, e.g.
    `river_noun bank_noun` or `*_noun boot*_noun`
- __mwe\_type__ : `LexiconType` <br/>
    The type of MWE templates that you want to return.

<h4 id="mwe_match.returns">Returns<a className="headerlink" href="#mwe_match.returns" title="Permanent link">&para;</a></h4>


- `Optional[List[str]]` <br/>

<h4 id="mwe_match.examples">Examples<a className="headerlink" href="#mwe_match.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.lexicon_collection import MWELexiconCollection, LexiconType
collection = MWELexiconCollection({'walking_noun boot_noun': ['Z2'], 'ski_noun boot_noun': ['Z2'], '*_noun boot_noun': ['Z2'], '*_noun *_noun': ['Z2']})
assert [] == collection.mwe_match('river_noun bank_noun', LexiconType.MWE_NON_SPECIAL)
assert ['walking_noun boot_noun'] == collection.mwe_match('walking_noun boot_noun', LexiconType.MWE_NON_SPECIAL)
assert ['*_noun boot_noun', '*_noun *_noun'] == collection.mwe_match('walking_noun boot_noun', LexiconType.MWE_WILDCARD)
```

<a id="pymusas.lexicon_collection.MWELexiconCollection.to_dictionary"></a>

### to\_dictionary

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def to_dictionary() -> Dict[str, List[str]]
```

Returns a dictionary of all MWE templates, the keys, stored in the
collection and their associated semantic tags, the values.

This can then be used to re-create a [`MWELexiconCollection`](#mwelexiconcollection).

<h4 id="to_dictionary.returns">Returns<a className="headerlink" href="#to_dictionary.returns" title="Permanent link">&para;</a></h4>


- `Dict[str, List[str]]` <br/>

<h4 id="to_dictionary.examples">Examples<a className="headerlink" href="#to_dictionary.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.lexicon_collection import (MWELexiconCollection,
LexiconType, LexiconMetaData)
mwe_collection = MWELexiconCollection()
mwe_collection['*_noun boot*_noun'] = ['Z0', 'Z3']
assert (mwe_collection['*_noun boot*_noun']
== LexiconMetaData(['Z0', 'Z3'], 2, LexiconType.MWE_WILDCARD, 2))
assert (mwe_collection.to_dictionary()
== {'*_noun boot*_noun': ['Z0', 'Z3']})
```

<a id="pymusas.lexicon_collection.MWELexiconCollection.from_tsv"></a>

### from\_tsv

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def from_tsv(
 |     tsv_file_path: Union[PathLike, str]
 | ) -> Dict[str, List[str]]
```

Given a `tsv_file_path` it will return a dictionary object
that can be used to create a [`MWELexiconCollection`](#mwelexiconcollection).

Each line in the TSV file will be read in and added to a temporary
[`MWELexiconCollection`](#mwelexiconcollection), once all lines
in the TSV have been parsed, the return value is the `data` attribute of
the temporary [`MWELexiconCollection`](#mwelexiconcollection).

If the file path is a URL, the file will be downloaded and cached using
[`pymusas.file_utils.download_url_file`](/pymusas/api/file_utils/#download_url_file).

Code reference, the identification of a URL and the idea to do this has
come from the [AllenNLP library](https://github.com/allenai/allennlp/blob/main/allennlp/common/file_utils.py#L205)

<h4 id="from_tsv.parameters">Parameters<a className="headerlink" href="#from_tsv.parameters" title="Permanent link">&para;</a></h4>


- __tsv\_file\_path__ : `Union[PathLike, str]` <br/>
    A file path or URL to a TSV file that contains at least these two
    fields:

    1. `mwe_template`,
    2. `semantic_tags`

    All other fields will be ignored.

<h4 id="from_tsv.returns">Returns<a className="headerlink" href="#from_tsv.returns" title="Permanent link">&para;</a></h4>


- `Dict[str, List[str]]` <br/>

<h4 id="from_tsv.raises">Raises<a className="headerlink" href="#from_tsv.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the minimum field headings, `mwe_template` and `semantic_tags`,
    do not exist in the given TSV file.

<h4 id="from_tsv.examples">Examples<a className="headerlink" href="#from_tsv.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.lexicon_collection import MWELexiconCollection
portuguese_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/mwe-pt.tsv'
mwe_lexicon_dict = MWELexiconCollection.from_tsv(portuguese_lexicon_url)
mwe_lexicon_collection = MWELexiconCollection(mwe_lexicon_dict)
assert mwe_lexicon_dict['abaixo_adv de_prep'][0] == 'M6'
assert mwe_lexicon_dict['arco_noun e_conj flecha_noun'][0] == 'K5.1'
```

<a id="pymusas.lexicon_collection.MWELexiconCollection.escape_mwe"></a>

### escape\_mwe

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def escape_mwe(mwe_template: str) -> str
```

Returns the MWE template escaped so that it can be used in a regular
expression.

The difference between this and the normal `re.escape`
method, is that we apply the `re.escape` method to the MWE template and
then replace `\*` with `[^\s_]*` so that the wildcards keep there original
meaning with respect to the MWE special syntax rules.

<h4 id="escape_mwe.parameters">Parameters<a className="headerlink" href="#escape_mwe.parameters" title="Permanent link">&para;</a></h4>


- __mwe\_template__ : `str` <br/>
    The MWE template that you want to escape, e.g.
    `river_noun bank_noun` or `*_noun boot*_noun`

<h4 id="escape_mwe.returns">Returns<a className="headerlink" href="#escape_mwe.returns" title="Permanent link">&para;</a></h4>


- `str` <br/>

<h4 id="escape_mwe.examples">Examples<a className="headerlink" href="#escape_mwe.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.lexicon_collection import MWELexiconCollection
mwe_escaped = MWELexiconCollection.escape_mwe('ano*_prep carta_noun')
assert r'ano[^\s_]*_prep\ carta_noun' == mwe_escaped
```

<a id="pymusas.lexicon_collection.MWELexiconCollection.__str__"></a>

### \_\_str\_\_

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def __str__() -> str
```

Human readable string.

<a id="pymusas.lexicon_collection.MWELexiconCollection.__repr__"></a>

### \_\_repr\_\_

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def __repr__() -> str
```

Machine readable string. When printed and run `eval()` over the string
you should be able to recreate the object.

