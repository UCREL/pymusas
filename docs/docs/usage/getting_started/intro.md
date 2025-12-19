---
slug: /
title: Introduction
sidebar_position: 1
---

# PyMUSAS

**Py**thon **M**ultilingual **U**crel **S**emantic **A**nalysis **S**ystem, is a semantic tagging framework that contains various different semantic taggers; rule based, neural network, and a hybrid of the two, of which all but the neural network can identify and tag Multi Word Expressions (MWE). The taggers can support any semantic tagset, however the tagset we have concentrated on and released pre-configured spaCy components for is the [Ucrel Semantic Analysis System (USAS)](https://ucrel.lancs.ac.uk/usas/).

Below we describe the different semantic taggers we supported and the pre-configured models we have released for each semantic tagger, as well how to read and navigate the documentation website.

## Semantic Taggers

As mentioned we have 3 different taggers; rule based, neural network (neural), and hybrid.

### Rule Based

The rule based tagger supports both single token and MWE and is a re-implementation of the USAS rule based tagger that has been developed in C and then Java programming languages by [Paul Rayson](https://www.lancaster.ac.uk/sci-tech/about-us/people/paul-rayson) and [Scott Piao](https://www.lancaster.ac.uk/sci-tech/about-us/people/scott-piao), of which it is heavily based on the rules from [Extracting Multiword Expressions with A Semantic Tagger by Scott Piao et al. 2003](https://aclanthology.org/W03-1807.pdf). For more information on exactly how the tagger works please read the API documentation specifically the [RuleBasedTagger class](/api/spacy_api/taggers/rule_based#rulebasedtagger) and the [Contextual Ranker class](/api/rankers/lexicon_entry#contextualrulebasedranker).

PyMUSAS currently support 11 different languages for the rule based tagger with pre-configured spaCy components that can be downloaded, each language has it's own [guide on how to tag text using PyMUSAS](/usage/how_to/tag_text). Below we show the languages supported, if the model for that language supports MWE identification and tagging (all languages support single token level tagging by default), and size of the model:

| Language (BCP 47 language code) | MWE Support | Size |
| --- | --- | --- |
| Mandarin Chinese (cmn) | :heavy_check_mark: | 1.28MB |
| Danish (da) | :heavy_check_mark: | 0.85MB |
| Dutch, Flemish (nl) | :x: | 0.15MB |
| English (en) | :heavy_check_mark: | 0.86MB |
| Finnish (fi) | :x: | 0.64MB |
| French (fr) | :x: | 0.08MB |
| Indonesian (id) | :x: | 0.24MB |
| Italian (it) | :heavy_check_mark: | 0.50MB |
| Portuguese (pt) | :heavy_check_mark: | 0.27MB |
| Spanish, Castilian (es) | :heavy_check_mark: | 0.26MB |
| Welsh (cy) | :heavy_check_mark: | 1.10MB |

## Reading the documentation

How the documentation website is split between the Usage and API pages:

* [Usage](/) - The usage pages contains how-to-guides, and explanations.
* [API](/api/spacy_api/taggers/rule_based) - Are the docstrings of the PyMUSAS library, best pages to look at if you want to know exactly what a class / function / attribute does in more technical detail. These do contain examples, but the examples are more like minimum working examples rather than real world examples.


## Future Plans

Our [road map](https://github.com/UCREL/pymusas/blob/main/ROADMAP.md) contains the most up to date future plans for PyMUSAS.