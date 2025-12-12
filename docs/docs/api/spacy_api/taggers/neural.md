<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><i>.taggers</i><strong>.neural</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/taggers/neural.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.spacy_api.taggers.neural.NeuralTagger"></a>

## NeuralTagger

```python
class NeuralTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def __init__(
 |     self,
 |     name: str = 'pymusas_neural_tagger',
 |     pymusas_tags_token_attr: str = 'pymusas_tags',
 |     pymusas_mwe_indexes_attr: str = 'pymusas_mwe_indexes',
 |     top_n: int = 5,
 |     device: str = 'cpu',
 |     tokenizer_kwargs: dict[str, Any] | None = None
 | ) -> None
```

[spaCy pipeline component](https://spacy.io/usage/processing-pipelines)
of the [`pymusas.taggers.neural.NeuralTagger`](/pymusas/api/taggers/neural/#neuraltagger).

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

<h4 id="neuraltagger.assigned_attributes">Assigned Attributes<a className="headerlink" href="#neuraltagger.assigned_attributes" title="Permanent link">&para;</a></h4>


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

<h4 id="neuraltagger.config_and_implementation">Config and implementation<a className="headerlink" href="#neuraltagger.config_and_implementation" title="Permanent link">&para;</a></h4>


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

<h4 id="neuraltagger.parameters">Parameters<a className="headerlink" href="#neuraltagger.parameters" title="Permanent link">&para;</a></h4>


- __name__ : `str`, optional (default = `pymusas_neural_tagger`) <br/>
    The component name. Defaults to the same name as the class variable
    `COMPONENT_NAME`.
- __pymusas\_tags\_token\_attr__ : `str`, optional (default = `pymusas_tags`) <br/>
    The name of the attribute to assign the predicted tags too under
    the `Token._` class.
- __pymusas\_mwe\_indexes\_attr__ : `str`, optional (default = `pymusas_mwe_indexes`) <br/>
    The name of the attribute to assign the start and end token index of the
    associated MWE too under the `Token._` class.
- __top\_n__ : `int`, optional (default = `5`) <br/>
    The number of tags to predict. If -1 all tags will be predicted.
    If 0 or less than 0 will raise a ValueError.
- __device__ : `str`, optional (default = `'cpu'`) <br/>
    The device to load the model, `wsd_model`, on. e.g. `'cpu'`, it has to
    be a string that can be passed to
    [`torch.device`](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device).
- __tokenizer\_kwargs__ : `dict[str, Any] | None`, optional (default = `None`) <br/>
    Keyword arguments to pass to the tokenizer's
    `transformers.AutoTokenizer.from_pretrained` method.
    These keyword arguments are only passed to the tokenizer on initialization.
    **NOTE** any value that is a custom object will not be serializable
    with the `to_bytes` and `from_bytes` when these methods have been
    implemented. If you save this component to disk when it is loaded
    this will become `None` as the tokenizer itself `self.tokenizer` will
    contain the the contents of `tokenizer_kwargs`.

<h4 id="neuraltagger.instance_attributes">Instance Attributes<a className="headerlink" href="#neuraltagger.instance_attributes" title="Permanent link">&para;</a></h4>


- __name__ : `str` <br/>
    The component name.
- __pymusas\_tags\_token\_attr__ : `str`, optional (default = `pymusas_tags`) <br/>
    The given `pymusas_tags_token_attr`
- __pymusas\_mwe\_indexes\_attr__ : `str`, optional (default = `pymusas_mwe_indexes`) <br/>
    The given `pymusas_mwe_indexes_attr`
- __top\_n__ : `int`, optional (default = `5`) <br/>
    The number of tags to predict. If -1 all tags will be predicted.
    If 0 or less than 0 will raise a ValueError.
- __device__ : `torch.device` <br/>
    The device that the `wsd_model` will be loaded on. e.g. `torch.device`
- __wsd\_model__ : `wsd_torch_models.bem.BEM | None`, optional (default = `None`) <br/>
    The neural Word Sense Disambiguation (WSD) model. This is `None` until
    the component is initialized or has been loaded from disk or bytes.
- __tokenizer__ : `transformers.PreTrainedTokenizerBase | None`, optional (default = `None`) <br/>
    The sub-word tokenizer that the `wsd_model` uses. This tokenizer
    further tokenizes the tokens from the spaCy tokenizer, hence it being a
    sub-word tokenizer. This is `None` until the component is initialized
    or has been loaded from disk or bytes.
- __\_tokenizer\_kwargs__ : `dict[str, Any] | None`, optional (default = `None`) <br/>
    The keyword arguments that have
    or will be passed to the tokenizer's `transformers.AutoTokenizer.from_pretrained`
    method. These keyword arguments are only passed to the tokenizer on
    initialization.

<h4 id="neuraltagger.class_attributes">Class Attributes<a className="headerlink" href="#neuraltagger.class_attributes" title="Permanent link">&para;</a></h4>


- __COMPONENT\_NAME__ : `str` <br/>
    Name of component factory that this component is registered under. This
    is used as the first argument to
    [`Language.add_pipe`](https://spacy.io/api/language#add_pipe)
    if you want to add this component to your spaCy pipeline.

<h4 id="neuraltagger.raises">Raises<a className="headerlink" href="#neuraltagger.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If `top_n` is 0 or less than -1.

<h4 id="neuraltagger.examples">Examples<a className="headerlink" href="#neuraltagger.examples" title="Permanent link">&para;</a></h4>


``` python
import spacy
from pymusas.spacy_api.taggers.neural import NeuralTagger
# Construction via spaCy pipeline
nlp = spacy.blank('en')
# Using default config
tagger = nlp.add_pipe('pymusas_neural_tagger')
tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
token = nlp('Hello')
assert token[0]._.pymusas_tags == ['Q2.2', 'Z4', 'Q2', 'X3.2', 'Q2.1']
assert token[0]._.pymusas_mwe_indexes == [(0, 1)]
# Custom config
custom_config = {'pymusas_tags_token_attr': 'semantic_tags',
                 'pymusas_mwe_indexes_attr': 'mwe_indexes',
                 'top_n': 2,
                 'tokenizer_kwargs': {'add_prefix_space': True}}
nlp = spacy.blank('en')
tagger = nlp.add_pipe('pymusas_neural_tagger', config=custom_config)
tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
token = nlp('Hello')
assert token[0]._.semantic_tags == ['Q2.2', 'Z4']
assert token[0]._.mwe_indexes == [(0, 1)]
```

<a id="pymusas.spacy_api.taggers.neural.NeuralTagger.COMPONENT_NAME"></a>

#### COMPONENT\_NAME

```python
class NeuralTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | COMPONENT_NAME = 'pymusas_neural_tagger'
```

<a id="pymusas.spacy_api.taggers.neural.NeuralTagger.initialize"></a>

### initialize

```python
class NeuralTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def initialize(
 |     self,
 |     get_examples: Optional[Callable[[], Iterable[Example]]] = None,
 |     *,
 |     nlp: Optional[Language] = None,
 |     pretrained_model_name_or_path: Optional[str | Path] = None
 | ) -> None
```

Initialize the tagger and load any of the resources given. The method is
typically called by
[`Language.initialize`](https://spacy.io/api/language#initialize)
and lets you customize arguments it receives via the
[`initialize.components`](https://spacy.io/api/data-formats#config-initialize)
block in the config. The loading only happens during initialization,
typically before training. At runtime, all data is load from disk.

<h4 id="initialize.parameters">Parameters<a className="headerlink" href="#initialize.parameters" title="Permanent link">&para;</a></h4>


- __pretrained\_model\_name\_or\_path__ : `str | Path` <br/>
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

<a id="pymusas.spacy_api.taggers.neural.NeuralTagger.__call__"></a>

### \_\_call\_\_

```python
class NeuralTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def __call__(doc: Doc) -> Doc
```

Applies the tagger to the spaCy document, modifies it in place, and
returns it. This usually happens under the hood when the `nlp` object is
called on a text and all pipeline components are applied to the `Doc` in
order.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __doc__ : `Doc` <br/>
    A [spaCy `Doc`](https://spacy.io/api/doc)

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `Doc` <br/>

<a id="pymusas.spacy_api.taggers.neural.NeuralTagger.to_disk"></a>

### to\_disk

```python
class NeuralTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def to_disk(
 |     self,
 |     path: Union[str, Path],
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> None
```

Serialises the tagger to the given `path`.

<h4 id="to_disk.parameters">Parameters<a className="headerlink" href="#to_disk.parameters" title="Permanent link">&para;</a></h4>


- __path__ : `Union[str, Path]` <br/>
    Path to a directory. Path may be either string or `Path`-like
    object. If the directory does not exist it attempts to create a
    directory at the given `path`.

- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="to_disk.returns">Returns<a className="headerlink" href="#to_disk.returns" title="Permanent link">&para;</a></h4>


- `None` <br/>

<h4 id="to_disk.examples">Examples<a className="headerlink" href="#to_disk.examples" title="Permanent link">&para;</a></h4>


```python
from tempfile import TemporaryDirectory
from pymusas.spacy_api.taggers.neural import NeuralTagger
tagger = NeuralTagger()
tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
with TemporaryDirectory() as temp_dir:
    _ = tagger.to_disk(temp_dir)

```

<a id="pymusas.spacy_api.taggers.neural.NeuralTagger.from_disk"></a>

### from\_disk

```python
class NeuralTagger(spacy.pipeline.pipe.Pipe):
 | ...
 | def from_disk(
 |     self,
 |     path: Union[str, Path],
 |     *,
 |     exclude: Iterable[str] = SimpleFrozenList()
 | ) -> "NeuralTagger"
```

Loads the tagger from the given `path` in place and returns it.

<h4 id="from_disk.parameters">Parameters<a className="headerlink" href="#from_disk.parameters" title="Permanent link">&para;</a></h4>


- __path__ : `Union[str, Path]` <br/>
    Path to an existing directory. Path may be either string or
    `Path`-like object.

- __exclude__ : `Iterable[str]`, optional (default = `SimpleFrozenList()`) <br/>
    This currently does not do anything, please ignore it.

<h4 id="from_disk.returns">Returns<a className="headerlink" href="#from_disk.returns" title="Permanent link">&para;</a></h4>


- [`NeuralTagger`](#neuraltagger) <br/>

<h4 id="from_disk.examples">Examples<a className="headerlink" href="#from_disk.examples" title="Permanent link">&para;</a></h4>


```python
from pathlib import Path
from tempfile import TemporaryDirectory
from pymusas.spacy_api.taggers.neural import NeuralTagger
tagger = NeuralTagger()
tagger_2 = NeuralTagger()
assert tagger_2.wsd_model is None
tagger.initialize(pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
with TemporaryDirectory() as temp_dir:
    _ = tagger.to_disk(temp_dir)
    _ = tagger_2.from_disk(temp_dir)

assert tagger_2.wsd_model.base_model_name == tagger.wsd_model.base_model_name
```

