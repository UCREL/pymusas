---
sidebar_label: lexicon_collection
title: lexicon_collection
---

## LexiconEntry Objects

```python
@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=True)
class LexiconEntry()
```

As frozen is true no values can be assigned after creation of an instance of
this class.

## LexiconCollection Objects

```python
class LexiconCollection(MutableMapping)
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
lexicon_entry = LexiconEntry(&#x27;London&#x27;, [&#x27;Z3&#x27;, &#x27;Z1&#x27;, &#x27;A1&#x27;], &#x27;noun&#x27;)
collection = LexiconCollection()
collection.add_lexicon_entry(lexicon_entry)
most_likely_tag = collection[&#x27;London|noun&#x27;][0]
least_likely_tag = collection[&#x27;London|noun&#x27;][-1]
```

#### \_\_str\_\_

```python
def __str__() -> str
```

Human readable string.

#### \_\_repr\_\_

```python
def __repr__() -> str
```

Machine readable string. When printed and run eval() over the string
you should be able to recreate the object.

#### add\_lexicon\_entry

```python
def add_lexicon_entry(value: LexiconEntry, include_pos: bool = True) -> None
```

Will add the LexiconEntry to the collection, whereby the key is the
combination of the lemma and pos and the value is the semantic tags.

The lemma and pos are combined as follows:
{lemma}|{pos}

If the pos value is None then then only the lemma is used, e.g.:
{lemma}

**Arguments**:

- `value`: A LexiconEntry.
- `include_pos`: Whether to include the POS tag within the key.

#### to\_dictionary

```python
def to_dictionary() -> Dict[str, List[str]]
```

**Returns**:

The dictionary object that stores all of the data.

#### from\_tsv

```python
@staticmethod
def from_tsv(tsv_file_path: Union[PathLike, str], include_pos: bool = True) -> Dict[str, List[str]]
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

**Arguments**:

                      fields with the following headings: 1. `lemma`,
                      and 2. `semantic_tags`. With an optional field
                      `pos`. All other fields will be ignored.
                      Each row will be used to create a `LexiconEntry`
                      which will then be added to the returneds
                      `LexiconCollection`
                    adding the `LexiconEntry` into the returned
                    `LexiconCollection`. For more information on this
                    see the `add_lexicon_entry` method.
- `tsv_file_path`: A path or URL to a TSV file that contains at least two
- `include_pos`: Whether to include the POS tag in the key when

**Returns**:

A dictionary object that can be used to create a

