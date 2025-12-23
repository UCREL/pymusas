---
title: Neural Tagger
sidebar_position: 2
---

In this guide we are going to show you how to tag text with the PyMUSAS [NeuralTagger](/api/spacy_api/taggers/neural.md#neuraltagger) so that you can extract token level [USAS semantic tags](https://ucrel.lancs.ac.uk/usas/) from the tagged text. The guide will first state the available neural taggers that can be used, then introduce the Neural Tagger by using the smallest English Neural Tagger as part of a spaCy pipeline, then we will introduce how to use the multilingual tagger, and finally how to use the Neural tagger outside of a spaCy pipeline.

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

:::note
If you would like to use the Neural Tagger without requiring `pymusas` python package, this is possible through following the `usage` guide on the relevant Neural Tagger HuggingFace model card, like this [usage guide for the small English Neural Tagger](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM#usage). `pymusas` is a convenient wrapper around the code given in the `usage` example.
:::
