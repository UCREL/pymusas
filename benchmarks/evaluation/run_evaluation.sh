#!/bin/bash
set -euo pipefail

# Default values
wiki_token_limit="100000"
text_unit="paragraph"
speed_repeats="3"
python_version="3.13"
spacy_model="en_core_web_sm"
spacy_model_version="3.8.0"

# Help message
usage() {
    echo "Usage: $0 [--wiki-token-limit WIKI_TOKEN_LIMIT] [--text-unit TEXT_UNIT] [--speed-repeats SPEED_REPEATS] [--python-version PYTHON_VERSION] [--spacy-model SPACY_MODEL] [--spacy-model-version SPACY_MODEL_VERSION] [--help]"
    echo "Evaluates the English rule based taggers for accuracy, coverage, speed, and resources,"
    echo "and prints the results as markdown tables to stdout. The taggers evaluated are:"
    echo "  1. The pre-built pymusas-models model, using the latest released version of pymusas."
    echo "  2. The tagger built from the lexicon files, without the autotag lexicon."
    echo "  3. The tagger built from the lexicon files, with the autotag lexicon."
    echo ""
    echo "Optional arguments:"
    echo "  --wiki-token-limit    The minimum number of tokens in the finewiki sample (default: 100000)"
    echo "  --text-unit    Whether each finewiki text is a paragraph or a whole article, document (default: paragraph)"
    echo "  --speed-repeats    The number of times to tag the finewiki sample when measuring speed (default: 3)"
    echo "  --python-version    The Python version every tagger is evaluated with, it must be supported by uv.lock (default: 3.13)"
    echo "  --help   Show this help message"
    exit 1
}

# Parse arguments using getopt
if ! TEMP=$(getopt -o 'w:u:s:p:m:v:h' --long 'wiki-token-limit:,text-unit:,speed-repeats:,python-version:,spacy-model:,spacy-model-version:,help' -n "$0" -- "$@"); then
    usage
fi

# Update positional parameters
eval set -- "$TEMP"

# Process options
while true; do
    case "$1" in
        -w|--wiki-token-limit)
            wiki_token_limit="$2"
            shift 2
            ;;
        -u|--text-unit)
            text_unit="$2"
            shift 2
            ;;
        -s|--speed-repeats)
            speed_repeats="$2"
            shift 2
            ;;
        -p|--python-version)
            python_version="$2"
            shift 2
            ;;
        -m|--spacy-model)
            spacy_model="$2"
            shift 2
            ;;
        -v|--spacy-model-version)
            spacy_model_version="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Internal error!"
            exit 1
            ;;
    esac
done

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${script_directory}"

# Every tagger is evaluated in its own isolated environment that only contains
# the evaluation requirements, e.g. it does not contain torch which is imported
# by spaCy when it is installed and would add to the memory used. All of the
# requirements, apart from pymusas, are the same in every environment as they
# come from uv.lock, and the same Python version is used.
# The rule based tagger's output can depend on Python's hash randomisation,
# when lexicon entries of equal rank match the same tokens, therefore the hash
# seed is fixed so that the results can be reproduced and compared.
export PYTHONHASHSEED=0
evaluation_options=(
    --wiki-token-limit "${wiki_token_limit}"
    --text-unit "${text_unit}"
    --speed-repeats "${speed_repeats}"
    --spacy-model "${spacy_model}"
)

# The spaCy model is not a dependency of the project, so that it is not installed
# by the development setup or CI. It is added to each isolated environment from
# its wheel, which uv downloads once and then reads from its cache.
spacy_model_url="https://github.com/explosion/spacy-models/releases/download/${spacy_model}-${spacy_model_version}/${spacy_model}-${spacy_model_version}-py3-none-any.whl"

results_file=$(mktemp --suffix=.jsonl)
lock_requirements_file=$(mktemp --suffix=.txt)
trap 'rm -f "${results_file}" "${lock_requirements_file}"' EXIT

uv export --frozen --no-default-groups --group evaluation --no-emit-project \
    --no-hashes --quiet -o "${lock_requirements_file}"

# The per run tables are written to stderr, so that only the combined tables
# are written to stdout.
echo "Evaluating the pre-built pymusas-models model" >&2
uv run --isolated --no-project --python "${python_version}" \
    --with-requirements "${lock_requirements_file}" \
    --with-requirements ./pymusas_model_requirements.txt \
    --with "${spacy_model_url}" \
    ./evaluate_rule_based_tagger.py --tagger pymusas-model \
    "${evaluation_options[@]}" --output-file "${results_file}" >&2

for autotag_option in --no-autotag --autotag; do
    echo "Evaluating the tagger built from the lexicon files with ${autotag_option}" >&2
    uv run --isolated --frozen --no-default-groups --group evaluation --python "${python_version}" \
        --with "${spacy_model_url}" \
        ./evaluate_rule_based_tagger.py --tagger lexicons "${autotag_option}" \
        "${evaluation_options[@]}" --output-file "${results_file}" >&2
done

uv run --isolated --frozen --no-default-groups --group evaluation --python "${python_version}" \
    ./format_evaluation_results.py "${results_file}"
