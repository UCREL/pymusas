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
class LexiconType(str, Enum)
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
assert 'Single Non Special' == LexiconType.SINGLE_NON_SPECIAL
assert 'Single Non Special' == LexiconType.SINGLE_NON_SPECIAL.value
assert 'SINGLE_NON_SPECIAL' == LexiconType.SINGLE_NON_SPECIAL.name
all_possible_values = {'Single Non Special', 'MWE Non Special',
'MWE Wildcard', 'MWE Curly Braces'}
assert all_possible_values == {lexicon_type.value for lexicon_type in LexiconType}
```

<a id="pymusas.lexicon_collection.LexiconType.SINGLE_NON_SPECIAL"></a>

#### SINGLE\_NON\_SPECIAL

```python
class LexiconType(str, Enum):
 | ...
 | SINGLE_NON_SPECIAL = 'Single Non Special'
```

<a id="pymusas.lexicon_collection.LexiconType.MWE_NON_SPECIAL"></a>

#### MWE\_NON\_SPECIAL

```python
class LexiconType(str, Enum):
 | ...
 | MWE_NON_SPECIAL = 'MWE Non Special'
```

<a id="pymusas.lexicon_collection.LexiconType.MWE_WILDCARD"></a>

#### MWE\_WILDCARD

```python
class LexiconType(str, Enum):
 | ...
 | MWE_WILDCARD = 'MWE Wildcard'
```

<a id="pymusas.lexicon_collection.LexiconType.MWE_CURLY_BRACES"></a>

#### MWE\_CURLY\_BRACES

```python
class LexiconType(str, Enum):
 | ...
 | MWE_CURLY_BRACES = 'MWE Curly Braces'
```

<a id="pymusas.lexicon_collection.LexiconType.__repr__"></a>

### \_\_repr\_\_

```python
class LexiconType(str, Enum):
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

If the pos value is None then only the lemma is used: `{lemma}`,
e.g. `Car`

**Note** If the key already exists then the most recent entry will
overwrite the existing entry.

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

<a id="pymusas.lexicon_collection.LexiconCollection.to_bytes"></a>

### to\_bytes

```python
class LexiconCollection(MutableMapping):
 | ...
 | def to_bytes() -> bytes
```

Serialises the [`LexiconCollection`](#lexiconcollection) to a bytestring.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.lexicon_collection.LexiconCollection.from_bytes"></a>

### from\_bytes

```python
class LexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def from_bytes(bytes_data: bytes) -> "LexiconCollection"
```

Loads [`LexiconCollection`](#lexiconcollection) from the given bytestring and
returns it.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`LexiconCollection`](#lexiconcollection) <br/>

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

<a id="pymusas.lexicon_collection.LexiconCollection.merge"></a>

### merge

```python
class LexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def merge(
 |     *lexicon_collections: "LexiconCollection"
 | ) -> "LexiconCollection"
```

Given more than one lexicon collection it will create a single lexicon
collection whereby the lexicon data from each will be combined.

**Note** the data is loaded in list order therefore the last lexicon
collection will take precedence, i.e. if the last contains `London`: [`Z3`]
and the first contains `London`: [`Z2`] then the returned
LexiconCollection will only contain the one entry; `London`: [`Z3`].

**Note** if the lexicon collections contain POS information we assume
that all of the lexicon collections use the same POS tagset,
if they do not this could cause issues during tag time.

<h4 id="merge.parameters">Parameters<a className="headerlink" href="#merge.parameters" title="Permanent link">&para;</a></h4>


- __*lexicon\_collections__ : `LexiconCollection` <br/>
    More than one lexicon collections that are to be merged.

<h4 id="merge.returns">Returns<a className="headerlink" href="#merge.returns" title="Permanent link">&para;</a></h4>


- [`LexiconCollection`](#lexiconcollection) <br/>

<h4 id="merge.examples">Examples<a className="headerlink" href="#merge.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.lexicon_collection import LexiconCollection
welsh_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/refs/heads/master/Welsh/semantic_lexicon_cy.tsv"
english_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/refs/heads/master/English/semantic_lexicon_en.tsv"
welsh_lexicon_data = LexiconCollection.from_tsv(welsh_lexicon_url, include_pos=True)
welsh_lexicon = LexiconCollection(welsh_lexicon_data)
english_lexicon_data = LexiconCollection.from_tsv(english_lexicon_url, include_pos=True)
english_lexicon = LexiconCollection(english_lexicon_data)
combined_lexicon_collection = LexiconCollection.merge(welsh_lexicon, english_lexicon)
assert isinstance(combined_lexicon_collection, LexiconCollection)
assert combined_lexicon_collection["Aber-lash|pnoun"] == ["Z2"]
assert combined_lexicon_collection["Aqua|PROPN"] == ["Z3c"]
```

<a id="pymusas.lexicon_collection.LexiconCollection.tsv_merge"></a>

### tsv\_merge

```python
class LexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def tsv_merge(
 |     *tsv_file_paths: PathLike,
 |     *,
 |     include_pos: bool = True
 | ) -> dict[str, list[str]]
```

Given one or more TSV files it will create a single dictionary object
with the combination of all the lexicon data in each TSV, this dictionary
object can then be used to create a [`LexiconCollection`](#lexiconcollection).

For more information on how the TSV data is loaded see [`from_tsv`](#from_tsv).

**Note** the data is loaded in list order therefore the last TSV file
will take precedence, i.e. if the last TSV file contains `London`: [`Z3`]
and the first TSV file contains `London`: [`Z2`] then the returned
dictionary will only contain the one entry; `London`: [`Z3`].

**Note** if the TSV files contain POS information we assume that all
of the TSV files use the same POS tagset, if they do not this could
cause issues during tag time.

<h4 id="tsv_merge.parameters">Parameters<a className="headerlink" href="#tsv_merge.parameters" title="Permanent link">&para;</a></h4>


- __*tsv\_file\_paths__ : `PathLike` <br/>
    File paths and/or URLs to a TSV file that contains at least two
    fields, with an optional third, with the following headings:

    1. `lemma`,
    2. `semantic_tags`
    3. `pos` (Optional)

    All other fields will be ignored.
- __include\_pos__ : `bool`, optional (default = `True`) <br/>
    Whether to include the POS information, if the information is available,
    or not. See [`add_lexicon_entry`](#add_lexicon_entry) for more information on this
    parameter.

<h4 id="tsv_merge.returns">Returns<a className="headerlink" href="#tsv_merge.returns" title="Permanent link">&para;</a></h4>


- `dict[str, list[str]]` <br/>

<h4 id="tsv_merge.raises">Raises<a className="headerlink" href="#tsv_merge.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the minimum field headings, `lemma` and `semantic_tags`, do not
    exist in the given TSV files.

<h4 id="tsv_merge.examples">Examples<a className="headerlink" href="#tsv_merge.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.lexicon_collection import LexiconCollection
welsh_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/refs/heads/master/Welsh/semantic_lexicon_cy.tsv"
english_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/refs/heads/master/English/semantic_lexicon_en.tsv"
tsv_urls = [welsh_lexicon_url, english_lexicon_url]
combined_lexicon_collection = LexiconCollection.tsv_merge(*tsv_urls, include_pos=True)
assert isinstance(combined_lexicon_collection, dict)
assert combined_lexicon_collection["Aber-lash|pnoun"] == ["Z2"]
assert combined_lexicon_collection["Aqua|PROPN"] == ["Z3c"]
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

<a id="pymusas.lexicon_collection.LexiconCollection.__eq__"></a>

### \_\_eq\_\_

```python
class LexiconCollection(MutableMapping):
 | ...
 | def __eq__(other: object) -> bool
```

Given another object to compare too it will return `True` if the other
object is the same class and contains the same `data` instance attribute.

<h4 id="__eq__.parameters">Parameters<a className="headerlink" href="#__eq__.parameters" title="Permanent link">&para;</a></h4>


- __other__ : `object` <br/>
    The object to compare too.

<h4 id="__eq__.returns">Returns<a className="headerlink" href="#__eq__.returns" title="Permanent link">&para;</a></h4>


- `True` <br/>

<a id="pymusas.lexicon_collection.MWELexiconCollection"></a>

## MWELexiconCollection

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def __init__(
 |     self,
 |     data: Optional[Dict[str, List[str]]] = None,
 |     pos_mapper: Optional[Dict[str, List[str]]] = None
 | ) -> None
```

A collection that stores Multi Word Expression (MWE) templates and their
associated meta data.

This collection allows users to:

1. Easily load MWE templates from a single TSV file.
2. Find strings that match MWE templates taking into account
any special syntax rules that should be applied, e.g. wildcards allow zero
or more characters to appear after the word token and/or Part Of Speech (POS) tag.
For more information on the MWE special syntax rules see the following
[notes](/usage/notes/mwe_syntax).
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

<h4 id="mwelexiconcollection.parameters">Parameters<a className="headerlink" href="#mwelexiconcollection.parameters" title="Permanent link">&para;</a></h4>


- __data__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>
    Dictionary where the keys are MWE templates, of any [`LexiconType`](#lexicontype),
    and the values are a list of associated semantic tags.
- __pos\_mapper__ : `Dict[str, List[str]]`, optional (default = `None`) <br/>
    If not `None`, maps from the lexicon's POS tagset to the desired
    POS tagset, whereby the mapping is a `List` of tags, at the moment there
    is no preference order in this list of POS tags. The POS mapping is
    useful in situations whereby the lexicon's POS tagset is different to
    the token's. **Note** that the longer the `List[str]` for each POS
    mapping the longer it will take to match MWE templates. A one to one
    mapping will have no speed impact on the tagger. A selection of POS
    mappers can be found in [`pymusas.pos_mapper`](/pymusas/api/pos_mapper).

<h4 id="mwelexiconcollection.instance_attributes">Instance Attributes<a className="headerlink" href="#mwelexiconcollection.instance_attributes" title="Permanent link">&para;</a></h4>


**Note** if the `data` parameter given was `None` then the value of all
dictionary attributes will be an empty dictionary and all integer values will
be `0`. If `pos_mapper` parameter was `None` then the `pos_mapper` attribute
will be an empty dictionary.

- __meta\_data__ : `Dict[str, LexiconMetaData]` <br/>
    Dictionary where the keys are MWE templates, of any type, and the values
    are their associated meta data stored in a [`LexiconMetaData`](#lexiconmetadata) object.
- __longest\_non\_special\_mwe\_template__ : `int` <br/>
    The longest MWE template with no special symbols measured by n-gram size.
    For example the MWE template `ski_noun boot_noun` will be of length 2.
- __longest\_wildcard\_mwe\_template__ : `int` <br/>
    The longest MWE template with at least one wildcard (`*`) measured by n-gram size.
    For example the MWE template `*_noun boot*_noun` will be of length 2.
- __longest\_mwe\_template__ : `int` <br/>
    The longest MWE template regardless of type measured by n-gram size.
- __most\_wildcards\_in\_mwe\_template__ : `int` <br/>
    The number of wildcards in the MWE template that contains the
    most wildcards, e.g. the MWE template `ski_* *_noun` would contain 2
    wildcards. This can be 0 if you have no wildcard MWE templates.
- __mwe\_regular\_expression\_lookup__ : `Dict[int, Dict[str, Dict[str, re.Pattern]]]` <br/>
    A dictionary that can lookup all special syntax MWE templates there
    regular expression pattern. These templates are found first by
    their n-gram length and then their first character symbol. The regular
    expression pattern is used for quick matching within the [`mwe_match`](#mwe_match).
    From the special syntax only wildcard (`*`) symbols are supported at the
    moment.
- __pos\_mapper__ : `Dict[str, List[str]]` <br/>
    The given `pos_mapper`.
- __one\_to\_many\_pos\_tags__ : `Set[str]` <br/>
    A set of POS tags that have a one to many mapping, this is created based
    on the `pos_mapper`. This is empty if `pos_mapper` is `None`
- __pos\_mapping\_lookup__ : `Dict[str, str]` <br/>
    Only used if `pos_mapper` is not `None`. For all one-to-one POS mappings
    will store the mapped POS MWE template as keys and the original non-mapped
    (original) MWE templates as values, which can be used to lookup the meta
    data from `meta_data`.
- __pos\_mapping\_regular\_expression\_lookup__ : `Dict[LexiconType, Dict[int, Dict[str, Dict[str, re.Pattern]]]]` <br/>
    Only used if `pos_mapper` is not `None` and will result in
    `mwe_regular_expression_lookup` being empty as it replaces it
    functionality and extends it and by handlining the one-to-many POS
    mapping cases. When we have a one-to-many POS mapping case this requires
    a regular expression mapping even for non special syntax MWE templates.
    Compared to the `mwe_regular_expression_lookup` the first set of keys
    represent the lexicon entry match type.

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
special syntax rules see the following [notes](/usage/notes/mwe_syntax).

<h4 id="mwe_match.parameters">Parameters<a className="headerlink" href="#mwe_match.parameters" title="Permanent link">&para;</a></h4>


- __mwe\_template__ : `str` <br/>
    The MWE template that you want to match against, e.g.
    `river_noun bank_noun` or `ski_noun boots_noun`
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

<a id="pymusas.lexicon_collection.MWELexiconCollection.to_bytes"></a>

### to\_bytes

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def to_bytes() -> bytes
```

Serialises the [`MWELexiconCollection`](#mwelexiconcollection) to a bytestring.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.lexicon_collection.MWELexiconCollection.from_bytes"></a>

### from\_bytes

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def from_bytes(bytes_data: bytes) -> "MWELexiconCollection"
```

Loads [`MWELexiconCollection`](#mwelexiconcollection) from the given bytestring and
returns it.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`MWELexiconCollection`](#mwelexiconcollection) <br/>

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

<a id="pymusas.lexicon_collection.MWELexiconCollection.tsv_merge"></a>

### tsv\_merge

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | @staticmethod
 | def tsv_merge(*tsv_file_paths: PathLike) -> dict[str, list[str]]
```

Given one or more TSV files it will create a dictionary
object that can be used to create a [`MWELexiconCollection`](#mwelexiconcollection) whereby
this dictionary is the combination of all of the lexicon information
in the TSV files.

**Note** the data is loaded in list order therefore the last TSV file
will take precedence, i.e. if the last TSV file contains
`London_* city_*`: [`Z3`] and the first TSV file contains
`London_* city_*`: [`Z2`] then the returned dictionary will only
contain the one entry; `London_* city_*`: [`Z3`].

**Note** if the POS tagset used in the TSV files are different this
could cause issues during tag time.

<h4 id="tsv_merge.parameters">Parameters<a className="headerlink" href="#tsv_merge.parameters" title="Permanent link">&para;</a></h4>


- __*tsv\_file\_paths__ : `Union[PathLike, str]` <br/>
    File paths or URLs to a TSV file that contains at least these two
    fields:

    1. `mwe_template`,
    2. `semantic_tags`

    All other fields will be ignored.

<h4 id="tsv_merge.returns">Returns<a className="headerlink" href="#tsv_merge.returns" title="Permanent link">&para;</a></h4>


- `dict[str, list[str]]` <br/>

<h4 id="tsv_merge.raises">Raises<a className="headerlink" href="#tsv_merge.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the minimum field headings, `mwe_template` and `semantic_tags`,
    do not exist in the given TSV file.

<h4 id="tsv_merge.examples">Examples<a className="headerlink" href="#tsv_merge.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.lexicon_collection import LexiconCollection
welsh_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/refs/heads/master/Welsh/mwe-welsh.tsv"
english_lexicon_url = "https://raw.githubusercontent.com/UCREL/Multilingual-USAS/refs/heads/master/English/mwe-en.tsv"
tsv_urls = [welsh_lexicon_url, english_lexicon_url]
combined_lexicon_data = MWELexiconCollection.tsv_merge(*tsv_urls)
assert isinstance(combined_lexicon_data, dict)
assert combined_lexicon_data["Academy_NOUN Award_NOUN"] == ["A5.1+/K1"]
assert combined_lexicon_data["Ffwrnais_* Dyfi_*"] == ["Z2"]
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
method, is that we apply the `re.escape` method to the tokens in the
MWE template and then replace `\*` with `[^\s_]*` so that the wildcards
keep there original meaning with respect to the MWE special syntax rules.
Furthermore, the POS tags in the MWE template replace the `*` with
`[^\s_]*`.

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
mwe_escaped = MWELexiconCollection.escape_mwe('ano_prep carta_*')
assert r'ano_prep\ carta_[^\s_]*' == mwe_escaped
```

<a id="pymusas.lexicon_collection.MWELexiconCollection.__setitem__"></a>

### \_\_setitem\_\_

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def __setitem__(key: str, value: List[str]) -> None
```

<h4 id="__setitem__.raises">Raises<a className="headerlink" href="#__setitem__.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If using a `pos_mapper` all POS tags within a MWE template cannot
    contain any wildcards or the POS tags can only be a wildcard, if
    this is not the case a `ValueError` will be raised.

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

<a id="pymusas.lexicon_collection.MWELexiconCollection.__eq__"></a>

### \_\_eq\_\_

```python
class MWELexiconCollection(MutableMapping):
 | ...
 | def __eq__(other: object) -> bool
```

Given another object to compare too it will return `True` if the other
object is the same class and contains the same `meta_data` and
`pos_mapper` instance attributes.

<h4 id="__eq__.parameters">Parameters<a className="headerlink" href="#__eq__.parameters" title="Permanent link">&para;</a></h4>


- __other__ : `object` <br/>
    The object to compare too.

<h4 id="__eq__.returns">Returns<a className="headerlink" href="#__eq__.returns" title="Permanent link">&para;</a></h4>


- `True` <br/>

