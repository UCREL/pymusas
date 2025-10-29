from pathlib import Path
from typing import Callable, Iterable, List, Optional, Union, cast

import spacy
from spacy.language import Language
from spacy.tokens import Doc
from spacy.training import Example
from spacy.util import SimpleFrozenList
import srsly

from pymusas.file_utils import ensure_path
from pymusas.rankers.lexicon_entry import LexiconEntryRanker
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.spacy_api.utils import set_custom_token_extension
from pymusas.taggers.rules.rule import Rule


class RuleBasedTagger(spacy.pipeline.pipe.Pipe):
    '''
    [spaCy pipeline component](https://spacy.io/usage/processing-pipelines)
    of the :class:`pymusas.taggers.rule_based.RuleBasedTagger`.

    This component applies one or more :class:`pymusas.taggers.rules.rule.Rule`s
    to create a list of possible candidate tags for each token in the sequence.
    Each candidate, represented as a
    :class:`pymusas.rankers.ranking_meta_data.RankingMetaData` object, for each
    token is then Ranked using a
    :class:`pymusas.rankers.lexicon_entry.LexiconEntryRanker` ranker. The best
    candidate and it's associated tag(s) for each token are then assigned to the
    `Token._.pymusas_tags` attribute in addition a `List` of token indexes
    indicating if the token is part of a Multi Word Expression (MWE) is assigned
    to the `Token._.pymusas_mwe_indexes`.

    If we cannot tag a token then the following process will happen:
    1. If the token's POS tag is in `default_punctuation_tags` then it will assign the
    tag `PUNCT`.
    2. If the token's POS tag is in `default_number_tags` then it will assign the tag
    `N1`.
    3. Assign the default tag `Z99`.

    **NOTE** this tagger has been designed to be flexible with the amount of
    resources avaliable, for example if you do not have a POS tagger or
    lemmatiser in your spaCy pipeline this ok, just use the default
    `pos_attribute` and `lemma_attribute`.

    # Assigned Attributes

    <table>
        <tr>
            <th> Location </th>
            <th> Type </th>
            <th> Value </th>
        </tr>
        <tr>
            <td> Token._.pymusas_tags </td>
            <td> `List[str]` </td>
            <td> Prediced tags, the first tag in the List of tags is the
            most likely tag.</td>
        </tr>
        <tr>
            <td> Token._.pymusas_mwe_indexes </td>
            <td> `List[Tuple[int, int]]` </td>
            <td> Each `Tuple` indicates the start and end token index of the
            associated Multi Word Expression (MWE). If the `List` contains
            more than one `Tuple` then the MWE is discontinuous. For single word
            expressions the `List` will only contain 1 `Tuple` which will be
            (token_start_index, token_start_index + 1).</td>
        </tr>
    </table>
    
    # Config and implementation

    The default config is defined by the pipeline component factory and describes
    how the component should be configured. You can override its settings via the `config`
    argument on [nlp.add_pipe](https://spacy.io/api/language#add_pipe) or in your
    [config.cfg for training](https://spacy.io/usage/training#config).

    | Setting                  | Description                  |
    |--------------------------|------------------------------|
    | pymusas_tags_token_attr  | See parameters section below |
    | pymusas_mwe_indexes_attr | See parameters section below |
    | pos_attribute            | See parameters section below |
    | lemma_attribute          | See parameters section below |

    # Parameters

    name : `str`, optional (default = `pymusas_rule_based_tagger`)
        The component name. Defaults to the same name as the class variable
        `COMPONENT_NAME`.
    pymusas_tags_token_attr : `str`, optional (default = `pymusas_tags`)
        The name of the attribute to assign the predicted tags too under
        the `Token._` class.
    pymusas_mwe_indexes_attr : `str`, optional (default = `pymusas_mwe_indexes`)
        The name of the attribute to assign the start and end token index of the
        associated MWE too under the `Token._` class.
    pos_attribute : `str`, optional (default = `pos_`)
        The name of the attribute that the Part Of Speech (POS) tag is assigned too
        within the `Token` class. The POS tag value that comes from this attribute
        has to be of type `str`. With the current default we take the POS tag
        from `Token.pos_`. The POS tag can be an empty string if you do not require
        POS information or if you do not have a POS tagger. **NOTE** that if you
        do not have a POS tagger the default value for `Token.pos_` is an empty
        string.
    lemma_attribute : `str`, optional (default = `lemma_`)
        The name of the attribute that the lemma is assigned too within the `Token`
        class. The lemma value that comes from this attribute has to be of
        type `str`. With the current default we take the lemma from `Token.lemma_`.
        The lemma can be an empty string if you do not require
        lemma information or if you do not have a lemmatiser. **NOTE** that if you
        do not have a lemmatiser the default value for `Token.lemma_` is an empty
        string.

    # Instance Attributes

    name : `str`
        The component name.
    rules : `List[pymusas.taggers.rules.rule.Rule]`, optional (default = `None`)
        The `rules` is set through the :func:`initialize` method. Before it is
        set by the :func:`initialize` method the value of this attribute is `None`.
    ranker : `pymusas.rankers.lexicon_entry.LexiconEntryRanker`, optional (default = `None`)
        The `ranker` is set through the :func:`initialize` method. Before it is
        set by the :func:`initialize` method the value of this attribute is `None`.
    default_punctuation_tags : `Set[str]`
        The `default_punctuation_tags` is set through the :func:`initialize` method.
    default_number_tags : `Set[str]`
        The `default_number_tags` is set through the :func:`initialize` method.
    pymusas_tags_token_attr : `str`, optional (default = `pymusas_tags`)
        The given `pymusas_tags_token_attr`
    pymusas_mwe_indexes_attr : `str`, optional (default = `pymusas_mwe_indexes`)
        The given `pymusas_mwe_indexes_attr`
    pos_attribute : `str`, optional (default = `pos_`)
        The given `pos_attribute`
    lemma_attribute : `str`, optional (default = `lemma_`)
        The given `lemma_attribute`

    # Class Attributes

    COMPONENT_NAME : `str`
        Name of component factory that this component is registered under. This
        is used as the first argument to
        [`Language.add_pipe`](https://spacy.io/api/language#add_pipe)
        if you want to add this component to your spaCy pipeline.

    # Examples

    ``` python
    >>> import spacy
    >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
    >>> from pymusas.pos_mapper import BASIC_CORCENCC_TO_USAS_CORE
    >>> from pymusas.lexicon_collection import LexiconCollection
    >>> from pymusas.taggers.rules.single_word import SingleWordRule
    >>> from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
    >>> # Construction via spaCy pipeline
    >>> nlp = spacy.blank('en')
    >>> # Using default config
    >>> single_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
    >>> single_lexicon = LexiconCollection.from_tsv(single_lexicon_url)
    >>> single_lemma_lexicon = LexiconCollection.from_tsv(single_lexicon_url,
    ...                                                   include_pos=False)
    >>> single_rule = SingleWordRule(single_lexicon, single_lemma_lexicon,
    ...                              pos_mapper=BASIC_CORCENCC_TO_USAS_CORE)
    >>> rules = [single_rule]
    >>> ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
    >>> tagger = nlp.add_pipe('pymusas_rule_based_tagger')
    >>> tagger.rules = rules
    >>> tagger.ranker = ranker
    >>> token = nlp('aberth')
    >>> assert token[0]._.pymusas_tags == ['S9', 'A9-']
    >>> assert token[0]._.pymusas_mwe_indexes == [(0, 1)]
    >>> # Custom config
    >>> custom_config = {'pymusas_tags_token_attr': 'semantic_tags',
    ...                  'pymusas_mwe_indexes_attr': 'mwe_indexes'}
    >>> nlp = spacy.blank('en')
    >>> tagger = nlp.add_pipe('pymusas_rule_based_tagger', config=custom_config)
    >>> tagger.rules = rules
    >>> tagger.ranker = ranker
    >>> token = nlp('aberth')
    >>> assert token[0]._.semantic_tags == ['S9', 'A9-']
    >>> assert token[0]._.mwe_indexes == [(0, 1)]

    ```
    '''
    COMPONENT_NAME = 'pymusas_rule_based_tagger'

    def __init__(self,
                 name: str = 'pymusas_rule_based_tagger',
                 pymusas_tags_token_attr: str = 'pymusas_tags',
                 pymusas_mwe_indexes_attr: str = 'pymusas_mwe_indexes',
                 pos_attribute: str = 'pos_',
                 lemma_attribute: str = 'lemma_'
                 ) -> None:
        self.name = name
        
        self._pymusas_tags_token_attr = pymusas_tags_token_attr
        set_custom_token_extension(pymusas_tags_token_attr)

        self._pymusas_mwe_indexes_attr = pymusas_mwe_indexes_attr
        set_custom_token_extension(pymusas_mwe_indexes_attr)
        
        self._pos_attribute = pos_attribute
        self._lemma_attribute = lemma_attribute
        
        self.rules: Optional[List[Rule]] = None
        self.ranker: Optional[LexiconEntryRanker] = None
        
        self.default_punctuation_tags = set(['punc'])
        self.default_number_tags = set(['num'])
        
        self._validated = False

    def _validate(self) -> None:
        '''
        Checks that `rules` and `ranker` are not `None`
        '''
        error_msg = ('The `{}` attribute cannot be `None`, this '
                     'attribute can be set through the `initialize` method.')
        if self.rules is None:
            raise ValueError(error_msg.format('rules'))
        
        if self.ranker is None:
            raise ValueError(error_msg.format('ranker'))

        self._validated = True
    
    def initialize(self,
                   get_examples: Optional[Callable[[], Iterable[Example]]] = None,
                   *,
                   nlp: Optional[Language] = None,
                   rules: Optional[List[Rule]] = None,
                   ranker: Optional[LexiconEntryRanker] = None,
                   default_punctuation_tags: Optional[List[str]] = None,
                   default_number_tags: Optional[List[str]] = None,
                   ) -> None:
        '''
        Initialize the tagger and load any of the resources given. The method is
        typically called by
        [`Language.initialize`](https://spacy.io/api/language#initialize)
        and lets you customize arguments it receives via the
        [`initialize.components`](https://spacy.io/api/data-formats#config-initialize)
        block in the config. The loading only happens during initialization,
        typically before training. At runtime, all data is load from disk.

        # Parameters
        
        rules : `List[pymusas.taggers.rules.rule.Rule]`
            A list of rules to apply to the sequence of tokens in the
            :func:`__call__`. The output from each rule is concatendated and given
            to the `ranker`.
        ranker : `pymusas.rankers.lexicon_entry.LexiconEntryRanker`
            A ranker to rank the output from all of the `rules`.
        default_punctuation_tags : `List[str]`, optional (default = `None`)
            The POS tags that represent punctuation. If `None` then we will use
            `['punc']`. The list will be converted into a `Set` before assigning
            to the `default_punctuation_tags` attribute.
        default_number_tags : `List[str]`, optional (default = `None`)
            The POS tags that represent numbers. If `None` then we will use
            `['num']`. The list will be converted into a `Set` before assigning
            to the `default_number_tags` attribute.
        '''
        if rules is not None:
            self.rules = rules
        
        if ranker is not None:
            self.ranker = ranker
        
        if default_punctuation_tags is not None:
            self.default_punctuation_tags = set(default_punctuation_tags)
        
        if default_number_tags is not None:
            self.default_number_tags = set(default_number_tags)
        
        self._validate()
    
    def __call__(self, doc: Doc) -> Doc:
        '''
        Applies the tagger to the spaCy document, modifies it in place, and
        returns it. This usually happens under the hood when the `nlp` object is
        called on a text and all pipeline components are applied to the `Doc` in
        order.
        
        # Parameters

        doc : `Doc`
            A [spaCy `Doc`](https://spacy.io/api/doc)

        # Returns

        `Doc`
        '''
        if not self._validated:
            self._validate()
        
        ranker = cast(LexiconEntryRanker, self.ranker)
        rules = cast(List[Rule], self.rules)
        
        # Try, catch error handling reference:
        # https://github.com/explosion/spaCy/blob/6af6c2e86cc7b08573b261563786bd1ab87d45e9/spacy/pipeline/lemmatizer.py#L131
        error_handler = self.get_error_handler()
        try:
            tokens: List[str] = []
            lemmas: List[str] = []
            pos_tags: List[str] = []
            for token in doc:
                tokens.append(token.text)
                lemmas.append(getattr(token, self.lemma_attribute))
                pos_tags.append(getattr(token, self.pos_attribute))
            token_ranking_meta_data: List[List[RankingMetaData]] \
                = [[] for _ in range(len(tokens))]
            for rule in rules:
                rule_ranking_meta_data = rule(tokens, lemmas, pos_tags)
                for token_index, ranking_meta_data in enumerate(rule_ranking_meta_data):
                    token_ranking_meta_data[token_index].extend(ranking_meta_data)
            
            token_ranks, token_best_rank = ranker(token_ranking_meta_data)
            
            for token_index, best_rank in enumerate(token_best_rank):
                token = doc[token_index]
                if best_rank is None:
                    pos_tag = pos_tags[token_index]
                    if pos_tag in self.default_punctuation_tags:
                        setattr(token._, self.pymusas_tags_token_attr, ['PUNCT'])
                        setattr(token._, self.pymusas_mwe_indexes_attr,
                                [(token_index, token_index + 1)])
                    elif pos_tag in self.default_number_tags:
                        setattr(token._, self.pymusas_tags_token_attr, ['N1'])
                        setattr(token._, self.pymusas_mwe_indexes_attr,
                                [(token_index, token_index + 1)])
                    else:
                        setattr(token._, self.pymusas_tags_token_attr, ['Z99'])
                        setattr(token._, self.pymusas_mwe_indexes_attr,
                                [(token_index, token_index + 1)])
                    continue
                tags = list(best_rank.semantic_tags)
                indexes = [(best_rank.token_match_start_index,
                            best_rank.token_match_end_index)]
            
                setattr(token._, self.pymusas_tags_token_attr, tags)
                setattr(token._, self.pymusas_mwe_indexes_attr, indexes)
        except Exception as e:
            error_handler(self.name, self, [doc], e)
        
        return doc

    def to_bytes(self, *, exclude: Iterable[str] = SimpleFrozenList()) -> bytes:
        '''
        Serialises the tagger to a bytestring.

        # Parameters

        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.
        
        # Returns

        `bytes`

        # Examples

        ``` python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.taggers.rules.single_word import SingleWordRule
        >>> from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
        >>> rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
        >>> ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
        >>> tagger = RuleBasedTagger()
        >>> tagger.initialize(rules=rules, ranker=ranker)
        >>> tagger_bytes = tagger.to_bytes()

        ```
        '''
        if not self._validated:
            self._validate()
        ranker = cast(LexiconEntryRanker, self.ranker)
        rules = cast(List[Rule], self.rules)

        default_punctuation_tags = list(self.default_punctuation_tags)
        default_number_tags = list(self.default_number_tags)
        
        serialise = {}
        serialise["rules"] = Rule.serialise_object_list_to_bytes(rules)
        serialise["ranker"] = LexiconEntryRanker.serialise_object_to_bytes(ranker)
        serialise["default_punctuation_tags"] = srsly.msgpack_dumps(default_punctuation_tags)
        serialise["default_number_tags"] = srsly.msgpack_dumps(default_number_tags)
        
        return cast(bytes, srsly.msgpack_dumps(serialise))

    def from_bytes(self, bytes_data: bytes, *,
                   exclude: Iterable[str] = SimpleFrozenList()
                   ) -> "RuleBasedTagger":
        '''
        Loads the tagger from the given bytestring in place and returns it.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.
        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        :class:`RuleBasedTagger`

        # Examples
        
        ``` python
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.taggers.rules.single_word import SingleWordRule
        >>> from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
        >>> rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
        >>> ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
        >>> tagger = RuleBasedTagger()
        >>> tagger.initialize(rules=rules, ranker=ranker)
        >>> # Create a new tagger, tagger 2
        >>> tagger_2 = RuleBasedTagger()
        >>> # Show that it is not the same as the original tagger
        >>> assert tagger_2.rules != rules
        >>> # Tagger 2 will now load in the data from the original tagger
        >>> _ = tagger_2.from_bytes(tagger.to_bytes())
        >>> assert tagger_2.rules == rules
        >>> assert tagger_2.ranker == ranker

        ```
        '''
        serialise_data = srsly.msgpack_loads(bytes_data)

        self.rules = cast(List[Rule],
                          Rule.serialise_object_list_from_bytes(serialise_data['rules']))

        self.ranker \
            = cast(LexiconEntryRanker,
                   LexiconEntryRanker.serialise_object_from_bytes(serialise_data['ranker']))

        default_punctuation_tags = srsly.msgpack_loads(serialise_data["default_punctuation_tags"])
        self.default_punctuation_tags = set(default_punctuation_tags)

        default_number_tags = srsly.msgpack_loads(serialise_data["default_number_tags"])
        self.default_number_tags = set(default_number_tags)
        
        self._validate()
        return self
    
    def to_disk(self, path: Union[str, Path], *,
                exclude: Iterable[str] = SimpleFrozenList()
                ) -> None:
        '''
        Serialises the tagger to the given `path`.

        # Parameters

        path : `Union[str, Path]`
            Path to a direcotry. Path may be either string or `Path`-like
            object. If the directory does not exist it attempts to create a
            directory at the given `path`.
        
        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        `None`

        # Examples

        ```python
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.taggers.rules.single_word import SingleWordRule
        >>> from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
        >>> rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
        >>> ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
        >>> tagger = RuleBasedTagger()
        >>> tagger.initialize(rules=rules, ranker=ranker)
        >>> with TemporaryDirectory() as temp_dir:
        ...     _ = tagger.to_disk(temp_dir)
        ...

        ```
        '''
        if not self._validated:
            self._validate()
        ranker = cast(LexiconEntryRanker, self.ranker)
        rules = cast(List[Rule], self.rules)

        component_folder = ensure_path(path)
        component_folder.mkdir(exist_ok=True)

        ranker_path = Path(component_folder, 'ranker.bin')
        srsly.write_msgpack(ranker_path,
                            LexiconEntryRanker.serialise_object_to_bytes(ranker))

        rules_path = Path(component_folder, 'rules.bin')
        srsly.write_msgpack(rules_path,
                            Rule.serialise_object_list_to_bytes(rules))

        default_punctuation_tags_path = Path(component_folder,
                                             'default_punctuation_tags.bin')
        default_punctuation_tags = list(self.default_punctuation_tags)
        srsly.write_msgpack(default_punctuation_tags_path, default_punctuation_tags)
        
        default_number_tags_path = Path(component_folder, 'default_number_tags.bin')
        default_number_tags = list(self.default_number_tags)
        srsly.write_msgpack(default_number_tags_path, default_number_tags)

    def from_disk(self, path: Union[str, Path], *,
                  exclude: Iterable[str] = SimpleFrozenList()
                  ) -> "RuleBasedTagger":
        '''
        Loads the tagger from the given `path` in place and returns it.

        # Parameters

        path : `Union[str, Path]`
            Path to an existing direcotry. Path may be either string or
            `Path`-like object.
        
        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        :class:`RuleBasedTagger`

        # Examples

        ```python
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
        >>> from pymusas.taggers.rules.single_word import SingleWordRule
        >>> from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
        >>> rules = [SingleWordRule({'example|noun': ['Z1']}, {})]
        >>> ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
        >>> tagger = RuleBasedTagger()
        >>> tagger.initialize(rules=rules, ranker=ranker)
        >>> # Create an empty second tagger
        >>> tagger_2 = RuleBasedTagger()
        >>> assert tagger_2.rules is None
        >>> with TemporaryDirectory() as temp_dir:
        ...     _ = tagger.to_disk(temp_dir)
        ...     _ = tagger_2.from_disk(temp_dir)
        ...
        >>> assert tagger_2.rules is not None
        >>> assert tagger_2.rules == tagger.rules

        ```

        '''
        component_folder = ensure_path(path)
        
        ranker_path = Path(component_folder, 'ranker.bin')
        serialised_ranker = srsly.read_msgpack(ranker_path)
        ranker = LexiconEntryRanker.serialise_object_from_bytes(serialised_ranker)
        self.ranker = cast(LexiconEntryRanker, ranker)

        rules_path = Path(component_folder, 'rules.bin')
        serialised_rules = srsly.read_msgpack(rules_path)
        rules = Rule.serialise_object_list_from_bytes(serialised_rules)
        self.rules = cast(List[Rule], rules)

        default_punctuation_tags_path = Path(component_folder,
                                             'default_punctuation_tags.bin')
        default_punctuation_tags = srsly.read_msgpack(default_punctuation_tags_path)
        self.default_punctuation_tags = set(default_punctuation_tags)
        
        default_number_tags_path = Path(component_folder, 'default_number_tags.bin')
        default_number_tags = srsly.read_msgpack(default_number_tags_path)
        self.default_number_tags = set(default_number_tags)

        self._validate()
        return self
        
    @property
    def pymusas_tags_token_attr(self) -> str:
        return self._pymusas_tags_token_attr

    @property
    def pymusas_mwe_indexes_attr(self) -> str:
        return self._pymusas_mwe_indexes_attr

    @property
    def pos_attribute(self) -> str:
        return self._pos_attribute

    @property
    def lemma_attribute(self) -> str:
        return self._lemma_attribute


@Language.factory(RuleBasedTagger.COMPONENT_NAME, requires=['token.pos', 'token.lemma'],
                  assigns=['token._.pymusas_tags', 'token._.pymusas_mwe_indexes'],
                  default_config={'pymusas_tags_token_attr': 'pymusas_tags',
                                  'pymusas_mwe_indexes_attr': 'pymusas_mwe_indexes',
                                  'pos_attribute': 'pos_',
                                  'lemma_attribute': 'lemma_'})
def make_usas_rule_based_tagger(nlp: Language, name: str,
                                pymusas_tags_token_attr: str,
                                pymusas_mwe_indexes_attr: str,
                                pos_attribute: str,
                                lemma_attribute: str
                                ) -> RuleBasedTagger:
    return RuleBasedTagger(name, pymusas_tags_token_attr,
                           pymusas_mwe_indexes_attr,
                           pos_attribute, lemma_attribute)
