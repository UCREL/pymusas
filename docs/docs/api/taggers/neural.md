<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><strong>.neural</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/neural.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.neural.NeuralTagger"></a>

## NeuralTagger

```python
class NeuralTagger:
 | ...
 | def __init__(
 |     self,
 |     pretrained_model_name_or_path: str | Path,
 |     top_n: int = -1,
 |     device: str = 'cpu',
 |     tokenizer_kwargs: dict[str, Any] | None = None
 | ) -> None
```

The tagger when called, through [`__call__`](#__call__), and given a sequence of
tokens, to create a list of possible candidate tags for each token in the sequence.

**NOTE** at the moment only single word expressions are supported.

The number of possible candidate tags for each token is determined by the
`top_n` parameter, of which this is then stored in the `top_n` attribute.

**Rule based exceptions**
* If the token is only whitespace, e.g. ` `, `  \t ` , ` \n `, etc. then the tagger
  will return only one tag which will be the `Z9` tag and no other tags,
  even if `top_n` is greater than 1.

<h4 id="neuraltagger.parameters">Parameters<a className="headerlink" href="#neuraltagger.parameters" title="Permanent link">&para;</a></h4>


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
- __top\_n__ : `int`, optional (default = `-1`) <br/>
    The number of tags to predict. Default -1 which
    predicts all tags. If 0 will raise a ValueError.
- __device__ : `str`, optional (default = `'cpu'`) <br/>
    The device to load the model on. e.g. `'cpu'`, it has to be a string
    that can be passed to
    [`torch.device`](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device).
- __tokenizer\_kwargs__ : `dict[str, Any] | None`, optional (default = `None`) <br/>
    Keyword arguments to pass to the tokenizer's
    `transformers.AutoTokenizer.from_pretrained` method.
    These keyword arguments are only passed to the tokenizer on initialization.

<h4 id="neuraltagger.instance_attributes">Instance Attributes<a className="headerlink" href="#neuraltagger.instance_attributes" title="Permanent link">&para;</a></h4>


- __wsd\_model__ : `wsd_torch_models.bem.BEM` <br/>
    The neural Word Sense Disambiguation (WSD) model that was loaded using
    the `pretrained_model_name_or_path`.
- __tokenizer__ : `transformers.PreTrainedTokenizerBase` <br/>
    The tokenizer that was loaded using the `pretrained_model_name_or_path`.
- __top\_n__ : `int` <br/>
    The number of tags to predict.
- __device__ : `torch.device` <br/>
    The device that the `wsd_model` was loaded on. e.g. `torch.device`
tokenizer_kwargs (dict[str, Any] | None): Keyword arguments to pass
    to the tokenizer's `transformers.AutoTokenizer.from_pretrained` method.
    Default None.

<h4 id="neuraltagger.raises">Raises<a className="headerlink" href="#neuraltagger.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If `top_n` is 0 or less than -1.

<h4 id="neuraltagger.examples">Examples<a className="headerlink" href="#neuraltagger.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.taggers.neural import NeuralTagger
tokenizer_kwargs = {"add_prefix_space": True}
neural_tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
                             device="cpu", top_n=2, tokenizer_kwargs=tokenizer_kwargs)
tokens = ["The", "river", "bank", "was", "full", "of", "fish", "   "]
tags_and_indices = neural_tagger(tokens)
expected_tags = [["Z5", "N5"], ["M4", "W3"], ["M4", "W3"], ["A3", "Z5"],
                 ["N5.1", "I3.2"], ["Z5", "N5"], ["L2", "F1"], ["Z9"]]
expected_tag_indices = [[(0, 1)], [(1, 2)], [(2, 3)], [(3, 4)],
                        [(4, 5)], [(5, 6)], [(6, 7)], [(7, 8)]]
assert tags_and_indices == list(zip(expected_tags, expected_tag_indices))
```

<a id="pymusas.taggers.neural.NeuralTagger.__call__"></a>

### \_\_call\_\_

```python
class NeuralTagger:
 | ...
 | @torch.inference_mode(mode=True)
 | def __call__(
 |     self,
 |     tokens: List[str]
 | ) -> List[Tuple[List[str], List[Tuple[int, int]]]]
```

Given a `List` of tokens it returns for each token:

1. A `List` of tags. The first tag in the `List` of tags is the most likely tag.
2. A `List` of `Tuples` whereby each `Tuple` indicates the start and end
token index of the associated Multi Word Expression (MWE). If the `List` contains
more than one `Tuple` then the MWE is discontinuous. For single word
expressions the `List` will only contain 1 `Tuple` which will be
(token_start_index, token_start_index + 1).

NOTE: we recommend that the number of tokens in the list should represent
a sentence, in addition the more tokens in the list the more
memory the model requires and on CPU at least the more time it will
take to predict the tags.

NOTE: Currently the Neural Tagger is limited to only tagging single word
expressions.

This function is wrapped in a
[`torch.inference_model`](https://docs.pytorch.org/docs/stable/generated/torch.autograd.grad_mode.inference_mode.html)
decorator which makes the model run more efficiently.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `List[str]` <br/>
    A List of full text form of the tokens to be tagged.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[Tuple[List[str], List[Tuple[int, int]]]]` <br/>

<h4 id="__call__.raises">Raises<a className="headerlink" href="#__call__.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    If the number of tokens given is not the same as the number of tags
    predicted/returned.

