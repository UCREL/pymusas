# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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