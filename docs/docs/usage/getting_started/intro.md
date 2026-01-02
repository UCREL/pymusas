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

We have 3 different types of taggers; rule based, neural, and hybrid, of which below;
* We state the advantages and dis-advantages of each tagger.
* The evaluation results on 4 different languages for all taggers.
* The resources required to run the taggers on different size texts as well as how fast in tokens per second the taggers are.

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
            * Slower than the rule based tagger, in general.
            * Can only generate single USAS/semantic tag categories, i.e. cannot generate tags with affixed symbols like `+`, `-`, `%`, `@`, etc or multi membership tags that are denoted through the use of a slash `/`, e.g. `F2/O2`.
            * All neural taggers have been fine tuned on English data, which makes it less accurate for non-English data.
            * Speed, quality, memory, and size depend on the tagger size, the bigger the tagger the more accurate the prediction, but the slower it is, the more disk space required to store it, and the more RAM/VRAM required to run the model.
        </NegativeArea>
    </TabItem>
    <TabItem value="hybrid">
        <PositiveArea>
            * Out of the 3 taggers it is typically the most accurate.
            * Can make a prediction for all words, unlike the rule based tagger, as for words the rule based tagger does not know the neural tagger is used.
            * For words that the neural tagger is used for it can be configured to generate a list of semantic tag prediction per word in most likely order. For instance you can pre-configure the tagger to generate the 4 or *N* most likely semantic tags for all words.
            * For words the the rule based tagger is used for it can generate USAS tags that contain affixed symbols like `+`, `-`, `%`, `@`, etc and multi membership tags that are denoted through the use of a slash `/`, e.g. `F2/O2`. For these words it can also identify and tag Multi Word Expressions. It is therefore also an explainable tagger for these words.
        </PositiveArea>
        <NegativeArea>
            * As on most texts it requires to run both the rule based and neural tagger it is the slowest of the three taggers.
            * As it requires both rule based and neural taggers, it requires the most resources, i.e. requires at least a lexicon for the rule based tagger, and a trained neural tagger.
            * As it uses the neural tagger requires additional disk space, memory (RAM/VRAM), and more processing time of which this is also dependent on the neural tagger size, the larger it is the more disk space, memory, and time required.
            * All neural taggers have been fine tuned on English data, which makes it less accurate for non-English data.
        </NegativeArea>
    </TabItem>
</Tabs>


The performance metrics for the 3 types of taggers for 4 different languages, these performance metrics reinforce the benefits and disadvantages using Top-N accuracy as the evaluation metric, whereby higher is better (100 is best);


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

Below you can find in the drop down box, a large table detailing the resource requirements of the taggers when ran/benchmarked using either the CPU or GPU on Wikipedia texts, specifically from the [HuggingFaceFW/finewiki dataset repository](https://huggingface.co/datasets/HuggingFaceFW/finewiki), we used Wikipedia as it has an open license and covers all of the languages that our taggers support. All of the memory statistics are in Mega Bytes (MB).

In general, from the table you can see that;
* The rule based taggers are the quickest and require the least memory
* The rule based taggers with MWE support are slower than the non-MWE taggers, e.g. Chinese (`cmn`) compared to French (`fr`). The larger the MWE lexicon that also has broad coverage the slower it is, e.g. English (`en`) compared to Chinese (`cmn`).
* The Chinese spaCy model requires more RAM than the other languages.
* The smallest English neural model (Neural-E-17M) is quicker than English rule based tagger.
* Using a GPU compared to CPU is quicker for Hybrid and Neural models.
* The Neural and Hybrid taggers require a lot of memory when processing a text that is very long, thus we advise to split a text up, e.g. using a sentence splitter, before running these taggers.

<details>
<summary>Resource requirements statistics</summary>

<Tabs
defaultValue="cpu"
values={[
    {label: 'CPU', value: 'cpu'},
    {label: 'GPU', value: 'gpu'}
]}>
    <TabItem value="cpu" label="CPU">

| Language | Tagger | Load Model Memory Requirements | Average Memory Requirements | Large Text Memory Requirements | Tokens Per Second | Number of Tokens Processed | Large Text Tokens Processed | Load Model GPU Memory Requirements | Average GPU Memory Requirements | Large Text GPU Memory Requirements |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| en| Rule Based| 167.98| 239.27| 210.25| 3,427.61| 100,866| 3,049| 0.00| 0.00| 0.00 |
| cmn| Rule Based| 447.89| 617.99| 561.73| 14,304.23| 103,015| 3,004| 0.00| 0.00| 0.00 |
| da| Rule Based| 135.69| 260.24| 116.89| 13,167.87| 100,003| 3,098| 0.00| 0.00| 0.00 |
| nl| Rule Based| 118.55| 227.26| 99.14| 31,501.24| 100,010| 3,015| 0.00| 0.00| 0.00 |
| fr| Rule Based| 252.42| 361.15| 364.08| 31,048.27| 100,119| 3,017| 0.00| 0.00| 0.00 |
| it| Rule Based| 133.99| 202.28| 132.24| 14,101.95| 101,134| 3,004| 0.00| 0.00| 0.00 |
| pt| Rule Based| 124.75| 136.16| 101.21| 14,699.95| 101,692| 3,006| 0.00| 0.00| 0.00 |
| es| Rule Based| 63.01| 116.35| 109.56| 13,901.97| 105,769| 3,044| 0.00| 0.00| 0.00 |
| fi| Rule Based| 146.83| 295.49| 145.79| 26,946.75| 100,368| 3,042| 0.00| 0.00| 0.00 |
| en| Neural-E-17M| 289.43| 1,264.57| 426.98| 3,962.53| 100,866| 3,049| 0.00| 0.00| 0.00 |
| en| Neural-E-68M| 481.97| 1,387.83| 809.92| 1,050.49| 100,866| 3,049| 0.00| 0.00| 0.00 |
| xx| Neural-M-140M| 1,101.14| 1,889.09| 1,884.47| 836.75| 100,866| 3,049| 0.00| 0.00| 0.00 |
| xx| Neural-M-304M| 955.84| 1,495.19| 1,604.79| 515.12| 100,866| 3,049| 0.00| 0.00| 0.00 |
| en| Hybrid-E-17M| 437.93| 1,090.82| 487.28 | 841.58| 100,866| 3,049| 0.00| 0.00| 0.00 |
| en| Hybrid-E-68M| 745.68| 1,598.41| 1,033.88 | 607.98| 100,866| 3,049| 0.00| 0.00| 0.00 |
| xx| Hybrid-M-140M| 1,480.70| 1,528.64| 2,298.70 | 793.95| 100,866| 3,049| 0.00| 0.00| 0.00 |
| xx| Hybrid-M-304M| 1,057.04| 1,849.71| 1,673.90 | 450.71 | 100,866| 3,049| 0.00| 0.00| 0.00 |

    </TabItem>
    <TabItem value="gpu" label="GPU">

| Language | Tagger | Load Model Memory Requirements | Average Memory Requirements | Large Text Memory Requirements | Tokens Per Second | Number of Tokens Processed | Large Text Tokens Processed | Load Model GPU Memory Requirements | Average GPU Memory Requirements | Large Text GPU Memory Requirements |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| en| Rule Based| 138.02| 125.20| 163.24| 3,419.45| 100,866| 1,533| 0.00| 0.00| 0.00 |
| cmn| Rule Based| 442.97| 540.37| 542.18| 13,837.79| 103,015| 1,502| 0.00| 0.00| 0.00 |
| da| Rule Based| 130.89| 176.18| 120.14| 13,004.09| 100,003| 1,570| 0.00| 0.00| 0.00 |
| nl| Rule Based| 133.16| 215.50| 114.63| 30,469.75| 100,010| 1,500| 0.00| 0.00| 0.00 |
| fr| Rule Based| 281.89| 310.44| 398.62| 30,963.86| 100,119| 1,523| 0.00| 0.00| 0.00 |
| it| Rule Based| 134.57| 154.14| 158.64| 13,963.39| 101,134| 1,521| 0.00| 0.00| 0.00 |
| pt| Rule Based| 110.93| 184.75| 121.99| 14,480.34| 101,692| 1,571| 0.00| 0.00| 0.00 |
| es| Rule Based| 119.37| 54.38| 149.06| 13,809.63| 105,769| 1,575| 0.00| 0.00| 0.00 |
| fi| Rule Based| 150.54| 307.13| 164.95| 26,633.59| 100,368| 1,500| 0.00| 0.00| 0.00 |
| en| Neural-E-17M| 289.43| 1,264.57| 426.98| 4,161.57| 100,866| 1,533| 65.11| 347.54| 2,910.08 |
| en| Neural-E-68M| 481.97| 1,387.83| 809.92| 1,993.60| 100,866| 1,533| 264.02| 1,005.18| 6,596.55 |
| xx| Neural-M-140M| 1,101.14| 1,889.09| 1,884.47| 1,713.40| 100,866| 1,533| 537.28| 1,324.89| 7,208.70 |
| xx| Neural-M-304M| 955.84| 1,495.19| 1,604.79| 1,720.66| 100,866| 1,533| 1,190.79| 2,544.10| 13,360.71 |
| en| Hybrid-E-17M| 437.93| 1,090.82| 487.28| 2,374.30| 100,866| 1,533| 65.11| 347.54| 2,909.96 |
| en| Hybrid-E-68M| 745.68| 1,598.41| 1,033.88| 1,829.27| 100,866| 1,533| 264.02| 1,007.17| 6,597.07 |
| xx| Hybrid-M-140M| 1,480.70| 1,528.64| 2,298.70| 1,679.67| 100,866| 1,533| 537.28| 1,324.40| 7,210.01 |
| xx| Hybrid-M-304M| 1,057.04| 1,849.71| 1,673.90| 1,678.30| 100,866| 1,533| 1,190.79| 2,544.10| 13,360.71 |

    </TabItem>

</Tabs>

Here we detail the meaning of each header in the markdown table;

* Language - The language code ([BCP 47 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)) of the Wikipedia data the tagger was processing, language codes are . **Note** for `xx` we use English.
* Tagger - The name of tagger type.
* Load Model Memory Requirements - The RAM/memory requirements to load the model.
* Average Memory Requirements - The RAM/memory requirements to load and run the model on the Wikipedia texts separated by new lines (not sentences therefore will be made up of multiple sentences, typically these represent paragraphs).
* Large Text Memory Requirements - The RAM/memory requirements to load and run the model on a single Wikipedia text that has been joined together from multiple Wikipedia texts to ensure the text is at least `--large-text-token-limit`.
* Tokens Per Second - Number of tokens the tagger processed per second.
* Number of Tokens Processed - Number of tokens processed to generate the `Tokens Per Second` metric, these tokens are from processing the Wikipedia texts separated by new lines, of which this is the same data that is used for `Average Memory Requirements`.
* Large Text Tokens Processed - The length in tokens of the large text that was processed to generate `Large Text Memory Requirements` metric.
* Load Model GPU Memory Requirements - The VRAM/GPU memory requirements to load the model.
* Average GPU Memory Requirements - The VRAM/GPU memory requirements to load and run the model on the Wikipedia texts separated by new lines (not sentences therefore will be made up of multiple sentences, typically these represent paragraphs).
* Large Text GPU Memory Requirements - The VRAM/GPU memory requirements to load and run the model on a single Wikipedia text that has been joined together from multiple Wikipedia texts to ensure the text is at least `--large-text-token-limit`.

:::note
The RAM/memory requirements are only estimates, but are a good guide. The reason they are only estimates as we cannot get the peak memory usage but rather the memory usage before and after a process has been completed, to get memory usage during the tagging process this would require running an external memory profiler, like [Scalene](https://github.com/plasma-umass/scalene) which we did not do here as it is difficult to get the memory requirement programmatically. For more accurate estimates you could run the [Scalene](https://github.com/plasma-umass/scalene) profile on an individual tagger benchmarking script, e.g. `scalene run benchmark_rule_based_tagger.py` (once you have installed `scalene`).
:::

These statistics were generated on a computer with an Nvidia 5070ti (16GB), 64GB DDR5 RAM, Intel Core Ultra 7 20 core 20 thread CPU, and 2TB PCIe Gen 5 SSD.

</details>



## Reading the documentation

How the documentation website is split between the Usage and API pages:

* [Usage](/) - The usage pages contains how-to-guides, and explanations.
* [API](/api/spacy_api/taggers/rule_based.md) - Are the docstrings of the PyMUSAS library, best pages to look at if you want to know exactly what a class / function / attribute does in more technical detail. These do contain examples, but the examples are more like minimum working examples rather than real world examples.


## Future Plans

Our [road map](https://github.com/UCREL/pymusas/blob/main/ROADMAP.md) contains the most up to date future plans for PyMUSAS.