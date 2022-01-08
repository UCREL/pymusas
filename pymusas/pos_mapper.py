'''
# Attributes

UPOS_TO_USAS_CORE: `Dict[str, List[str]]`
    A mapping from the [Universal Part Of Speech (UPOS) tagset](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf)
    to the USAS core tagset. UPOS is used by the
    [Universal Dependencies Tree Bank.](https://universaldependencies.org/u/pos/)

CHINESE_PENN_TREEBANK_TO_USAS_CORE: `Dict[str, List[str]]`
    A mapping from the [Chinese Penn Treebank tagset](https://verbs.colorado.edu/chinese/posguide.3rd.ch.pdf)
    to the USAS core tagset. The Chinese Penn Treebank tagset here is slightly different to the original
    as it contains three extra tags, `X`, `URL`, and `INF`, that are appear to be unique to
    the [spaCy Chinese models](https://spacy.io/models/zh). For more information on how this mapping was
    created, see the following [GitHub issue](https://github.com/UCREL/pymusas/issues/19).
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

CHINESE_PENN_TREEBANK_TO_USAS_CORE: Dict[str, List[str]] = {
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
