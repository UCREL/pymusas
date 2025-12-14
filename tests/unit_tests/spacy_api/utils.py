from spacy.tokens import Doc


def compare_output(expected_output: list[tuple[list[str], list[tuple[int, int]]]],
                   doc: Doc,
                   pymusas_tags_token_attr: str,
                   pymusas_mwe_indexes_attr: str,
                   top_n: int | None = None) -> None:
    '''
    Compares the `expected_output` with the output from the tagger which is
    stored in the `doc` within the token attributes `pymusas_tags_token_attr`
    and `pymusas_mwe_indexes_attr`.
    '''
    assert len(expected_output) == len(doc)
    for token_index, token in enumerate(doc):
        predicted_tags = getattr(token._, pymusas_tags_token_attr)
        predicted_mwe_indexes = getattr(token._, pymusas_mwe_indexes_attr)

        expected_tags = expected_output[token_index][0]
        expected_mwe_indexes = expected_output[token_index][1]
        if top_n is not None:
            expected_tags = expected_tags[:top_n]
            expected_mwe_indexes = expected_mwe_indexes[:top_n]

        assert expected_tags == predicted_tags
        assert expected_mwe_indexes == predicted_mwe_indexes
