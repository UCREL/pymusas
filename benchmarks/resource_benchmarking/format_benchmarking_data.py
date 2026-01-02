from pathlib import Path
import json

import typer

def load_json_file(file_path: Path) -> dict[str, int | float | str]:
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)

benchmarking_data_file_help = (
    "The file that contains the benchmarking data that will be formatted into "
    "a markdown table and printed to the console."
)

def main(benchmarking_data_file: Path = typer.Argument(help=benchmarking_data_file_help)) -> None:
    """
    Creates a markdown table from the benchmarking data in the specified file.
    The benchmarking data should come from the output files of the following scripts:
    * benchmark_rule_based_tagger.py
    * benchmark_neural_tagger.py
    * benchmark_hybrid_tagger.py

    An example markdown table that will be printed to the console is as follows:
    | Language | Tagger | Load Model Memory Requirements | Average Memory Requirements | Large Text Memory Requirements | Tokens Per Second | Number of Tokens Processed | Large Text Tokens Processed | Load Model GPU Memory Requirements | Average GPU Memory Requirements | Large Text GPU Memory Requirements |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| en| Rule Based| 161.40| 204.74| 160.91| 2698.62| 1,643| 1,084| 0.00| 0.00| 0.00 |
    """
    
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
    heading_order = [
        language_code_key,
        tagger_name_key,
        load_memory_requirements_key,
        average_memory_required_key,
        large_text_memory_requirements_key,
        tokens_per_second_key,
        number_of_tokens_processed_key,
        large_text_tokens_processed_key,
        load_gpu_requirements_key,
        average_gpu_memory_required_key,
        large_gpu_memory_requirements_key
    ]

    benchmarking_data = load_json_file(benchmarking_data_file)
    number_benchmarking_rows = len(benchmarking_data[heading_order[0]])

    markdown_table_header_string = "|"
    markdown_table_column_string = "|"
    markdown_table_content: list[list[str]] = [[] for _ in range(number_benchmarking_rows)]
    for heading in heading_order:
        markdown_table_header_string += f" {heading} |"
        markdown_table_column_string += " --- |"
        
        for row_index, heading_row_data in enumerate(benchmarking_data[heading]):
            if isinstance(heading_row_data, float):
                heading_row_data = f"{heading_row_data:,.2f}"
            if isinstance(heading_row_data, int):
                heading_row_data = f"{heading_row_data:,}"
            markdown_table_content[row_index].append(str(heading_row_data))

    print(markdown_table_header_string)
    print(markdown_table_column_string)

    for benchmarking_row_data in markdown_table_content:
        benchmarking_row_markdown_format = "| ".join(benchmarking_row_data)
        benchmarking_row_markdown_format = f"| {benchmarking_row_markdown_format} |"
        print(benchmarking_row_markdown_format)

if __name__ == "__main__":
    typer.run(main)