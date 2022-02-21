<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><i>.rules</i><strong>.util</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rules/util.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.rules.util.n_gram_indexes"></a>

### n\_gram\_indexes

```python
def n_gram_indexes(
    sequence: Sequence[Any],
    min_n: int,
    max_n: int
) -> Iterator[Tuple[int, int]]
```

Returns n-grams as indexes of the `sequence`,
in the range from `max_n` to `min_n`, in
order of largest n-grams first. If you only want one n-gram size then set
`min_n` equal to `max_n`, for example to get bi-grams indexes set both
`min_n` and `max_n` to `2`.

<h4 id="n_gram_indexes.parameters">Parameters<a className="headerlink" href="#n_gram_indexes.parameters" title="Permanent link">&para;</a></h4>


- __sequence__ : `Sequence[Any]` <br/>
    The sequence to generate n-gram indexes from.
- __min\_n__ : `int` <br/>
    Minimum size n-gram. Has to be greater than `0`.
- __max\_n__ : `int` <br/>
    Maximim size n-gram. This has to be equal to or greater than `min_n`.
    If this is greater than the length of the `sequence` then it is set to
    length of the `sequence`.

<h4 id="n_gram_indexes.returns">Returns<a className="headerlink" href="#n_gram_indexes.returns" title="Permanent link">&para;</a></h4>


- `Iterator[Tuple[int, int]]` <br/>

<h4 id="n_gram_indexes.raises">Raises<a className="headerlink" href="#n_gram_indexes.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If `min_n` is less than `1` or `max_n` is less than `min_n`.

<h4 id="n_gram_indexes.examples">Examples<a className="headerlink" href="#n_gram_indexes.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.taggers.rule_based_mwe import n_gram_indexes
tokens = ['hello', 'how', 'are', 'you', ',']
token_n_gram_indexes = n_gram_indexes(tokens, 2, 3)
expected_n_grams_indexes = [(0, 3), (1, 4), (2, 5), (0, 2), (1, 3), (2, 4), (3, 5)]
assert expected_n_grams_indexes == list(token_n_gram_indexes)
```

<a id="pymusas.taggers.rules.util.n_grams"></a>

### n\_grams

```python
def n_grams(
    sequence: Sequence[Any],
    min_n: int,
    max_n: int
) -> Iterator[Sequence[Any]]
```

Returns n-grams, in the range from `max_n` to `min_n`, of the `sequence` in
order of largest n-grams first. If you only want one n-gram size then set
`min_n` equal to `max_n`, for example to get bi-grams set both `min_n` and
`max_n` to `2`.

<h4 id="n_grams.parameters">Parameters<a className="headerlink" href="#n_grams.parameters" title="Permanent link">&para;</a></h4>


- __sequence__ : `Sequence[Any]` <br/>
    The sequence to generate n-grams from.
- __min\_n__ : `int` <br/>
    Minimum size n-gram. Has to be greater than `0`.
- __max\_n__ : `int` <br/>
    Maximim size n-gram. This has to be equal to or greater than `min_n`.
    If this is greater than the length of the `sequence` then it is set to
    length of the `sequence`.

<h4 id="n_grams.returns">Returns<a className="headerlink" href="#n_grams.returns" title="Permanent link">&para;</a></h4>


- `Iterator[Sequence[Any]]` <br/>

<h4 id="n_grams.raises">Raises<a className="headerlink" href="#n_grams.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If `min_n` is less than `1` or `max_n` is less than `min_n`.

<h4 id="n_grams.examples">Examples<a className="headerlink" href="#n_grams.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.taggers.rule_based_mwe import n_grams
tokens = ['hello', 'how', 'are', 'you', ',']
token_n_grams = n_grams(tokens, 2, 3)
expected_n_grams = [['hello', 'how', 'are'], ['how', 'are', 'you'], ['are', 'you', ','],
                    ['hello', 'how'], ['how', 'are'], ['are', 'you'], ['you', ',']]
assert expected_n_grams == list(token_n_grams)
```

