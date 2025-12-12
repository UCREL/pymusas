<div className="source-div">
 <p><i>pymusas</i><strong>.utils</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/utils.py">[SOURCE]</a></p>
</div>
<div></div>

---

This module contains various helper functions that are used in other modules.

<h4 id="pymusas.utils.attributes">Attributes<a className="headerlink" href="#pymusas.utils.attributes" title="Permanent link">&para;</a></h4>


- __NEURAL\_EXTRA\_PACKAGES__ : `list[str]` <br/>
    The Python packages that are required for the `pymusas[neural]` extra.

<a id="pymusas.utils.NEURAL_EXTRA_PACKAGES"></a>

#### NEURAL\_EXTRA\_PACKAGES

```python
NEURAL_EXTRA_PACKAGES: list[str] = ['transformers', 'wsd_torch_models', 'torch']
```

<a id="pymusas.utils.token_pos_tags_in_lexicon_entry"></a>

### token\_pos\_tags\_in\_lexicon\_entry

```python
def token_pos_tags_in_lexicon_entry(
    lexicon_entry: str
) -> Iterable[Tuple[str, str]]
```

Yields the token and associated POS tag in the given `lexicon_entry`.

<h4 id="token_pos_tags_in_lexicon_entry.parameters">Parameters<a className="headerlink" href="#token_pos_tags_in_lexicon_entry.parameters" title="Permanent link">&para;</a></h4>


- __lexicon\_entry__ : `str` <br/>
    Either a Multi Word Expression template or single word lexicon entry,
    which is a sequence of words/tokens and Part Of Speech (POS) tags
    joined together by an underscore and separated by a single whitespace,
    e.g. `word1_POS1 word2_POS2 word3_POS3`. For a single word lexicon it
    would be `word1_POS1`.

<h4 id="token_pos_tags_in_lexicon_entry.returns">Returns<a className="headerlink" href="#token_pos_tags_in_lexicon_entry.returns" title="Permanent link">&para;</a></h4>


- `Iterable[Tuple[str, str]]` <br/>

<h4 id="token_pos_tags_in_lexicon_entry.raises">Raises<a className="headerlink" href="#token_pos_tags_in_lexicon_entry.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the lexicon entry when split on whitespace and then split by `_`
    does not create a `Iterable[Tuple[str, str]]` whereby the tuple contains
    the `token text` and it's associated `POS tag`.

<h4 id="token_pos_tags_in_lexicon_entry.examples">Examples<a className="headerlink" href="#token_pos_tags_in_lexicon_entry.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.utils import token_pos_tags_in_lexicon_entry
mwe_template = 'East_noun London_noun is_det great_adj'
assert ([('East', 'noun'), ('London', 'noun'), ('is', 'det'), ('great', 'adj')]
        == list(token_pos_tags_in_lexicon_entry(mwe_template)))
single_word_lexicon = 'East_noun'
assert ([('East', 'noun')]
        == list(token_pos_tags_in_lexicon_entry(single_word_lexicon)))
```

<a id="pymusas.utils.unique_pos_tags_in_lexicon_entry"></a>

### unique\_pos\_tags\_in\_lexicon\_entry

```python
def unique_pos_tags_in_lexicon_entry(
    lexicon_entry: str
) -> Set[str]
```

Returns the unique POS tag values in the given `lexicon_entry`.

<h4 id="unique_pos_tags_in_lexicon_entry.parameters">Parameters<a className="headerlink" href="#unique_pos_tags_in_lexicon_entry.parameters" title="Permanent link">&para;</a></h4>


- __lexicon\_entry__ : `str` <br/>
    Either a Multi Word Expression template or single word lexicon entry,
    which is a sequence of words/tokens and Part Of Speech (POS) tags
    joined together by an underscore and separated by a single whitespace,
    e.g. `word1_POS1 word2_POS2 word3_POS3`. For a single word lexicon it
    would be `word1_POS1`.

<h4 id="unique_pos_tags_in_lexicon_entry.returns">Returns<a className="headerlink" href="#unique_pos_tags_in_lexicon_entry.returns" title="Permanent link">&para;</a></h4>


- `Set[str]` <br/>

<h4 id="unique_pos_tags_in_lexicon_entry.raises">Raises<a className="headerlink" href="#unique_pos_tags_in_lexicon_entry.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the lexicon entry when split on whitespace and then split by `_`
    does not create a `List[Tuple[str, str]]` whereby the tuple contains
    the `token text` and it's associated `POS tag`.

<h4 id="unique_pos_tags_in_lexicon_entry.examples">Examples<a className="headerlink" href="#unique_pos_tags_in_lexicon_entry.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.utils import unique_pos_tags_in_lexicon_entry
mwe_template = 'East_noun London_noun is_det great_adj'
assert ({'noun', 'adj', 'det'}
        == unique_pos_tags_in_lexicon_entry(mwe_template))
single_word_lexicon = 'East_noun'
assert {'noun'} == unique_pos_tags_in_lexicon_entry(single_word_lexicon)
```

<a id="pymusas.utils.are_packages_installed"></a>

### are\_packages\_installed

```python
def are_packages_installed(packages: list[str]) -> bool
```

Returns True if all packages are installed, False otherwise.

<h4 id="are_packages_installed.parameters">Parameters<a className="headerlink" href="#are_packages_installed.parameters" title="Permanent link">&para;</a></h4>


- __packages__ : `list[str]` <br/>
    A list of package names to check if they are installed.

<h4 id="are_packages_installed.returns">Returns<a className="headerlink" href="#are_packages_installed.returns" title="Permanent link">&para;</a></h4>


- `bool` <br/>

<a id="pymusas.utils.neural_extra_installed"></a>

### neural\_extra\_installed

```python
def neural_extra_installed() -> None
```

Checks if the `pymusas[neural]` extra is installed by checking if the
packages required for the `neural` extra are installed.

<h4 id="neural_extra_installed.raises">Raises<a className="headerlink" href="#neural_extra_installed.raises" title="Permanent link">&para;</a></h4>


- `ImportError` <br/>
    If `pymusas[neural]` is not installed.

