'''
# Attributes

UPOS_TO_USAS_CORE: `Dict[str, List[str]]`
    A mapping from the Universal Part Of Speech (UPOS) tagset to the USAS core tagset. The UPOS tagset used
    here is the same as that used by the [Universal Dependencies Treebank project](https://universaldependencies.org/u/pos/).
    This is slightly different to the original presented in the
    [paper by Petrov et al. 2012](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf),
    for this original tagset see the following [GitHub repository](https://github.com/slavpetrov/universal-pos-tags).

USAS_CORE_TO_UPOS : `Dict[str, List[str]]`
    The reverse of :var:`UPOS_TO_USAS_CORE`.

PENN_CHINESE_TREEBANK_TO_USAS_CORE: `Dict[str, List[str]]`
    A mapping from the [Penn Chinese Treebank tagset](https://verbs.colorado.edu/chinese/posguide.3rd.ch.pdf)
    to the USAS core tagset. The Penn Chinese Treebank tagset here is slightly different to the original
    as it contains three extra tags, `X`, `URL`, and `INF`, that appear to be unique to
    the [spaCy Chinese models](https://spacy.io/models/zh). For more information on how this mapping was
    created, see the following [GitHub issue](https://github.com/UCREL/pymusas/issues/19).

USAS_CORE_TO_PENN_CHINESE_TREEBANK : `Dict[str, List[str]]`
    The reverse of :var:`PENN_CHINESE_TREEBANK_TO_USAS_CORE`.

BASIC_CORCENCC_TO_USAS_CORE: `Dict[str, List[str]]`
    A mapping from the [basic CorCenCC tagset](https://cytag.corcencc.org/tagset?lang=en)
    to the USAS core tagset. This mapping has come from table A.1
    in the paper [Leveraging Pre-Trained Embeddings for Welsh Taggers.](https://aclanthology.org/W19-4332.pdf)
    and from table 6 in the paper [Towards A Welsh Semantic Annotation System](https://aclanthology.org/L18-1158.pdf).

USAS_CORE_TO_BASIC_CORCENCC: `Dict[str, List[str]]`
    The reverse of :var:`BASIC_CORCENCC_TO_USAS_CORE`.
'''
from typing import Dict, List


UPOS_TO_USAS_CORE: Dict[str, List[str]] = {
    'ADJ': ['adj'],
    'ADP': ['prep'],
    'ADV': ['adv'],
    'AUX': ['verb'],
    'CCONJ': ['conj'],
    'DET': ['det', 'art'],
    'INTJ': ['intj'],
    'NOUN': ['noun'],
    'NUM': ['num'],
    'PART': ['part'],
    'PRON': ['pron'],
    'PROPN': ['pnoun'],
    'PUNCT': ['punc'],
    'SCONJ': ['conj'],
    'SYM': ['code'],
    'VERB': ['verb'],
    'X': ['fw', 'xx']
}

USAS_CORE_TO_UPOS: Dict[str, List[str]] = {
    'adj': ['ADJ'],
    'prep': ['ADP'],
    'adv': ['ADV'],
    'verb': ['VERB', 'AUX'],
    'conj': ['CCONJ', 'SCONJ'],
    'det': ['DET'],
    'art': ['DET'],
    'intj': ['INTJ'],
    'noun': ['NOUN'],
    'num': ['NUM'],
    'part': ['PART'],
    'pron': ['PRON'],
    'pnoun': ['PROPN'],
    'punc': ['PUNCT'],
    'code': ['SYM'],
    'fw': ['X'],
    'xx': ['X']
}

PENN_CHINESE_TREEBANK_TO_USAS_CORE: Dict[str, List[str]] = {
    'AS': ['part'],
    'DEC': ['part'],
    'DEG': ['part'],
    'DER': ['part'],
    'DEV': ['part'],
    'ETC': ['part'],
    'LC': ['part'],
    'MSP': ['part'],
    'SP': ['part'],
    'BA': ['fw', 'xx'],
    'FW': ['fw', 'xx'],
    'IJ': ['intj'],
    'LB': ['fw', 'xx'],
    'ON': ['fw', 'xx'],
    'SB': ['fw', 'xx'],
    'X': ['fw', 'xx'],
    'URL': ['fw', 'xx'],
    'INF': ['fw', 'xx'],
    'NN': ['noun'],
    'NR': ['pnoun'],
    'NT': ['noun'],
    'VA': ['verb'],
    'VC': ['verb'],
    'VE': ['verb'],
    'VV': ['verb'],
    'CD': ['num'],
    'M': ['num'],
    'OD': ['num'],
    'DT': ['det', 'art'],
    'CC': ['conj'],
    'CS': ['conj'],
    'AD': ['adv'],
    'JJ': ['adj'],
    'P': ['prep'],
    'PN': ['pron'],
    'PU': ['punc']
}


USAS_CORE_TO_PENN_CHINESE_TREEBANK: Dict[str, List[str]] = {
    'part': ['AS', 'DEC', 'DEG', 'DER', 'DEV', 'ETC', 'LC', 'MSP', 'SP'],
    'fw': ['BA', 'FW', 'LB', 'ON', 'SB', 'X', 'URL', 'INF'],
    'xx': ['BA', 'FW', 'LB', 'ON', 'SB', 'X', 'URL', 'INF'],
    'intj': ['IJ'],
    'noun': ['NN', 'NT'],
    'pnoun': ['NR'],
    'verb': ['VA', 'VC', 'VE', 'VV'],
    'num': ['CD', 'M', 'OD'],
    'det': ['DT'],
    'art': ['DT'],
    'conj': ['CC', 'CS'],
    'adv': ['AD'],
    'adj': ['JJ'],
    'prep': ['P'],
    'pron': ['PN'],
    'punc': ['PU'],
    'code': ['PU']
}


BASIC_CORCENCC_TO_USAS_CORE: Dict[str, List[str]] = {
    "E": ["noun"],
    "YFB": ["art"],
    "Ar": ["prep"],
    "Cys": ["conj"],
    "Rhi": ["num"],
    "Ans": ["adj"],
    "Adf": ["adv"],
    "B": ["verb"],
    "Rha": ["pron"],
    "U": ["part"],
    "Ebych": ["intj"],
    "Gw": ["xx"],
    "Atd": ["punc"]
}


USAS_CORE_TO_BASIC_CORCENCC: Dict[str, List[str]] = {
    "noun": ["E"],
    "pnoun": ["E"],
    "art": ["YFB"],
    "det": ["YFB"],
    "prep": ["Ar"],
    "conj": ["Cys"],
    "num": ["Rhi"],
    "adj": ["Ans"],
    "adv": ["Adf"],
    "verb": ["B"],
    "pron": ["Rha"],
    "part": ["U"],
    "intj": ["Ebych"],
    "xx": ["Gw"],
    "fw": ["Gw"],
    "code": ["Gw"],
    "punc": ["Atd"]
}


def upos_to_usas_core(upos_tag: str) -> List[str]:
    '''
    Given a [Universal Part Of Speech (UPOS) tag](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf)
    it returns a `List` of USAS core POS tags that are equivalent, whereby if the
    length of the `List` is greater than `1` then the first tag in the `List`
    is the most equivalent tag.

    If the List is empty then an invalid UPOS tag was given.

    The mappings between UPOS and USAS core can be seen in :var:`UPOS_TO_USAS_CORE`

    # Parameters

    upos_tag: `str`
        UPOS tag, expected to be all upper case.

    # Returns

    `List[str]`

    # Examples

    ``` python
    >>> from pymusas.pos_mapper import upos_to_usas_core
    >>> assert upos_to_usas_core('CCONJ') == ['conj']
    >>> # Most equivalent tag for 'X' is 'fw'
    >>> assert upos_to_usas_core('X') == ['fw', 'xx']
    >>> assert upos_to_usas_core('Unknown') == []

    ```
    '''
    
    return UPOS_TO_USAS_CORE.get(upos_tag, [])
