# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- The usage documentation, for the "How-to Tag Text", has been updated so that it includes an Indonesian example which does not use spaCy instead uses the [Indonesian TreeTagger](https://github.com/UCREL/Indonesian-TreeTagger-Docker-Build).

## [v0.2.0](https://github.com/UCREL/pymusas/releases/tag/v0.2.0) - 2022-01-18

### Added

- Release process guide adapted from the [AllenNLP release process guide](https://github.com/allenai/allennlp/blob/2cdb8742c8c8c3c38ace4bdfadbdc750a1aa2475/RELEASE_PROCESS.md), many thanks to the AllenNLP team for creating the original guide.
- A mapping from the [basic CorCenCC POS tagset](https://cytag.corcencc.org/tagset?lang=en) to USAS core POS tagset.
- The usage documentation, for the "How-to Tag Text", has been updated so that it includes a Welsh example which does not use spaCy instead uses the [CyTag toolkit](https://github.com/UCREL/CyTag).
- A mapping from the [Penn Chinese Treebank POS tagset](https://verbs.colorado.edu/chinese/posguide.3rd.ch.pdf) to USAS core POS tagset.
- In the documentation it clarifies that we used the [Universal Dependencies Treebank](https://universaldependencies.org/u/pos/) version of the UPOS tagset rather than the original version from the [paper by Petrov et al. 2012](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf).
- The usage documentation, for the "How-to Tag Text", has been updated so that the Chinese example includes using POS information.
- A `CHANGELOG` file has been added. The format of the `CHANGELOG` file will now be used for the formats of all current and future GitHub release notes. For more information on the `CHANGELOG` file format see [Keep a Changelog.](https://keepachangelog.com/en/1.0.0/)

## [v0.1.0](https://github.com/UCREL/pymusas/releases/tag/v0.1.0) - 2021-12-07

### Added

- A rule based tagger that has been built in two different ways:
    - As a spaCy component that can be added to a spaCy pipeline, `pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger`
    - A non-spaCy version, `pymusas.taggers.rule_based.USASRuleBasedTagger`
- Usage guides for the spaCy version of the rule based tagger, which can be found within the [documentation website](https://ucrel.github.io/pymusas/).
- A Lexicon Collection class, `pymusas.lexicon_collection.LexiconCollection`, which allows a user to easily create and / or load in from a TSV file a lexicon, like the single word lexicons from the [Multilingual USAS repository](https://github.com/UCREL/Multilingual-USAS).
- POS mapping module, `pymusas.pos_mapper`, that contains a mapping between [Universal Part Of Speech (UPOS) tagset](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf) and the USAS core POS tagset.
- The [documentation website](https://ucrel.github.io/pymusas/) has been created.