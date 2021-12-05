import copy
import logging
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Union, cast

from spacy.language import Language
from spacy.pipe_analysis import validate_attrs
from spacy.tokens import Doc, Token
from spacy.training import Example
from spacy.util import SimpleFrozenList
import srsly

from ...file_utils import ensure_path
from ...taggers.rule_based import _tag_token


logger = logging.getLogger(__name__)


class USASRuleBasedTagger:
    '''
    [spaCy pipeline component](https://spacy.io/usage/processing-pipelines)
    for rule based USAS tagger.

    This component allows you to add [USAS semantic tags](http://ucrel.lancs.ac.uk/usas/)
    to each spaCy [Token](https://spacy.io/api/token), whereby these USAS tags
    have been predicted through the following [rules](#usasrulebasedtagger.rules), all of these rules depend on
    two Lexicon like data structures, the `lexicon_lookup` and the `lemma_lexicon_lookup`.
    Both of these lexicons are of type `Dict[str, List[str]]` which map a lemma
    (with or without it's Part Of Speech (POS) ) to a `List` of USAS tags. The
    first semantic tag in the `List` of tags is the most likely tag.

    Furthermore, the optional POS mapper, `pos_mapper`, is used in this tagger when the POS tagset
    within the lexicons does not match the tagset used by the POS model, which has
    preceding this tagger in the spaCy pipeline. The POS mapper is expected to
    map from the tagset of the POS model to the tagset of the lexicons, whereby the
    mapping is a one-to-many mapping. The first tag in the `List` is assumed to be the
    most relevant and the last to be the least. Some pre-compiled Dictionaries can be
    found in the :mod:`pymusas.pos_mapper` module, e.g. the UPOS to USAS
    core :var:`pymusas.pos_mapper.UPOS_TO_USAS_CORE`.
    
    # Rules

    1. **If `pos_mapper` is not `None`**, map the POS, from the POS model,
    to the first POS value in the `List` from the `pos_mapper`s `Dict`. **If** the
    `pos_mapper` cannot map the POS, from the POS model, go to step 9.
    2. If `POS==punc` label as `PUNCT`
    3. Lookup token and POS tag
    4. Lookup lemma and POS tag
    5. Lookup lower case token and POS tag
    6. Lookup lower case lemma and POS tag
    7. if `POS==num` label as `N1`
    8. **If there is another POS value in the `pos_mapper`** go back to step 2
    with this new POS value else carry on to step 9.
    9. Lookup token with any POS tag and choose first entry in lexicon.
    10. Lookup lemma with any POS tag and choose first entry in lexicon.
    11. Lookup lower case token with any POS tag and choose first entry in lexicon.
    12. Lookup lower case lemma with any POS tag and choose first entry in lexicon.
    13. Label as `Z99`, this is the unmatched semantic tag.

    **NOTE** this tagger has been designed to be flexible with the amount of
    resources avaliable, if you do not have a POS tagger in the spaCy pipeline
    it will not use POS information. If you do not have a lexicon file with
    POS information then `lexicon_lookup` will be an empty `Dict`. However, the fewer
    resources avaliable, less rules, stated above, will be applied making the
    tagger less effective.

    # Assigned Attributes

    The component assigns the predicted USAS tags to each spaCy [Token](https://spacy.io/api/token) under
    `Token._.usas_tags` attribute by default, this can be changed with the
    `usas_tags_token_attr` parameter to another attribute of
    the `Token._`, e.g. if `usas_tags_token_attr=semantic_tags` then the attribute
    the USAS tags will be assigned to for each token will be `Token._.semantic_tags`.

    | Location | Type | Value |
    |----------|------|-------|
    | Token._.usas_tags | `List[str]` | Prediced USAS tags, the first semantic tag in the List of tags is the most likely tag. |

    # Config and implementation

    The default config is defined by the pipeline component factory and describes
    how the component should be configured. You can override its settings via the `config`
    argument on [nlp.add_pipe](https://spacy.io/api/language#add_pipe) or in your
    [config.cfg for training](https://spacy.io/usage/training#config).

    | Setting | Description |
    |---------|-------------|
    | usas_tags_token_attr | See parameters section below |
    | pos_attribute | See parameters section below |
    | lemma_attribute | See parameters section below |

    # Parameters

    usas_tags_token_attr : `str`, optional (default = `usas_tags`)
        The name of the attribute to assign the predicted USAS tags too under
        the `Token._` class.
    
    pos_attribute : `str`, optional (default = `pos_`)
        The name of the attribute that the Part Of Speech (POS) tag is assigned too
        within the `Token` class. The POS tag value that comes from this attribute
        has to be of type `str`. With the current default we take the POS tag
        from `Token.pos_`
    
    lemma_attribute : `str`, optional (default = `lemma_`)
        The name of the attribute that the lemma is assigned too within the `Token`
        class. The lemma value that comes from this attribute has to be of
        type `str`. With the current default we take the lemma from `Token.lemma_`

    # Instance Attributes

    usas_tags_token_attr : `str`, optional (default = `usas_tags`)

    pos_attribute : `str`, optional (default = `pos_`)
    
    lemma_attribute : `str`, optional (default = `lemma_`)

    lexicon_lookup : `Dict[str, List[str]]`
        The lexicon data structure with both lemma and POS information mapped
        to a `List` of USAS semantic tags e.g. `{'Car|noun': ['Z2', 'Z1']}`.
        By default this is an empty `Dict`, but can be added to either by setting
        it, e.g. `self.leixcon_lookup={'Car|noun': ['Z1']}` or through adding to
        the existing dictionary, e.g. `self.lexicon_lookup['Car|noun'] = ['Z1']`

    lemma_lexicon_lookup : `Dict[str, List[str]]`
        The lexicon data structure with only lemma information mapped to a
        `List` of USAS semantic tags e.g. `{'Car': ['Z2', 'Z1']}`.
        By default this is an empty `Dict`, but can be added to either by setting
        it, e.g. `self.lemma_leixcon_lookup={'Car': ['Z1']}` or through adding to
        the existing dictionary, e.g. `self.lemma_lexicon_lookup['Car'] = ['Z1']`
    
    pos_mapper : `Dict[str, List[str]]`, optional (default = `None`)
        If not `None`, maps from the POS model tagset to the lexicon data POS
        tagset, whereby the mapping is a `List` of tags, the first in the list is
        assumed to be the most relevant and the last to be the least.

    # Examples

    ``` python
    >>> import spacy
    >>> from pymusas.spacy_api.taggers import rule_based
    >>> # Construction via spaCy pipeline
    >>> nlp = spacy.blank('en')
    >>> # Using default config
    >>> tagger = nlp.add_pipe('usas_tagger')
    >>> tagger.lemma_lexicon_lookup = {'car': ['Z1']}
    >>> token = nlp('car')
    >>> assert token[0]._.usas_tags == ['Z1']
    ...
    >>> # Construction from class, same defaults as the default config
    >>> from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
    >>> tagger = USASRuleBasedTagger()
    ...
    >>> # Custom config
    >>> custom_config = {'usas_tags_token_attr': 'semantic_tags'}
    >>> nlp = spacy.blank('en')
    >>> tagger = nlp.add_pipe('usas_tagger', config=custom_config)
    >>> tagger.lemma_lexicon_lookup = {'car': ['Z1']}
    >>> token = nlp('car')
    >>> assert token[0]._.semantic_tags == ['Z1']

    ```

    '''

    def __init__(self,
                 usas_tags_token_attr: str = 'usas_tags',
                 pos_attribute: str = 'pos_',
                 lemma_attribute: str = 'lemma_'
                 ) -> None:
        self.lexicon_lookup: Dict[str, List[str]] = {}
        self.lemma_lexicon_lookup: Dict[str, List[str]] = {}
        self.pos_mapper: Union[Dict[str, List[str]], None] = None
        
        self._usas_tags_token_attr = usas_tags_token_attr
        self._pos_attribute = pos_attribute
        self._lemma_attribute = lemma_attribute
        self._set_custom_token_extension(self._usas_tags_token_attr)
        
        # Dynamically assigns the token attribute this spaCy component
        # creates and requires. This is normally done in the
        # `spacy.language.Language.factory` decoration function.
        usas_factory_meta = Language.get_factory_meta('usas_tagger')
        usas_factory_meta.assigns = validate_attrs([f'token._.{self.usas_tags_token_attr}'])
        
        pos_required = self.pos_attribute
        if pos_required in ['pos_', 'tag_']:
            pos_required = pos_required[:-1]
        lemma_required = lemma_attribute
        if lemma_required == 'lemma_':
            lemma_required = 'lemma'
        usas_factory_meta.requires = validate_attrs([f'token.{lemma_required}',
                                                     f'token.{pos_required}'])

    @property
    def usas_tags_token_attr(self) -> str:
        return self._usas_tags_token_attr
    
    @usas_tags_token_attr.setter
    def usas_tags_token_attr(self, value: str) -> None:
        self._set_custom_token_extension(value)
        usas_factory_meta = Language.get_factory_meta('usas_tagger')
        usas_factory_meta.assigns = validate_attrs([f'token._.{value}'])
        self._usas_tags_token_attr = value

    @property
    def pos_attribute(self) -> str:
        return self._pos_attribute

    @pos_attribute.setter
    def pos_attribute(self, value: str) -> None:
        value_required = value
        if value_required in ['pos_', 'tag_']:
            value_required = value_required[:-1]
        value_required_to_remove = f'token.{self._pos_attribute}'
        if value_required_to_remove in ['token.pos_', 'token.tag_']:
            value_required_to_remove = value_required_to_remove[:-1]
        
        self._update_factory_attributes(value_required, value_required_to_remove)
        
        self._pos_attribute = value

    @property
    def lemma_attribute(self) -> str:
        return self._lemma_attribute

    @lemma_attribute.setter
    def lemma_attribute(self, value: str) -> None:
        value_required = value
        if value_required == 'lemma_':
            value_required = value_required[:-1]
        value_required_to_remove = f'token.{self._lemma_attribute}'
        if value_required_to_remove == 'token.lemma_':
            value_required_to_remove = value_required_to_remove[:-1]
        self._update_factory_attributes(value_required, value_required_to_remove)
        
        self._lemma_attribute = value
    
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
        for token in doc:
            text = token.text
            lemma = getattr(token, self.lemma_attribute)
            initital_pos = getattr(token, self.pos_attribute)
            pos = [initital_pos]
            if self.pos_mapper is not None:
                pos = self.pos_mapper.get(initital_pos, [])
            semantic_tags = _tag_token(text, lemma, pos,
                                       self.lexicon_lookup,
                                       self.lemma_lexicon_lookup)
            setattr(token._, self.usas_tags_token_attr, semantic_tags)
        return doc

    def initialize(self, get_examples: Optional[Callable[[], Iterable[Example]]] = None,
                   nlp: Optional[Language] = None,
                   lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                   lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,
                   pos_mapper: Optional[Dict[str, List[str]]] = None,
                   usas_tags_token_attr: str = 'usas_tags',
                   pos_attribute: str = 'pos_',
                   lemma_attribute: str = 'lemma_'
                   ) -> None:
        
        if lexicon_lookup is not None:
            self.lexicon_lookup = lexicon_lookup
        if lemma_lexicon_lookup is not None:
            self.lemma_lexicon_lookup = lemma_lexicon_lookup
        self.pos_mapper = pos_mapper
        self.usas_tags_token_attr = usas_tags_token_attr
        self.pos_attribute = pos_attribute
        self.lemma_attribute = lemma_attribute
    
    def to_bytes(self, *, exclude: Iterable[str] = SimpleFrozenList()) -> bytes:
        '''
        Serialises the USAS tagger's lexicon lookups and POS mapper to a bytestring.

        # Parameters

        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.
        
        # Returns

        `bytes`

        # Examples

        ```python
        >>> from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
        >>> tagger = USASRuleBasedTagger()
        >>> tagger_bytes = tagger.to_bytes()

        ```
        '''
        serialise = {}
        serialise["lexicon_lookup"] = srsly.msgpack_dumps(self.lexicon_lookup)
        serialise["lemma_lexicon_lookup"] = srsly.msgpack_dumps(self.lemma_lexicon_lookup)
        serialise["pos_mapper"] = srsly.msgpack_dumps(self.pos_mapper)
        return cast(bytes, srsly.msgpack_dumps(serialise))

    def from_bytes(self, bytes_data: bytes, *,
                   exclude: Iterable[str] = SimpleFrozenList()
                   ) -> "USASRuleBasedTagger":
        '''
        This modifies the USASRuleBasedTagger in place and returns it. It loads
        in the data from the given bytestring.

        The easiest way to generate a bytestring to load from is through the
        :func:`to_bytes` method.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.

        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        :class:`USASRuleBasedTagger`

        # Examples

        ```python
        >>> from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
        >>> custom_lexicon = {'example|noun': ['A1']}
        >>> tagger = USASRuleBasedTagger()
        >>> tagger.lexicon_lookup = custom_lexicon
        >>> tagger_bytes = tagger.to_bytes()
        >>> new_tagger = USASRuleBasedTagger()
        >>> _ = new_tagger.from_bytes(tagger_bytes)
        >>> assert new_tagger.lexicon_lookup == tagger.lexicon_lookup

        ```
        '''
        serialise_data = srsly.msgpack_loads(bytes_data)
        self.lexicon_lookup = srsly.msgpack_loads(serialise_data['lexicon_lookup'])
        self.lemma_lexicon_lookup = srsly.msgpack_loads(serialise_data['lemma_lexicon_lookup'])
        self.pos_mapper = srsly.msgpack_loads(serialise_data['pos_mapper'])
        return self
    
    def to_disk(self, path: Union[str, Path], *,
                exclude: Iterable[str] = SimpleFrozenList()
                ) -> None:
        '''
        Saves the follwing information, if it exists, to the given `path`, we assume the `path`
        is an existing directory.

        * `lexicon_lookup` -- as a JSON file at the following path `path/lexicon_lookup.json`
        * `lemma_lexicon_lookup` -- as a JSON file at the following path `path/lemma_lexicon_lookup.json`
        * `pos_mapper` -- as a JSON file at the following path `path/pos_mapper.json`

        # Parameters

        path : `Union[str, Path]`
            Path to an existing direcotry. Path may be either strings or `Path`-like objects.
        
        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        `None`

        # Examples

        ```python
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
        >>> tagger = USASRuleBasedTagger()
        >>> tagger.lexicon_lookup = {'example|noun': ['A1']}
        >>> with TemporaryDirectory() as temp_dir:
        ...     tagger.to_disk(temp_dir)
        ...     assert Path(temp_dir, 'lexicon_lookup.json').exists()
        ...     assert not Path(temp_dir, 'lemma_lexicon_lookup.json').exists()
        ...     assert not Path(temp_dir, 'pos_mapper.json').exists()

        ```
        '''
        component_folder = ensure_path(path)
        component_folder.mkdir(exist_ok=True)
        if self.lexicon_lookup:
            with Path(component_folder, 'lexicon_lookup.json').open('w', encoding='utf-8') as lexicon_file:
                lexicon_file.write(srsly.json_dumps(self.lexicon_lookup))
        if self.lemma_lexicon_lookup:
            with Path(component_folder, 'lemma_lexicon_lookup.json').open('w', encoding='utf-8') as lexicon_file:
                lexicon_file.write(srsly.json_dumps(self.lemma_lexicon_lookup))
        if self.pos_mapper is not None:
            with Path(component_folder, 'pos_mapper.json').open('w', encoding='utf-8') as pos_mapper_file:
                pos_mapper_file.write(srsly.json_dumps(self.pos_mapper))

    def from_disk(self, path: Union[str, Path], *,
                  exclude: Iterable[str] = SimpleFrozenList()
                  ) -> "USASRuleBasedTagger":
        '''
        Loads the following information in place and returns the USASRuleBasedTagger
        from the given `path`, we assume the `path` is an existing directory.
        None of the following information is required to exist and no error or
        debug information will be raised or outputted if it does not exist.

        * `lexicon_lookup` -- loads from the following path `path/lexicon_lookup.json`
        * `lemma_lexicon_lookup` --  loads from the following path `path/lemma_lexicon_lookup.json`
        * `pos_mapper` -- loads from the following path `path/pos_mapper.json`

        # Parameters

        path : `Union[str, Path]`
            Path to an existing direcotry. Path may be either strings or `Path`-like objects.
        
        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        :class:`USASRuleBasedTagger`

        # Examples

        ```python
        >>> from tempfile import TemporaryDirectory
        >>> from pymusas.spacy_api.taggers.rule_based import USASRuleBasedTagger
        >>> tagger = USASRuleBasedTagger()
        >>> tagger.lexicon_lookup = {'example|noun': ['A1']}
        >>> new_tagger = USASRuleBasedTagger()
        >>> with TemporaryDirectory() as temp_dir:
        ...     tagger.to_disk(temp_dir)
        ...     _ = new_tagger.from_disk(temp_dir)
        ...
        >>> assert new_tagger.lexicon_lookup == tagger.lexicon_lookup
        >>> assert new_tagger.pos_mapper is None

        ```

        '''
        component_folder = ensure_path(path)
        lexicon_file = Path(component_folder, 'lexicon_lookup.json')
        if lexicon_file.exists():
            with lexicon_file.open('r', encoding='utf-8') as lexicon_data:
                self.lexicon_lookup = srsly.json_loads(lexicon_data.read())
        lemma_lexicon_file = Path(component_folder, 'lemma_lexicon_lookup.json')
        if lemma_lexicon_file.exists():
            with lemma_lexicon_file.open('r', encoding='utf-8') as lemma_lexicon_data:
                self.lemma_lexicon_lookup = srsly.json_loads(lemma_lexicon_data.read())
        pos_mapper_file = Path(component_folder, 'pos_mapper.json')
        if pos_mapper_file.exists():
            with pos_mapper_file.open('r', encoding='utf-8') as pos_mapper_data:
                self.pos_mapper = srsly.json_loads(pos_mapper_data.read())
        return self
        
    @classmethod
    def _update_factory_attributes(cls, new_attribute_name: str,
                                   old_attribute_name: str) -> None:
        '''
        Updates the [spaCy Language required attributes meta information](https://spacy.io/api/language#factorymeta)
        for this component, by replacing the `old_attribute_name`
        with the `new_attribute_name`.

        # Parameters

        new_attribute_name : `str`
            The name of the new `token.{new_attribute_name}` attribute that is
            required for this component. An example, `pos`

        old_attribute_name : `str`
            The name of the `{old_attribute_name}` that is to be replaced with
            the `new_attribute_name`. An example, `token.tag`
        '''
        usas_factory_meta = Language.get_factory_meta('usas_tagger')
        required_attributes = copy.deepcopy(usas_factory_meta.requires)
        updated_attributes = [attribute for attribute in required_attributes
                              if attribute != old_attribute_name]
        updated_attributes.append(f'token.{new_attribute_name}')
        
        usas_factory_meta.requires = validate_attrs(updated_attributes)

    @classmethod
    def _set_custom_token_extension(cls, extension_name: str) -> None:
        '''
        Defines a custom attribute of the spaCy Token which becomes avaliable
        via `Token._.{extension_name}`. The difference between this and using the
        spaCy [Token.set_extension method](https://spacy.io/api/token#set_extension)
        is this method will check if the extension exists already and if so will force it
        through and output a log message that it has had to force this through.

        # Parameters

        extension_name : `str`
            Name of the custom attribute that will become avaliable through
            `Token._.{extension_name}`.
        '''
        if Token.has_extension(extension_name):
            old_extension = Token.get_extension(extension_name)
            Token.set_extension(extension_name, default=None, force=True)
            log_message = (f' Overwritten the spaCy Token extension `{extension_name}`'
                           ' which currently has the following (default, method, getter, setter):'
                           f'`{old_extension}`. And replacing it with the following:'
                           f'`{Token.get_extension(extension_name)}`'
                           '. This would only become a problem if the the two Tuples'
                           ' of four are different, if they are the same there is'
                           ' no problem.')
            logger.debug(log_message)
        else:
            Token.set_extension(extension_name, default=None)


@Language.factory("usas_tagger",
                  default_config={'usas_tags_token_attr': 'usas_tags',
                                  'pos_attribute': 'pos_',
                                  'lemma_attribute': 'lemma_'})
def make_usas_rule_based_tagger(nlp: Language, name: str,
                                usas_tags_token_attr: str,
                                pos_attribute: str,
                                lemma_attribute: str
                                ) -> USASRuleBasedTagger:
    return USASRuleBasedTagger(usas_tags_token_attr,
                               pos_attribute, lemma_attribute)
