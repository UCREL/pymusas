---
sidebar_label: basic_tagger
title: basic_tagger
---

#### load\_lexicon

```python
def load_lexicon(lexicon_path: Path, has_headers: bool = True, include_pos: bool = True) -> Dict[str, List[str]]
```

**Arguments**:

                     TSV format with the following data in this column / field
                     order: 1. lemma, 2. Part Of Speech (POS) label / tag,
                     3. USAS / Semantic label.
                    first line contains a header row e.g. the first line
                    contain no lexicon data. When this is set to True the
                    first line of the lexicon file is ignored.
param include_pos: Whether or not the returned dictionary uses POS
                   within it&#x27;s key.
- `lexicon_path`: File path to the lexicon data. This data should be in
- `has_headers`: This should be set to True if the lexicon file on it&#x27;s

**Returns**:

A dictionary whereby the key is a tuple of

## RuleBasedTagger Objects

```python
class RuleBasedTagger()
```

#### tag\_data

```python
def tag_data(tokens: List[Tuple[str, str, str]]) -> List[List[str]]
```

**Arguments**:

               following lingustic information per token: 1. token text,
               2. lemma, 3. Part Of Speech.
- `tokens`: Each tuple represents a token. The tuple must contain the

