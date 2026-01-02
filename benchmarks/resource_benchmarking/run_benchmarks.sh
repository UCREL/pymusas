#!/bin/bash

# Default values
device="cpu"
token_limit="1000"
large_text_token_limit="1000"

# Help message
usage() {
    echo "Usage: $0 [--device DEVICE] [--token-limit TOKEN_LIMIT] [--large-text-token-limit LARGE_TEXT_TOKEN_LIMIT] [--help]"
    echo "Runs all of the resource (tokens per second, memory usage) benchmarks for the different taggers."
    echo ""
    echo "Optional arguments:"
    echo "  --device    Set device to use (default: cpu)"
    echo "  --token-limit    The minimum number of tokens to process in the "
    echo "benchmark, once we have downloaded a sufficient number of Wikipedia "
    echo "articles to reach this limit, these tokens are used as the benchmark."
    echo " (default: 1000)"
    echo "  --large-text-token-limit    The minimum number of tokens to "
    echo "process for the large text benchmark. The tokens come from the "
    echo "Wikipedia articles, once this token limit is reached no more tokens "
    echo "are added to the large text that will be processed as one text. "
    echo "(default: 1000)"
    echo "  --help    Show this help message"
    exit 1
}

# Parse arguments using getopt
TEMP=$(getopt -o 'd:t:l:h' --long 'device:,token-limit:,large-text-token-limit:,help' -n "$0" -- "$@")
if [ $? -ne 0 ]; then
    usage
fi

# Update positional parameters
eval set -- "$TEMP"

# Process options
while true; do
    case "$1" in
        -d|--device)
            device="$2"
            shift 2
            ;;
        -t|--token-limit)
            token_limit="$2"
            shift 2
            ;;
        -l|--large-text-token-limit)
            large_text_token_limit="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
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

json_statistics_data_file=$(mktemp --suffix=.json)

# Run the rule based taggers first as they are smallest and quickest
rule_based_tagger_languages=(
    "en"
    "cmn"
    "da"
    "nl"
    "fr"
    "it"
    "pt"
    "es"
    "fi"
)

for language_code in ${rule_based_tagger_languages[@]}; do
    uv run ./benchmark_rule_based_tagger.py \
        ${language_code} \
        ${json_statistics_data_file} \
        --token-limit ${token_limit} \
        --large-text-token-limit ${large_text_token_limit}   
done

# Run the neural taggers
neural_tagger_languages=(
    "en"
    "xx"
)

neural_tagger_sizes=(
    "small"
    "base"
)

for language_code in ${neural_tagger_languages[@]}; do
    for neural_tagger_size in ${neural_tagger_sizes[@]}; do
        uv run ./benchmark_neural_tagger.py \
            ${language_code} \
            ${neural_tagger_size} \
            ${json_statistics_data_file} \
            --device ${device} \
            --token-limit ${token_limit} \
            --large-text-token-limit ${large_text_token_limit}
    done
done

# Run the hybrid taggers

for language_code in ${neural_tagger_languages[@]}; do
    for neural_tagger_size in ${neural_tagger_sizes[@]}; do
        uv run ./benchmark_hybrid_tagger.py \
            ${language_code} \
            ${neural_tagger_size} \
            ${json_statistics_data_file} \
            --device ${device} \
            --token-limit ${token_limit} \
            --large-text-token-limit ${large_text_token_limit}
    done
done

uv run ./format_benchmarking_data.py ${json_statistics_data_file}
rm -f ${json_statistics_data_file}