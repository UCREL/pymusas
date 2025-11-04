<div className="source-div">
 <p><i>pymusas</i><i>.rankers</i><strong>.lexical_match</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/rankers/lexical_match.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.rankers.lexical_match.LexicalMatch"></a>

## LexicalMatch

```python
class LexicalMatch(IntEnum)
```

Descriptions of the lexical matches and their ordering in tagging priority
during ranking. Lower the value and rank the higher the tagging priority.

The `value` attribute of each instance attribute is of type `int`. For the
best explanation see the example below.

<h4 id="lexicalmatch.instance_attributes">Instance Attributes<a className="headerlink" href="#lexicalmatch.instance_attributes" title="Permanent link">&para;</a></h4>


- __TOKEN__ : `int` <br/>
    The lexicon entry matched on the token text.
- __LEMMA__ : `int` <br/>
    The lexicon entry matched on the lemma of the token.
- __TOKEN\_LOWER__ : `int` <br/>
    The lexicon entry matched on the lower cased token text.
- __LEMMA\_LOWER__ : `int` <br/>
    The lexicon entry matched on the lower cased lemma of the token.

<h4 id="lexicalmatch.examples">Examples<a className="headerlink" href="#lexicalmatch.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.rankers.lexical_match import LexicalMatch
assert 1 == LexicalMatch.TOKEN
assert 'TOKEN' == LexicalMatch.TOKEN.name
assert 1 == LexicalMatch.TOKEN.value

assert 2 == LexicalMatch.LEMMA
assert 3 == LexicalMatch.TOKEN_LOWER
assert 4 == LexicalMatch.LEMMA_LOWER

assert 2 < LexicalMatch.LEMMA_LOWER
```

<a id="pymusas.rankers.lexical_match.LexicalMatch.TOKEN"></a>

#### TOKEN

```python
class LexicalMatch(IntEnum):
 | ...
 | TOKEN = 1
```

<a id="pymusas.rankers.lexical_match.LexicalMatch.LEMMA"></a>

#### LEMMA

```python
class LexicalMatch(IntEnum):
 | ...
 | LEMMA = 2
```

<a id="pymusas.rankers.lexical_match.LexicalMatch.TOKEN_LOWER"></a>

#### TOKEN\_LOWER

```python
class LexicalMatch(IntEnum):
 | ...
 | TOKEN_LOWER = 3
```

<a id="pymusas.rankers.lexical_match.LexicalMatch.LEMMA_LOWER"></a>

#### LEMMA\_LOWER

```python
class LexicalMatch(IntEnum):
 | ...
 | LEMMA_LOWER = 4
```

<a id="pymusas.rankers.lexical_match.LexicalMatch.__repr__"></a>

### \_\_repr\_\_

```python
class LexicalMatch(IntEnum):
 | ...
 | def __repr__() -> str
```

Machine readable string. When printed and run `eval()` over the string
you should be able to recreate the object.

<a id="pymusas.rankers.lexical_match.LexicalMatch.__str__"></a>

### \_\_str\_\_

```python
class LexicalMatch(IntEnum):
 | ...
 | def __str__() -> str
```

Returns the `class_name.name`, e.g. `LexicalMatch.TOKEN`

Overridden as from Python version 3.11 IntEnum.__str__  by default would
return the integer as a string.

