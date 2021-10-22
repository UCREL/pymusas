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

As frozen is true no values can be assigned after creation of an instance of
this class.

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

This is a dictionary object that will hold LexiconEntry data in a fast to
access object. The keys of the dictionary are expected to be either just a
lemma or a combination of lemma and pos in the following format:
{lemma}|{pos}

The value to each key is the associated semantic tags, whereby the semantic
tags are in rank order, the most likely tag is the first tag in the list.
For example in the collection below, for the lemma London with a POS tag noun
the most likely semantic tag is Z3 and the least likely tag is A1:

```
from pymusas.lexicon_collection import LexiconEntry, LexiconCollection
lexicon_entry = LexiconEntry('London', ['Z3', 'Z1', 'A1'], 'noun')
collection = LexiconCollection()
collection.add_lexicon_entry(lexicon_entry)
most_likely_tag = collection['London|noun'][0]
least_likely_tag = collection['London|noun'][-1]
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

Machine readable string. When printed and run eval() over the string
you should be able to recreate the object.

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

Will add the LexiconEntry to the collection, whereby the key is the
combination of the lemma and pos and the value is the semantic tags.

The lemma and pos are combined as follows:
{lemma}|{pos}

If the pos value is None then then only the lemma is used, e.g.:
{lemma}

:param value: A LexiconEntry.
:param include_pos: Whether to include the POS tag within the key.

<a id="pymusas.lexicon_collection.LexiconCollection.to_dictionary"></a>

### to\_dictionary

```python
class LexiconCollection(MutableMapping):
 | ...
 | def to_dictionary() -> Dict[str, List[str]]
```

:returns: The dictionary object that stores all of the data.

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

If `include_pos` is True and the TSV file does not contain a
`pos` field heading then this will return a LexiconCollection that is
identical to a collection that ran this method with `include_pos` equal
to False.

If the file path is a URL, the file will be downloaded and cached using
`file_utils.download_url_file` function.

Reference, the identification of a URL and the idea to do this has
come from the AllenNLP library:
https://github.com/allenai/allennlp/blob/main/allennlp/common/file_utils.py#L205

:param tsv_file_path: A path or URL to a TSV file that contains at least two
                      fields with the following headings: 1. `lemma`,
                      and 2. `semantic_tags`. With an optional field
                      `pos`. All other fields will be ignored.
                      Each row will be used to create a `LexiconEntry`
                      which will then be added to the returneds
                      `LexiconCollection`
:param include_pos: Whether to include the POS tag in the key when
                    adding the `LexiconEntry` into the returned
                    `LexiconCollection`. For more information on this
                    see the `add_lexicon_entry` method.
:returns: A dictionary object that can be used to create a
          `LexiconCollection`
:raises: ValueError if the minimum field headings, lemma and
         semantic_tags, do not exist in the given TSV file.

