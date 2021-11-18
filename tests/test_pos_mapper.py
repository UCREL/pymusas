from pymusas.pos_mapper import ud_to_usas_core


def test_ud_to_usas_core() -> None:
    assert ud_to_usas_core('CCONJ') == ['conj']
    assert ud_to_usas_core('X') == ['fw', 'xx']
    assert ud_to_usas_core('Unknown') == []

    all_ud_tags = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN',
                   'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM',
                   'VERB', 'X']
    for ud_tag in all_ud_tags:
        usas_tags = ud_to_usas_core(ud_tag)
        assert usas_tags != []
        for usas_tag in usas_tags:
            assert usas_tag.lower() == usas_tag
