from pathlib import Path
from typing import Iterable
import warnings
from contextlib import contextmanager
from enum import Enum
import json
import os

import spacy
import datasets
import psutil
import torch

from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.rule import Rule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker

class LanguageCodes(str, Enum):
    en = "en"
    cmn = "cmn"
    da = "da"
    nl = "nl"
    fr = "fr"
    it = "it"
    pt = "pt"
    es = "es"
    fi = "fi"
    xx = "xx"

class NeuralTaggerSizes(str, Enum):
    small = "small"
    base = "base"

LANGUAGE_CODE_TO_SPACY_MODEL = {
    "en": "en_core_web_sm",
    "cmn": "zh_core_web_sm",
    "da": "da_core_news_sm",
    "nl": "nl_core_news_sm",
    "fr": "fr_core_news_sm",
    "it": "it_core_news_sm",
    "pt": "pt_core_news_sm",
    "es": "es_core_news_sm",
    "fi": "fi_core_news_sm",
    "xx": "en_core_web_sm"
}

LANGUAGE_CODE_SIZE_TO_NEURAL_MODEL_NAME = {
    "en_small": "Neural-E-17M",
    "en_base": "Neural-E-68M",
    "xx_small": "Neural-M-140M",
    "xx_base": "Neural-M-304M",
}

LANGUAGE_CODE_SIZE_TO_HYBRID_MODEL_NAME = {
    "en_small": "Hybrid-E-17M",
    "en_base": "Hybrid-E-68M",
    "xx_small": "Hybrid-M-140M",
    "xx_base": "Hybrid-M-304M",
}

hybrid_tagger_supported_languages = set(["en", "xx"])

language_code_to_pymusas_rule_based_model = {
    "en": "en_dual_none_contextual_none",
    "cmn": "cmn_dual_upos2usas_contextual_none",
    "da": "da_dual_none_contextual_none",
    "nl": "nl_single_upos2usas_contextual_none",
    "fr": "fr_single_upos2usas_contextual_none",
    "it": "it_dual_upos2usas_contextual_none",
    "pt": "pt_dual_upos2usas_contextual_none",
    "es": "es_dual_upos2usas_contextual_none",
    "fi": "fi_single_upos2usas_contextual_none"
}

language_code_to_pymusas_neural_model = {
    "en": 
    {
        "small": "en_none_none_none_englishsmallbem",
        "base": "en_none_none_none_englishbasebem"
    },
    "xx": 
    {
        "small": "xx_none_none_none_multilingualsmallbem",
        "base": "xx_none_none_none_multilingualbasebem"
    }
}

language_code_to_neural_model_huggingface_id = {
    "en": 
    {
        "small": "ucrelnlp/PyMUSAS-Neural-English-Small-BEM",
        "base": "ucrelnlp/PyMUSAS-Neural-English-Base-BEM"
    },
    "xx": 
    {
        "small": "ucrelnlp/PyMUSAS-Neural-Multilingual-Small-BEM",
        "base": "ucrelnlp/PyMUSAS-Neural-Multilingual-Base-BEM"
    }
}


# See https://huggingface.co/datasets/HuggingFaceFW/finewiki/blob/main/language_subsets.csv
language_code_to_wiki = {
    "en": "en",
    "cmn": "zh",
    "da": "da",
    "nl": "nl",
    "fr": "fr",
    "it": "it",
    "pt": "pt",
    "es": "es",
    "fi": "fi",
    "xx": "en"
}

@contextmanager
def track_memory_usage(memory_statistic_name: str,
                       gpu_memory_statistic_name: str,
                       memory_statistics: dict[str, float],
                       device: str) -> Iterable[None]:
    """
    Context manager to track memory usage of the enclosed code.

    The RAM is tracked using the psutil library, specifically `psutil.virtual_memory`.

    The GPU memory is tracked using the torch library, specifically `torch.cuda.memory.max_memory_allocated`
    of which the max memory peak is reset before the enclosed code is executed.

    Args:
        memory_statistic_name (str): name of the key to store the memory statistic
            too in the memory_statistics dictionary.
        gpu_memory_statistic_name (str): name of the key to store the GPU memory statistic
            too in the memory_statistics dictionary.
        memory_statistics (dict[str, float]]): dictionary to store the memory statistics
        device (str): If `cuda` then GPU memory will also be tracked else the
            reported value will be 0.0 for `gpu_memory_statistic_name`.

    Yields:
        None
    """
    if device == "cuda":
        torch.cuda.memory.reset_peak_memory_stats()

    memory_checkpoint = psutil.virtual_memory().used
    yield None
    memory_used = psutil.virtual_memory().used - memory_checkpoint
    memory_used_mb = memory_used / (1024 ** 2)
    memory_statistics[memory_statistic_name] = round(memory_used_mb, 2)
    
    if device == "cuda":
        gpu_memory_used = torch.cuda.memory.max_memory_allocated() / (1024 ** 2)
        memory_statistics[gpu_memory_statistic_name] = round(gpu_memory_used, 2)


def load_spacy_pipeline_as_tokenizer(language_code: str) -> spacy.Language:
    """
    Loads the Spacy pipeline as a tokenizer for the given language code.

    The pipeline is loaded with all components excluded except for the tokenizer.
    This is required as compared to the `blank` pipeline for some languages
    the tokenizer is a downloaded model which would not be part of the `blank` pipeline.

    Args:
        language_code (str): The language code of the Spacy pipeline to load.

    Returns:
        spacy.Language: The loaded Spacy pipeline as a tokenizer.
    """
    pipes_to_exclude = spacy.load(LANGUAGE_CODE_TO_SPACY_MODEL[language_code]).pipe_names
    return spacy.load(LANGUAGE_CODE_TO_SPACY_MODEL[language_code], exclude=pipes_to_exclude)


def to_json_file(path: Path,
                 data: dict[str, int | float]
                 ) -> None:
    """
    Writes data to a JSON file, whereby the values of the data will be saved in
    a list, thus allowing future data to be appended to it, if required.

    If the file already exists, it will append the given data to the existing data.
    The keys of the existing data and the new data must match, otherwise a KeyError is raised.

    Args:
        path (Path): The path to the JSON file.
        data (dict[str, int | float]): The data to write to the JSON file.

    Returns:
        None

    Raises:
        KeyError: If the keys of the existing data and the new data do not match.
    """
    data_with_list_values = {
        key: [value] for key, value in data.items()
    }
    if path.exists():
        # First check that the file is not empty
        if os.stat(str(path.resolve())).st_size != 0:
            with path.open("r", encoding="utf-8") as json_fp:
                additional_data = json.load(json_fp)
                if additional_data.keys() != data.keys():
                    raise KeyError(f"The keys of the existing JSON data in {path} "
                                "does not match the keys of the new data.")
                for key, value in additional_data.items():
                    data_with_list_values[key] = value + [data[key]]
    with path.open("w", encoding="utf-8") as json_fp:
        json.dump(data_with_list_values, json_fp)

def wikipedia_dataset_to_directory(huggingface_dataset_id: str,
                                   directory: str,
                                   file_prefix: str,
                                   spacy_model: spacy.Language,
                                   number_tokens: int,
                                   language_code: str) -> int:
    """
    Saves a subset of Wikipedia articles from the given language code to the
    specified directory, whereby the number of articles saved is based on
    the number of tokens.

    Args:
        huggingface_dataset_id (str): The Hugging Face dataset ID of the Wikipedia dataset, e.g. HuggingFaceFW/finewiki
        directory (str): The directory to which the files should be saved.
        file_prefix (str): The prefix of the file names. Each prefix is appended with a unique article number.
        spacy_model (spacy.Language): The Spacy language model that should be used to tokenize the text.
        number_tokens (int): The minimum number of tokens to be saved. Once the
            number of tokens is reached no more articles are saved.
        language_code (str): The language code of the dataset to be saved.

    Returns:
        int: The number of tokens saved.
    """
    wikipedia_language_code = language_code_to_wiki[language_code]
    wikipedia_languages = datasets.get_dataset_config_names(huggingface_dataset_id)
    if wikipedia_language_code not in wikipedia_languages:
        raise ValueError(f"Language {wikipedia_language_code} not found in dataset {huggingface_dataset_id}")
    split = "train"
    assert split in datasets.get_dataset_split_names(huggingface_dataset_id)

    wikipedia_language_dataset = datasets.load_dataset(huggingface_dataset_id,
                                                       wikipedia_language_code,
                                                       split=split,
                                                       streaming=True,
                                                       columns=["text"])
    article_count = 0
    token_count = 0
    for object in wikipedia_language_dataset:
        text = object["text"]
        # We skip any article that contains a table
        if "| -" in text:
            continue
        # Removes markdown headers
        text = text.replace("#", "")
        # Tried to remove markdown lists, but I think this creates a worse format
        #text = re.sub(r"\s*-\s+", "", text)
        token_count += len(spacy_model(text))
        article_count += 1

        temp_file = Path(directory, f"{file_prefix}{article_count}")
        with temp_file.open("w", encoding="utf-8") as f:
            f.write(text)
        if token_count > number_tokens:
            break
    return token_count



def text_from_files(file_directory: Path,
                    file_prefix: str) -> Iterable[str]:
    """
    Yields lines of non empty text from files in a directory whereby the file
    names start with the given file prefix.

    All lines of text are stripped of leading and trailing whitespace.

    Args:
        file_directory (Path): The directory to read files from.
        file_prefix (str): The prefix of the file names to read.

    Yields:
        An iterable of strings, where each string is a non-empty line from
        one of the files with leading and trailing whitespace stripped.
    """
    for file in file_directory.iterdir():
        if file.name.startswith(file_prefix):
            with file.open("r", encoding="utf-8") as file_fp:
                for line in file_fp:
                    line = line.strip()
                    if line:
                        yield line


def load_rule_based_tagger(language_code: str) -> spacy.Language:
    """
    Loads a spaCy model with the rule-based tagger for the given language code.

    Args:
        language_code (str): The language code to load the spaCy and rule based
            tagger for.

    Returns:
        spacy.Language: The loaded spaCy model with the rule-based tagger.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        spacy_model = spacy.load(LANGUAGE_CODE_TO_SPACY_MODEL[language_code],
                                 exclude=['parser', 'ner'])
        rule_based_tagger = spacy.load(language_code_to_pymusas_rule_based_model[language_code])
        spacy_model.add_pipe('pymusas_rule_based_tagger', source=rule_based_tagger)
        return spacy_model
    

def load_neural_tagger(language_code: str, size: str, device: str) -> spacy.Language:
    """
    Loads a spaCy model with the neural tagger for the given language code and size
    using the given device.

    Args:
        language_code (str): The language code to load the spaCy and neural tagger for.
        size (str): The size of the neural tagger to load.
        device (str): The device to use for the neural tagger. This should be a
            [torch device string like cpu or cuda](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device).

    Returns:
        spacy.Language: The loaded spaCy model with the neural tagger.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Only want the tokenizer therefore get all pipes to exclude them
        spacy_model = load_spacy_pipeline_as_tokenizer(language_code)
        neural_model = spacy.load(language_code_to_pymusas_neural_model[language_code][size],
                                  config={"components.pymusas_neural_tagger.device": device})
        spacy_model.add_pipe('pymusas_neural_tagger', source=neural_model)
        return spacy_model
    
def get_hybrid_tagger_initializer_kwargs(language_code: str, size: str
                                         ) -> dict[str, set[str] | ContextualRuleBasedRanker | list[Rule] | str]:
    """
    Returns the keyword arguments to use for the initializer of the hybrid tagger
    for the given language code and size.

    Args:
        language_code (str): The language code of the language specific resources
            required to initialize the hybrid tagger.
        size (str): The size of the neural tagger model to load within the hybrid tagger.

    Returns:
        dict[str, Any]: The keyword arguments to use for the initializer of the hybrid tagger.
    """
    if language_code not in hybrid_tagger_supported_languages:
        raise ValueError("The benchmarking script currently only supports the "
                         f"following language codes: {hybrid_tagger_supported_languages}")
    english_single_lexicon_url = ('https://raw.githubusercontent.com/UCREL/Multilingual-USAS/'
                                  '2cc9966a3bdcc84bc204d16bdf4318fc28495016/'
                                  'English/semantic_lexicon_en.tsv')
    english_mwe_lexicon_url = ('https://raw.githubusercontent.com/UCREL/Multilingual-USAS/'
                               '2cc9966a3bdcc84bc204d16bdf4318fc28495016/'
                               'English/mwe-en.tsv')
    lexicon_lookup = LexiconCollection.from_tsv(english_single_lexicon_url, include_pos=True)
    lemma_lexicon_lookup = LexiconCollection.from_tsv(english_single_lexicon_url, include_pos=False)
    mwe_lexicon_lookup = MWELexiconCollection.from_tsv(english_mwe_lexicon_url)
    # The rules that use the lexicons
    single_word_rule = SingleWordRule(lexicon_lookup, lemma_lexicon_lookup)
    mwe_word_rule = MWERule(mwe_lexicon_lookup)
    word_rules = [single_word_rule, mwe_word_rule]
    # The ranker that determines which rule should be used/applied
    ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments(word_rules)
    ranker = ContextualRuleBasedRanker(*ranker_arguments)
    # POS that indicate a Punctuation and Numeric value
    default_punctuation_tags = set(['PUNCT'])
    default_number_tags = set(['NUM'])

    pretrained_model_name = language_code_to_neural_model_huggingface_id[language_code][size]

    return {"rules": word_rules,
            "ranker": ranker,
            "default_punctuation_tags": default_punctuation_tags,
            "default_number_tags": default_number_tags,
            "pretrained_model_name_or_path": pretrained_model_name
            }
    
def load_hybrid_tagger(language_code: str, size: str, device: str) -> spacy.Language:
    """
    Loads a spaCy model with the hybrid tagger for the given language code and size
    using the given device.

    Args:
        language_code (str): The language code to load the spaCy and hybrid tagger for.
        size (str): The size of the neural tagger model to load within the hybrid tagger.
        device (str): The device to use for the neural tagger model. This should be a
            [torch device string like cpu or cuda](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device).

    Returns:
        spacy.Language: The loaded spaCy model with the hybrid tagger.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        spacy_model = spacy.load(LANGUAGE_CODE_TO_SPACY_MODEL[language_code],
                                 exclude=['parser', 'ner'])
        hybrid_tagger = spacy_model.add_pipe("pymusas_hybrid_tagger",
                                             config={"top_n": 5,
                                                     "device": device})
        hybrid_tagger.initialize(**get_hybrid_tagger_initializer_kwargs(language_code, size))
        return spacy_model

def tagger_speed_test(spacy_model: spacy.Language,
                                 wikipedia_data_directory: Path,
                                 file_prefix: str,
                                 max_texts: int = -1) -> None:
    """
    Tests the speed of a given spaCy pipeline, which includes the rule-based tagger.
    The speed test is performed on the given Wikipedia dataset text files, whereby the
    tagger has to tag all tokens in each file.

    Args:
        spacy_model (spacy.Language): The spaCy pipeline to test, this should include
            the rule-based tagger, which can be created using the
            `load_rule_based_tagger` function.
        wikipedia_data_directory (Path): The directory containing the Wikipedia
            dataset text files.
        file_prefix (str): The prefix of the file names to read from the directory.
        max_texts (int): The maximum number of Wikipedia articles to process.
            If -1 then all Wikipedia articles are processed. Defaults to -1.

    Returns:
        None
    """
    if max_texts == -1:
        for _ in spacy_model.pipe(text_from_files(wikipedia_data_directory, file_prefix)):
            pass
    else:
        for text_index, _ in enumerate(spacy_model.pipe(text_from_files(wikipedia_data_directory, file_prefix))):
            if text_index == max_texts:
                break
