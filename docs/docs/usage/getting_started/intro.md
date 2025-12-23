---
slug: /
title: Introduction
sidebar_position: 1
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import { PositiveArea, NegativeArea } from '@site/src/components/MarkdownReact/admonition'

# PyMUSAS

**Py**thon **M**ultilingual **U**crel **S**emantic **A**nalysis **S**ystem, is a semantic tagging framework that contains various different semantic taggers; rule based, neural network, and a hybrid of the two, of which all but the neural network can identify and tag Multi Word Expressions (MWE). The taggers can support any semantic tagset, however the tagset we have concentrated on and released pre-configured spaCy components for is the [Ucrel Semantic Analysis System (USAS)](https://ucrel.lancs.ac.uk/usas/).

Below we describe the different semantic taggers we supported and the pre-configured models we have released for each semantic tagger, as well how to read and navigate the documentation website.

## Semantic Taggers

As mentioned we have 3 different taggers; rule based, neural network (neural), and hybrid. A guide on how to choose the right tagger for you can be found in the [tagger comparison section below,](#tagger-comparison) of which in these section we also compare the taggers based on performance across various languages.

:::tip
The USAS special tags;
* `Z99` - tagger does not know how to tag that word. Only the Rule Based taggers can generate this tag.
* `PUNCT` - tagger believes the word to be punctuation and therefore does not have any further semantic meaning.
:::

### Rule Based

The rule based tagger supports both single token and MWE and is a re-implementation of the USAS rule based tagger that has been developed in C and then Java programming languages by [Paul Rayson](https://www.lancaster.ac.uk/sci-tech/about-us/people/paul-rayson) and [Scott Piao](https://www.lancaster.ac.uk/sci-tech/about-us/people/scott-piao), of which it is heavily based on the rules from [Extracting Multiword Expressions with A Semantic Tagger by Scott Piao et al. 2003](https://aclanthology.org/W03-1807.pdf). For more information on exactly how the tagger works please read the API documentation specifically the [RuleBasedTagger class](/api/spacy_api/taggers/rule_based.md#rulebasedtagger) and the [Contextual Ranker class](/api/rankers/lexicon_entry.md#contextualrulebasedranker).

PyMUSAS currently support 11 different languages for the rule based tagger with pre-configured spaCy components that can be downloaded, each language has it's own [guide on how to tag text using PyMUSAS with the Rule Based Tagger](/usage/how_to/tag_text_with/rule_based_tagger.md). Below we show the languages supported, if the model for that language supports MWE identification and tagging (all languages support single token level tagging by default), and disk space size in Mega Bytes (MB) of the model:

| Language (BCP 47 language code) | MWE Support | Disk Space (MB) |
| --- | --- | --- |
| Mandarin Chinese (cmn) | :heavy_check_mark: | 1.28 |
| Danish (da) | :heavy_check_mark: | 0.85 |
| Dutch, Flemish (nl) | :x: | 0.15 |
| English (en) | :heavy_check_mark: | 0.86 |
| Finnish (fi) | :x: | 0.64 |
| French (fr) | :x: | 0.08 |
| Indonesian (id) | :x: | 0.24 |
| Italian (it) | :heavy_check_mark: | 0.50 |
| Portuguese (pt) | :heavy_check_mark: | 0.27 |
| Spanish, Castilian (es) | :heavy_check_mark: | 0.26 |
| Welsh (cy) | :heavy_check_mark: | 1.10 |


### Neural

The neural tagger, as the name suggests, is Neural Network based whereby we have trained a model to predict semantic tags, specifically USAS tags, for all single tokens it is given, more specifically we have fine tuned various different BERT like models. The models we have trained all use the same English training data which are 1,083 English Wikipedia articles that contain ~5.3 million token labels, whereby the labels have been automatically generated using the C version of the English rule based USAS semantic tagger.

Currently we have 4 trained neural taggers, 2 for English and 2 that are highly multilingual, with a [guide on how to tag text using PyMUSAS with these neural taggers](../how_to/tag_text_with/neural_tagger.md). The table below show the size of these models in both number of Millions (M) of parameters and disk space size in Mega Bytes (MB), as well as the name of the tuned models on HuggingFace with a link to each model's card which details how they were trained and how they perform in more detail.

|Language     | HuggingFace ID with model card link | Parameter Size (M) | Disk Space (MB) |
| --- | --- | --- | --- |
| English      | [ucrelnlp/PyMUSAS-Neural-English-Small-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM) | 17 | 60 |
| English      | [ucrelnlp/PyMUSAS-Neural-English-Base-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Base-BEM) | 68 | 242 |
| Multilingual | [ucrelnlp/PyMUSAS-Neural-Multilingual-Small-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-Multilingual-Small-BEM) | 140 | 501 |
| Multilingual | [ucrelnlp/PyMUSAS-Neural-Multilingual-Base-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-Multilingual-Base-BEM) | 307 | 1,060 |

### Hybrid

Hybrid is a combination of a rule based and neural tagger. This tagger in essence runs the configured rule based tagger on a given text and if it has one or more unknown words in the text it cannot tag then it uses the neural tagger to assign a tag to those words, more details can be found in the API documentation of the [HybridTagger class.](/api/spacy_api/taggers/hybrid.md#hybridtagger). The hybrid tagger does not come with any pre-configured spaCy components, all hybrid tagger must be configured for your own use case, but we have a detailed how to guide on this at [how to tag text with hybrid tagger.](../how_to/tag_text_with/hybrid_tagger.md)

### Tagger Comparison

We have 3 different types of taggers; rule based, neural, and hybrid, of which below we state the advantages and dis-advantages of each tagger as well as their evaluation results on 4 different languages;


<Tabs
defaultValue="rule-based"
values={[
    {label: 'Rule Based', value: 'rule-based'},
    {label: 'Neural', value: 'neural'},
    {label: 'Hybrid', value: 'hybrid'}
]}>
    <TabItem value="rule-based">
        <PositiveArea>
            * Very fast.
            * Requires little amount of disk space and memory (RAM).
            * An explainable/interpretable tagger.
            * Can generate USAS tags that contain affixed symbols like `+`, `-`, `%`, `@`, etc and multi membership tags that are denoted through the use of a slash `/`, e.g. `F2/O2`.
            * Can identify and tag Multi Word Expressions.
        </PositiveArea>
        <NegativeArea>
            * Depending on the size and content of the lexicon determines the number of words it can generate a semantic tag for. In essence this tagger is unlikely to make a prediction for all words.
            * Unlike the neural tagger, cannot generate a controllable number of semantic tags per word, the number of semantic tags generated is based on the lexicon within the tagger.
        </NegativeArea>
    </TabItem>
    <TabItem value="neural">
        <PositiveArea>
            * Can make a prediction for all words, unlike the rule based tagger.
            * Can be configured to generate a list of semantic tag prediction per word in most likely order. For instance you can pre-configure the tagger to generate the 4 or *N* most likely semantic tags for all words.
        </PositiveArea>
        <NegativeArea>
            * Slowest of the 3 taggers.
            * Can only generate single USAS/semantic tag categories, i.e. cannot generate tags with affixed symbols like `+`, `-`, `%`, `@`, etc or multi membership tags that are denoted through the use of a slash `/`, e.g. `F2/O2`.
            * All neural taggers have been fine tuned on English data, which makes it less accurate for non-English data.
            * Speed, quality, memory, and size depend on the tagger size, the bigger the tagger the more accurate the prediction, but the slower it is, the more disk space required to store it, and the more RAM/VRAM required to run the model.
        </NegativeArea>
    </TabItem>
    <TabItem value="hybrid">
        <PositiveArea>
            * Out of the 3 taggers it is typically the most accurate.
            * Can be faster than the neural tagger as for some texts the neural tagger is not required.
            * Can make a prediction for all words, unlike the rule based tagger, as for words the rule based tagger does not know the neural tagger is used.
            * For words that the neural tagger is used for it can be configured to generate a list of semantic tag prediction per word in most likely order. For instance you can pre-configure the tagger to generate the 4 or *N* most likely semantic tags for all words.
            * For words the the rule based tagger is used for it can generate USAS tags that contain affixed symbols like `+`, `-`, `%`, `@`, etc and multi membership tags that are denoted through the use of a slash `/`, e.g. `F2/O2`. For these words it can also identify and tag Multi Word Expressions. It is therefore also an explainable tagger for these words.
        </PositiveArea>
        <NegativeArea>
            * As it requires both rule based and neural taggers, it requires the most resources, i.e. requires at least a lexicon for the rule based tagger, and a trained neural tagger.
            * As it uses the neural tagger requires additional disk space, memory (RAM/VRAM), and more processing time of which this is also dependent on the neural tagger size, the larger it is the more disk space, memory, and time required.
            * All neural taggers have been fine tuned on English data, which makes it less accurate for non-English data.
        </NegativeArea>
    </TabItem>
</Tabs>


We also have performance metrics for the 3 types of taggers for 4 different languages, these performance metrics reinforce the benefits and disadvanytag using Top-N accuracy as the evaluation metric, whereby higher is better (100 is best);


<Tabs
defaultValue="top-1"
values={[
    {label: 'Top-1', value: 'top-1'},
    {label: 'Top-5', value: 'top-5'}
]}>
    <TabItem value="top-1" label="Top-1">

| Models | English | Chinese | Finnish | Welsh |
|----|----------|----|----|----|
| Rule Based  | 72.4 | 32.6 | 58.4 | 70.6 |
| Neural-E-17M  | 66.4 | - | - | - |
| Neural-E-68M  | 70.1 | - | - | - |
| Neural-M-140M  | 66.0 | 42.2 | 15.8 | 21.7 |
| Neural-M-307M  | 70.2 | 47.9 | 25.9 | 42.0 |
| Hybrid-E-17M  | 72.5 | - | - | - |
| Hybrid-E-68M  | 72.5 | - | - | - |
| Hybrid-M-140M  | 72.5 | 39.8 | 59.1 | 71.3 |
| Hybrid-M-307M  | 72.5 | 39.8 | 60.3 | 72.4 |

    </TabItem>
    <TabItem value="top-5" label="Top-5">

| Models | English | Chinese | Finnish | Welsh |
|----|----------|----|----|----|
| Rule Based  | 81.8 | 43.6 | 64.0 | 73.2 |
| Neural-E-17M  | 87.6 | - | - | - |
| Neural-E-68M  | 90.0 | - | - | - |
| Neural-M-140M  | 88.9 | 66.3 | 32.8 | 40.8 |
| Neural-M-307M  | 90.1 | 70.4 | 42.4 | 56.4 |
| Hybrid-E-17M  | 81.9 | - | - | - |
| Hybrid-E-68M  | 82.0 | - | - | - |
| Hybrid-M-140M  | 82.0 | 55.6 | 65.8 | 75.5 |
| Hybrid-M-307M  | 82.0 | 56.3 | 67.3 | 75.9 |


    </TabItem>
</Tabs>

<details>
<summary>Full Model Names</summary>

* Neural-E-17M - Neural English 17 Million parameter tagger.
* Neural-E-68M - Neural English 68 Million parameter tagger.
* Neural-M-140M - Neural Multilingual 140 Million parameter tagger.
* Neural-M-307M - Neural Multilingual 307 Million parameter tagger.

This naming convention is the same for the Hybrid models. For the Hybrid models we used the rule base tagger for the given dataset language and where possible we would use the rule based tagger with the Multi Word Expressions.

</details>

<details>
<summary>Top-N evaluation explanation</summary>

Top-1 and top-5 evaluation is a top-N accuracy based evaluation whereby if one of the tagger's top `N` predictions is the correct prediction then it is correct else it is not, of which this is performed on each token that a human has annotated with a semantic tag in the given datasets.
</details>



## Reading the documentation

How the documentation website is split between the Usage and API pages:

* [Usage](/) - The usage pages contains how-to-guides, and explanations.
* [API](/api/spacy_api/taggers/rule_based.md) - Are the docstrings of the PyMUSAS library, best pages to look at if you want to know exactly what a class / function / attribute does in more technical detail. These do contain examples, but the examples are more like minimum working examples rather than real world examples.


## Future Plans

Our [road map](https://github.com/UCREL/pymusas/blob/main/ROADMAP.md) contains the most up to date future plans for PyMUSAS.