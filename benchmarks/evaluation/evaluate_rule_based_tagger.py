from dataclasses import asdict
import os
from pathlib import Path

import evaluation_utils
from evaluation_utils import TextUnit
import tagger_utils
from tagger_utils import TaggerConfig, TaggerType
import typer


tagger_help = (
    "Whether to build the tagger from the Multilingual-USAS lexicon files (`lexicons`) "
    "or to use the pre-built pymusas-models model (`pymusas-model`). The pre-built "
    "model is evaluated in its own isolated environment by `run_evaluation.sh`."
)
autotag_help = "Whether to use the English autotag lexicon, only for `--tagger lexicons`."
lexicon_repo_help = (
    "The GitHub repository of the lexicon files, only for `--tagger lexicons`. "
    f"Defaults to `{tagger_utils.DEFAULT_LEXICON_REPO}`."
)
lexicon_commit_help = (
    "The commit of the lexicon files, only for `--tagger lexicons`. "
    f"Defaults to `{tagger_utils.DEFAULT_LEXICON_COMMIT}`."
)
spacy_model_help = "The spaCy model that provides the POS tags and lemmas to the tagger."
top_n_help = "The `n` of the top-n accuracy, can be given more than once."
speed_repeats_help = (
    "The number of times to tag the finewiki sample when measuring speed, "
    "the fastest time is used."
)
wiki_token_limit_help = "The minimum number of tokens in the finewiki sample."
wiki_revision_help = "The revision (commit) of the finewiki dataset to sample from."
text_unit_help = (
    "Whether each finewiki text that is tagged is a paragraph (a line of an article) "
    "or a whole article (document)."
)
output_file_help = (
    "A JSON Lines file to append the results to, the results of different runs "
    "can then be formatted together using `format_evaluation_results.py`."
)


def main(tagger: TaggerType = typer.Option(TaggerType.lexicons, help=tagger_help),
         autotag: bool = typer.Option(False, help=autotag_help),
         lexicon_repo: str | None = typer.Option(None, help=lexicon_repo_help),
         lexicon_commit: str | None = typer.Option(None, help=lexicon_commit_help),
         spacy_model: str = typer.Option("en_core_web_sm", help=spacy_model_help),
         top_n: list[int] = typer.Option([1, 5], help=top_n_help),
         speed_repeats: int = typer.Option(3, help=speed_repeats_help),
         wiki_token_limit: int = typer.Option(100_000, min=1,
                                             max=evaluation_utils.MAX_FINEWIKI_TOKEN_LIMIT,
                                             help=wiki_token_limit_help),
         wiki_revision: str = typer.Option(evaluation_utils.DEFAULT_FINEWIKI_REVISION,
                                           help=wiki_revision_help),
         text_unit: TextUnit = typer.Option(TextUnit.paragraph, help=text_unit_help),
         output_file: Path | None = typer.Option(None, help=output_file_help)
         ) -> None:
    """
    Evaluates the English rule based tagger for:

    * Accuracy - top-n accuracy on the English gold datasets of the USAS Evaluation Framework.
    * Coverage - the percentage of tokens a lexicon rule matched (lexicon coverage)
      and the percentage not tagged `Z99` (tag coverage), on the gold datasets and a
      finewiki sample.
    * Speed - tokens per second of the tagger on the finewiki sample.
    * Resources - memory required to load and run the tagger on the finewiki sample,
      and the size of the tagger on disk.

    The results are printed as markdown tables to stdout.
    """
    if tagger == TaggerType.pymusas_model:
        if autotag or lexicon_repo is not None or lexicon_commit is not None:
            raise typer.BadParameter("`--autotag`, `--lexicon-repo`, and `--lexicon-commit` "
                                     "can only be used with `--tagger lexicons`.")
        config = TaggerConfig(tagger, spacy_model)
    else:
        config = TaggerConfig(tagger, spacy_model,
                              lexicon_repo or tagger_utils.DEFAULT_LEXICON_REPO,
                              lexicon_commit or tagger_utils.DEFAULT_LEXICON_COMMIT,
                              autotag)

    if os.environ.get("PYTHONHASHSEED") is None:
        typer.echo("Warning: `PYTHONHASHSEED` is not set, the tagger's output can depend on "
                   "Python's hash randomisation, therefore set it, e.g. `PYTHONHASHSEED=0`, "
                   "to reproduce and compare results.", err=True)
    typer.echo(f"Evaluating: {config.label()}", err=True)
    nlp = tagger_utils.load_spacy_model(spacy_model)
    tagger_utils.add_tagger(nlp, config)
    result = evaluation_utils.new_evaluation_result(config)

    for gold_dataset in evaluation_utils.load_gold_datasets():
        typer.echo(f"Evaluating on the {gold_dataset.name} gold dataset", err=True)
        result.gold.append(evaluation_utils.evaluate_gold_dataset(nlp, gold_dataset, top_n))

    typer.echo("Evaluating on the finewiki sample", err=True)
    finewiki_texts = evaluation_utils.load_finewiki_sample(wiki_token_limit, wiki_revision, text_unit)
    result.finewiki = evaluation_utils.evaluate_finewiki(nlp, config, finewiki_texts, wiki_revision,
                                                         text_unit, speed_repeats)

    if output_file is not None:
        evaluation_utils.append_result(output_file, result)
    typer.echo(evaluation_utils.format_results([asdict(result)]))


if __name__ == "__main__":
    typer.run(main)
