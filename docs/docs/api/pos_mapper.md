<div className="source-div">
 <p><i>pymusas</i><strong>.pos_mapper</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/pos_mapper.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.pos_mapper.UD_TO_USAS_CORE"></a>

#### UD\_TO\_USAS\_CORE

```python
UD_TO_USAS_CORE: Dict[str, List[str]] = {
    'ADJ': ['adj'],
    'ADP': ['prep'],
    'ADV': ['adv'],
    'AUX': ['verb'],
    'CCONJ': ['c ...
```

<a id="pymusas.pos_mapper.ud_to_usas_core"></a>

### ud\_to\_usas\_core

```python
def ud_to_usas_core(ud_tag: str) -> List[str]
```

Given a Universal Dependency (UD) POS tag it returns a `List` of USAS core POS
tags that are equivalent, whereby if the length of the `List` is greater
than `1` then the first tag in the `List` is the most equivalent tag.

If the List is empty then an invalid UD tag was given.

The mappings between UD and USAS core can be seen in [`UD_TO_USAS_CORE`](#ud_to_usas_core)

<h4 id="ud_to_usas_core.parameters">Parameters<a className="headerlink" href="#ud_to_usas_core.parameters" title="Permanent link">&para;</a></h4>


- __ud\_tag__ : `str` <br/>
    Universal Dependency POS tag, from the [UD tagset](https://universaldependencies.org/u/pos/).
    Expected to be all upper case.

<h4 id="ud_to_usas_core.returns">Returns<a className="headerlink" href="#ud_to_usas_core.returns" title="Permanent link">&para;</a></h4>


- `List[str]` <br/>

<h4 id="ud_to_usas_core.examples">Examples<a className="headerlink" href="#ud_to_usas_core.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.pos_mapper import ud_to_usas_core
assert ud_to_usas_core('CCONJ') == ['conj']
# Most equivalent tag for 'X' is 'fw'
assert ud_to_usas_core('X') == ['fw', 'xx']
assert ud_to_usas_core('Unknown') == []
```

