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
- __DEFAULT\_TAG\_RE__ : `re.Pattern[str]` <br/>
    Matches a default (`Df`) semantic tag, e.g. `Df`, `Df+++`, `Dfc`, `Df-m%`,
    or `Dfm+`. The `suffix` group captures everything after `Df`, which can be
    any combination, in any order, of `+`/`-` affixes, lower case markers,
    e.g. gender markers, and rarity markers (`%` and `@`).

<a id="pymusas.utils.NEURAL_EXTRA_PACKAGES"></a>

#### NEURAL\_EXTRA\_PACKAGES

```python
NEURAL_EXTRA_PACKAGES: list[str] = ['transformers', 'wsd_torch_models', 'torch']
```

<a id="pymusas.utils.DEFAULT_TAG_RE"></a>

#### DEFAULT\_TAG\_RE

```python
DEFAULT_TAG_RE: re.Pattern[str] = re.compile(r'^Df(?P<suffix>[+\-a-z%@]*)$')
```

<a id="pymusas.utils.token_pos_tags_in_lexicon_entry"></a>

### token\_pos\_tags\_in\_lexicon\_entry

```python
def token_pos_tags_in_lexicon_entry(
    lexicon_entry: str
) -> Iterable[tuple[str, str]]
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


- `Iterable[tuple[str, str]]` <br/>

<h4 id="token_pos_tags_in_lexicon_entry.raises">Raises<a className="headerlink" href="#token_pos_tags_in_lexicon_entry.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the lexicon entry when split on whitespace and then split by `_`
    does not create a `Iterable[tuple[str, str]]` whereby the tuple contains
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
) -> set[str]
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


- `set[str]` <br/>

<h4 id="unique_pos_tags_in_lexicon_entry.raises">Raises<a className="headerlink" href="#unique_pos_tags_in_lexicon_entry.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the lexicon entry when split on whitespace and then split by `_`
    does not create a `list[tuple[str, str]]` whereby the tuple contains
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

<a id="pymusas.utils.contains_default_tag"></a>

### contains\_default\_tag

```python
def contains_default_tag(semantic_tags: list[str]) -> bool
```

Returns `True` if any of the given `semantic_tags`, including any part of
a slash (`/`) tag, is a default (`Df`) tag, see [`DEFAULT_TAG_RE`](#default_tag_re).

<h4 id="contains_default_tag.parameters">Parameters<a className="headerlink" href="#contains_default_tag.parameters" title="Permanent link">&para;</a></h4>


- __semantic\_tags__ : `list[str]` <br/>
    The semantic tags of a lexicon entry, e.g. `['C1/Df', 'Z3']`.

<h4 id="contains_default_tag.returns">Returns<a className="headerlink" href="#contains_default_tag.returns" title="Permanent link">&para;</a></h4>


- `bool` <br/>

<h4 id="contains_default_tag.examples">Examples<a className="headerlink" href="#contains_default_tag.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.utils import contains_default_tag
assert contains_default_tag(['Z3', 'C1/Df+'])
assert contains_default_tag(['Dfc'])
assert contains_default_tag(['Df%'])
assert contains_default_tag(['Dfm+'])
assert not contains_default_tag(['Z3', 'A1/B2'])
```

<a id="pymusas.utils.default_token_index"></a>

### default\_token\_index

```python
def default_token_index(mwe_template: str) -> int | None
```

Returns the index of the first token in the `mwe_template` whose token
text starts with a wildcard (`*`). This is the token that a default (`Df`)
semantic tag refers to. `None` is returned if no token starts with a
wildcard.

<h4 id="default_token_index.parameters">Parameters<a className="headerlink" href="#default_token_index.parameters" title="Permanent link">&para;</a></h4>


- __mwe\_template__ : `str` <br/>
    A Multi Word Expression template, e.g. `half_DET a*_DET *_NOUN`.

<h4 id="default_token_index.returns">Returns<a className="headerlink" href="#default_token_index.returns" title="Permanent link">&para;</a></h4>


- `int | None` <br/>

<h4 id="default_token_index.raises">Raises<a className="headerlink" href="#default_token_index.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the `mwe_template` is not in the format expected by
    [`token_pos_tags_in_lexicon_entry`](#token_pos_tags_in_lexicon_entry).

<h4 id="default_token_index.examples">Examples<a className="headerlink" href="#default_token_index.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.utils import default_token_index
assert 2 == default_token_index('half_DET a*_DET *_NOUN')
assert 0 == default_token_index('*ing_NOUN job*_*')
assert default_token_index('ski_NOUN boot*_NOUN') is None
```

<a id="pymusas.utils.resolve_default_tags"></a>

### resolve\_default\_tags

```python
def resolve_default_tags(
    semantic_tags: list[str],
    replacement: str | None
) -> list[str]
```

Returns the `semantic_tags` whereby every default (`Df`) tag, including
those within a slash (`/`) tag, has been replaced using the `replacement`
semantic tag.

Only the first part of a slash `replacement` tag is used and all of its
affixes, lower case markers, and rarity markers (`%` and `@`) are removed,
e.g. `A5.1+++mfn@/Z3` becomes `A5.1`. Any affixes, lower case markers, and
rarity markers on the `Df` tag are then added to it in the same order,
e.g. `Df++` with the replacement `A1-` becomes `A1++`, `Df-m%` becomes
`A1-m%`, and `Dfm+` becomes `A1m+`. If the
`replacement` is `None` the `Df` tag is replaced with `Z99` with no suffixes
even if the Df tag contains suffixes.

<h4 id="resolve_default_tags.parameters">Parameters<a className="headerlink" href="#resolve_default_tags.parameters" title="Permanent link">&para;</a></h4>


- __semantic\_tags__ : `list[str]` <br/>
    The semantic tags that may contain `Df` tags, e.g. `['C1/Df']`.
- __replacement__ : `str | None` <br/>
    The semantic tag to replace the `Df` tags with, this would be the
    single word semantic tag of the token the `Df` tag refers to.

<h4 id="resolve_default_tags.returns">Returns<a className="headerlink" href="#resolve_default_tags.returns" title="Permanent link">&para;</a></h4>


- `list[str]` <br/>

<h4 id="resolve_default_tags.examples">Examples<a className="headerlink" href="#resolve_default_tags.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.utils import resolve_default_tags
assert ['A1'] == resolve_default_tags(['Df'], 'A1/Z3')
assert ['C1/A1'] == resolve_default_tags(['C1/Df'], 'A1')
assert ['N3.8+++'] == resolve_default_tags(['Df+++'], 'N3.8+')
assert ['I2.1c', 'B1'] == resolve_default_tags(['Dfc', 'B1'], 'I2.1mf')
assert ['A1-m%'] == resolve_default_tags(['Df-m%'], 'A1+@')
assert ['A1m+'] == resolve_default_tags(['Dfm+'], 'A1')
assert ['C1/Z99'] == resolve_default_tags(['C1/Df'], None)
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

