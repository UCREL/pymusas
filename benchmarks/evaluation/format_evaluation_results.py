from pathlib import Path

import evaluation_utils
import typer


def main(results_file: Path = typer.Argument(help="JSON Lines file of results from `evaluate_rule_based_tagger.py`.")
         ) -> None:
    """
    Formats the results, from one or more runs of
    `evaluate_rule_based_tagger.py`, as markdown tables and prints them to stdout.
    """
    typer.echo(evaluation_utils.format_results(evaluation_utils.read_results(results_file)))


if __name__ == "__main__":
    typer.run(main)
