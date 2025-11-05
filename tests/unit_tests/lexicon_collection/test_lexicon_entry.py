from dataclasses import FrozenInstanceError

import pytest

from pymusas.lexicon_collection import LexiconEntry


LEXICON_ENTRY = LexiconEntry('London', ['Z2'], 'noun')
LEXICON_ENTRY_MULTI_SEM = LexiconEntry('Laptop', ['Z3', 'Z0'], 'noun')
NON_POS_ENTRY = LexiconEntry('London', ['Z2'])


def test_lexicon_entry() -> None:
        
    assert LEXICON_ENTRY.lemma == "London"
    assert LEXICON_ENTRY.pos == "noun"
    assert LEXICON_ENTRY.semantic_tags == ["Z2"]
    assert str(LEXICON_ENTRY) == "LexiconEntry(lemma='London', semantic_tags=['Z2'], pos='noun')"
    
    with pytest.raises(FrozenInstanceError):
        for attribute in ['lemma', 'pos', 'semantic_tags']:
            setattr(LEXICON_ENTRY, attribute, 'test')

    assert LEXICON_ENTRY_MULTI_SEM.lemma == "Laptop"
    assert LEXICON_ENTRY_MULTI_SEM.pos == "noun"
    assert LEXICON_ENTRY_MULTI_SEM.semantic_tags == ["Z3", "Z0"]
    assert str(LEXICON_ENTRY_MULTI_SEM) == "LexiconEntry(lemma='Laptop', semantic_tags=['Z3', 'Z0'], pos='noun')"

    assert LEXICON_ENTRY != LEXICON_ENTRY_MULTI_SEM
    assert LEXICON_ENTRY == LexiconEntry('London', pos='noun', semantic_tags=['Z2'])

    assert str(NON_POS_ENTRY) == "LexiconEntry(lemma='London', semantic_tags=['Z2'], pos=None)"
    assert NON_POS_ENTRY == LexiconEntry('London', ['Z2'], None)
