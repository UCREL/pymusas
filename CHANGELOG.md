# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- The documentation now has a `How-to` guide on `Tag CoNLL-U Files`.
- The documentation now has a `How-to Tag Text` guide for Finnish and English.
- The documentation now has a `How to Combine/Merge Lexicons` guide.
- Using [developer/dev containers](https://containers.dev/) of which the files for this can be found in the [.devcontainer folder](./.devcontainer). This will allow for easier on boarding and development consistency.
- Functional tests have been added and can be found in the following directory: [./tests/functional_tests/](./tests/functional_tests/)
- The ability to merge `LexiconCollection`s either through `pymusas.lexicon_collection.LexiconCollection.merge`.
- The ability to merge `LexiconCollection` data through a list of file paths to TSV files using `pymusas.lexicon_collection.LexiconCollection.tsv_merge`, which when merged will allow the creation of a combined `LexiconCollection` instance.
- The ability to merge `MWELexiconCollection` data through a list of file paths to TSV files using `pymusas.lexicon_collection.MWELexiconCollection.tsv_merge`, which when merged will allow the creation of a combined `MWELexiconCollection` instance.
- Added a usage example to the documentation showing how to combine/merge lexicon collections together and add them to a PyMUSAS rule based tagger.
- Added the extra group `neural` to the [pyproject.toml](./pyproject.toml) so that the required `torch`, `transformers`, and `wsd-torch-models` libraries are installed allowing the neural models to run.
- Added `pymusas.taggers.neural` module that includes the first Neural based tagger using the taggers from [WSD-Torch-Models](https://github.com/UCREL/WSD-Torch-Models).
- Added `pymusas.spacy_api.taggers.neural` module that includes the Neural based tagger that can be used as a spacy pipeline.
- Added `pymusas.taggers.hybrid` module that includes the first Hybrid based tagger, `pymusas.taggers.hybrid.HybridTagger`, which inherits from the `pymusas.taggers.rule-based.RuleBasedTagger` and uses the Neural tagger, `pymusas.taggers.neural.NeuralTagger`, when the rule based tagger does not know what to predict, i.e. when it usually predicts `Z99` it will now use the neural tagger.
- The CI pipeline `.github/workflows/ci.yml` now caches the Neural based tagger that we test (`ucrelnlp/PyMUSAS-Neural-English-Small-BEM`) so that it does not get downloaded each time the tests are ran for each Python version for each Operating System.
- Supports `Python 3.14`.
- `typer` Python package, this is a requirement from `spacy`, since version `3.8.7` (26th of May 2025) it had dropped the requirement for `typer` but instead used `typer-slim`, however `typer-slim` does not appear to work when imported `import typer` and it raises an error when we import `spacy`, thus the need to add `typer` as a requirement.
- `scripts/create_temporary_version.py` - this creates a temporary `pyproject.toml` with a unique version of the project so that functional testing through `make functional-tests` does not use a cached/out-dated version of the codebase once the code base has been built while still using cached Python packages for the packages `pymusas` depends on.
- `makefile` the target `functional-tests` has been removed and replaced with `full-coverage-tests`. The difference being that it will also run the unit tests and report coverage that uses the results from all of the tests, unit, functional, and documentation tests while using an install that has come a the built distribution. This code is also now used in the CI pipeline so that the coverage results are more representative.

### Changed

- [./scripts/py2md.py](./scripts/py2md.py) script has been updated so that it works with the newest version of Python that [pydoc_markdown](https://github.com/NiklasRosenstein/pydoc-markdown) supports, which is version 3.11. This required upgrading `pydoc_markdown` from version `4.6.0` to `>=4.7` which did come with some breaking changes for this repository hence the updates to the script. With the release of [uv](https://docs.astral.sh/uv/) the Python package manager we have made use of it's ability to have script level isolated virtual environments therefore removing any `py2md` script specific requirements from the dev/tests requirements that this package requires, e.g. `pydoc_markdown` requirement has been removed and is `py2md` script specific requirement. This also means that the [makefile](./makefile) has been changed to reflect this through the command `create-api-docs` which has been changed but it's functionility and use is the same.
- [github/workflows/documentation_check_build_deploy.yml](./.github/workflows/documentation_check_build_deploy.yml) has been added but this is a change to the original documentation build and deploy workflow. This workflow now uses [uv](https://docs.astral.sh/uv/) for managing Python as it runs the `py2md.py` script. It only deploys the documentation website when there are push events to the `main` branch rather than pull requests. In addition during the build test we save the build artifact, when we want to deploy we use that build artifact to save processing time.
- Removed the `Docs_Docker.dockerfile` as we have setup a DevContainer that encompasses all of the requirements that this Dockerfile provides. Therefore the [makefile](./makefile) commands that correspond to building/serving the documentation have been updated, along with the [documentation](./CONTRIBUTING.md).
- Removed the requirement for a docker container to validate the [CITATION.cff file](./CITATION.cff), now we use `uv tool run`, of which this has been documentated in [RELEASE_PROCESS.md](./RELEASE_PROCESS.md).
- Using [uv](https://docs.astral.sh/uv/) as the Python package manager and the package build front and back end replacing setup tools for the build backend.
- Setting the new version of PyMUSAS is through the [uv tool](https://docs.astral.sh/uv/guides/package/#updating-your-version) and this uses the version set in [./pyproject.toml](./pyproject.toml) rather than [./pymusas/__init__.py](./pymusas/__init__.py)
- [./scripts/release_notes.py script](./scripts/release_notes.py) has been updated so that it is isolated with respect to python packages that are required to be installed. This has been doing through the makefile, CI commands in the GitHub action, and the script itself containing it's own dependencies.
- The publishing and release process now uses `uv`. The version of PyMUSAS is fully determined by the `TAG` environment variable. 
- The unit tests have been moved to [./tests/unit_tests/](./tests/unit_tests/) from `./tests`
- `pyproject.toml` - we do not support `pytest` version `9.0.2` it appears to generate an error when testing entry points.

### Fixed

- All of the semantic lexicon resources that are referenced in the code base as documentation strings or tests and the documentation itself are now linked to a commit hash, e.g. for the Welsh semantic lexicons rather than it being originally linked to the head reference; https://raw.githubusercontent.com/UCREL/Multilingual-USAS/refs/heads/master/Welsh/semantic_lexicon_cy.tsv it is now linked to a commit hash; https://raw.githubusercontent.com/UCREL/Multilingual-USAS/64dbdf19d8d090c6f4183984ff16529d09f77b02/Welsh/semantic_lexicon_cy.tsv. This makes the tests, documentation tests, and the documentation itself more reproducible and reliable.

### Removed

- `Docs_Docker.dockerfile` - see the Changed section above for the reason.
- `requirements.txt`, `dev_requirements.txt`, and `setup.cfg`. These files are no longer needed as we have moved to using [uv](https://docs.astral.sh/uv/) as the Python package manager, and using [./pyproject.toml](./pyproject.toml) to store all of the packages's requirements and build dependencies.

## [v0.3.0](https://github.com/UCREL/pymusas/releases/tag/v0.3.0) - 2022-05-04

### Added

- Roadmap added.
-  Define the MWE template and it's syntax, this is stated in `Notes -> Multi Word Expression Syntax` in the `Usage` section of the documentation. This is the first task of issue [#24](https://github.com/UCREL/pymusas/issues/24).
- [PEP 561](https://peps.python.org/pep-0561/) (Distributing and Packaging Type Information) compatible by adding `py.typed` file.
- Added [srsly](https://github.com/explosion/srsly) as a pip requirement, we use srsly to serialise components to bytes, for example the `pymusas.lexicon_collection.LexiconCollection.to_bytes` function uses `srsly` to serialise the `LexiconCollection` to `bytes`.
- An abstract class, `pymusas.base.Serialise`, that requires sub-classes to create two methods `to_bytes` and `from_bytes` so that the class can be serialised. 
- `pymusas.lexicon_collection.LexiconCollection` has three new methods `to_bytes`, `from_bytes`, and `__eq__`. This allows the collection to be serialised and to be compared to other collections.
- A Lexicon Collection class for Multi Word Expression (MWE), `pymusas.lexicon_collection.MWELexiconCollection`, which allows a user to easily create and / or load in from a TSV file a MWE lexicon, like the MWE lexicons from the [Multilingual USAS repository](https://github.com/UCREL/Multilingual-USAS). In addition it contains the functionality to match a MWE template to templates stored in the `MWELexiconCollection` class following the MWE special syntax rules, this is all done through the `mwe_match` method. It also supports Part Of Speech mapping so that you can map from the lexicon's POS tagset to the tagset of your choice, in both a one-to-one and one-to-many mapping. Like the `pymusas.lexicon_collection.LexiconCollection` it contains `to_bytes`, `from_bytes`, and `__eq__` methods for serialisation and comparisons.
- The rule based taggers have now been componentised so that they are based off a `List` of `Rule`s and a `Ranker` whereby each `Rule` defines how a token(s) in a text can be matched to a semantic category. Given the matches from the `Rule`s the for each token, a token can have zero or more matches, the `Ranker` ranks each match and finds the global best match for each token in the text. The taggers now support direct match and wildcard Multi Word Expressions. Due to this:
    - `pymusas.taggers.rule_based.USASRuleBasedTagger` has been changed and re-named to `pymusas.taggers.rule_based.RuleBasedTagger` and now only has a `__call__` method.
    - `pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger` has been changed and re-named to `pymusas.spacy_api.taggers.rule_based.RuleBasedTagger`.
- A Rule system, of which all rules can be found in `pymusas.taggers.rules`:
    - `pymusas.taggers.rules.rule.Rule` an abstract class that describes how other sub-classes define the `__call__` method and it's signature. This abstract class is sub-classed from `pymusas.base.Serialise`.
    - `pymusas.taggers.rules.single_word.SingleWordRule` a concrete sub-class of `Rule` for finding Single word lexicon entry matches.
    - `pymusas.taggers.rules.mwe.MWERule` a concrete sub-class of `Rule` for finding Multi Word Expression entry matches.
- A Ranking system, of which all of the components that are linked to ranking can be found in `pymusas.rankers`:
    - `pymusas.rankers.ranking_meta_data.RankingMetaData` describes a lexicon entry match, that are typically generated from `pymusas.taggers.rules.rule.Rule` classes being called. These matches indicate that some part of a text, one or more tokens, matches a lexicon entry whether that is a Multi Word Expression or single word lexicon.
    - `pymusas.rankers.lexicon_entry.LexiconEntryRanker` an abstract class that describes how other sub-classes should rank each token in the text and the expected output through the class's `__call__` method. This abstract class is sub-classed from `pymusas.base.Serialise`.
    - `pymusas.rankers.lexicon_entry.ContextualRuleBasedRanker` a concrete sub-class of `LexiconEntryRanker` based off the ranking rules from [Piao et al. 2003](https://aclanthology.org/W03-1807.pdf).
    - `pymusas.rankers.lexical_match.LexicalMatch` describes the lexical match within a `pymusas.rankers.ranking_meta_data.RankingMetaData` object.
- `pymusas.utils.unique_pos_tags_in_lexicon_entry` a function that given a lexicon entry, either Multi Word Expression or Single word, returns a `Set[str]` of unique POS tags in the lexicon entry.
- `pymusas.utils.token_pos_tags_in_lexicon_entry` a function that given a lexicon entry, either Multi Word Expression or Single word, yields a `Tuple[str, str]` of word and POS tag from the lexicon entry.
- A mapping from USAS core to [Universal Part Of Speech (UPOS) tagset](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf).
- A mapping from USAS core to [basic CorCenCC POS tagset](https://cytag.corcencc.org/tagset?lang=en).
- A mapping from USAS core to [Penn Chinese Treebank POS tagset](https://verbs.colorado.edu/chinese/posguide.3rd.ch.pdf) tagset.
- `pymusas.lexicon_collection.LexiconMetaData`, object that contains all of the meta data about a single or Multi Word Expression lexicon entry.
- `pymusas.lexicon_collection.LexiconType` which describes the different types of single and Multi Word Expression (MWE) lexicon entires and templates that PyMUSAS uses or will use in the case of curly braces.
- The usage documentation, for the "How-to Tag Text", has been updated so that it includes an Indonesian example which does not use spaCy instead uses the [Indonesian TreeTagger](https://github.com/UCREL/Indonesian-TreeTagger-Docker-Build).
- spaCy registered functions for reading in a `LexiconCollection` or `MWELexiconCollection` from a TSV. These can be found in `pymusas.spacy_api.lexicon_collection`.
- spaCy registered functions for creating `SingleWordRule` and `MWERule`. These can be found in `pymusas.spacy_api.taggers.rules`.
- spaCy registered function for creating `ContextualRuleBasedRanker`. This can be found in `pymusas.spacy_api.rankers`.
- spaCy registered function for creating a `List` of `Rule`s, this can be found here: `pymusas.spacy_api.taggers.rules.rule_list`.
- `LexiconCollection` and `MWELexiconCollection` open the TSV file downloaded through `from_tsv` method by default using `utf-8` encoding.
- `pymusas_rule_based_tagger` is now a spacy registered factory by using an entry point.
- `MWELexiconCollection` warns users that it does not support curly braces MWE template expressions.
- All of the POS mappings can now be called through a spaCy registered function, all of these functions can be found in the `pymusas.spacy_api.pos_mapper` module.
- Updated the `Introduction` and `How-to Tag Text` usage documentation with the new updates that PyMUSAS now supports, e.g. MWE's. Also the `How-to Tag Text` is updated so that it uses the pre-configured spaCy components that have been created for each language, this spaCy components can be found and downloaded from the [pymusas-models repository](https://github.com/UCREL/pymusas-models).


### Removed

- `pymusas.taggers.rule_based.USASRuleBasedTagger` this is now replaced with `pymusas.taggers.rule_based.RuleBasedTagger`.
- `pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger` this is now replaced with `pymusas.spacy_api.taggers.rule_based.RuleBasedTagger`.
- `Using PyMUSAS` usage documentation page as it requires updating.

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
- `pymusas.lexicon_collection.LexiconEntry` which describes the data that is normally added to a `pymusas.lexicon_collection.LexiconCollection`.
- POS mapping module, `pymusas.pos_mapper`, that contains a mapping between [Universal Part Of Speech (UPOS) tagset](http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf) and the USAS core POS tagset.
- The [documentation website](https://ucrel.github.io/pymusas/) has been created.