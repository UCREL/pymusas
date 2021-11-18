from typing import Dict, List


UD_TO_USAS_CORE: Dict[str, List[str]] = {
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


def ud_to_usas_core(ud_tag: str) -> List[str]:
    '''
    Given a Universal Dependency (UD) POS tag it returns a `List` of USAS core POS
    tags that are equivalent, whereby if the length of the `List` is greater
    than `1` then the first tag in the `List` is the most equivalent tag.

    If the List is empty then an invalid UD tag was given.

    The mappings between UD and USAS core can be seen in :var:`UD_TO_USAS_CORE`

    # Parameters

    ud_tag: `str`
        Universal Dependency POS tag, from the [UD tagset](https://universaldependencies.org/u/pos/).
        Expected to be all upper case.

    # Returns

    `List[str]`

    # Examples

    ``` python
    >>> from pymusas.pos_mapper import ud_to_usas_core
    >>> assert ud_to_usas_core('CCONJ') == ['conj']
    >>> # Most equivalent tag for 'X' is 'fw'
    >>> assert ud_to_usas_core('X') == ['fw', 'xx']
    >>> assert ud_to_usas_core('Unknown') == []

    ```
    '''
    
    return UD_TO_USAS_CORE.get(ud_tag, [])
