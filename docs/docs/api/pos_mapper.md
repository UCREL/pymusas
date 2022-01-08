<div className="source-div">
 <p><i>pymusas</i><strong>.pos_mapper</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/pos_mapper.py">[SOURCE]</a></p>
</div>
<div></div>

---

<h4 id="pymusas.pos_mapper.attributes">Attributes<a className="headerlink" href="#pymusas.pos_mapper.attributes" title="Permanent link">&para;</a></h4>


- __UPOS\_TO\_USAS\_CORE__ : `Dict[str, List[str]]` <br/>
    A mapping from the [Universal Part Of Speech (UPOS) tagset](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf)
    to the USAS core tagset. UPOS is used by the
    [Universal Dependencies Tree Bank.](https://universaldependencies.org/u/pos/)

- __CHINESE\_PENN\_TREEBANK\_TO\_USAS\_CORE__ : `Dict[str, List[str]]` <br/>
    A mapping from the [Chinese Penn Treebank tagset](https://verbs.colorado.edu/chinese/posguide.3rd.ch.pdf)
    to the USAS core tagset. The Chinese Penn Treebank tagset here is slightly different to the original
    as it contains three extra tags, `X`, `URL`, and `INF`, that are appear to be unique to
    the [spaCy Chinese models](https://spacy.io/models/zh). For more information on how this mapping was
    created, see the following [GitHub issue](https://github.com/UCREL/pymusas/issues/19).

<a id="pymusas.pos_mapper.UPOS_TO_USAS_CORE"></a>

#### UPOS\_TO\_USAS\_CORE

```python
UPOS_TO_USAS_CORE: Dict[str, List[str]] = {
    'ADJ': ['adj'],
    'ADP': ['prep'],
    'ADV': ['adv'],
    'AUX': ['verb'],
    'CCONJ': ['c ...
```

<a id="pymusas.pos_mapper.CHINESE_PENN_TREEBANK_TO_USAS_CORE"></a>

#### CHINESE\_PENN\_TREEBANK\_TO\_USAS\_CORE

```python
CHINESE_PENN_TREEBANK_TO_USAS_CORE: Dict[str, List[str]] = {
    'AS': ['part'],
    'DEC': ['part'],
    'DEG': ['part'],
    'DER': ['part'],
    'DEV': ['pa ...
```

<a id="pymusas.pos_mapper.upos_to_usas_core"></a>

### upos\_to\_usas\_core

```python
def upos_to_usas_core(upos_tag: str) -> List[str]
```

Given a [Universal Part Of Speech (UPOS) tag](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf)
it returns a `List` of USAS core POS tags that are equivalent, whereby if the
length of the `List` is greater than `1` then the first tag in the `List`
is the most equivalent tag.

If the List is empty then an invalid UPOS tag was given.

The mappings between UPOS and USAS core can be seen in [`UPOS_TO_USAS_CORE`](#upos_to_usas_core)

<h4 id="upos_to_usas_core.parameters">Parameters<a className="headerlink" href="#upos_to_usas_core.parameters" title="Permanent link">&para;</a></h4>


- __upos\_tag__ : `str` <br/>
    UPOS tag, expected to be all upper case.

<h4 id="upos_to_usas_core.returns">Returns<a className="headerlink" href="#upos_to_usas_core.returns" title="Permanent link">&para;</a></h4>


- `List[str]` <br/>

<h4 id="upos_to_usas_core.examples">Examples<a className="headerlink" href="#upos_to_usas_core.examples" title="Permanent link">&para;</a></h4>


``` python
from pymusas.pos_mapper import upos_to_usas_core
assert upos_to_usas_core('CCONJ') == ['conj']
# Most equivalent tag for 'X' is 'fw'
assert upos_to_usas_core('X') == ['fw', 'xx']
assert upos_to_usas_core('Unknown') == []
```

