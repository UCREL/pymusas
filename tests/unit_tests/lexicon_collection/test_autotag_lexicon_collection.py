from collections.abc import MutableMapping
import importlib
from pathlib import Path
import re
import tempfile

import pytest
from pytest import MonkeyPatch
import responses

from pymusas import config
from pymusas.lexicon_collection import AutotagLexiconCollection


DATA_DIR = Path(__file__, '..', '..', 'data').resolve()
AUTOTAG_DATA_DIR = Path(DATA_DIR, 'lexicon_collection', 'AutotagLexiconCollection')
AUTOTAG_LEXICON_FILE_PATH = Path(AUTOTAG_DATA_DIR, 'autotag_lexicon.tsv')
SECOND_AUTOTAG_LEXICON_FILE_PATH = Path(AUTOTAG_DATA_DIR, 'second_autotag_lexicon.tsv')
POS_WILDCARD_LEXICON_FILE_PATH = Path(AUTOTAG_DATA_DIR, 'pos_wildcard_lexicon.tsv')
UNCLOSED_CLASS_LEXICON_FILE_PATH = Path(AUTOTAG_DATA_DIR, 'unclosed_class_lexicon.tsv')
NO_POS_LEXICON_FILE_PATH = Path(AUTOTAG_DATA_DIR, 'no_pos_lexicon.tsv')

AUTOTAG_ENTRIES: dict[str, list[str]] = {
    '*kg|NUM': ['N3.5'],
    '[0-9][0-9]*ish|NUM': ['N1'],
    '*|PUNCT': ['PUNCT'],
    '*MB|N*': ['N3.2', 'N5']
}


def test_autotag_lexicon_collection_class_type() -> None:
    empty_collection = AutotagLexiconCollection()
    assert isinstance(empty_collection, AutotagLexiconCollection)
    assert isinstance(empty_collection, MutableMapping)


def test_autotag_lexicon_collection_init() -> None:
    empty_collection = AutotagLexiconCollection()
    assert {} == empty_collection.data
    assert {} == empty_collection.patterns

    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    assert AUTOTAG_ENTRIES == collection.data
    assert list(AUTOTAG_ENTRIES) == list(collection.patterns)
    lemma_regex, pos_regex = collection.patterns['*kg|NUM']
    assert re.compile('.*kg') == lemma_regex
    assert re.compile('NUM') == pos_regex


@pytest.mark.parametrize('pattern, matches, non_matches', [
    ('*kg', ['15kg', 'kg'], ['15KG', '15kgs']),
    ('*-year-old', ['10-year-old', '-year-old'], ['10 year old']),
    ('[0-9]*ish', ['9ish', '10ish', 'ish'], ['a9ish', 'nineish']),
    ('[0-9][0-9]*ish', ['9ish', '10ish'], ['ish']),
    ('[0-9]', ['9'], ['10', '']),
    ('[a-z]', ['a'], ['A']),
    ('*MB', ['10MB'], ['10mb']),
    ('N*', ['N', 'NOUN', 'NUM'], ['PROPN']),
    ('*', ['', 'anything'], []),
    ('a.b+c?(d)', ['a.b+c?(d)'], ['axbbc(d)', 'a.bc']),
    ('|', ['|'], ['']),
])
def test_pattern_to_regex(pattern: str, matches: list[str],
                          non_matches: list[str]) -> None:
    regex = AutotagLexiconCollection.pattern_to_regex(pattern)
    for value in matches:
        assert regex.fullmatch(value) is not None, value
    for value in non_matches:
        assert regex.fullmatch(value) is None, value


def test_pattern_to_regex_escaped_brackets() -> None:
    regex = AutotagLexiconCollection.pattern_to_regex(r'[\[\]]*x')
    assert regex.fullmatch('[]][x') is not None
    assert regex.fullmatch('a') is None
    assert AutotagLexiconCollection.pattern_to_regex(r'a[\]b]').fullmatch('a]') is not None


def test_pattern_to_regex_output() -> None:
    assert '.*kg' == AutotagLexiconCollection.pattern_to_regex('*kg').pattern
    assert '[0-9][0-9]*ish' == AutotagLexiconCollection.pattern_to_regex('[0-9][0-9]*ish').pattern
    assert '[0-9]*.*' == AutotagLexiconCollection.pattern_to_regex('[0-9]**').pattern
    assert '\\.\\+' == AutotagLexiconCollection.pattern_to_regex('.+').pattern


@pytest.mark.parametrize('pattern', ['[0-9*ish', '[', 'a[b', '[]', '[z-a]',
                                     'hello[102[]', '[[0-9]', 'a[1[2]3]', '[\\]', 'a[\\]',
                                     'hello[a-z]]', ']', 'a]b', '[a]]*'])
def test_pattern_to_regex_invalid(pattern: str) -> None:
    with pytest.raises(ValueError):
        AutotagLexiconCollection.pattern_to_regex(pattern)


@pytest.mark.parametrize('key', ['*kg', '*kg|*', '[0-9*ish|NUM', '*kg|N[UM'])
def test_setitem_invalid(key: str) -> None:
    collection = AutotagLexiconCollection()
    with pytest.raises(ValueError):
        collection[key] = ['N3.5']
    assert 0 == len(collection)
    assert {} == collection.patterns

    with pytest.raises(ValueError):
        AutotagLexiconCollection({key: ['N3.5']})


def test_setitem_lemma_containing_pipe() -> None:
    collection = AutotagLexiconCollection({'|*|PUNCT': ['PUNCT']})
    assert ['|*|PUNCT'] == collection.match('||', 'PUNCT')
    assert [] == collection.match('||', 'NOUN')


def test_match() -> None:
    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    assert ['*kg|NUM'] == collection.match('15kg', 'NUM')
    assert [] == collection.match('15kg', 'NOUN')
    assert ['[0-9][0-9]*ish|NUM'] == collection.match('10ish', 'NUM')
    assert [] == collection.match('ish', 'NUM')
    assert ['*|PUNCT'] == collection.match('!', 'PUNCT')
    assert ['*MB|N*'] == collection.match('10MB', 'NOUN')
    assert [] == collection.match('10mb', 'NOUN')
    assert [] == collection.match('10MB', 'PROPN')
    # A POS pattern has to match the whole POS tag.
    assert [] == collection.match('15kg', 'NUMBER')

    # Matches are returned in the order they were added.
    collection = AutotagLexiconCollection({'*|NUM': ['N1'], '*kg|NUM': ['N3.5']})
    assert ['*|NUM', '*kg|NUM'] == collection.match('15kg', 'NUM')


def test_mutable_mapping_methods() -> None:
    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    assert 4 == len(collection)
    assert list(AUTOTAG_ENTRIES) == list(collection)
    assert ['N3.2', 'N5'] == collection['*MB|N*']

    del collection['*kg|NUM']
    assert 3 == len(collection)
    assert '*kg|NUM' not in collection
    assert '*kg|NUM' not in collection.patterns
    assert [] == collection.match('15kg', 'NUM')

    with pytest.raises(KeyError):
        collection['*kg|NUM']


def test_to_dictionary() -> None:
    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    assert AUTOTAG_ENTRIES == collection.to_dictionary()


def test_to_from_bytes() -> None:
    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    collection_from_bytes = AutotagLexiconCollection.from_bytes(collection.to_bytes())
    assert collection == collection_from_bytes
    assert collection.patterns == collection_from_bytes.patterns

    # Entry order sets priority, so serialisation must preserve it, the keys are
    # deliberately not alphabetical so that sorting during serialisation would fail.
    unsorted_collection = AutotagLexiconCollection({'*z|NUM': ['N1'], '*a|NUM': ['N2'], '*m|NUM': ['N3']})
    unsorted_from_bytes = AutotagLexiconCollection.from_bytes(unsorted_collection.to_bytes())
    assert list(unsorted_collection) == list(unsorted_from_bytes)
    assert unsorted_collection == unsorted_from_bytes

    empty_collection = AutotagLexiconCollection()
    assert empty_collection == AutotagLexiconCollection.from_bytes(empty_collection.to_bytes())


def test_from_tsv() -> None:
    assert AUTOTAG_ENTRIES == AutotagLexiconCollection.from_tsv(AUTOTAG_LEXICON_FILE_PATH)
    assert AUTOTAG_ENTRIES == AutotagLexiconCollection.from_tsv(str(AUTOTAG_LEXICON_FILE_PATH))


def test_from_tsv_url(monkeypatch: MonkeyPatch) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        monkeypatch.setenv('PYMUSAS_HOME', temp_dir)
        importlib.reload(config)
        with responses.RequestsMock() as rsps:
            req_kwargs = {"stream": True}
            expected_response = 'lemma\tpos\tsemantic_tags\n*kg\tNUM\tN3.5\n'
            lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/English/semantic_lexicon_en_autotag.tsv'
            rsps.add(responses.GET, lexicon_url, status=200,
                     body=expected_response,
                     match=[responses.matchers.request_kwargs_matcher(req_kwargs)])
            assert {'*kg|NUM': ['N3.5']} == AutotagLexiconCollection.from_tsv(lexicon_url)


@pytest.mark.parametrize('tsv_file_path', [POS_WILDCARD_LEXICON_FILE_PATH,
                                           UNCLOSED_CLASS_LEXICON_FILE_PATH,
                                           NO_POS_LEXICON_FILE_PATH])
def test_from_tsv_invalid(tsv_file_path: Path) -> None:
    with pytest.raises(ValueError):
        AutotagLexiconCollection.from_tsv(tsv_file_path)


def test_tsv_merge() -> None:
    merged = AutotagLexiconCollection.tsv_merge(AUTOTAG_LEXICON_FILE_PATH,
                                                SECOND_AUTOTAG_LEXICON_FILE_PATH)
    # Entries from the later file come first, in their file order, and take
    # priority. `*kg|NUM` is in both files, so it uses the tags and position
    # from the later file. The remaining entries from the first file follow
    # in their file order.
    expected = {'*kg|NUM': ['N1'],
                '*-year-old|ADJ': ['T3'],
                '[0-9][0-9]*ish|NUM': ['N1'],
                '*|PUNCT': ['PUNCT'],
                '*MB|N*': ['N3.2', 'N5']}
    assert expected == merged
    assert list(expected) == list(merged)
    assert list(expected) == list(AutotagLexiconCollection(merged))

    merged = AutotagLexiconCollection.tsv_merge(SECOND_AUTOTAG_LEXICON_FILE_PATH,
                                                AUTOTAG_LEXICON_FILE_PATH)
    expected = dict(AUTOTAG_ENTRIES)
    expected['*-year-old|ADJ'] = ['T3']
    assert expected == merged
    assert list(expected) == list(merged)

    assert AUTOTAG_ENTRIES == AutotagLexiconCollection.tsv_merge(AUTOTAG_LEXICON_FILE_PATH)


def test__str__() -> None:
    assert ('AutotagLexiconCollection() (0 entires in the collection)'
            == str(AutotagLexiconCollection()))
    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    expected_str = ("AutotagLexiconCollection(('*kg|NUM': ['N3.5']), "
                    "('[0-9][0-9]*ish|NUM': ['N1']), ... ) "
                    "(4 entires in the collection)")
    assert expected_str == str(collection)


def test__repr__() -> None:
    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    expected_repr = f'AutotagLexiconCollection(data={AUTOTAG_ENTRIES})'
    assert expected_repr == repr(collection)
    assert collection == eval(repr(collection))


def test__eq__() -> None:
    collection = AutotagLexiconCollection(AUTOTAG_ENTRIES)
    assert collection == AutotagLexiconCollection(dict(AUTOTAG_ENTRIES))
    assert collection != AutotagLexiconCollection()
    assert collection != AutotagLexiconCollection({'*kg|NUM': ['N3.5']})
    assert collection != AUTOTAG_ENTRIES
    assert AutotagLexiconCollection() == AutotagLexiconCollection()

    # The order of the entries sets their priority, so it must affect equality.
    reordered_entries = dict(reversed(AUTOTAG_ENTRIES.items()))
    assert AUTOTAG_ENTRIES == reordered_entries
    assert collection != AutotagLexiconCollection(reordered_entries)
    assert AutotagLexiconCollection(reordered_entries) \
        == AutotagLexiconCollection(dict(reversed(AUTOTAG_ENTRIES.items())))
