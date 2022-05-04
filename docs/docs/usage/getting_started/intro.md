---
slug: /
title: Introduction
sidebar_position: 1
---

# PyMUSAS

**Py**thon **M**ultilingual **U**crel **S**emantic **A**nalysis **S**ystem, is a rule based token and Multi Word Expression (MWE) semantic tagger. The tagger can support any semantic tagset, however the tagset we have concentrated on and released pre-configured spaCy components for is the [Ucrel Semantic Analysis System (USAS)](https://ucrel.lancs.ac.uk/usas/).

PyMUSAS currently support 8 different languages with pre-configured spaCy components that can be downloaded, each language has it's own [guide on how to tag text using PyMUSAS](/usage/how_to/tag_text). Below we show the languages supported, if the model for that language supports MWE identification and tagging (all languages support token level tagging by default), and size of the model:

| Language (BCP 47 language code) | MWE Support | Size |
| --- | --- | --- |
| Mandarin Chinese (cmn) | :heavy_check_mark: | 1.28MB |
| Welsh (cy) | :heavy_check_mark: | 1.09MB |
| Spanish, Castilian (es) | :heavy_check_mark: | 0.20MB |
| French (fr) | :x: | 0.08MB |
| Indonesian (id) | :x: | 0.24MB |
| Italian (it) | :heavy_check_mark: | 0.50MB |
| Dutch, Flemish (nl) | :x: | 0.15MB |
| Portuguese (pt) | :heavy_check_mark: | 0.27MB |

## Reading the documentation

How the documentation website is split between the Usage and API pages:

* [Usage](/) - The usage pages contains how-to-guides, and explanations.
* [API](/api/spacy_api/taggers/rule_based) - Are the docstrings of the PyMUSAS library, best pages to look at if you want to know exactly what a class / function / attribute does in more technical detail. These do contain examples, but the examples are more like minimum working examples rather than real world examples.


## Future Plans

Our [road map](https://github.com/UCREL/pymusas/blob/main/ROADMAP.md) contains the most up to date future plans for PyMUSAS.