from typing import cast

import srsly

from pymusas import utils
from pymusas.lexicon_collection import LexiconType, MWELexiconCollection
from pymusas.rankers.lexical_match import LexicalMatch
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.taggers.rules import util
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule


class MWERule(Rule):
    '''
    A Multi Word Expression (MWE) rule match can be one of the following matches:

    1. `MWE_NON_SPECIAL` match - whereby the combined token/lemma and POS
    is found within the given MWE Lexicon Collection (`self.mwe_lexicon_collection`).
    2. `MWE_WILDCARD` match - whereby the combined token/lemma and POS matches
    a wildcard MWE template that is within the MWE Lexicon Collection
    (`self.mwe_lexicon_collection`).

    All rule matches use the
    `pymusas.lexicon_collection.MWELexiconCollection.mwe_match`
    method for matching. Matches are found based on the original token/lemma and
    lower cased versions of the token/lemma.

    **Default (`Df`) semantic tags**

    A MWE template can contain a default (`Df`) semantic tag, e.g. the
    template `*_ADJ style_NOUN` with the semantic tags `C1/Df`. The `Df` tag is
    replaced with the single word semantic tag of the token that matched the
    first token in the MWE template that starts with a wildcard (`*`), in
    this example the adjective. The single word semantic tag is found using the
    `single_word_rule`, whereby the best single word match is found using
    the :func:`pymusas.taggers.rules.single_word.best_match` method of
    :class:`pymusas.taggers.rules.single_word.SingleWordRule`, this includes
    `autotag` pattern matches if the token has no exact single word lexicon
    match, e.g. `15kg` with the POS `NUM` can match the `autotag` entry
    `*kg|NUM`. From this single word match the first semantic tag is used, and of that
    semantic tag only the first part of any slash tag, with all affixes and
    lower case markers removed, e.g. `A1+/Z3` becomes `A1`. Any affixes and
    lower case markers on the `Df` tag are added to it, e.g. `Df++` becomes
    `A1++`. For more details see :func:`pymusas.utils.resolve_default_tags`.

    If the `single_word_rule` is `None` or the token has no single word match
    then the `Df` tag is replaced with `Z99`.

    # Parameters

    mwe_lexicon_lookup : `dict[str, list[str]]`
        The data to create `mwe_lexicon_collection` instance attribute. A
        Dictionary where the keys are MWE templates, of any
        :class:`pymusas.lexicon_collection.LexiconType`,
        and the values are a list of associated semantic tags.
    pos_mapper : `dict[str, list[str]]`, optional (default = `None`)
        If not `None`, maps from the `mwe_lexicon_lookup` POS tagset to the
        desired POS tagset,whereby the mapping is a `list` of tags,
        at the moment there is no preference order in this list of POS tags.
        **Note** the longer the `list[str]` for
        each POS mapping the slower the tagger, a one to one mapping will have
        no speed impact on the tagger. A selection of POS mappers can be found in
        :mod:`pymusas.pos_mapper`.
    single_word_rule : `pymusas.taggers.rules.single_word.SingleWordRule`, optional (default = `None`)
        The single word rule used to find the semantic tags that replace
        default (`Df`) semantic tags, see the default semantic tags section
        above. If `None` all `Df` tags will be replaced with `Z99`.

    # Instance Attributes

    mwe_lexicon_collection : `pymusas.lexicon_collection.MWELexiconCollection`
        A :class:`pymusas.lexicon_collection.MWELexiconCollection` instance that
        has been initialised using the `mwe_lexicon_lookup` and `pos_mapper`
        parameters. This collection is used to find MWE rule matches.
    single_word_rule : `pymusas.taggers.rules.single_word.SingleWordRule`, optional (default = `None`)
        The given `single_word_rule`.

    # Examples
    ``` python
    >>> from pymusas.taggers.rules.mwe import MWERule
    >>> from pymusas.taggers.rules.single_word import SingleWordRule
    >>> single_word_rule = SingleWordRule({'acting|ADJ': ['A1/Z3']}, {})
    >>> mwe_rule = MWERule({'*_ADJ style_NOUN': ['C1/Df']},
    ...                    single_word_rule=single_word_rule)
    >>> ranking_meta_data = mwe_rule(['The', 'acting', 'style'],
    ...                              ['the', 'acting', 'style'],
    ...                              ['DET', 'ADJ', 'NOUN'])
    >>> assert ('C1/A1',) == ranking_meta_data[1][0].semantic_tags

    ```
    '''

    def __init__(self, mwe_lexicon_lookup: dict[str, list[str]],
                 pos_mapper: dict[str, list[str]] | None = None,
                 single_word_rule: SingleWordRule | None = None) -> None:
        
        self.mwe_lexicon_collection = MWELexiconCollection(mwe_lexicon_lookup,
                                                           pos_mapper)
        self.single_word_rule = single_word_rule

    def __call__(self, tokens: list[str], lemmas: list[str], pos_tags: list[str]
                 ) -> list[list[RankingMetaData]]:
        '''
        Given the tokens, lemmas, and POS tags for each word in a text,
        it returns for each token a `list` of rules matches defined by
        the :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object based on
        the rule matches stated in the class docstring above.
        
        # Parameters

        tokens : `list[str]`
            The tokens that are within the text.
        lemmas : `list[str]`
            The lemmas of the tokens.
        pos_tags : `list[str]`
            The Part Of Speech tags of the tokens.
        
        # Returns

        `list[list[RankingMetaData]]`

        # Raises

        `ValueError`
            If the length of the `tokens`, `lemmas`, and `pos_tags` are not of
            the same length.
        '''

        default_semantic_tag_cache: dict[int, str | None] = {}

        def default_semantic_tag(token_index: int) -> str | None:
            '''
            Returns the first semantic tag of the best single word match for
            the token at `token_index`, or `None` if there is no single word
            rule or match.
            '''
            if token_index in default_semantic_tag_cache:
                return default_semantic_tag_cache[token_index]

            semantic_tag: str | None = None
            if self.single_word_rule is not None:
                best_match = self.single_word_rule.best_match(tokens[token_index],
                                                              lemmas[token_index],
                                                              pos_tags[token_index])
                if best_match is not None and best_match.semantic_tags:
                    semantic_tag = best_match.semantic_tags[0]

            default_semantic_tag_cache[token_index] = semantic_tag
            return semantic_tag

        def tag_n_gram_indexes(_n_gram_indexes: list[tuple[int, int]],
                               mwe_type: LexiconType,
                               token_templates: list[str], lemma_templates: list[str],
                               token_lower_templates: list[str], lemma_lower_templates: list[str],
                               ranking_meta_data_by_token: list[list[RankingMetaData]]
                               ) -> None:
            '''
            Given a `list` of n gram indexes, whereby all grams have the same value
            of *n*, it will find all MWE rule matches of type `mwe_type` for those
            n-grams in the four token `list`s (`token_templates`, `lemma_templates`,
            `token_lower_templates`, `lemma_lower_templates`). All rule matches will crate a
            `RankingMetaData` object for each token in the match, of which these
            objects are appended to the relevant token indexes within the
            `ranking_meta_data_by_token` object.

            Nothing is returned but the `ranking_meta_data_by_token` object will have
            been updated if at least one rule match has been found.
            '''
            token_list_type: list[tuple[list[str], LexicalMatch]]
            token_list_type = [(token_templates, LexicalMatch.TOKEN),
                               (lemma_templates, LexicalMatch.LEMMA),
                               (token_lower_templates, LexicalMatch.TOKEN_LOWER),
                               (lemma_lower_templates, LexicalMatch.LEMMA_LOWER)]
            
            for token_list, token_type in token_list_type:
                for n_gram_index in _n_gram_indexes:
                    start_index, end_index = n_gram_index
                    mwe_template = ''
                    for token_index in range(start_index, end_index):
                        if (token_index + 1) == end_index:
                            mwe_template += f'{token_list[token_index]}'
                            continue
                        mwe_template += f'{token_list[token_index]} '
                    matched_mwe_templates = self.mwe_lexicon_collection.mwe_match(mwe_template,
                                                                                  mwe_type)
                    if not matched_mwe_templates:
                        continue

                    for matched_mwe_template in matched_mwe_templates:
                        mwe_meta_data = self.mwe_lexicon_collection[matched_mwe_template]
                        semantic_tags = tuple(mwe_meta_data.semantic_tags)
                        if utils.contains_default_tag(mwe_meta_data.semantic_tags):
                            default_index = utils.default_token_index(matched_mwe_template)
                            replacement_tag: str | None = None
                            # `default_index` should never be `None` as the
                            # `MWELexiconCollection` ignores MWE templates
                            # that have a `Df` tag but no token that starts
                            # with a wildcard.
                            if default_index is not None:
                                replacement_tag = default_semantic_tag(start_index + default_index)
                            semantic_tags = tuple(utils.resolve_default_tags(mwe_meta_data.semantic_tags,
                                                                             replacement_tag))
                        ranking_meta_data = RankingMetaData(mwe_type,
                                                            mwe_meta_data.n_gram_length,
                                                            mwe_meta_data.wildcard_count,
                                                            False, token_type, start_index,
                                                            end_index,
                                                            matched_mwe_template,
                                                            semantic_tags)
                        for token_index in range(start_index, end_index):
                            ranking_meta_data_by_token[token_index].append(ranking_meta_data)
                
        def tag_n_gram_based_MWE(mwe_type: LexiconType,
                                 token_templates: list[str], lemma_templates: list[str],
                                 token_lower_templates: list[str], lemma_lower_templates: list[str],
                                 ranking_meta_data_by_token: list[list[RankingMetaData]]
                                 ) -> None:
            '''
            Any type of rule match that uses n-grams should use this function.
            At the moment only the `MWE_NON_SPECIAL` and `MWE_WILDCARD` matches
            are supported.
            
            The function for each token list () creates n-grams, up to the size
            of the maximum n-gram for the match type requested, of these tokens
            and then matches those n-grams using the
            `pymusas.lexicon_collection.MWELexiconCollection.mwe_match`
            method.

            Nothing is returned but the `ranking_meta_data_by_token` object will have
            been updated if at least one rule match has been found.
            '''
            largest_mwe_in_lexicon = 0
            if mwe_type == LexiconType.MWE_NON_SPECIAL:
                largest_mwe_in_lexicon = self.mwe_lexicon_collection.longest_non_special_mwe_template
            elif mwe_type == LexiconType.MWE_WILDCARD:
                largest_mwe_in_lexicon = self.mwe_lexicon_collection.longest_wildcard_mwe_template
            
            # If we do not have any MWE lexicons that are at least 2 grams
            # then return
            if largest_mwe_in_lexicon < 2:
                return
            
            largest_n_gram = largest_mwe_in_lexicon + 1
            largest_n_gram_indexes: list[tuple[int, int]] = []

            for n_gram_index in util.n_gram_indexes(token_templates, 2, largest_mwe_in_lexicon):
                start_index, end_index = n_gram_index
                n_gram_size = end_index - start_index
                if largest_n_gram > n_gram_size:
                    largest_n_gram = n_gram_size
                    tag_n_gram_indexes(largest_n_gram_indexes, mwe_type,
                                       token_templates, lemma_templates, token_lower_templates,
                                       lemma_lower_templates,
                                       ranking_meta_data_by_token)
                    largest_n_gram_indexes = []

                largest_n_gram_indexes.append(n_gram_index)
            
            tag_n_gram_indexes(largest_n_gram_indexes, mwe_type, token_templates,
                               lemma_templates, token_lower_templates,
                               lemma_lower_templates, ranking_meta_data_by_token)
        
        tokens_with_pos: list[str] = []
        tokens_lower_with_pos: list[str] = []
        lemmas_with_pos: list[str] = []
        lemmas_lower_with_pos: list[str] = []
        for token, lemma, pos in zip(tokens, lemmas, pos_tags, strict=True):
            tokens_with_pos.append(f'{token}_{pos}')
            tokens_lower_with_pos.append(f'{token}_{pos}'.lower())
            lemmas_with_pos.append(f'{lemma}_{pos}')
            lemmas_lower_with_pos.append(f'{lemma}_{pos}'.lower())
        
        number_tokens = len(tokens)
        token_ranking_meta_data: list[list[RankingMetaData]] \
            = [[] for _ in range(number_tokens)]
        
        if number_tokens < 2:
            return token_ranking_meta_data

        # First match on `MWE_NON_SPECIAL`
        tag_n_gram_based_MWE(LexiconType.MWE_NON_SPECIAL, tokens_with_pos, lemmas_with_pos,
                             tokens_lower_with_pos, lemmas_lower_with_pos,
                             token_ranking_meta_data)

        # Second match on `MWE_WILDCARD`
        tag_n_gram_based_MWE(LexiconType.MWE_WILDCARD, tokens_with_pos, lemmas_with_pos,
                             tokens_lower_with_pos, lemmas_lower_with_pos,
                             token_ranking_meta_data)

        return token_ranking_meta_data

    def to_bytes(self) -> bytes:
        '''
        Serialises the :class:`MWERule` to a bytestring.

        # Returns

        `bytes`
        '''
        serialise: dict[str, bytes | None] = {}
        serialise['mwe_lexicon_collection'] = self.mwe_lexicon_collection.to_bytes()
        serialise['single_word_rule'] = None
        if self.single_word_rule is not None:
            serialise['single_word_rule'] = self.single_word_rule.to_bytes()
        return cast(bytes, srsly.msgpack_dumps(serialise))

    @staticmethod
    def from_bytes(bytes_data: bytes) -> "MWERule":
        '''
        Loads :class:`MWERule` from the given bytestring and returns it.

        Bytestrings created before the `single_word_rule` was added, which
        only contain the serialised `mwe_lexicon_collection`, can also be
        loaded.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.
        
        # Returns

        :class:`MWERule`
        '''
        mwe_rule = MWERule({}, None)
        serialise_data = srsly.msgpack_loads(bytes_data)
        if 'mwe_lexicon_collection' not in serialise_data:
            mwe_rule.mwe_lexicon_collection = MWELexiconCollection.from_bytes(bytes_data)
            return mwe_rule

        mwe_rule.mwe_lexicon_collection \
            = MWELexiconCollection.from_bytes(serialise_data['mwe_lexicon_collection'])
        if serialise_data['single_word_rule'] is not None:
            mwe_rule.single_word_rule \
                = SingleWordRule.from_bytes(serialise_data['single_word_rule'])
        return mwe_rule

    def __eq__(self, other: object) -> bool:
        '''
        Given another object to compare too it will return `True` if the other
        object is the same class and initialised using with the same argument
        values.

        # Parameters

        other : `object`
            The object to compare too.
        
        # Returns

        `True`
        '''
        if not isinstance(other, MWERule):
            return False
        
        if self.mwe_lexicon_collection != other.mwe_lexicon_collection:
            return False

        if self.single_word_rule != other.single_word_rule:
            return False

        return True
