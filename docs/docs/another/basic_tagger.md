<div className="source-div">
 <p><i>pymusas</i><strong>.basic_tagger</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/basic_tagger.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.basic_tagger.load_lexicon"></a>

### load\_lexicon

```python
def load_lexicon(
    lexicon_path: Path,
    has_headers: bool = True,
    include_pos: bool = True
) -> Dict[str, List[str]]
```

**Arguments**:

                     TSV format with the following data in this column / field
                     order: 1. lemma, 2. Part Of Speech (POS) label / tag,
                     3. USAS / Semantic label.
                    first line contains a header row e.g. the first line
                    contain no lexicon data. When this is set to True the
                    first line of the lexicon file is ignored.
param include_pos: Whether or not the returned dictionary uses POS
                   within it's key.
- `lexicon_path`: File path to the lexicon data. This data should be in
- `has_headers`: This should be set to True if the lexicon file on it's

**Returns**:

A dictionary whereby the key is a tuple of

<a id="pymusas.basic_tagger.tag_token"></a>

### tag\_token

```python
def tag_token(
    text: str,
    lemma: str,
    pos: str,
    lexicon_lookup: Dict[str, List[str]],
    lemma_lexicon_lookup: Dict[str, List[str]]
) -> List[str]
```

__Parameters__


- __text __: [`RuleBasedTagger`](#rulebasedtagger)

<a id="pymusas.basic_tagger.RuleBasedTagger"></a>

## RuleBasedTagger

```python
class RuleBasedTagger:
 | ...
 | def __init__(lexicon_path: Path, has_headers: bool) -> None
```

__Parameters__


- __lexicon_path __: `Path`
    File path to the USAS lexicon.

- __has_headers __: `bool`
    Whether the USAS lexicon contains any header information.

__Attributes__


- `lexicon_lookup `: `Dict[str, List[str]]`

- `lexicon_lemma_lookup `: `Dict[str, List[str]]`

<a id="pymusas.basic_tagger.RuleBasedTagger.tag_data"></a>

### tag\_data

```python
class RuleBasedTagger:
 | ...
 | def tag_data(
 |     self,
 |     tokens: List[Tuple[str, str, str]]
 | ) -> List[List[str]]
```

__Parameters__


- __tokens __: `List[Tuple[str, str, str]]`
    Each tuple represents a token. The tuple must contain the
    following lingustic information per token;
    1. token text,
    2. lemma,
    3. Part Of Speech.

__Returns__


`List[List[str]]`

