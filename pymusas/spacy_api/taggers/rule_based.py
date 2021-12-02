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
        
        if Token.has_extension(self.usas_tags_token_attr):
            old_extension = Token.get_extension(self.usas_tags_token_attr)
            Token.set_extension(self.usas_tags_token_attr, default=None, force=True)
            log_message = (f' Overwritten the spaCy Token extension `{self.usas_tags_token_attr}`'
                           ' which currently has the following (default, method, getter, setter):'
                           f'`{old_extension}`. And replacing it with the following:'
                           f'`{Token.get_extension(self.usas_tags_token_attr)}`'
                           '. This would only become a problem if the the two Tuples'
                           ' of four are different, if they are the same there is'
                           ' no problem.')
            logger.debug(log_message)
        else:
            Token.set_extension(self.usas_tags_token_attr, default=None)
        
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
        usas_factory_meta.requires = [f'token.{lemma_required}',
                                      f'token.{pos_required}']

    @property
    def usas_tags_token_attr(self) -> str:
        return self._usas_tags_token_attr
    
    @usas_tags_token_attr.setter
    def usas_tags_token_attr(self, value: str) -> None:
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
    def _update_factory_attributes(cls, new_attribute_name: str, old_attribute_name: str) -> None:
        usas_factory_meta = Language.get_factory_meta('usas_tagger')
        required_attributes = copy.deepcopy(usas_factory_meta.requires)
        updated_attributes = [attribute for attribute in required_attributes
                              if attribute != old_attribute_name]
        updated_attributes.append(f'token.{new_attribute_name}')
        
        usas_factory_meta.requires = updated_attributes


@Language.factory("usas_tagger")
def make_usas_rule_based_tagger(nlp: Language, name: str,
                                usas_tags_token_attr: str = 'usas_tags',
                                pos_attribute: str = 'pos_',
                                lemma_attribute: str = 'lemma_'
                                ) -> USASRuleBasedTagger:
    return USASRuleBasedTagger(usas_tags_token_attr,
                               pos_attribute, lemma_attribute)
