# Resource Benchmarking

This directory contains all of the scripts required to run all the different taggers to benchmark them for;
* Memory usage
    * RAM
    * GPU - when used
* Speed - Tokens per second

We benchmarks each type of tagger;
* Rule based
    * Test is performed for each supported spaCy model, but we only use one tagger per language of which that tagger is always the most resource intensive tagger (uses all the languages lexicons).
* Neural
    * Test is performed for each neural tagger model, but only on English data.
* Hybrid
    * Test only performed using the English rule based tagger resources on English data, but for each different neural tagger model.

## How to run the benchmark

We assume you have the development setup installed following these [instructions in the main README](../../README.md#setup).

And then you will need to download the relevant rule based and neural spaCy models like so (this can take a bit of time and will download up to 5GB of models to your disk via `pip`);

``` bash
./download_models.sh
```

To run all of the benchmarks on CPU (this will take between 5-30 minutes to run);

``` bash
./run_benchmarks.sh --device cpu
```

This will then produce on stdout the following MarkDown table;

<details>
<summary>Example Benchmark Markdown table</summary>

| Language | Tagger | Load Model Memory Requirements | Average Memory Requirements | Large Text Memory Requirements | Tokens Per Second | Number of Tokens Processed | Large Text Tokens Processed | Load Model GPU Memory Requirements | Average GPU Memory Requirements | Large Text GPU Memory Requirements |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| en| Rule Based| 161.40| 204.74| 160.91| 2698.62| 1,643| 1,084| 0.00| 0.00| 0.00 |
| en| Neural-E-17M| 259.38| 339.66| 691.49| 11323.55| 1,643| 1,084| 0.00| 0.00| 0.00 |
| en| Hybrid-E-17M| 179.99| 212.40| 502.98| 1302.13| 1,643| 1,084| 0.00| 0.00| 0.00 |
</details>

To run on GPU (you will need a Nvidia GPU), this first requires building the following docker container (this is best done in a terminal outside of your editor/IDE);

``` bash
docker build -t pymusas-gpu-benchmarking:0.1.0 -f ./Dockerfile ../..
```

And then you can run the benchmarks on GPU like so (you can also use this to run the CPU benchmarks as well)

``` bash
docker run --rm --gpus all --shm-size 4g pymusas-gpu-benchmarking:0.1.0 ARGUMENTS TO THE `run_benchmarks.sh` SCRIPT
```

Example;

``` bash
docker run --rm --gpus all --shm-size 4g pymusas-gpu-benchmarking:0.1.0 --device cuda --token-limit 100000 --large-text-token-limit 3000
```

### Run the benchmarks that are in the documentation

The commands we use to generate the benchmark statistics that are in the documentation;

``` bash
docker run --rm --gpus all --shm-size 4g pymusas-gpu-benchmarking:0.1.0 --device cpu --token-limit 100000 --large-text-token-limit 3000 > cpu_benchmarks.md
docker run --rm --gpus all --shm-size 4g pymusas-gpu-benchmarking:0.1.0 --device cuda --token-limit 100000 --large-text-token-limit 1500 > gpu_benchmarks.md
```

## How to interpret the benchmark results

All of the benchmarking uses Wikipedia texts, specifically from the [HuggingFaceFW/finewiki dataset repository](https://huggingface.co/datasets/HuggingFaceFW/finewiki), we used Wikipedia as it has an open license and covers all of the languages that our taggers support. All of the memory statistics are in Mega Bytes (MB).

Here we detail the meaning of each header in the markdown table;

* Language - The language code ([BCP 47 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)) of the Wikipedia data the tagger was processing, language codes are . **Note** for `xx` we use English.
* Tagger - The name of tagger type.
* Load Model Memory Requirements - The RAM/memory requirements to load the model.
* Average Memory Requirements - The RAM/memory requirements to load and run the model on the Wikipedia texts separated by new lines (not sentences therefore will be made up of multiple sentences, typically these represent paragraphs).
* Large Text Memory Requirements - The RAM/memory requirements to load and run the model on a single Wikipedia text that has been joined together from multiple Wikipedia texts to ensure the text is at least `--large-text-token-limit`.
* Tokens Per Second - Number of tokens the tagger processed per second.
* Number of Tokens Processed - Number of tokens processed to generate the `Tokens Per Second` metric, these tokens are from processing the Wikipedia texts separated by new lines, of which this is the same data that is used for `Average Memory Requirements`.
* Large Text Tokens Processed - The length in tokens of the large text that was processed to generate `Large Text Memory Requirements` metric.
* Load Model GPU Memory Requirements - The VRAM/GPU memory requirements to load the model.
* Average GPU Memory Requirements - The VRAM/GPU memory requirements to load and run the model on the Wikipedia texts separated by new lines (not sentences therefore will be made up of multiple sentences, typically these represent paragraphs).
* Large Text GPU Memory Requirements - The VRAM/GPU memory requirements to load and run the model on a single Wikipedia text that has been joined together from multiple Wikipedia texts to ensure the text is at least `--large-text-token-limit`.

**Note** the RAM/memory requirements are only estimates, but are a good guide. The reason they are only estimates as we cannot get the peak memory usage but rather the memory usage before and after a process has been completed, to get memory usage during the tagging process this would require running an external memory profiler, like [Scalene](https://github.com/plasma-umass/scalene) which we did not do here as it is difficult to get the memory requirement programmatically. For more accurate estimates you could run the [Scalene](https://github.com/plasma-umass/scalene) profile on an individual tagger benchmarking script, e.g. `scalene run benchmark_rule_based_tagger.py` (once you have installed `scalene`).

## Brief description of the benchmarking scripts

All of the scripts come with a `--help` guide if you want to know more about a specific script;

* `benchmark_rule_based_tagger.py` -- Used to benchmark the rule based tagger
* `benchmark_neural_tagger.py` -- Used to benchmark the neural tagger
* `benchmark_hybrid_tagger.py` -- Used to benchmark the hybrid tagger
* `benchmarking_utils.py` -- NOT A SCRIPT but a module used by the last 3 scripts that contains function used by all 3 scripts.
* `format_benchmarking_data.py` -- Formats the output generated from the 3 benchmarking scripts into a markdown table that is used to display the benchmarking results.
* `run_benchmarks.sh` -- A BASH script that calls the 3 Python scripts to benchmark all of the taggers across the different languages and Neural tagger model sizes, and then calls the `format_benchmarking_data.py` script to format the generated benchmarking results.
* `download_models.sh` -- downloads the spaCy models required for benchmarking the rule based and neural taggers within the `run_benchmarks.sh` script.
