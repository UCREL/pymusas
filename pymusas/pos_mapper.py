'''
# Attributes

UPOS_TO_USAS_CORE: `Dict[str, List[str]]`
    A mapping from the [Universal Part Of Speech (UPOS) tagset](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf)
    to the USAS core tagset. UPOS is used by the
    [Universal Dependencies Tree Bank.](https://universaldependencies.org/u/pos/)

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
