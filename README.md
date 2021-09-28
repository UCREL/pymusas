# PymUSAS 

PYthon Multilingual Ucrel Semantic Analysis System

<hr/>

<p align="center">
    <a href="https://github.com/UCREL/pymusas/actions/workflows/ci.yml">
        <img alt="CI" src="https://github.com/UCREL/pymusas/actions/workflows/ci.yml/badge.svg?branch=main&event=push"/>
    </a>
    <a href="https://codecov.io/gh/UCREL/pymusas">
        <img alt="Code coverage" src="https://codecov.io/gh/UCREL/pymusas/branch/main/graph/badge.svg" />
    </a>
</p>

## Requirements

```
pip install -r requirements.txt
```

To test:

``` bash
python -m pytest --cov=pymusas --cov-report term-missing
```

### Development

When developing on the project you will want to install the Python package locally in editable format with all the extra requirements, this can be done like so:

```bash
pip install -e .[tests]
```

For a `zsh` shell, which is the default shell for the new Macs you will need to escape with `\` the brackets:

```zsh
pip install -e .\[tests\]
```

## Benchmarking

**NOTE** all of the benchmarking code requires a Linux based operating system due to the requirement to access the amount of memory used, using the [resource `getrusage` method.](https://docs.python.org/3/library/resource.html#resource.getrusage)

In this section we benchmark the taggers (currently only the one tagger), based on resource utilisation (memory and speed) and performance. The performance uses two metrics, both are percentages:

1. Accuracy
2. Coverage -- the number of tokens that have been tagged, that are not tagged with the unmatched tag (the `Z99` tag).

### Rule based tagger

Code to benchmark the rule based tagger:

``` bash
python benchmarks/rule_based_tagger.py --markdown
```

Output, this is based on the [Welsh gold standard dataset](https://github.com/CorCenCC/welsh_pos_sem_tagger/blob/master/data/cy_both_tagged.data), from the paper [Leveraging Pre-Trained Embeddings for Welsh Taggers.](https://aclanthology.org/W19-4332.pdf):

| Memory (MB) | Tokens Per Second | Accuracy (%) | Coverage (%) |
|-------------|-------------------|--------------|--------------|
| 112.78  | 20,046  | 68.94 | 91.97 |

**Note** that between different computers these figures are going to be different. On the Apple MacBook Air 2021 (M1) this uses a lot more memory, but is quicker than the Ubuntu desktop. The figures above are generated from my AMD Ryzen 5 1600 Six-Core Processor with 16GB of RAM on the Ubuntu operating system.


## Rule based tagging process

1. If `pos==punc` label as `PUNCT`
2. Lookup token and pos tag
3. Lookup lemma and pos tag
4. Lookup lower case token and pos tag
5. Lookup lower case lemma and pos tag
6. if `pos==num` label as `N1`
7. Lookup token with any POS tag and choose first entry in lexicon.
8. Lookup lemma with any POS tag and choose first entry in lexicon.
9. Lookup lower case token with any POS tag and choose first entry in lexicon.
10. Lookup lower case lemma with any POS tag and choose first entry in lexicon.
11. Label as `Z99`, this is the unmatched semantic tag.

## Resources

1. [Multilingual USAS lexicons](https://github.com/UCREL/Multilingual-USAS)
2. [Welsh Semantic Tagger, Java version.](https://github.com/CorCenCC/CySemTagger)
3. [Welsh gold standard dataset](https://github.com/CorCenCC/welsh_pos_sem_tagger/blob/master/data/cy_both_tagged.data), this dataset uses the basic POS tags, see appendix A1 of this [paper](https://aclanthology.org/W19-4332.pdf), from the [CyTag](https://github.com/CorCenCC/CyTag) POS tagger.
4. [Mapping basic CyTag POS tags to core POS tags used by the USAS lexicon.](./resources/basic_cy_tags_to_core_tags.json)
5. [Detailed paper on the USAS tagset](https://e-space.mmu.ac.uk/619652/1/C%3A%5CUsers%5C55119166%5CDesktop%5CComparing%20USAS%20with%20lexicographical%20taxonomies.pdf)

## Semantic Resources

### USAS tagset

The text from this sub-section has been copied from the TAGSET section of the [USAS guide](https://ucrel-web.lancs.ac.uk/usas/usas_guide.pdf).

The semantic tags are composed of:

1. an upper case letter indicating general discourse field.
2. a digit indicating a first subdivision of the field.
3. (optionally) a decimal point followed by a further digit to indicate a finer subdivision.
4. (optionally) one or more ‘pluses’ or ‘minuses’ to indicate a positive or negative position on a semantic scale.
5. (optionally) a slash followed by a second tag to indicate clear double membership of categories.
6. (optionally) a left square bracket followed by ‘i’ to indicate a semantic template (multi-word unit). 

Other symbols utilised:

* % = rarity marker (1)
* @ = rarity marker (2)
* f = female
* m = male
* c = potential antecedents of conceptual anaphors (neutral for number)
* n = neuter
* i = indicates a semantic idiom

Antonymity of conceptual classifications is indicated by +/- markers on tags Comparatives and superlatives receive double and triple +/- markers respectively. Certain words and collocational units show a clear double (and in some instances, triple) membership of categories. Such cases are dealt with using slash tags, that is, all tags are indicated and separated by a slash (e.g. anti-royal = E2-/S7.1+, accountant = I2.1/S2mf, bunker = G3/H1 K5.1/W3, Admiral = G3/M4/S2mf S7 1+/S2mf, dowry = S4/I1/A9-). The initial tagset was loosely based on Tom McArthur's Longman Lexicon of Contemporary English (McArthur, 1981) as this appeared to offer the most appropriate thesaurus type classification of word senses for this kind of analysis. We have since considerably revised the tagset in the light of practical tagging problems met in the course of the research. The revised tagset is arranged in a hierarchy with 21 major discourse fields expanding into 232 category labels. 

The following table shows the 21 labels at the top level of the hierarchy.

<table style="text-align:center;">
    <tbody>
        <tr>
            <td><strong>A</strong></br>general and abstract terms</td>
            <td><strong>B</strong></br>the body and the individual</td>
            <td><strong>C</strong></br>arts and crafts</td>
            <td><strong>E</strong></br>emotion</td>
        </tr>
        <tr>
            <td><strong>F</strong></br>food and farming</td>
            <td><strong>G</strong></br>government and public</td>
            <td><strong>H</strong></br>architecture, housing and the home</td>
            <td><strong>I</strong></br>money and commerce in industry</td>
        </tr>
        <tr>
            <td><strong>K</strong></br>entertainment, sports and games</td>
            <td><strong>L</strong></br>life and living things</td>
            <td><strong>M</strong></br>movement, location, travel and transport</td>
            <td><strong>N</strong></br>numbers and measurement</td>
        </tr>
        <tr>
            <td><strong>O</strong></br>substances, materials, objects and equipment</td>
            <td><strong>P</strong></br>education</td>
            <td><strong>Q</strong></br>language and communication</td>
            <td><strong>S</strong></br>social actions, states and processes</td>
        </tr>
        <tr>
            <td><strong>T</strong></br>time</td>
            <td><strong>W</strong></br>world and environment</td>
            <td><strong>X</strong></br>psychological actions, states and processes</td>
            <td><strong>Y</strong></br>science and technology</td>
        </tr>
        <tr>
            <td><strong>Z</strong></br>names and grammar</td>
        </tr>
    </tbody>
</table>