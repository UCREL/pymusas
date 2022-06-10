# PyMUSAS Roadmap

This document outlines our high level plans for expected developments in PyMUSAS.

## Completed development (with UCREL research centre funding)

- v0.1: Semantic tagger framework implementing single word lexicon using spaCy POS tagger and lemmatisers for Chinese, Dutch, French, Italian, Portuguese, Spanish (released 7th December 2021)
- v0.2: Semantic tagger framework using external POS tagger and lemmatisers (released 18th January 2022) with exemplars for Welsh (using CorCenCC CyTag) and Indonesian (using TreeTagger)
- v0.3: Semantic tagger framework implementing Multi Word Expression (MWE) lexicons for languages where we currently have MWE lexicons: Chinese, Italian, Portuguese, Spanish, Welsh plus to support loading of models (released 4th May 2022)
- Inclusion of the Finnish semantic lexicons and spaCy tagging pipeline into pymusas (released 11th May 2022)
- Open release of the English semantic lexicons in the [Multilingual USAS repository](https://github.com/UCREL/Multilingual-USAS) (released 1st June 2022)
- Incorporation of English semantic tagger into the pymusas spaCy pipeline (released 2nd June 2022)

## Ongoing development (by end June 2022)

- Set up simple web page interface on http://ucrel-api.lancaster.ac.uk/ and REST API

## Future development (in 2022 or later; funding dependent)

- Further development of Spanish, German, French, Dutch and Danish system and lexicons
- Further extensions to other languages or to incorporate POS taggers and lemmatisers beyond the list of languages supported by spaCy: Finnish (with a new compound engine), Arabic (with CAMeL tools), Korean, Persian, Spanish (with Grampal POS tagger), Urdu (with UNLT POS tagger)
- Further disambiguation methods e.g. vector based, machine learning, deep learning
- Creation and release of gold and/or silver standard corpora
- Inclusion into Wmatrix
