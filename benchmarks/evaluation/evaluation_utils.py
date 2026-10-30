"""
Functions shared by the evaluation scripts in this directory.

This module must also run against the latest released version of pymusas, as
the pre-built model baseline is evaluated in an isolated environment that has
the released pymusas installed rather than this repository's working tree.
Therefore any import from pymusas that only exists in newer versions of
pymusas has to be imported within the function that uses it.
"""
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from enum import Enum
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import time
from typing import Any, cast

from huggingface_hub import HfFileSystem
import pyarrow.parquet as pq
import spacy
from spacy.tokens import Doc
from tagger_utils import (
    PYMUSAS_PIPE_NAME,
    MemoryStats,
    TaggerConfig,
    TaggerType,
    get_tagger,
    measure_memory,
)
from usas_evaluation_framework.data_utils import load_usas_mapper, parse_usas_token_group
from usas_evaluation_framework.dataset import EvaluationDataset, EvaluationTexts
from usas_evaluation_framework.metrics.top_n_accuracy import top_n_accuracy
from usas_evaluation_framework.parsers.benedict import EnglishBenedict
from usas_evaluation_framework.parsers.english_wikipedia import EnglishWikipediaUSAS

import pymusas
from pymusas.config import PYMUSAS_CACHE_HOME
from pymusas.file_utils import download_url_file
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.rankers.ranking_meta_data import RankingMetaData
from pymusas.spacy_api.taggers.rule_based import RuleBasedTagger
from pymusas.taggers.rules.rule import Rule


EVALUATION_FRAMEWORK_COMMIT = "08f95072f74afefdb4b1207e8320938f860f940e"
EVALUATION_FRAMEWORK_DATA_URL = ("https://raw.githubusercontent.com/UCREL/USAS-Evaluation-Framework/"
                                 f"{EVALUATION_FRAMEWORK_COMMIT}/tests/data/parsers")
# Name of each gold dataset to the URL of its data and the parser for that data.
GOLD_DATASETS = {
    "Benedict English": (f"{EVALUATION_FRAMEWORK_DATA_URL}/benedict/english/benedict_english_corpus.txt",
                         EnglishBenedict.parse),
    "English Wikipedia": (f"{EVALUATION_FRAMEWORK_DATA_URL}/english_wikipedia/english_wikipedia_corpus.csv",
                          EnglishWikipediaUSAS.parse),
}

FINEWIKI_DATASET_ID = "HuggingFaceFW/finewiki"
DEFAULT_FINEWIKI_REVISION = "8bd13e72e6a002407649b3e898535f42ceb1aeb9"
FINEWIKI_ENGLISH_FILE = "data/enwiki/000_00000.parquet"
# Upper bound on the sample size, so that a mistyped limit does not stream a
# very large amount of data from the HuggingFace Hub.
MAX_FINEWIKI_TOKEN_LIMIT = 500_000

# Semantic tags that represent punctuation, either can be used.
PUNCTUATION_TAGS = frozenset({"PUNCT", "Z9"})
UNKNOWN_TAG = "Z99"


class TextUnit(str, Enum):
    paragraph = "paragraph"
    document = "document"


@dataclass
class CoverageCounts:
    """
    Number of tokens, and of those the number that were matched by a lexicon
    rule (`lexicon_matched`) and the number that were not tagged `Z99`
    (`tag_covered`).
    """
    tokens: int = 0
    lexicon_matched: int = 0
    tag_covered: int = 0

    def add(self, lexicon_matched: bool, tag_covered: bool) -> None:
        self.tokens += 1
        self.lexicon_matched += int(lexicon_matched)
        self.tag_covered += int(tag_covered)


@dataclass
class GoldDataset:
    """
    A gold dataset to evaluate against.

    Args:
        name (str): Name of the dataset.
        accuracy_gold (EvaluationDataset): The gold dataset with the punctuation
            (`PUNCT` and `Z9`) and `Z99` labels filtered out, used for accuracy.
        punctuation (list[list[bool]]): For each text, whether each token has a
            gold punctuation label (`PUNCT` or `Z9`).
    """
    name: str
    accuracy_gold: EvaluationDataset
    punctuation: list[list[bool]]


@dataclass
class GoldResult:
    dataset: str
    tokens: int
    punctuation_excluded: int
    scored_tokens: int
    accuracy: dict[str, float]
    coverage: dict[str, CoverageCounts]


@dataclass
class DiskStats:
    """
    Disk statistics in MB, `lexicon_files` is `None` for a pre-built model.
    """
    saved_pipe: float
    lexicon_files: float | None


@dataclass
class FinewikiResult:
    revision: str
    text_unit: str
    texts: int
    tokens: int
    pymusas_seconds: float
    preprocess_seconds: float
    pymusas_tokens_per_second: float
    full_pipeline_tokens_per_second: float
    coverage: dict[str, CoverageCounts]
    memory: MemoryStats
    disk: DiskStats


@dataclass
class EvaluationResult:
    tagger: str
    tagger_type: str
    pymusas_version: str
    pymusas_install: str
    python_hash_seed: str | None
    spacy_model: str
    spacy_model_version: str
    lexicon_repo: str | None
    lexicon_commit: str | None
    autotag: bool
    gold: list[GoldResult] = field(default_factory=list)
    finewiki: FinewikiResult | None = None


def load_gold_datasets() -> list[GoldDataset]:
    """
    Downloads and parses the English gold datasets from the USAS Evaluation
    Framework.

    Each dataset is parsed twice, once with the punctuation (`PUNCT` and `Z9`)
    and `Z99` labels filtered out, which is used for accuracy, and once with
    only `Z99` filtered out, which is used to find the tokens that have a gold
    punctuation label.

    Returns:
        list[GoldDataset]: The gold datasets.
    """
    label_validation = set(load_usas_mapper(None, {UNKNOWN_TAG}).keys())
    accuracy_label_filter = set(PUNCTUATION_TAGS) | {UNKNOWN_TAG}

    gold_datasets: list[GoldDataset] = []
    for name, (url, parser) in GOLD_DATASETS.items():
        dataset_path = Path(download_url_file(url))
        accuracy_gold = parser(dataset_path, label_validation, accuracy_label_filter, name, "English")
        all_labels_gold = parser(dataset_path, label_validation, {UNKNOWN_TAG}, name, "English")
        if not accuracy_gold.text_tokens_equal(all_labels_gold):
            raise ValueError(f"The tokens of the {name} dataset differ between label filters.")

        punctuation: list[list[bool]] = []
        for text in all_labels_gold.texts:
            semantic_tags = text.semantic_tags or [[] for _ in text.tokens]
            punctuation.append([any(tag in PUNCTUATION_TAGS for tag in tags)
                                for tags in semantic_tags])
        gold_datasets.append(GoldDataset(name, accuracy_gold, punctuation))
    return gold_datasets


def _finewiki_cache_path(revision: str, token_limit: int, text_unit: TextUnit) -> Path:
    file_name = f"finewiki_en_{revision[:12]}_{token_limit}_{text_unit.value}.json"
    return Path(PYMUSAS_CACHE_HOME, "evaluation", file_name)


def load_finewiki_sample(token_limit: int, revision: str, text_unit: TextUnit) -> list[str]:
    """
    Returns a sample of English Wikipedia texts from the finewiki dataset that
    contains at least `token_limit` tokens.

    The articles are read in order from the first English parquet file of the
    given dataset revision, so that the same revision and token limit always
    returns the same sample. The articles are processed in the same way as
    `wikipedia_dataset_to_directory` in
    `benchmarks/resource_benchmarking/benchmarking_utils.py`; articles that
    contain a table are skipped and markdown headers are removed.

    The sample is cached as a JSON file within the pymusas cache directory.

    Args:
        token_limit (int): The minimum number of tokens in the sample, tokens are
            counted using the spaCy English tokenizer.
        revision (str): The revision (commit) of the finewiki dataset.
        text_unit (TextUnit): Whether each text is a paragraph (a non-empty line
            of an article) or a whole article.

    Returns:
        list[str]: The texts in the sample.

    Raises:
        ValueError: If `token_limit` is not between 1 and
            `MAX_FINEWIKI_TOKEN_LIMIT`, or if the English parquet file contains
            fewer than `token_limit` tokens.
    """
    if not 0 < token_limit <= MAX_FINEWIKI_TOKEN_LIMIT:
        raise ValueError(f"The token limit must be between 1 and {MAX_FINEWIKI_TOKEN_LIMIT}, "
                         f"got {token_limit}.")

    cache_path = _finewiki_cache_path(revision, token_limit, text_unit)
    if cache_path.exists():
        with cache_path.open("r", encoding="utf-8") as cache_fp:
            return json.load(cache_fp)

    tokenizer = spacy.blank("en").tokenizer
    texts: list[str] = []
    token_count = 0
    file_system = HfFileSystem()
    parquet_path = f"datasets/{FINEWIKI_DATASET_ID}@{revision}/{FINEWIKI_ENGLISH_FILE}"
    with file_system.open(parquet_path, "rb") as parquet_fp:
        parquet_file = pq.ParquetFile(parquet_fp)
        for row_group_index in range(parquet_file.num_row_groups):
            row_group = parquet_file.read_row_group(row_group_index, columns=["text"])
            for article in row_group.column("text").to_pylist():
                if "| -" in article:
                    continue
                article = article.replace("#", "")
                match text_unit:
                    case TextUnit.paragraph:
                        article_texts = [line.strip() for line in article.splitlines() if line.strip()]
                    case TextUnit.document:
                        article_texts = [article.strip()]
                for text in article_texts:
                    token_count += len(tokenizer(text))
                    texts.append(text)
                if token_count > token_limit:
                    break
            if token_count > token_limit:
                break

    if token_count <= token_limit:
        raise ValueError(f"{FINEWIKI_ENGLISH_FILE} only contains {token_count} tokens, "
                         f"which is not more than the requested limit of {token_limit}.")

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("w", encoding="utf-8") as cache_fp:
        json.dump(texts, cache_fp)
    return texts


def preprocess(nlp: spacy.Language, inputs: Iterable[str | Doc]) -> tuple[list[Doc], float]:
    """
    Runs every component of the spaCy pipeline, apart from the pymusas tagger,
    over the inputs.

    Args:
        nlp (spacy.Language): The spaCy pipeline.
        inputs (Iterable[str | Doc]): The texts or pre-tokenised documents.

    Returns:
        tuple[list[Doc], float]: The processed documents and the number of
            seconds it took to process them.
    """
    start_time = time.perf_counter()
    with nlp.select_pipes(disable=[PYMUSAS_PIPE_NAME]):
        docs = list(nlp.pipe(inputs))
    return docs, time.perf_counter() - start_time


def time_tagger(tagger: RuleBasedTagger, docs: list[Doc], repeats: int) -> float:
    """
    Returns the minimum number of seconds, over `repeats` runs, that it takes
    the pymusas tagger to tag all of the documents. The documents are tagged in
    place.

    Args:
        tagger (RuleBasedTagger): The pymusas tagger.
        docs (list[Doc]): Documents that have been processed by the rest of the
            spaCy pipeline, see :func:`preprocess`.
        repeats (int): Number of times to tag all of the documents.

    Returns:
        float: The minimum number of seconds.
    """
    run_times: list[float] = []
    for _ in range(repeats):
        start_time = time.perf_counter()
        for doc in docs:
            tagger(doc)
        run_times.append(time.perf_counter() - start_time)
    return min(run_times)


def lexicon_matches(tagger: RuleBasedTagger, doc: Doc) -> list[bool]:
    """
    Returns for each token whether it was matched by any of the tagger's
    lexicon rules. Tokens that are not matched are tagged by the tagger's
    POS fallback, i.e. `PUNCT`, `N1`, or `Z99`.

    Args:
        tagger (RuleBasedTagger): The pymusas tagger.
        doc (Doc): A document processed by the rest of the spaCy pipeline.

    Returns:
        list[bool]: Whether each token was matched by a lexicon rule.
    """
    rules = cast(list[Rule], tagger.rules)
    ranker = cast(ContextualRuleBasedRanker, tagger.ranker)
    tokens = [token.text for token in doc]
    lemmas = [getattr(token, tagger.lemma_attribute) for token in doc]
    pos_tags = [getattr(token, tagger.pos_attribute) for token in doc]

    token_ranking_meta_data: list[list[RankingMetaData]] = [[] for _ in tokens]
    for rule in rules:
        for token_index, ranking_meta_data in enumerate(rule(tokens, lemmas, pos_tags)):
            token_ranking_meta_data[token_index].extend(ranking_meta_data)
    _token_ranks, token_best_rank = ranker(token_ranking_meta_data)
    return [best_rank is not None for best_rank in token_best_rank]


def predicted_tags(tagger: RuleBasedTagger, doc: Doc) -> list[list[str]]:
    """
    Returns the semantic tags the pymusas tagger predicted for each token.
    """
    return [getattr(token._, tagger.pymusas_tags_token_attr) for token in doc]


def coverage_counts(tagger: RuleBasedTagger, docs: list[Doc],
                    punctuation: list[list[bool]],
                    labelled: list[list[bool]] | None = None
                    ) -> dict[str, CoverageCounts]:
    """
    Counts the coverage of the tagger over all tokens (`all`), non-punctuation
    tokens (`non_punctuation`), and if `labelled` is given gold labelled tokens
    (`labelled`).

    Args:
        tagger (RuleBasedTagger): The pymusas tagger.
        docs (list[Doc]): Documents that have been tagged by the tagger.
        punctuation (list[list[bool]]): For each document, whether each token is
            punctuation.
        labelled (list[list[bool]] | None): For each document, whether each
            token has a gold label that is used for accuracy.

    Returns:
        dict[str, CoverageCounts]: The coverage counts for each set of tokens.
    """
    coverage = {"all": CoverageCounts(), "non_punctuation": CoverageCounts()}
    if labelled is not None:
        coverage["labelled"] = CoverageCounts()

    for doc_index, doc in enumerate(docs):
        matches = lexicon_matches(tagger, doc)
        for token_index, tags in enumerate(predicted_tags(tagger, doc)):
            lexicon_matched = matches[token_index]
            tag_covered = tags != [UNKNOWN_TAG]
            coverage["all"].add(lexicon_matched, tag_covered)
            if not punctuation[doc_index][token_index]:
                coverage["non_punctuation"].add(lexicon_matched, tag_covered)
            if labelled is not None and labelled[doc_index][token_index]:
                coverage["labelled"].add(lexicon_matched, tag_covered)
    return coverage


def predicted_punctuation(tagger: RuleBasedTagger, docs: list[Doc]) -> list[list[bool]]:
    """
    Returns for each document whether each token is punctuation, based on
    whether the tagger's top predicted tag is a punctuation tag (`PUNCT` or `Z9`).
    """
    return [[bool(tags) and tags[0] in PUNCTUATION_TAGS for tags in predicted_tags(tagger, doc)]
            for doc in docs]


def normalise_tags(tags: list[str]) -> list[str]:
    """
    Normalises the semantic tags predicted by pymusas so that they can be
    compared to the gold tags of the USAS Evaluation Framework. The `+`/`-`
    and `f`, `m`, `c`, `n`, `%`, `@` markers are removed, slash separated
    tags, e.g. `Z2/S2`, and the rank order of the tags are kept. Tags that
    cannot be parsed are kept as they are.

    Args:
        tags (list[str]): The predicted tags of a token in rank order.

    Returns:
        list[str]: The normalised tags in rank order.

    Examples:
        >>> normalise_tags(["X5.2+", "Z2/S2mf", "Z99"])
        ['X5.2', 'Z2/S2', 'Z99']
    """
    normalised_tags: list[str] = []
    for tag in tags:
        try:
            tag_groups = parse_usas_token_group(tag)
        except ValueError:
            normalised_tags.append(tag)
            continue
        for tag_group in tag_groups:
            normalised_tags.append("/".join(usas_tag.tag for usas_tag in tag_group.tags))
    return normalised_tags


def predicted_dataset(tagger: RuleBasedTagger, gold: EvaluationDataset,
                      docs: list[Doc]) -> EvaluationDataset:
    """
    Converts the tagger's predictions into an `EvaluationDataset` that can be
    compared to the `gold` dataset.

    Args:
        tagger (RuleBasedTagger): The pymusas tagger.
        gold (EvaluationDataset): The gold dataset the documents were created from.
        docs (list[Doc]): Documents that have been tagged by the tagger, one for
            each text in the gold dataset.

    Returns:
        EvaluationDataset: The predicted dataset.
    """
    texts: list[EvaluationTexts] = []
    for gold_text, doc in zip(gold.texts, docs, strict=True):
        semantic_tags = [normalise_tags(tags) for tags in predicted_tags(tagger, doc)]
        texts.append(EvaluationTexts(text=gold_text.text, tokens=gold_text.tokens,
                                     lemmas=None, pos_tags=None,
                                     semantic_tags=semantic_tags, mwe_indexes=None))
    return EvaluationDataset(name=f"{gold.name} predictions", text_level=gold.text_level,
                             language=gold.language, labels_removed=gold.labels_removed,
                             texts=texts)


def evaluate_gold_dataset(nlp: spacy.Language, gold_dataset: GoldDataset,
                          top_n: list[int]) -> GoldResult:
    """
    Tags the gold dataset's tokens and returns the accuracy and coverage of the
    tagger on it.

    Args:
        nlp (spacy.Language): The spaCy pipeline that contains the pymusas tagger.
        gold_dataset (GoldDataset): The gold dataset.
        top_n (list[int]): The `n` values of the top-n accuracy.

    Returns:
        GoldResult: The accuracy and coverage results.
    """
    tagger = get_tagger(nlp)
    gold = gold_dataset.accuracy_gold
    docs, _ = preprocess(nlp, (Doc(nlp.vocab, words=text.tokens) for text in gold.texts))
    for doc in docs:
        tagger(doc)

    labelled: list[list[bool]] = []
    for text in gold.texts:
        semantic_tags = text.semantic_tags or [[] for _ in text.tokens]
        labelled.append([any(tag for tag in tags) for tags in semantic_tags])

    prediction = predicted_dataset(tagger, gold, docs)
    accuracy: dict[str, float] = {}
    for n in top_n:
        for average in ("micro", "macro"):
            accuracy[f"top_{n}_{average}"] = top_n_accuracy(gold, prediction, n, average)

    return GoldResult(dataset=gold_dataset.name,
                      tokens=sum(len(doc) for doc in docs),
                      punctuation_excluded=sum(sum(text) for text in gold_dataset.punctuation),
                      scored_tokens=sum(sum(text) for text in labelled),
                      accuracy=accuracy,
                      coverage=coverage_counts(tagger, docs, gold_dataset.punctuation, labelled))


def directory_size_mb(directory: Path) -> float:
    """
    Returns the total size of all the files within the directory in MB.
    """
    return sum(file.stat().st_size for file in directory.rglob("*") if file.is_file()) / (1024 ** 2)


def disk_stats(tagger: RuleBasedTagger, config: TaggerConfig) -> DiskStats:
    """
    Returns the size of the tagger when saved to disk and, for taggers built
    from lexicon files, the size of the lexicon files.

    Args:
        tagger (RuleBasedTagger): The pymusas tagger.
        config (TaggerConfig): The tagger configuration.

    Returns:
        DiskStats: The disk statistics.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        tagger_directory = Path(temp_dir, "tagger")
        tagger.to_disk(tagger_directory)
        saved_pipe = directory_size_mb(tagger_directory)

    lexicon_files: float | None = None
    if config.tagger_type == TaggerType.lexicons:
        lexicon_files = sum(Path(download_url_file(url)).stat().st_size
                            for url in config.lexicon_urls().values()) / (1024 ** 2)
        lexicon_files = round(lexicon_files, 2)
    return DiskStats(saved_pipe=round(saved_pipe, 2), lexicon_files=lexicon_files)


def evaluate_finewiki(nlp: spacy.Language, config: TaggerConfig, texts: list[str],
                      revision: str, text_unit: TextUnit,
                      speed_repeats: int) -> FinewikiResult:
    """
    Measures the speed, memory, disk, and coverage of the tagger on the
    finewiki sample.

    Args:
        nlp (spacy.Language): The spaCy pipeline that contains the pymusas tagger.
        config (TaggerConfig): The tagger configuration, used to re-create the
            tagger in a fresh process to measure memory.
        texts (list[str]): The finewiki sample.
        revision (str): The revision of the finewiki dataset.
        text_unit (TextUnit): The text unit of the finewiki sample.
        speed_repeats (int): Number of times to time the tagger.

    Returns:
        FinewikiResult: The finewiki results.
    """
    tagger = get_tagger(nlp)
    docs, preprocess_seconds = preprocess(nlp, texts)
    number_tokens = sum(len(doc) for doc in docs)
    pymusas_seconds = time_tagger(tagger, docs, speed_repeats)

    coverage = coverage_counts(tagger, docs, predicted_punctuation(tagger, docs))
    return FinewikiResult(
        revision=revision,
        text_unit=text_unit.value,
        texts=len(texts),
        tokens=number_tokens,
        pymusas_seconds=round(pymusas_seconds, 4),
        preprocess_seconds=round(preprocess_seconds, 4),
        pymusas_tokens_per_second=round(number_tokens / pymusas_seconds, 2),
        full_pipeline_tokens_per_second=round(number_tokens / (preprocess_seconds + pymusas_seconds), 2),
        coverage=coverage,
        memory=measure_memory(config, texts),
        disk=disk_stats(tagger, config),
    )


def pymusas_install() -> str:
    """
    Returns how pymusas is installed, either `working tree` when it is an
    editable install of this repository, else `release`.
    """
    direct_url = importlib.metadata.distribution("pymusas").read_text("direct_url.json")
    if direct_url is not None and json.loads(direct_url).get("dir_info", {}).get("editable", False):
        return "working tree"
    return "release"


def new_evaluation_result(config: TaggerConfig) -> EvaluationResult:
    """
    Returns an `EvaluationResult`, without any results, that describes the
    tagger configuration and the versions of the software used.
    """
    spacy_model_version = importlib.metadata.version(config.spacy_model)
    return EvaluationResult(tagger=config.label(),
                            tagger_type=config.tagger_type.value,
                            pymusas_version=pymusas.__version__,
                            pymusas_install=pymusas_install(),
                            python_hash_seed=os.environ.get("PYTHONHASHSEED"),
                            spacy_model=config.spacy_model,
                            spacy_model_version=spacy_model_version,
                            lexicon_repo=config.lexicon_repo,
                            lexicon_commit=config.lexicon_commit,
                            autotag=config.autotag)


def append_result(path: Path, result: EvaluationResult) -> None:
    """
    Appends the result as one line of JSON to the JSON Lines file at `path`.
    """
    with path.open("a", encoding="utf-8") as result_fp:
        result_fp.write(json.dumps(asdict(result)) + "\n")


def read_results(path: Path) -> list[dict[str, Any]]:
    """
    Reads all of the results from the JSON Lines file at `path`.
    """
    with path.open("r", encoding="utf-8") as result_fp:
        return [json.loads(line) for line in result_fp if line.strip()]


def _percentage(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "-"
    return f"{100 * numerator / denominator:.2f}"


def _coverage_cells(coverage: dict[str, Any]) -> list[str]:
    """
    Returns the coverage table cells: number of tokens, number of
    non-punctuation tokens, lexicon coverage (all, non-punctuation, labelled),
    and tag coverage (all, non-punctuation).
    """
    all_tokens = coverage["all"]
    non_punctuation = coverage["non_punctuation"]
    labelled = coverage.get("labelled")
    labelled_cell = "-"
    if labelled is not None:
        labelled_cell = _percentage(labelled["lexicon_matched"], labelled["tokens"])
    return [f"{all_tokens['tokens']:,}",
            f"{non_punctuation['tokens']:,}",
            _percentage(all_tokens["lexicon_matched"], all_tokens["tokens"]),
            _percentage(non_punctuation["lexicon_matched"], non_punctuation["tokens"]),
            labelled_cell,
            _percentage(all_tokens["tag_covered"], all_tokens["tokens"]),
            _percentage(non_punctuation["tag_covered"], non_punctuation["tokens"])]


def _markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def format_results(results: list[dict[str, Any]]) -> str:
    """
    Formats the evaluation results as three markdown tables; accuracy,
    coverage, and resources.

    Args:
        results (list[dict[str, Any]]): The evaluation results, each result is
            an `EvaluationResult` converted to a dictionary.

    Returns:
        str: The markdown tables.
    """
    accuracy_keys: list[str] = []
    for result in results:
        for gold_result in result["gold"]:
            for key in gold_result["accuracy"]:
                if key not in accuracy_keys:
                    accuracy_keys.append(key)

    accuracy_headers = ["Tagger", "Dataset", "Scored Tokens", "Punctuation Excluded"]
    accuracy_headers += [key.replace("_", " ").title().replace("Top ", "Top-") for key in accuracy_keys]
    accuracy_rows: list[list[str]] = []

    coverage_headers = ["Tagger", "Dataset", "Tokens", "Non-Punctuation Tokens",
                        "Lexicon Coverage", "Lexicon Coverage (No Punctuation)",
                        "Lexicon Coverage (Scored Tokens)",
                        "Tag Coverage", "Tag Coverage (No Punctuation)"]
    coverage_rows: list[list[str]] = []

    resource_headers = ["Tagger", "Text Unit", "Tokens", "pymusas Tokens Per Second",
                        "Pipeline Tokens Per Second", "Load Peak Memory (MB)",
                        "Peak Memory (MB)", "Saved Tagger (MB)", "Lexicon Files (MB)"]
    resource_rows: list[list[str]] = []

    for result in results:
        tagger = result["tagger"]
        for gold_result in result["gold"]:
            accuracy = gold_result["accuracy"]
            accuracy_rows.append([tagger, gold_result["dataset"],
                                  f"{gold_result['scored_tokens']:,}",
                                  f"{gold_result['punctuation_excluded']:,}"]
                                 + [f"{100 * accuracy[key]:.2f}" if key in accuracy else "-"
                                    for key in accuracy_keys])
            coverage_rows.append([tagger, gold_result["dataset"]]
                                 + _coverage_cells(gold_result["coverage"]))

        finewiki = result["finewiki"]
        if finewiki is None:
            continue
        coverage_rows.append([tagger, f"finewiki ({finewiki['text_unit']})"]
                             + _coverage_cells(finewiki["coverage"]))
        memory = finewiki["memory"]
        disk = finewiki["disk"]
        lexicon_files = disk["lexicon_files"]
        resource_rows.append([tagger, finewiki["text_unit"], f"{finewiki['tokens']:,}",
                              f"{finewiki['pymusas_tokens_per_second']:,.2f}",
                              f"{finewiki['full_pipeline_tokens_per_second']:,.2f}",
                              f"{memory['load_peak_memory']:.2f}",
                              f"{memory['peak_memory']:.2f}",
                              f"{disk['saved_pipe']:.2f}",
                              "-" if lexicon_files is None else f"{lexicon_files:.2f}"])

    return "\n\n".join([
        "## Accuracy (%)\n\n" + _markdown_table(accuracy_headers, accuracy_rows),
        "## Coverage (%)\n\n" + _markdown_table(coverage_headers, coverage_rows),
        "## Resources (finewiki)\n\n" + _markdown_table(resource_headers, resource_rows),
    ])
