import tempfile
from pathlib import Path
import timeit

import typer

import benchmarking_utils

language_code_help = (
    "The language code of the hybrid tagger to benchmark. "
    "When using the Multilingual tagger (`xx` as the language code) the tagger "
    "will be benchmarked on English data and tokenized using the English spaCy tokenizer."
)
tagger_size_help = (
    "The size of the neural tagger model to use in the hybrid tagger."
)
output_file_help = (
    "The file to which the benchmark statistics are written too in JSON format. If the file already exists it will be appended too."
)
number_of_repeats_help = (
    "The number of times to load the setup for benchmarking and then run the benchmark for the `number_of_repeat_calls`"
)
number_of_repeat_calls_help = (
    "The number of times to run the tagger over a specified minimum number of tokens (`token_limit`)."
)
token_limit_help = (
    "The minimum number of tokens to process in the benchmark, once we have "
    "downloaded a sufficient number of Wikipedia articles to reach this limit, "
    "these tokens are used as the benchmark."
)
large_text_token_limit_help = (
    "The minimum number of tokens to process for the large text benchmark. "
    "The tokens come from the Wikipedia articles, once this token limit is reached "
    "no more tokens are added to the large text that will be processed as one text."
)
device_help = (
    "The device to use for the neural tagger model within the hybrid tagger. This should be a "
    "[torch device string like cpu or cuda](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.device)."
)

def main(language_code: benchmarking_utils.LanguageCodes = typer.Argument(help=language_code_help),
         tagger_size: benchmarking_utils.NeuralTaggerSizes = typer.Argument(help=tagger_size_help),
         output_file: Path = typer.Argument(help="The file to which the output will be written."),
         token_limit: int = typer.Option(1_000, help=token_limit_help),
         number_repeats: int = typer.Option(1, help=number_of_repeats_help),
         number_of_repeat_calls: int = typer.Option(1, help=number_of_repeat_calls_help),
         large_text_token_limit: int = typer.Option(1_000, help=large_text_token_limit_help),
         device: str = typer.Option("cpu", help=device_help)
         ) -> None:
    """
    The script performs the following steps:
    * Creates the hybrid tagger for the specified language code and tagger size.
    * Downloads a sufficient number of Wikipedia articles to reach the token limit.
    * Processes the downloaded articles and tags the text using the hybrid tagger.
    * Calculates the benchmark statistics, including memory requirements and tokens per second.
    * Appends the benchmark statistics to the specified output file in JSON format.

    The benchmark statistics in the JSON output file are as follows:
    {
        "Language": <language_code>,
        "Tagger": "Rule Based",
        "Load Model Memory Requirements": <load_memory_requirements>,
        "Average Memory Requirements": <average_memory_required>,
        "Large Text Memory Requirements": <large_text_memory_requirements>,
        "Tokens Per Second": <tokens_per_second>,
        "Number of Tokens Processed": <number_of_tokens_processed>,
        "Large Text Tokens Processed": <large_text_tokens_processed>,
        "Load Model GPU Memory Requirements": <load_gpu_requirements>,
        "Average GPU Memory Requirements": <average_gpu_memory_required>,
        "Large Text GPU Memory Requirements": <large_gpu_memory_requirements>
    }
    Whereby each value is a `list` and this script either creates the list with
    a single value or appends to it. In creating a list of values we can then
    create a table of benchmark statistics.
    """
    wikipedia_dataset_id = "HuggingFaceFW/finewiki"
    temp_file_prefix = "document_"

    language_code_key = "Language"
    tagger_name_key = "Tagger"
    load_memory_requirements_key = "Load Model Memory Requirements"
    average_memory_required_key = "Average Memory Requirements"
    large_text_memory_requirements_key = "Large Text Memory Requirements"
    tokens_per_second_key = "Tokens Per Second"
    number_of_tokens_processed_key = "Number of Tokens Processed"
    large_text_tokens_processed_key = "Large Text Tokens Processed"
    
    load_gpu_requirements_key = "Load Model GPU Memory Requirements"
    average_gpu_memory_required_key = "Average GPU Memory Requirements"
    large_gpu_memory_requirements_key = "Large Text GPU Memory Requirements"
    output_statistics = {
        language_code_key: language_code,
        tagger_name_key: benchmarking_utils.LANGUAGE_CODE_SIZE_TO_HYBRID_MODEL_NAME[language_code + "_" + tagger_size],
        load_memory_requirements_key: 0.0,
        average_memory_required_key: 0.0,
        large_text_memory_requirements_key: 0.0,
        tokens_per_second_key: 0.0,
        number_of_tokens_processed_key: 0,
        large_text_tokens_processed_key: 0,
        load_gpu_requirements_key: 0.0,
        average_gpu_memory_required_key: 0.0,
        large_gpu_memory_requirements_key: 0.0
    }

    with benchmarking_utils.track_memory_usage(load_memory_requirements_key, load_gpu_requirements_key, output_statistics, device):
        benchmarking_utils.load_hybrid_tagger(language_code, tagger_size, device)

    with tempfile.TemporaryDirectory() as temp_dir:
        spacy_nlp = benchmarking_utils.load_spacy_pipeline_as_tokenizer(language_code)
        number_tokens = benchmarking_utils.wikipedia_dataset_to_directory(wikipedia_dataset_id,
                                                                          temp_dir,
                                                                          temp_file_prefix,
                                                                          spacy_nlp,
                                                                          token_limit,
                                                                          language_code)
        output_statistics[number_of_tokens_processed_key] = number_tokens

        total_times: list[float] = []
        with benchmarking_utils.track_memory_usage(average_memory_required_key, average_gpu_memory_required_key, output_statistics, device):
            total_times = timeit.repeat(stmt='benchmarking_utils.tagger_speed_test(hybrid_spacy_tagger, Path(temp_dir), temp_file_prefix)', 
                                        setup='hybrid_spacy_tagger = benchmarking_utils.load_hybrid_tagger(language_code, tagger_size, device)',
                                        number=number_of_repeat_calls, 
                                        repeat=number_repeats,
                                        globals={**globals(), **locals()})
        average_time = min(total_times) / number_repeats
        tokens_per_seconds = round(number_tokens / average_time, 2)
        output_statistics[tokens_per_second_key] = tokens_per_seconds

        large_text = ""
        for line in benchmarking_utils.text_from_files(Path(temp_dir), temp_file_prefix):
            large_text += line
            spacy_doc = spacy_nlp(line)
            output_statistics[large_text_tokens_processed_key] += len(spacy_doc)

            if output_statistics[large_text_tokens_processed_key] >= large_text_token_limit:
                break
        
        with benchmarking_utils.track_memory_usage(large_text_memory_requirements_key, large_gpu_memory_requirements_key, output_statistics, device):
            tagger = benchmarking_utils.load_hybrid_tagger(language_code, tagger_size, device)
            tagger(large_text)

    output_statistics[average_memory_required_key] += output_statistics[load_memory_requirements_key]
    output_statistics[large_text_memory_requirements_key] += output_statistics[load_memory_requirements_key]
    benchmarking_utils.to_json_file(output_file, output_statistics)


if __name__ == "__main__":
    typer.run(main)

