<div className="source-div">
 <p><i>pymusas</i><strong>.pos_mapper</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/pos_mapper.py">[SOURCE]</a></p>
</div>
<div></div>

---

<h4 id="pymusas.pos_mapper.attributes">Attributes<a className="headerlink" href="#pymusas.pos_mapper.attributes" title="Permanent link">&para;</a></h4>


- __UPOS\_TO\_USAS\_CORE__ : `Dict[str, List[str]]` <br/>
    A mapping from the Universal Part Of Speech (UPOS) tagset to the USAS core tagset. The UPOS tagset used
    here is the same as that used by the [Universal Dependencies Treebank project](https://universaldependencies.org/u/pos/).
    This is slightly different to the original presented in the
    [paper by Petrov et al. 2012](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf),
    for this original tagset see the following [GitHub repository](https://github.com/slavpetrov/universal-pos-tags).

- __USAS\_CORE\_TO\_UPOS__ : `Dict[str, List[str]]` <br/>
    The reverse of [`UPOS_TO_USAS_CORE`](#upos_to_usas_core).

- __PENN\_CHINESE\_TREEBANK\_TO\_USAS\_CORE__ : `Dict[str, List[str]]` <br/>
    A mapping from the [Penn Chinese Treebank tagset](https://verbs.colorado.edu/chinese/posguide.3rd.ch.pdf)
    to the USAS core tagset. The Penn Chinese Treebank tagset here is slightly different to the original
    as it contains three extra tags, `X`, `URL`, and `INF`, that appear to be unique to
    the [spaCy Chinese models](https://spacy.io/models/zh). For more information on how this mapping was
    created, see the following [GitHub issue](https://github.com/UCREL/pymusas/issues/19).

- __USAS\_CORE\_TO\_PENN\_CHINESE\_TREEBANK__ : `Dict[str, List[str]]` <br/>
    The reverse of [`PENN_CHINESE_TREEBANK_TO_USAS_CORE`](#penn_chinese_treebank_to_usas_core).

- __BASIC\_CORCENCC\_TO\_USAS\_CORE__ : `Dict[str, List[str]]` <br/>
    A mapping from the [basic CorCenCC tagset](https://cytag.corcencc.org/tagset?lang=en)
    to the USAS core tagset. This mapping has come from table A.1
    in the paper [Leveraging Pre-Trained Embeddings for Welsh Taggers.](https://aclanthology.org/W19-4332.pdf)
    and from table 6 in the paper [Towards A Welsh Semantic Annotation System](https://aclanthology.org/L18-1158.pdf).

- __USAS\_CORE\_TO\_BASIC\_CORCENCC__ : `Dict[str, List[str]]` <br/>
    The reverse of [`BASIC_CORCENCC_TO_USAS_CORE`](#basic_corcencc_to_usas_core).

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

<a id="pymusas.pos_mapper.USAS_CORE_TO_UPOS"></a>

#### USAS\_CORE\_TO\_UPOS

```python
USAS_CORE_TO_UPOS: Dict[str, List[str]] = {
    'adj': ['ADJ'],
    'prep': ['ADP'],
    'adv': ['ADV'],
    'verb': ['VERB', 'AUX'],
    'con ...
```

<a id="pymusas.pos_mapper.PENN_CHINESE_TREEBANK_TO_USAS_CORE"></a>

#### PENN\_CHINESE\_TREEBANK\_TO\_USAS\_CORE

```python
PENN_CHINESE_TREEBANK_TO_USAS_CORE: Dict[str, List[str]] = {
    'AS': ['part'],
    'DEC': ['part'],
    'DEG': ['part'],
    'DER': ['part'],
    'DEV': ['pa ...
```

<a id="pymusas.pos_mapper.USAS_CORE_TO_PENN_CHINESE_TREEBANK"></a>

#### USAS\_CORE\_TO\_PENN\_CHINESE\_TREEBANK

```python
USAS_CORE_TO_PENN_CHINESE_TREEBANK: Dict[str, List[str]] = {
    'part': ['AS', 'DEC', 'DEG', 'DER', 'DEV', 'ETC', 'LC', 'MSP', 'SP'],
    'fw': ['BA', 'FW', ' ...
```

<a id="pymusas.pos_mapper.BASIC_CORCENCC_TO_USAS_CORE"></a>

#### BASIC\_CORCENCC\_TO\_USAS\_CORE

```python
BASIC_CORCENCC_TO_USAS_CORE: Dict[str, List[str]] = {
    "E": ["noun"],
    "YFB": ["art"],
    "Ar": ["prep"],
    "Cys": ["conj"],
    "Rhi": ["num"] ...
```

<a id="pymusas.pos_mapper.USAS_CORE_TO_BASIC_CORCENCC"></a>

#### USAS\_CORE\_TO\_BASIC\_CORCENCC

```python
USAS_CORE_TO_BASIC_CORCENCC: Dict[str, List[str]] = {
    "noun": ["E"],
    "pnoun": ["E"],
    "art": ["YFB"],
    "det": ["YFB"],
    "prep": ["Ar"], ...
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

