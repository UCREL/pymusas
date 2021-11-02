<div className="source-div">
 <p><i>pymusas</i><strong>.lexicon_collection</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/lexicon_collection.py">[SOURCE]</a></p>
</div>
<div></div>

---

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

**Note** the parameters to the `__init__` are the same as the Instance
Attributes.

<h4 id="lexiconentry.instance_attributes">Instance Attributes<a className="headerlink" href="#lexiconentry.instance_attributes" title="Permanent link">&para;</a></h4>


- __lemma__ : `str` <br/>
    The lemma of a token or the token itself.
- __semantic\_tags__ : `List[str]` <br/>
    The semantic tags associated with the `lemma` and optional `POS`.
    The semantic tags are in rank order, the most likely tag associated
    tag is the first tag in the list.
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

