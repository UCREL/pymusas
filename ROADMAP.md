# PyMUSAS Roadmap

This document outlines our high level plans for expected developments in PyMUSAS.

## Completed development

- v0.1: Semantic tagger framework implementing single word lexicon using spaCy POS tagger and lemmatisers for Chinese, Dutch, French, Italian, Portuguese, Spanish (released 7th December 2021)
- v0.2: Semantic tagger framework using external POS tagger and lemmatisers (released 18th January 2022) with exemplars for Welsh (using CorCenCC CyTag) and Indonesian (using TreeTagger)

## Ongoing development (as at March 2022)

- v0.3: Semantic tagger framework implementing MWE lexicon for languages where we currently have MWE lexicons: Chinese, Italian, Portuguese, Spanish, Welsh

## Future development (by end June 2022; with current UCREL research centre funding)

- Set up simple web page interface on http://ucrel-api.lancaster.ac.uk/ and REST API
- Open release of the English USAS semantic lexicon
- Incorporation of English semantic tagger into spaCy pipeline

## Future development (in 2022 or later; funding dependent)

- Further development of Spanish, German, French, Dutch and Danish system and lexicons
- Further extensions to other languages or to incorporate POS taggers and lemmatisers beyond the list of languages supported by spaCy: Finnish (with a new compound engine), Arabic (with CAMeL tools), Korean, Persian, Spanish (with Grampal POS tagger), Urdu (with UNLT POS tagger)
- Further disambiguation methods e.g. vector based, machine learning, deep learning
- Creation and release of gold and/or silver standard corpora
- Inclusion into Wmatrix
