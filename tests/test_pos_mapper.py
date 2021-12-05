from pymusas.pos_mapper import upos_to_usas_core


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
