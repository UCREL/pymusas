import json
from pathlib import Path
from typing import Any, Callable, Iterable, List, Optional, Union, cast

import spacy
from spacy.language import Language
from spacy.tokens import Doc
from spacy.training import Example
from spacy.util import SimpleFrozenList


try:
    import torch
    from transformers import AutoTokenizer, PreTrainedTokenizerBase
    from wsd_torch_models.bem import BEM
except ImportError:
    pass

from pymusas.file_utils import ensure_path
from pymusas.spacy_api.utils import set_custom_token_extension
from pymusas.utils import neural_extra_installed


class NeuralTagger(spacy.pipeline.pipe.Pipe):
    '''
    [spaCy pipeline component](https://spacy.io/usage/processing-pipelines)
    of the :class:`pymusas.taggers.neural.NeuralTagger`.

    The component creates a list of possible candidate semantic/sense tags for
    each token in the sequence, these tags are then assigned to
    `Token._.pymusas_tags` attribute in addition a `List` of token indexes
    indicating if the token is part of a Multi Word Expression (MWE) is assigned
    to the `Token._.pymusas_mwe_indexes`. **NOTE** at the moment
    only single word expressions are supported.

    The number of possible candidate tags for each token is determined by the
    `top_n` parameter, of which this is then stored in the `top_n` attribute.

    **Rule based exceptions**
    * If the token is only whitespace, e.g. ` `, `  \t ` , ` \n `, etc. then the tagger
      will return only one tag which will be the `Z9` tag and no other tags,
      even if `top_n` is greater than 1.

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
            <td> Predicted tags, the first tag in the List of tags is the
            most likely tag.</td>
        </tr>
        <tr>
            <td> Token._.pymusas_mwe_indexes </td>
            <td> `List[Tuple[int, int]]` </td>
            <td> Each `Tuple` indicates the start and end token index of the
            associated Multi Word Expression (MWE). If the `List` contains
            more than one `Tuple` then the MWE is discontinuous. For single word
            expressions the `List` will only contain 1 `Tuple` which will be
            (token_start_index, token_start_index + 1). **NOTE** at the moment
            only single word expressions are supported.</td>
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
    | top_n                    | See parameters section below |
    | device                   | See parameters section below |
    | tokenizer_kwargs         | See parameters section below |

    # Parameters

    name : `str`, optional (default = `pymusas_neural_tagger`)
        The component name. Defaults to the same name as the class variable
        `COMPONENT_NAME`.
    pymusas_tags_token_attr : `str`, optional (default = `pymusas_tags`)
        The name of the attribute to assign the predicted tags too under
        the `Token._` class.
    pymusas_mwe_indexes_attr : `str`, optional (default = `pymusas_mwe_indexes`)
        The name of the attribute to assign the start and end token index of the
        associated MWE too under the `Token._` class.
    top_n : `int`, optional (default = `5`)
        The number of tags to predict. If -1 all tags will be predicted.
        If 0 or less than 0 will raise a ValueError.
    device : `str`, optional (default = `'cpu'`)
        The device to load the model, `wsd_model`, on. e.g. `'cpu'`, it has to
        be a string that can be passed to
        [`torch.device`](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device).
    tokenizer_kwargs : `dict[str, Any] | None` (default = `None`)
        Keyword arguments to pass to the tokenizer's
        `transformers.AutoTokenizer.from_pretrained` method.
        These keyword arguments are only passed to the tokenizer on initialization.
        **NOTE** any value that is a custom object will not be serializable
        with the `to_bytes` and `from_bytes` when these methods have been
        implemented. If you save this component to disk when it is loaded
        this will become `None` as the tokenizer itself `self.tokenizer` will
        contain the the contents of `tokenizer_kwargs`.

    # Instance Attributes

    name : `str`
        The component name.
    pymusas_tags_token_attr : `str`, optional (default = `pymusas_tags`)
        The given `pymusas_tags_token_attr`
    pymusas_mwe_indexes_attr : `str`, optional (default = `pymusas_mwe_indexes`)
        The given `pymusas_mwe_indexes_attr`
    top_n : `int`, optional (default = `5`)
        The number of tags to predict. If -1 all tags will be predicted.
        If 0 or less than 0 will raise a ValueError.
    device : `torch.device`
        The device that the `wsd_model` will be loaded on. e.g. `torch.device`
    wsd_model : `wsd_torch_models.bem.BEM | None` (default = `None`)
        The neural Word Sense Disambiguation (WSD) model. This is `None` until
        the component is initialized or has been loaded from disk or bytes.
    tokenizer : `transformers.PreTrainedTokenizerBase | None` (default = `None`)
        The sub-word tokenizer that the `wsd_model` uses. This tokenizer
        further tokenizes the tokens from the spaCy tokenizer, hence it being a
        sub-word tokenizer. This is `None` until the component is initialized
        or has been loaded from disk or bytes.
    _tokenizer_kwargs : `dict[str, Any] | None` (default = `None`)
        The keyword arguments that have
        or will be passed to the tokenizer's `transformers.AutoTokenizer.from_pretrained`
        method. These keyword arguments are only passed to the tokenizer on
        initialization.

    # Class Attributes

    COMPONENT_NAME : `str`
        Name of component factory that this component is registered under. This
        is used as the first argument to
        [`Language.add_pipe`](https://spacy.io/api/language#add_pipe)
        if you want to add this component to your spaCy pipeline.

    # Raises
    
    `ValueError`
        If `top_n` is 0 or less than -1.

    # Examples

    ``` python
    >>> import spacy
    >>> from pymusas.spacy_api.taggers.neural import NeuralTagger
    >>> # Construction via spaCy pipeline
    >>> nlp = spacy.blank('en')
    >>> # Using default config
    >>> tagger = nlp.add_pipe('pymusas_neural_tagger')
    >>> tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
    >>> token = nlp('Hello')
    >>> assert token[0]._.pymusas_tags == ['Q2.2', 'Z4', 'Q2', 'X3.2', 'Q2.1']
    >>> assert token[0]._.pymusas_mwe_indexes == [(0, 1)]
    >>> # Custom config
    >>> custom_config = {'pymusas_tags_token_attr': 'semantic_tags',
    ...                  'pymusas_mwe_indexes_attr': 'mwe_indexes',
    ...                  'top_n': 2,
    ...                  'tokenizer_kwargs': {'add_prefix_space': True}}
    >>> nlp = spacy.blank('en')
    >>> tagger = nlp.add_pipe('pymusas_neural_tagger', config=custom_config)
    >>> tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
    >>> token = nlp('Hello')
    >>> assert token[0]._.semantic_tags == ['Q2.2', 'Z4']
    >>> assert token[0]._.mwe_indexes == [(0, 1)]

    ```
    '''
    COMPONENT_NAME = 'pymusas_neural_tagger'

    def __init__(self,
                 name: str = 'pymusas_neural_tagger',
                 pymusas_tags_token_attr: str = 'pymusas_tags',
                 pymusas_mwe_indexes_attr: str = 'pymusas_mwe_indexes',
                 top_n: int = 5,
                 device: str = 'cpu',
                 tokenizer_kwargs: dict[str, Any] | None = None
                 ) -> None:
        neural_extra_installed()

        if top_n == 0 or top_n < -1:
            raise ValueError(f"The top_n argument cannot be {top_n}, has to be either "
                             "-1 or a positive integer > 0.")
        self.name = name
        
        self._pymusas_tags_token_attr = pymusas_tags_token_attr
        set_custom_token_extension(pymusas_tags_token_attr)

        self._pymusas_mwe_indexes_attr = pymusas_mwe_indexes_attr
        set_custom_token_extension(pymusas_mwe_indexes_attr)
        
        self._tokenizer_kwargs = tokenizer_kwargs
        self.top_n = top_n
        self.device = torch.device(device)

        self.wsd_model: BEM | None = None
        self.tokenizer: PreTrainedTokenizerBase | None = None
        
        self._validated = False

    def _validate(self) -> None:
        '''
        Checks that `self.wsd_model` and `self.tokenizer` are not `None`.

        In addition if the `self.wsd_model` is not loaded onto `self.device`,
        the model is loaded onto `self.device`.

        # Raises

        `ValueError`
            If `self.wsd_model` or `self.tokenizer` are `None`
        '''
        error_msg = ('The `{}` attribute cannot be `None`, this '
                     'attribute can be set through the `initialize` method.')
        if self.wsd_model is None:
            raise ValueError(error_msg.format('wsd_model'))
        
        if self.tokenizer is None:
            raise ValueError(error_msg.format('tokenizer'))
        
        self.wsd_model = cast(BEM, self.wsd_model)
        if self.wsd_model.base_model.device != self.device:
            self.wsd_model.to(self.device)

        self._validated = True
    
    def initialize(self,
                   get_examples: Optional[Callable[[], Iterable[Example]]] = None,
                   *,
                   nlp: Optional[Language] = None,
                   pretrained_model_name_or_path: Optional[str | Path] = None,
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
        
        pretrained_model_name_or_path : `str | Path`
            The string ID or path of the pretrained neural
            Word Sense Disambiguation (WSD) model to load.

            **NOTE:** currently we only support the
            [wsd_torch_models.bem.BEM model](https://github.com/UCREL/WSD-Torch-Models/blob/main/src/wsd_torch_models/bem.py#L29)
        
            * A string, the model id of a pretrained
            [wsd-torch-models](https://github.com/UCREL/WSD-Torch-Models/tree/main)
            that is hosted on the HuggingFace Hub.
            * A `Path` or `str` that is a directory that can be loaded
            through `from_pretrained` method from a
            [wsd-torch-models model](https://github.com/UCREL/WSD-Torch-Models/tree/main)

            **NOTE:** this model name or path has to also be able to load the tokenizer
            using the function `transformers.AutoTokenizer.from_pretrained(pretrained_model_name_or_path)`
        '''
        neural_extra_installed()
        if pretrained_model_name_or_path is not None:
            self.wsd_model = BEM.from_pretrained(pretrained_model_name_or_path)
            tokenizer_kwargs = {}
            if self._tokenizer_kwargs is not None:
                tokenizer_kwargs = self._tokenizer_kwargs
            tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path,  # type: ignore
                                                      **tokenizer_kwargs)
            assert isinstance(tokenizer, PreTrainedTokenizerBase)
            self.tokenizer = tokenizer
        
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
        self.tokenizer = cast(PreTrainedTokenizerBase, self.tokenizer)
        self.wsd_model = cast(BEM, self.wsd_model)
        
        # Try, catch error handling reference:
        # https://github.com/explosion/spaCy/blob/6af6c2e86cc7b08573b261563786bd1ab87d45e9/spacy/pipeline/lemmatizer.py#L131
        error_handler = self.get_error_handler()
        try:
            tokens: List[str] = []
            for token in doc:
                tokens.append(token.text)

            predicted_tags_candidates = self.wsd_model.predict(tokens,
                                                               sub_word_tokenizer=self.tokenizer,
                                                               top_n=self.top_n)
            for token_index, predicted_tag_candidates in enumerate(predicted_tags_candidates):
                start_end_index = [(token_index, token_index + 1)]
                assigned_tags = predicted_tag_candidates
                if tokens[token_index].strip() == "":
                    assigned_tags = ["Z9"]
                
                token = doc[token_index]
                setattr(token._, self.pymusas_tags_token_attr, assigned_tags)
                setattr(token._, self.pymusas_mwe_indexes_attr, start_end_index)
        except Exception as e:
            error_handler(self.name, self, [doc], e)
        
        return doc

    def to_disk(self,
                path: Union[str, Path],
                *,
                exclude: Iterable[str] = SimpleFrozenList()
                ) -> None:
        '''
        Serialises the tagger to the given `path`.

        # Parameters

        path : `Union[str, Path]`
            Path to a directory. Path may be either string or `Path`-like
            object. If the directory does not exist it attempts to create a
            directory at the given `path`.
        
        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        `None`

        # Examples

        ```python
        >>> from tempfile import TemporaryDirectory
        >>> from pymusas.spacy_api.taggers.neural import NeuralTagger
        >>> tagger = NeuralTagger()
        >>> tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
        >>> with TemporaryDirectory() as temp_dir:
        ...     _ = tagger.to_disk(temp_dir)
        ...

        ```
        '''
        if not self._validated:
            self._validate()
        tokenizer = cast(PreTrainedTokenizerBase, self.tokenizer)
        wsd_model = cast(BEM, self.wsd_model)

        component_folder = ensure_path(path)
        component_folder.mkdir(exist_ok=True)

        model_path = component_folder / "model"
        wsd_model.save_pretrained(model_path, push_to_hub=False)
        
        # This I believe is an error in the HuggingFace Hub library
        # as a similar issue did exist but for the key `revision`
        # https://github.com/huggingface/huggingface_hub/issues/1313
        # This is a workaround.
        wsd_model_config_path = model_path / "config.json"
        wsd_model_config_data: dict[str, Any] = {}
        changed_config = False
        with wsd_model_config_path.open("r", encoding="utf8") as read_fp:
            wsd_model_config_data = json.load(read_fp)
            config_entries_to_delete = ["proxies", "resume_download"]
            for config_entry_to_delete in config_entries_to_delete:
                if config_entry_to_delete in wsd_model_config_data:
                    del wsd_model_config_data[config_entry_to_delete]
                    changed_config = True
        if changed_config:
            with wsd_model_config_path.open("w", encoding="utf8") as write_fp:
                json.dump(wsd_model_config_data, write_fp)

        tokenizer_path = component_folder / "tokenizer"
        tokenizer.save_pretrained(tokenizer_path, push_to_hub=False)

    def from_disk(self,
                  path: Union[str, Path],
                  *,
                  exclude: Iterable[str] = SimpleFrozenList()
                  ) -> "NeuralTagger":
        '''
        Loads the tagger from the given `path` in place and returns it.

        # Parameters

        path : `Union[str, Path]`
            Path to an existing directory. Path may be either string or
            `Path`-like object.
        
        exclude : `Iterable[str]`, optional (default = `SimpleFrozenList()`)
            This currently does not do anything, please ignore it.

        # Returns

        :class:`NeuralTagger`

        # Examples

        ```python
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> from pymusas.spacy_api.taggers.neural import NeuralTagger
        >>> tagger = NeuralTagger()
        >>> tagger_2 = NeuralTagger()
        >>> assert tagger_2.wsd_model is None
        >>> tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
        >>> with TemporaryDirectory() as temp_dir:
        ...     _ = tagger.to_disk(temp_dir)
        ...     _ = tagger_2.from_disk(temp_dir)
        ...

        ```

        '''
        neural_extra_installed()
        component_folder = ensure_path(path)
        
        model_path = component_folder / "model"
        self.wsd_model = BEM.from_pretrained(model_path)

        tokenizer_path = component_folder / "tokenizer"
        self.tokenizer = cast(PreTrainedTokenizerBase,
                              AutoTokenizer.from_pretrained(tokenizer_path))  # type: ignore[no-untyped-call]

        self._validate()
        return self
        
    @property
    def pymusas_tags_token_attr(self) -> str:
        return self._pymusas_tags_token_attr

    @property
    def pymusas_mwe_indexes_attr(self) -> str:
        return self._pymusas_mwe_indexes_attr


@Language.factory(NeuralTagger.COMPONENT_NAME,
                  assigns=['token._.pymusas_tags', 'token._.pymusas_mwe_indexes'],
                  default_config={'pymusas_tags_token_attr': 'pymusas_tags',
                                  'pymusas_mwe_indexes_attr': 'pymusas_mwe_indexes',
                                  'top_n': 5,
                                  'device': 'cpu',
                                  'tokenizer_kwargs': None})
def make_usas_neural_tagger(nlp: Language,
                            name: str,
                            pymusas_tags_token_attr: str,
                            pymusas_mwe_indexes_attr: str,
                            top_n: int,
                            device: str,
                            tokenizer_kwargs: None | dict[str, Any]
                            ) -> NeuralTagger:
    return NeuralTagger(name,
                        pymusas_tags_token_attr,
                        pymusas_mwe_indexes_attr,
                        top_n,
                        device,
                        tokenizer_kwargs)
