"""
Functions to build or load the rule based tagger and to measure its memory.

This module only imports spaCy, pymusas, and psutil, as the memory of the
tagger is measured in fresh processes that import this module, and so any
other import would add to the measured memory.

This module must also run against the latest released version of pymusas, see
the module docstring of `evaluation_utils`.
"""
from dataclasses import dataclass
from enum import Enum
import importlib.metadata
import multiprocessing
from pathlib import Path
import sys
from typing import cast
import warnings

import psutil
import spacy

from pymusas.file_utils import download_url_file
from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.taggers.rules.single_word import SingleWordRule


PYMUSAS_PIPE_NAME = "pymusas_rule_based_tagger"
PRE_BUILT_MODEL_NAME = "en_dual_none_contextual_none"

DEFAULT_LEXICON_REPO = "apmoore1/Multilingual-USAS"
DEFAULT_LEXICON_COMMIT = "73d2313fa356acaef30e838f001b10ecd8188935"

class TaggerType(str, Enum):
    lexicons = "lexicons"
    pymusas_model = "pymusas-model"



@dataclass(frozen=True)
class TaggerConfig:
    """
    The configuration of the rule based tagger to evaluate.

    Args:
        tagger_type (TaggerType): Whether the tagger is built from the lexicon
            files or loaded from the pre-built pymusas-models model.
        spacy_model (str): Name of the spaCy model that provides the POS tags and lemmas.
        lexicon_repo (str | None): The GitHub repository of the lexicon files,
            only used when `tagger_type` is `lexicons`.
        lexicon_commit (str | None): The commit of the lexicon files, only used
            when `tagger_type` is `lexicons`.
        autotag (bool): Whether to use the autotag lexicon, only used when
            `tagger_type` is `lexicons`.
    """
    tagger_type: TaggerType
    spacy_model: str
    lexicon_repo: str | None = None
    lexicon_commit: str | None = None
    autotag: bool = False

    def lexicon_urls(self) -> dict[str, str]:
        """
        Returns the URLs of the English lexicon files to use, keyed by the type
        of lexicon: `single`, `mwe`, and when `autotag` is True `autotag`.

        Raises:
            ValueError: If the lexicon repository or commit is not set.
        """
        if self.lexicon_repo is None or self.lexicon_commit is None:
            raise ValueError("The lexicon repository and commit are required "
                             "to build a tagger from lexicon files.")
        base_url = f"https://raw.githubusercontent.com/{self.lexicon_repo}/{self.lexicon_commit}/English"
        urls = {
            "single": f"{base_url}/semantic_lexicon_en.tsv",
            "mwe": f"{base_url}/mwe-en.tsv",
        }
        if self.autotag:
            urls["autotag"] = f"{base_url}/semantic_lexicon_en_autotag.tsv"
        return urls

    def label(self) -> str:
        """
        Returns a short human readable name of the tagger configuration, e.g.
        `lexicons@73d2313 + autotag`.
        """
        match self.tagger_type:
            case TaggerType.pymusas_model:
                model_version = importlib.metadata.version(PRE_BUILT_MODEL_NAME)
                return f"pymusas-models {PRE_BUILT_MODEL_NAME} {model_version}"
            case TaggerType.lexicons:
                commit = (self.lexicon_commit or "")[:7]
                label = f"lexicons@{commit}"
                if self.autotag:
                    label += " + autotag"
                return label



@dataclass
class MemoryStats:
    """
    The memory, in MB, required to load and run the whole pipeline, i.e. the
    spaCy model that creates the tokens, POS tags, and lemmas, and the pymusas
    tagger. It is the peak memory of a fresh process, which only imports
    spaCy, pymusas, and psutil, at two points in time:

    * `load_peak_memory`, after loading the spaCy model and the tagger.
    * `peak_memory`, after also running the pipeline over the finewiki sample.
      This is the memory required to run pymusas.
    """
    load_peak_memory: float
    peak_memory: float



def load_spacy_model(spacy_model: str) -> spacy.Language:
    """
    Loads the spaCy model that provides the POS tags and lemmas, without the
    parser and named entity recogniser as they are not needed.

    Args:
        spacy_model (str): Name of the spaCy model.

    Returns:
        spacy.Language: The loaded spaCy model.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return spacy.load(spacy_model, exclude=["parser", "ner"])


def add_lexicon_tagger(nlp: spacy.Language, config: TaggerConfig) -> None:
    """
    Builds the rule based tagger from the lexicon files and adds it to the
    end of the spaCy pipeline.

    Args:
        nlp (spacy.Language): The spaCy pipeline to add the tagger to.
        config (TaggerConfig): The tagger configuration.
    """
    lexicon_paths = {lexicon_type: download_url_file(url)
                     for lexicon_type, url in config.lexicon_urls().items()}
    lexicon_lookup = LexiconCollection.from_tsv(lexicon_paths["single"], include_pos=True)
    lemma_lexicon_lookup = LexiconCollection.from_tsv(lexicon_paths["single"], include_pos=False)
    mwe_lexicon_lookup = MWELexiconCollection.from_tsv(lexicon_paths["mwe"])

    single_word_rule = SingleWordRule(lexicon_lookup, lemma_lexicon_lookup)
    if config.autotag:
        # Only exists in newer versions of pymusas, see module docstring.
        from pymusas.lexicon_collection import AutotagLexiconCollection
        autotag_lexicon_lookup = AutotagLexiconCollection.from_tsv(lexicon_paths["autotag"])
        single_word_rule = SingleWordRule(lexicon_lookup, lemma_lexicon_lookup,
                                          autotag_lexicon_collection=autotag_lexicon_lookup)

    rules: list[Rule] = [single_word_rule, MWERule(mwe_lexicon_lookup)]
    ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
    tagger = cast(RuleBasedTagger, nlp.add_pipe(PYMUSAS_PIPE_NAME))
    tagger.initialize(rules=rules, ranker=ranker,
                      default_punctuation_tags=["PUNCT"],
                      default_number_tags=["NUM"])


def add_pre_built_tagger(nlp: spacy.Language) -> None:
    """
    Adds the rule based tagger from the pre-built pymusas-models model to the
    end of the spaCy pipeline.

    Args:
        nlp (spacy.Language): The spaCy pipeline to add the tagger to.

    Raises:
        OSError: If the pre-built model is not installed.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            pre_built_model = spacy.load(PRE_BUILT_MODEL_NAME)
        except OSError as error:
            raise OSError(f"The pre-built model `{PRE_BUILT_MODEL_NAME}` is not installed. "
                          "It is evaluated in its own isolated environment, "
                          "see `benchmarks/evaluation/run_evaluation.sh`.") from error
        nlp.add_pipe(PYMUSAS_PIPE_NAME, source=pre_built_model)


def add_tagger(nlp: spacy.Language, config: TaggerConfig) -> None:
    """
    Adds the rule based tagger described by the `config` to the end of the
    spaCy pipeline.

    Args:
        nlp (spacy.Language): The spaCy pipeline to add the tagger to.
        config (TaggerConfig): The tagger configuration.
    """
    match config.tagger_type:
        case TaggerType.lexicons:
            add_lexicon_tagger(nlp, config)
        case TaggerType.pymusas_model:
            add_pre_built_tagger(nlp)


def get_tagger(nlp: spacy.Language) -> RuleBasedTagger:
    """
    Returns the pymusas rule based tagger within the spaCy pipeline.
    """
    return cast(RuleBasedTagger, nlp.get_pipe(PYMUSAS_PIPE_NAME))



def get_peak_memory_mb() -> float:
    """
    Returns the peak memory of this process, over its lifetime, in MB.

    On Linux the peak is read from `VmHWM` in `/proc/self/status` rather than
    `ru_maxrss` from `resource.getrusage`, as `ru_maxrss` is preserved across
    `execve`, therefore a process started by multiprocessing's `spawn` (a fork
    then an exec) would report the peak memory of the process it was forked
    from if that was larger. `VmHWM` belongs to the process's address space,
    which `execve` replaces.

    If `VmHWM` is not available on Linux, e.g. in a sandbox with a restricted
    `/proc`, or on any other platform, `ru_maxrss` is used instead. It is
    preserved across `execve`, so in the process that `measure_memory` spawns
    it can over-report, as it is never lower than the parent's memory at the
    time of the spawn.
    """
    if sys.platform == "win32":
        return psutil.Process().memory_info().peak_wset / (1024 ** 2)
    if sys.platform == "linux":
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmHWM:"):
                # Reported in kilobytes, e.g. `VmHWM:    123456 kB`
                return int(line.split()[1]) / 1024
    import resource
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports `ru_maxrss` in bytes, Linux and the BSDs in kilobytes
    divisor = 1024 ** 2 if sys.platform == "darwin" else 1024
    return max_rss / divisor


def _measure_pipeline_memory(config: TaggerConfig, texts: list[str]) -> tuple[float, float]:
    """
    Returns the peak memory, in MB, of this process after loading the spaCy
    model and the tagger, and after also running the pipeline over the texts.
    This should be run in a fresh process.
    """
    nlp = load_spacy_model(config.spacy_model)
    add_tagger(nlp, config)
    load_peak_memory = get_peak_memory_mb()
    for _ in nlp.pipe(texts):
        pass
    return load_peak_memory, get_peak_memory_mb()


def measure_memory(config: TaggerConfig, texts: list[str]) -> MemoryStats:
    """
    Measures the memory required to load and run the whole pipeline, the
    spaCy model and the tagger, over the texts within a fresh process, see
    `MemoryStats`.

    Args:
        config (TaggerConfig): The tagger configuration.
        texts (list[str]): The texts to tag.

    Returns:
        MemoryStats: The memory statistics.
    """
    with multiprocessing.get_context("spawn").Pool(1) as pool:
        load_peak_memory, peak_memory = pool.apply(_measure_pipeline_memory, (config, texts))
    return MemoryStats(load_peak_memory=round(load_peak_memory, 2),
                       peak_memory=round(peak_memory, 2))
