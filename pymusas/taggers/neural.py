from pathlib import Path
from typing import Any, List, Tuple

import torch
from transformers import AutoTokenizer, PreTrainedTokenizerBase
from wsd_torch_models.bem import BEM


class NeuralTagger():
    '''
    The tagger when called, through :func:`__call__`, and given a sequence of
    tokens, to create a list of possible candidate tags for each token in the sequence.

    The number of possible candidate tags for each token is determined by the
    `top_n` parameter, of which this is then stored in the `top_n` attribute.

    **Rule based exceptions**
    * If the token is only whitespace, e.g. ` `, `  \t ` , ` \n `, etc. then the tagger
      will return only one tag which will be the `Z9` tag and no other tags,
      even if `top_n` is greater than 1.

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
    top_n : `int`, optional (default = `-1`)
        The number of tags to predict. Default -1 which
        predicts all tags. If 0 will raise a ValueError.
    device : `str`, optional (default = `'cpu'`)
        The device to load the model on. e.g. `'cpu'`, it has to be a string
        that can be passed to
        [`torch.device`](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device).
    
    # Instance Attributes

    wsd_model : `wsd_torch_models.bem.BEM`
        The neural Word Sense Disambiguation (WSD) model that was loaded using
        the `pretrained_model_name_or_path`.
    tokenizer : `transformers.PreTrainedTokenizerBase`
        The tokenizer that was loaded using the `pretrained_model_name_or_path`.
    top_n : `int`
        The number of tags to predict.
    device : `torch.device`
        The device that the `wsd_model` was loaded on. e.g. `torch.device`
    tokenizer_kwargs (dict[str, Any] | None): Keyword arguments to pass
        to the tokenizer's `transformers.AutoTokenizer.from_pretrained` method.
        Default None.

    # Raises
    
    `ValueError`
        If `top_n` is 0 or less than -1.

    # Examples
    ``` python
    >>> from pymusas.taggers.neural import NeuralTagger
    >>> tokenizer_kwargs = {"add_prefix_space": True}
    >>> neural_tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
    ...                              device="cpu", top_n=2, tokenizer_kwargs=tokenizer_kwargs)
    >>> tokens = ["The", "river", "bank", "was", "full", "of", "fish", "   "]
    >>> tags_and_indices = neural_tagger(tokens)
    >>> expected_tags = [["Z5", "N5"], ["M4", "W3"], ["M4", "W3"], ["A3", "Z5"],
    ...                  ["N5.1", "I3.2"], ["Z5", "N5"], ["L2", "F1"], ["Z9"]]
    >>> expected_tag_indices = [[(0, 1)], [(1, 2)], [(2, 3)], [(3, 4)],
    ...                         [(4, 5)], [(5, 6)], [(6, 7)], [(7, 8)]]
    >>> assert tags_and_indices == list(zip(expected_tags, expected_tag_indices))

    ```
    '''

    def __init__(self,
                 pretrained_model_name_or_path: str | Path,
                 top_n: int = -1,
                 device: str = 'cpu',
                 tokenizer_kwargs: dict[str, Any] | None = None) -> None:
        
        if top_n == 0 or top_n < -1:
            raise ValueError(f"The top_n argument cannot be {top_n}, has to be either "
                             "-1 or a positive integer > 0.")

        self.wsd_model = BEM.from_pretrained(pretrained_model_name_or_path)
        if tokenizer_kwargs is None:
            tokenizer_kwargs = {}
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path,  # type: ignore
                                                  **tokenizer_kwargs)
        assert isinstance(tokenizer, PreTrainedTokenizerBase)
        self.tokenizer = tokenizer
        self.top_n = top_n
        self.device = torch.device(device)
        self.wsd_model.to(self.device)
        self.wsd_model.eval()

    @torch.inference_mode(mode=True)
    def __call__(self, tokens: List[str]
                 ) -> List[Tuple[List[str], List[Tuple[int, int]]]]:
        '''
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
        
        # Parameters

        tokens : `List[str]`
            A List of full text form of the tokens to be tagged.
 
        # Returns

        `List[Tuple[List[str], List[Tuple[int, int]]]]`

        # Raises

        `ValueError`
            If the number of tokens given is not the same as the number of tags
            predicted/returned.
        '''

        predicted_tags_candidates = self.wsd_model.predict(tokens, sub_word_tokenizer=self.tokenizer, top_n=self.top_n)
        
        tags_indexes: List[Tuple[List[str], List[Tuple[int, int]]]] = []

        for token_index, predicted_tag_candidates in enumerate(predicted_tags_candidates):
            start_end_index = [(token_index, token_index + 1)]
            assigned_tags = predicted_tag_candidates
            if tokens[token_index].strip() == "":
                assigned_tags = ["Z9"]
            tags_indexes.append((assigned_tags, start_end_index))
        
        return tags_indexes
