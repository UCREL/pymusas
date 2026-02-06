---
title: Neural Tagger
sidebar_position: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

In this guide we are going to show you how to tag text with the PyMUSAS [NeuralTagger](/api/spacy_api/taggers/neural.md#neuraltagger) so that you can extract token level [USAS semantic tags](https://ucrel.lancs.ac.uk/usas/) from the tagged text. The guide will;

* State the available neural taggers that can be used.
* Introduce the Neural Tagger by using the smallest English Neural Tagger as part of a spaCy pipeline.
* Introduce how to use the multilingual tagger.
* How to use the Neural tagger outside of a spaCy pipeline.
* How to efficient use the Neural tagger when processing long and or large amounts of text.

## Available taggers

As stated in the introduction we have 4 trained neural taggers 2 for English and 2 that are highly multilingual. The table below show the size of these models in both number of Millions (M) of parameters and disk space size in Mega Bytes (MB), the name of the tuned models on HuggingFace with a link to each model's card which details how they were trained and how they perform in more detail, and lastly the spaCy name of the neural tagger that is used when loading the neural tagger in spaCy with a link to the pre-configured spaCy component that contains the neural tagger for spaCy only that can be installed using pip.

|Language     | HuggingFace ID with model card link | Parameter Size (M) | Disk Space (MB) | spaCy neural tagger name |
| --- | --- | --- | --- | --- |
| English      | [ucrelnlp/PyMUSAS-Neural-English-Small-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM) | 17 | 60 | [en_none_none_none_englishsmallbem](https://github.com/UCREL/pymusas-models/releases/tag/en_none_none_none_englishsmallbem-0.4.0) |
| English      | [ucrelnlp/PyMUSAS-Neural-English-Base-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Base-BEM) | 68 | 242 |  [en_none_none_none_englishbasebem](https://github.com/UCREL/pymusas-models/releases/tag/en_none_none_none_englishbasebem-0.4.0) |
| Multilingual | [ucrelnlp/PyMUSAS-Neural-Multilingual-Small-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-Multilingual-Small-BEM) | 140 | 501 | [xx_none_none_none_multilingualsmallbem](https://github.com/UCREL/pymusas-models/releases/tag/xx_none_none_none_multilingualsmallbem-0.4.0) |
| Multilingual | [ucrelnlp/PyMUSAS-Neural-Multilingual-Base-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-Multilingual-Base-BEM) | 307 | 1,060 | [xx_none_none_none_multilingualbasebem](https://github.com/UCREL/pymusas-models/releases/tag/xx_none_none_none_multilingualbasebem-0.4.0) |

## Introduction with the English neural tagger

<!--:::note
We assume you have already installed PyMUSAS with the neural extra as shown in the installation [documentation](../../getting_started/installation.md#install-for-neural-or-hybrid-taggers).
:::-->

We are going to use the [small neural English 17 million parameter pre-configured spaCy pipeline](https://github.com/UCREL/pymusas-models/releases/tag/en_none_none_none_englishsmallbem-0.4.0), and download it like so:

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/en_none_none_none_englishsmallbem-0.4.0/en_none_none_none_englishsmallbem-0.4.0-py3-none-any.whl
```

We don't need any other spaCy pipeline, but for the best results we do need a tokenizer of which we can use the English tokenizer that comes with the spaCy library, we can load that tokenizer like so:

``` python
import spacy
# loads the English tokenizer
nlp = spacy.blank("en")
```

We can then add our neural tagger to this tokenizer like so, whereby `en_none_none_none_englishsmallbem` is the spaCy name of the neural tagger we want to load that we installed earlier using pip:

``` python
english_neural_tagger_pipeline = spacy.load("en_none_none_none_englishsmallbem")

nlp.add_pipe("pymusas_neural_tagger", source=english_neural_tagger_pipeline)
```
:::tip

If you would like to use a different tagger see the [available taggers section above](#available-taggers), pip install the tagger you would like to use and change the spaCy name to relevant installed tagger, e.g. if you installed the [base English model](https://github.com/UCREL/pymusas-models/releases/tag/en_none_none_none_englishbasebem-0.4.0) the spaCy name would be `en_none_none_none_englishbasebem`
:::

The tagger is now set up for tagging text through the spaCy pipeline like so. The example text is taken from the English Wikipedia page on the topic of [`The Nile River`](https://en.wikipedia.org/wiki/Nile), we capitalised the *n* in `Northeastern`:

``` python
text = "The Nile is a major north-flowing river in Northeastern Africa."

output_doc = nlp(text)

print(f'{"Text":<20}USAS Tags')
for token in output_doc:
    print(f'{token.text:<20}{token._.pymusas_tags}')
```


<details>
<summary>Output</summary>

``` tsv
Text                USAS Tags
The                 ['Z5', 'Z3', 'Z2', 'Z1', 'Z8']
Nile                ['Z2', 'Z3', 'T1.1.1', 'B1', 'Z1']
is                  ['A3', 'Z5', 'A6.2', 'A5.1', 'X5.2']
a                   ['Z5', 'N5', 'A11.1', 'A5.1', 'M7']
major               ['A11.1', 'N3.2', 'T1.2', 'T1.3', 'A4.2']
north               ['M6', 'Z2', 'M7', 'Z1', 'Z3']
-                   ['Z5', 'Z3', 'Z2', 'Z1', 'S2']
flowing             ['M1', 'N5', 'Q2.1', 'A1.1.1', 'T2']
river               ['M4', 'N5', 'W3', 'M1', 'Q1.2']
in                  ['Z5', 'M1', 'Z2', 'M7', 'A1.8']
Northeastern        ['Z2', 'M7', 'M6', 'Z3', 'Z1']
Africa              ['Z2', 'Z3', 'Z1', 'M7', 'S2']
.                   ['S2', 'Z2', 'Z3', 'Z1', 'Q3']
```
</details>

As you can see from the output we have exactly 5 semantic tags per word, these tags like in all of our taggers are a ranked list of tags whereby the first tag is the most likely tag. One of the benefits of the neural tagger is that we can configure the number of semantic tags it produces at tagger initialization time like so:

``` python
nlp.remove_pipe("pymusas_neural_tagger")
# the top_n attribute in the config determines the number of semantic tags outputted
english_neural_tagger_pipeline = spacy.load("en_none_none_none_englishsmallbem",
                                            config={"components.pymusas_neural_tagger.top_n": 2})

nlp.add_pipe("pymusas_neural_tagger", source=english_neural_tagger_pipeline)

text = "The Nile is a major north-flowing river in Northeastern Africa."

output_doc = nlp(text)

print(f'{"Text":<20}USAS Tags')
for token in output_doc:
    print(f'{token.text:<20}{token._.pymusas_tags}')
```

The `components.pymusas_neural_tagger.top_n` key-value determines the number of semantic tags the tagger outputs. This config can in-fact be used to set any of the default configuration settings outlined in [NeuralTagger class](/api/spacy_api/taggers/neural.md#neuraltagger) for instances the `device` by default it is `cpu` but it could be set to `cuda` to use the GPU.

<details>
<summary>Output</summary>

``` tsv
Text                USAS Tags
The                 ['Z5', 'Z3']
Nile                ['Z2', 'Z3']
is                  ['A3', 'Z5']
a                   ['Z5', 'N5']
major               ['A11.1', 'N3.2']
north               ['M6', 'Z2']
-                   ['Z5', 'Z3']
flowing             ['M1', 'N5']
river               ['M4', 'N5']
in                  ['Z5', 'M1']
Northeastern        ['Z2', 'M7']
Africa              ['Z2', 'Z3']
.                   ['S2', 'Z2']
```
</details>

## Multilingual neural tagger

The multilingual neural tagger works in the same way as the English neural tagger, it just requires a relevant tokenizer just like the English neural tagger. spaCy provides tokenizers for [many languages](https://spacy.io/usage/models#languages), in this example we are going to apply the small multilingual tagger to Danish.

:::danger
As the tagger can be used with numerous languages (1,811 languages see the relevant model card on HuggingFace) but has only been fine tuned on the semantic tagging task in English it is more important to check the quality of semantic tags produced as the tagger can be inaccurate for the language you are applying it too. We do provide accuracy results for all of taggers for select languages in the [tagger comparison section of the introduction.](../../getting_started/intro.md#tagger-comparison)
:::

:::tip
If you would prefer to use a tokenizer that is not a spaCy component then please see the section.
:::

First we need to download the [small neural multilingual 140 million parameter pre-configured spaCy pipeline](https://github.com/UCREL/pymusas-models/releases/tag/xx_none_none_none_multilingualsmallbem-0.4.0), and download it like so:

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/xx_none_none_none_multilingualsmallbem-0.4.0/xx_none_none_none_multilingualsmallbem-0.4.0-py3-none-any.whl
```

We can then add the Danish spaCy tokenizer, that comes with the spaCy library, like so:

```python
import spacy
# loads the Danish tokenizer
nlp = spacy.blank("da")
```

We can then add our neural tagger to this tokenizer like so, whereby `xx_none_none_none_multilingualsmallbem` is the spaCy name of the neural tagger we want to load that we installed earlier using pip:

``` python
multilingual_neural_tagger_pipeline = spacy.load("xx_none_none_none_multilingualsmallbem")

nlp.add_pipe("pymusas_neural_tagger", source=multilingual_neural_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so. The example text is taken from the Danish Wikipedia page on the topic of [`The Nile River`](https://da.wikipedia.org/wiki/Nilen):

```python
text = "Mindst 65% af Nilens vand kommer fra Den Blå Nil, som udspringer ved Tanasøen i Etiopien."

output_doc = nlp(text)

print(f'{"Text":<20}USAS Tags')
for token in output_doc:
    print(f'{token.text:<20}{token._.pymusas_tags}')
```

<details>
<summary>Output</summary>

``` tsv
Text                USAS Tags
Mindst              ['A1.3', 'Z1', 'Z3', 'A11.1', 'E6']
65                  ['N1', 'T1.3', 'N3.2', 'T3', 'T1.2']
%                   ['N5', 'A9', 'Z5', 'N5.1', 'A2.2']
af                  ['Z5', 'Z3', 'Z1', 'E2', 'I1.1']
Nilens              ['Z3', 'Z1', 'Z2', 'S9', 'O4.3']
vand                ['O1.2', 'O1.1', 'M4', 'Z3', 'O1']
kommer              ['M1', 'A2.2', 'A9', 'A3', 'S4']
fra                 ['Z5', 'Z3', 'Z1', 'I2.2', 'I2.1']
Den                 ['Z1', 'Z3', 'A10', 'Z2', 'Q4.3']
Blå                 ['Z1', 'Z3', 'Z2', 'O4.3', 'Z5']
Nil                 ['Z3', 'Z1', 'Z2', 'S9', 'N1']
,                   ['Z5', 'Z3', 'Z1', 'K5.1', 'T1.3']
som                 ['Q3', 'S9', 'Y2', 'S2', 'K2']
udspringer          ['S2', 'Z3', 'Z1', 'N5', 'L2']
ved                 ['Z5', 'Z3', 'Z1', 'S2', 'Z2']
Tanasøen            ['Z3', 'Z2', 'Z1', 'S2', 'B1']
i                   ['Z5', 'Z3', 'Z1', 'Z8', 'T3']
Etiopien            ['S2', 'Z2', 'Q3', 'Z3', 'Z1']
.                   ['Z5', 'Z3', 'Z1', 'E2', 'K5.1']
```
</details>

## Neural taggers without spaCy

Currently we have only shown you how to use the neural tagger through a spaCy pipeline. However, you may have a use case whereby the spaCy pipeline is constraining you, e.g. you want to use a different tokenizer. Here we will show you how to setup the neural tagger without spaCy using whitespace as your tokenizer.

:::note
For this section we assume you have already installed PyMUSAS with the neural extra as shown in the installation [documentation](../../getting_started/installation.md#install-for-neural-or-hybrid-taggers).
:::

We are going to use the [small neural English 17 million parameter tagger](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM), we are going to initialize the tagger like so, when it initializes it will download the tagger from the [HuggingFace hub](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM) using the HuggingFace model id `ucrelnlp/PyMUSAS-Neural-English-Small-BEM`:

``` python
from pymusas.taggers.neural import NeuralTagger

tokenizer_kwargs = {"add_prefix_space": True}
neural_tagger = NeuralTagger("ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
                             device="cpu", top_n=2, tokenizer_kwargs=tokenizer_kwargs)
```

Just like using the pre-configured spaCy pipeline version we can configure the neural tagger when we load/initialize it, of which the configuration settings you can set and their default value can be found in the [NeuralTagger class documentation.](/api/taggers/neural.md#neuraltagger)

The tagger is now setup for tagging and we are going to use the same example text as before, taken from the English Wikipedia page on the topic of [`The Nile River`](https://en.wikipedia.org/wiki/Nile), we capitalised the *n* in `Northeastern`

``` python
text = "The Nile is a major north-flowing river in Northeastern Africa."
words = text.split()
all_tags_and_indices = neural_tagger(words)

print(f'{"Text":<15}{"Start and End USAS Tag index":<30}{"USAS Tags"}')
for word, tags_and_indices in zip(words, all_tags_and_indices):
    tag, tag_indices = tags_and_indices
    print(f"{word:<15}{str(tag_indices):<30}{tag}")
```

As you can see in the output, the tagger produces a `List[Tuple[List[str], List[Tuple[int, int]]]]` whereby each `Tuple` corresponds to a word of the same index, and each `Tuple` is made up of:

1. A `List` of USAS tags. The first tag in the `List` of tags is the most likely tag. The number of USAS tags generated is determined by the `top_n` parameter given to the `NeuralTagger` class at initialization.
2. A `List` of `Tuples` whereby each `Tuple` indicates the start and end token index of the associated Multi Word Expression (MWE). If the `List` contains more than one `Tuple` then the MWE is discontinuous. For single word expressions the `List` will only contain 1 `Tuple` which will be (token_start_index, token_start_index + 1).

:::note
Currently the neural taggers only support single word expressions.
:::

<details>
<summary>Output</summary>

``` tsv
Text           Start and End USAS Tag index  USAS Tags
The            [(0, 1)]                      ['Z5', 'Z3']
Nile           [(1, 2)]                      ['Z2', 'Z3']
is             [(2, 3)]                      ['A3', 'Z5']
a              [(3, 4)]                      ['Z5', 'N5']
major          [(4, 5)]                      ['A11.1', 'N3.2']
north-flowing  [(5, 6)]                      ['M6', 'Z2']
river          [(6, 7)]                      ['M4', 'W3']
in             [(7, 8)]                      ['Z5', 'M1']
Northeastern   [(8, 9)]                      ['Z2', 'M7']
Africa.        [(9, 10)]                     ['Z2', 'Z3']
```
</details>

:::tip
If you would like to use the Neural Tagger without requiring `pymusas` python package, this is possible through following the `usage` guide on the relevant Neural Tagger HuggingFace model card, like this [usage guide for the small English Neural Tagger](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM#usage). `pymusas` is a convenient wrapper around the code given in the `usage` example.
:::

## How to efficiently process long or large texts

:::note
This section applies to any tagger that uses a neural tagger, i.e. the Hybrid Tagger.
:::

The neural tagger is very memory intensive when processing long sequences due to the neural network model that is used (transformer based model, specifically [ModernBERT](https://aclanthology.org/2025.acl-long.127.pdf)), it has a quadratic memory cost based on the length of the text, therefore when using the neural tagger it is advised to process at most sentence length texts rather than paragraph, document, or multi-document, in doing so it will keep the memory requirements consistent.

We will show how to tag at least 10,000 tokens of English Wikipedia articles from the [HuggingFaceFW/finewiki](https://huggingface.co/datasets/HuggingFaceFW/finewiki) dataset using the [larger 68 million parameter English Neural Tagger model](https://github.com/UCREL/pymusas-models/releases/tag/en_none_none_none_englishbasebem-0.4.0) by sentence splitting the text as we process the Wikipedia articles.

### Setup

We need:
* `pymusas[neural]` with the neural extra for tagging.
* `datasets` the HuggingFace datasets library to download the Wikipedia data.
* `en_core_web_sm` the small spaCy English pipeline to sentence split the data. This could be any sentence splitter but we have chosen spaCy, to note we are going to use the default sentence splitter that requires a dependency parser, but with spaCy, at least for English, you do have other options that are quicker and do not require a dependency parser, [see here for more details.](https://spacy.io/usage/linguistic-features#sbd)
* `en_none_none_none_englishbasebem` the [larger 68 million parameter English Neural Tagger model.](https://github.com/UCREL/pymusas-models/releases/tag/en_none_none_none_englishbasebem-0.4.0)

To download these run the following:


<Tabs groupId="shell-choice">
<TabItem value="bash" label="bash">

``` bash
pip install pymusas[neural] datasets
# small spaCy English pipeline
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
# PyMUSAS neural tagger
pip install https://github.com/UCREL/pymusas-models/releases/download/en_none_none_none_englishbasebem-0.4.0/en_none_none_none_englishbasebem-0.4.0-py3-none-any.whl
```

</TabItem>
<TabItem value="zsh" label="zsh">

``` bash
pip install 'pymusas[neural]' datasets
# small spaCy English pipeline
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
# PyMUSAS neural tagger
pip install https://github.com/UCREL/pymusas-models/releases/download/en_none_none_none_englishbasebem-0.4.0/en_none_none_none_englishbasebem-0.4.0-py3-none-any.whl
```

</TabItem>
</Tabs>

### Tagging long or large texts

First we import the relevant libraries, create a few helper functions that will download and process the Wikipedia articles, and then use these functions to download *N* English Wikipedia articles to a temporary directory (so that after the script has ran they will be deleted to save disk space), whereby the number of articles we download will contain at least 10,000 tokens/words after we have got to this token limit we will not download anymore Wikipedia articles;

``` python
from pathlib import Path
import tempfile
from typing import Iterable

from datasets import get_dataset_config_names, get_dataset_split_names, load_dataset
import spacy


def wikipedia_dataset_to_directory(huggingface_dataset_id: str,
                                   directory: str,
                                   file_prefix: str,
                                   spacy_model: spacy.Language,
                                   number_tokens: int,
                                   language_code: str) -> int:
    """
    Saves a subset of Wikipedia articles from the given language code to the
    specified directory, whereby the number of articles saved is based on
    the number of tokens.

    Args:
        huggingface_dataset_id (str): The Hugging Face dataset ID of the Wikipedia dataset, e.g. HuggingFaceFW/finewiki
        directory (str): The directory to which the files should be saved.
        file_prefix (str): The prefix of the file names. Each prefix is appended with a unique article number.
        spacy_model (spacy.Language): The Spacy language model that should be used to tokenize the text.
        number_tokens (int): The minimum number of tokens to be saved. Once the
            number of tokens is reached no more articles are saved.
        language_code (str): The language code of the dataset to be saved.

    Returns:
        int: The number of tokens saved.
    """
    wikipedia_languages = get_dataset_config_names(huggingface_dataset_id)
    if language_code not in wikipedia_languages:
        raise ValueError(f"Language {language_code} not found in dataset {huggingface_dataset_id}")
    split = "train"
    assert split in get_dataset_split_names(huggingface_dataset_id)

    wikipedia_language_dataset = load_dataset(huggingface_dataset_id,
                                              language_code,
                                              split=split,
                                              streaming=True,
                                              columns=["text"])
    article_count = 0
    token_count = 0
    for object in wikipedia_language_dataset:
        text = object["text"]
        # We skip any article that contains a table
        if "| -" in text:
            continue
        # Removes markdown headers
        text = text.replace("#", "")
        # Tried to remove markdown lists, but I think this creates a worse format
        # text = re.sub(r"\s*-\s+", "", text)
        token_count += len(spacy_model(text))
        article_count += 1

        temp_file = Path(directory, f"{file_prefix}{article_count}")
        with temp_file.open("w", encoding="utf-8") as f:
            f.write(text)
        if token_count > number_tokens:
            break
    return token_count


def text_from_files(file_directory: Path,
                    file_prefix: str) -> Iterable[str]:
    """
    Yields lines of non empty text from files in a directory whereby the file
    names start with the given file prefix.

    All lines of text are stripped of leading and trailing whitespace.

    Args:
        file_directory (Path): The directory to read files from.
        file_prefix (str): The prefix of the file names to read.

    Yields:
        An iterable of strings, where each string is a non-empty line from
        one of the files with leading and trailing whitespace stripped.
    """
    for file in file_directory.iterdir():
        if file.name.startswith(file_prefix):
            with file.open("r", encoding="utf-8") as file_fp:
                for line in file_fp:
                    line = line.strip()
                    if line:
                        yield line


def sentences_from_texts(text_iterator: Iterable[str],
                         spacy_model: spacy.Language) -> Iterable[str]:
    """
    Given an iterable of texts, it returns the texts split into sentences by the
    given spaCy model.

    Args:
        text_iterator (Iterable[str]): The iterable of texts to be sentence split.
        spacy_model (spacy.Language): The spaCy language model to be used to sentence split the text.

    Yields:
        Sentences from the text iterator.
    """
    for spacy_doc in spacy_model.pipe(text_iterator):
        for sentence in spacy_doc.sents:
            yield sentence.text

# Temporary directory that we are storing the Wikipedia articles too
with tempfile.TemporaryDirectory() as temp_dir:
    # spaCy pipeline for sentence splitting, for a choice of sentence splitters
    # see https://spacy.io/usage/linguistic-features#sbd
    spacy_sentence_splitter_pipeline = spacy.load("en_core_web_sm")
    # Each Wikipedia article we download will be saved to a file with this prefix
    # and a unique article number appended, of which these articles will be within
    # the temp_dir
    data_file_prefix = "wikipedia_article_"
    # HuggingFace dataset ID for Wikipedia dataset: https://huggingface.co/datasets/HuggingFaceFW/finewiki
    wikipedia_dataset_id = "HuggingFaceFW/finewiki"
    # We are going to download enough Wikipedia articles so that we have at least 10,000 tokens
    # of text.
    minimum_number_tokens = 10_000
    # Downloads the Wikipedia articles
    wikipedia_dataset_to_directory(wikipedia_dataset_id,
                                   temp_dir,
                                   data_file_prefix,
                                   spacy_sentence_splitter_pipeline, minimum_number_tokens,
                                   "en")
```

Now that we have the Wikipedia articles in a temporary directory we can use the `text_from_files` and `sentences_from_texts` functions to create an iterable that will efficently get each line of text from a file and then per line sentence split it, by using an iterable we only store the current line in memory rather than the whole text (for Wikipedia the line of text can be a whole paragraph).

``` python
    # We read the Wikipedia article one text at a time
    wikipedia_texts = text_from_files(Path(temp_dir), data_file_prefix)
    # For each line of text in the Wikipedia article we sentence split it
    wikipedia_texts_sentence_split = sentences_from_texts(wikipedia_texts,
                                                          spacy_sentence_splitter_pipeline)
```

Currently we have not processed any of the Wikipedia text as these are [generators](https://www.w3schools.com/python/python_generators.asp) whereby until we loop over them with a for loop they will not do anything.

We now create the English neural tagger using the pre-configured spaCy pipeline, as shown in the [earlier section](#introduction-with-the-english-neural-tagger) but this time with a larger neural tagger model.

``` python
    # We create the spaCy neural tagger pipeline which uses the CPU rather than the GPU/CUDA
    pymusas_neural_nlp = spacy.blank("en")
    device = "cpu"
    pymusas_neural_tagger_pipeline = spacy.load("en_none_none_none_englishbasebem",
                                                config={"components.pymusas_neural_tagger.device": device})
    pymusas_neural_nlp.add_pipe("pymusas_neural_tagger", source=pymusas_neural_tagger_pipeline)
```

We can now efficently process the 10,000 tokens of English text like so, whereby the neural tagger will be given a sentence at a time to process from the `wikipedia_texts_sentence_split` generator.

``` python
    # We now efficient process each sentence in all of the Wikipedia articles
    for doc in pymusas_neural_nlp.pipe(wikipedia_texts_sentence_split,
                                       n_process=1):
        for token in doc:
            token_text = token.text
            # USAS tags
            usas_tags = token._.pymusas_tags
```

:::note
We set `n_process=1` as the neural tagger model will be using as many CPU processors as possible therefore we do not want to assign any processors away from this.
:::

For the full python script see the drop down below;

<details>
<summary>Full Python Script</summary>

``` python
from pathlib import Path
import tempfile
from typing import Iterable

from datasets import get_dataset_config_names, get_dataset_split_names, load_dataset
import spacy


def wikipedia_dataset_to_directory(huggingface_dataset_id: str,
                                   directory: str,
                                   file_prefix: str,
                                   spacy_model: spacy.Language,
                                   number_tokens: int,
                                   language_code: str) -> int:
    """
    Saves a subset of Wikipedia articles from the given language code to the
    specified directory, whereby the number of articles saved is based on
    the number of tokens.

    Args:
        huggingface_dataset_id (str): The Hugging Face dataset ID of the Wikipedia dataset, e.g. HuggingFaceFW/finewiki
        directory (str): The directory to which the files should be saved.
        file_prefix (str): The prefix of the file names. Each prefix is appended with a unique article number.
        spacy_model (spacy.Language): The Spacy language model that should be used to tokenize the text.
        number_tokens (int): The minimum number of tokens to be saved. Once the
            number of tokens is reached no more articles are saved.
        language_code (str): The language code of the dataset to be saved.

    Returns:
        int: The number of tokens saved.
    """
    wikipedia_languages = get_dataset_config_names(huggingface_dataset_id)
    if language_code not in wikipedia_languages:
        raise ValueError(f"Language {language_code} not found in dataset {huggingface_dataset_id}")
    split = "train"
    assert split in get_dataset_split_names(huggingface_dataset_id)

    wikipedia_language_dataset = load_dataset(huggingface_dataset_id,
                                              language_code,
                                              split=split,
                                              streaming=True,
                                              columns=["text"])
    article_count = 0
    token_count = 0
    for object in wikipedia_language_dataset:
        text = object["text"]
        # We skip any article that contains a table
        if "| -" in text:
            continue
        # Removes markdown headers
        text = text.replace("#", "")
        # Tried to remove markdown lists, but I think this creates a worse format
        # text = re.sub(r"\s*-\s+", "", text)
        token_count += len(spacy_model(text))
        article_count += 1

        temp_file = Path(directory, f"{file_prefix}{article_count}")
        with temp_file.open("w", encoding="utf-8") as f:
            f.write(text)
        if token_count > number_tokens:
            break
    return token_count


def text_from_files(file_directory: Path,
                    file_prefix: str) -> Iterable[str]:
    """
    Yields lines of non empty text from files in a directory whereby the file
    names start with the given file prefix.

    All lines of text are stripped of leading and trailing whitespace.

    Args:
        file_directory (Path): The directory to read files from.
        file_prefix (str): The prefix of the file names to read.

    Yields:
        An iterable of strings, where each string is a non-empty line from
        one of the files with leading and trailing whitespace stripped.
    """
    for file in file_directory.iterdir():
        if file.name.startswith(file_prefix):
            with file.open("r", encoding="utf-8") as file_fp:
                for line in file_fp:
                    line = line.strip()
                    if line:
                        yield line


def sentences_from_texts(text_iterator: Iterable[str],
                         spacy_model: spacy.Language) -> Iterable[str]:
    """
    Given an iterable of texts, it returns the texts split into sentences by the
    given spaCy model.

    Args:
        text_iterator (Iterable[str]): The iterable of texts to be sentence split.
        spacy_model (spacy.Language): The spaCy language model to be used to sentence split the text.

    Yields:
        Sentences from the text iterator.
    """
    for spacy_doc in spacy_model.pipe(text_iterator):
        for sentence in spacy_doc.sents:
            yield sentence.text


# Temporary directory that we are storing the Wikipedia articles too
with tempfile.TemporaryDirectory() as temp_dir:
    # spaCy pipeline for sentence splitting, for a choice of sentence splitters
    # see https://spacy.io/usage/linguistic-features#sbd
    spacy_sentence_splitter_pipeline = spacy.load("en_core_web_sm")
    # Each Wikipedia article we download will be saved to a file with this prefix
    # and a unique article number appended, of which these articles will be within
    # the temp_dir
    data_file_prefix = "wikipedia_article_"
    # HuggingFace dataset ID for Wikipedia dataset: https://huggingface.co/datasets/HuggingFaceFW/finewiki
    wikipedia_dataset_id = "HuggingFaceFW/finewiki"
    # We are going to download enough Wikipedia articles so that we have at least 10,000 tokens
    # of text.
    minimum_number_tokens = 10_000
    # Downloads the Wikipedia articles
    wikipedia_dataset_to_directory(wikipedia_dataset_id, temp_dir, data_file_prefix, spacy_sentence_splitter_pipeline, minimum_number_tokens, "en")
    
    # We read the Wikipedia article one text at a time
    wikipedia_texts = text_from_files(Path(temp_dir), data_file_prefix)
    # For each line of text in the Wikipedia article we sentence split it
    wikipedia_texts_sentence_split = sentences_from_texts(wikipedia_texts, spacy_sentence_splitter_pipeline)
    
    # We create the spaCy neural tagger pipeline which uses the CPU rather than the GPU/CUDA
    pymusas_neural_nlp = spacy.blank("en")
    device = "cpu"
    pymusas_neural_tagger_pipeline = spacy.load("en_none_none_none_englishbasebem",
                                                config={"components.pymusas_neural_tagger.device": device})
    pymusas_neural_nlp.add_pipe("pymusas_neural_tagger", source=pymusas_neural_tagger_pipeline)

    # We now efficient process each sentence in all of the Wikipedia articles
    for doc in pymusas_neural_nlp.pipe(wikipedia_texts_sentence_split,
                                       n_process=1):
        for token in doc:
            token_text = token.text
            # USAS tags
            usas_tags = token._.pymusas_tags
```
</details>

