from enum import IntEnum


class LexicalMatch(IntEnum):
    '''
    Descriptions of the lexical matches and their ordering in tagging priority
    during ranking. Lower the value and rank the higher the tagging priority.

    The `value` attribute of each instance attribute is of type `int`. For the
    best explanation see the example below.

    # Instance Attributes

    TOKEN : `int`
        The lexicon entry matched on the token text.
    LEMMA : `int`
        The lexicon entry matched on the lemma of the token.
    TOKEN_LOWER : `int`
        The lexicon entry matched on the lower cased token text.
    LEMMA_LOWER : `int`
        The lexicon entry matched on the lower cased lemma of the token.

    # Examples
    ``` python
    >>> from pymusas.rankers.lexical_match import LexicalMatch
    >>> assert 1 == LexicalMatch.TOKEN
    >>> assert 'TOKEN' == LexicalMatch.TOKEN.name
    >>> assert 1 == LexicalMatch.TOKEN.value
    ...
    >>> assert 2 == LexicalMatch.LEMMA
    >>> assert 3 == LexicalMatch.TOKEN_LOWER
    >>> assert 4 == LexicalMatch.LEMMA_LOWER
    ...
    >>> assert 2 < LexicalMatch.LEMMA_LOWER

    ```
    '''
    TOKEN = 1
    LEMMA = 2
    TOKEN_LOWER = 3
    LEMMA_LOWER = 4

    def __repr__(self) -> str:
        '''
        Machine readable string. When printed and run `eval()` over the string
        you should be able to recreate the object.
        '''
        return self.__str__()
    
    def __str__(self) -> str:
        '''
        Returns the `class_name.name`, e.g. `LexicalMatch.TOKEN`

        Overridden as from Python version 3.11 IntEnum.__str__  by default would
        return the integer as a string.
        '''

        class_name = "LexicalMatch"
        return f"{class_name}.{self.name}"
