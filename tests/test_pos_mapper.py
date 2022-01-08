from pymusas.pos_mapper import CHINESE_PENN_TREEBANK_TO_USAS_CORE, upos_to_usas_core


def test_upos_to_usas_core() -> None:
    assert upos_to_usas_core('CCONJ') == ['conj']
    assert upos_to_usas_core('X') == ['fw', 'xx']
    assert upos_to_usas_core('Unknown') == []

    all_upos_tags = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN',
                     'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM',
                     'VERB', 'X']
    for upos_tag in all_upos_tags:
        usas_tags = upos_to_usas_core(upos_tag)
        assert usas_tags != []
        for usas_tag in usas_tags:
            assert usas_tag.lower() == usas_tag


def test_chinese_penn_to_usas_core() -> None:
    assert len(CHINESE_PENN_TREEBANK_TO_USAS_CORE) == 36
    chinese_penn_treebank_mapping = {'VA': ['verb'],
                                     'VC': ['verb'],
                                     'VE': ['verb'],
                                     'VV': ['verb'],
                                     'NR': ['pnoun'],
                                     'NT': ['noun'],
                                     'NN': ['noun'],
                                     'LC': ['part'],
                                     'PN': ['pron'],
                                     'DT': ['det', 'art'],
                                     'CD': ['num'],
                                     'OD': ['num'],
                                     'M': ['num'],
                                     'AD': ['adv'],
                                     'P': ['prep'],
                                     'CC': ['conj'],
                                     'CS': ['conj'],
                                     'DEC': ['part'],
                                     'DEG': ['part'],
                                     'DER': ['part'],
                                     'DEV': ['part'],
                                     'SP': ['part'],
                                     'AS': ['part'],
                                     'ETC': ['part'],
                                     'MSP': ['part'],
                                     'IJ': ['intj'],
                                     'ON': ['fw', 'xx'],
                                     'PU': ['punc'],
                                     'JJ': ['adj'],
                                     'FW': ['fw', 'xx'],
                                     'LB': ['fw', 'xx'],
                                     'SB': ['fw', 'xx'],
                                     'BA': ['fw', 'xx'],
                                     'INF': ['fw', 'xx'],
                                     'URL': ['fw', 'xx'],
                                     'X': ['fw', 'xx']}
    assert 36 == len(chinese_penn_treebank_mapping)

    for chinese_penn_tag, usas_core_tag in CHINESE_PENN_TREEBANK_TO_USAS_CORE.items():
        assert chinese_penn_treebank_mapping[chinese_penn_tag] == usas_core_tag
