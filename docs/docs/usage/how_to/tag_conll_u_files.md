---
title: Tag CoNLL-U Files
sidebar_position: 2
---

In this guide we will show how to tag text that is in [CoNLL-U formatted files](https://universaldependencies.org/format.html) and save the output to a TSV file. To make this guide as simple as possible we are going to base it on one language, **French**, and we are going to tag the [French GSD Universal Dependencies version 2.10 development treebank](https://raw.githubusercontent.com/UniversalDependencies/UD_French-GSD/r2.10/fr_gsd-ud-dev.conllu). As we are tagging a treebank that contains gold standard tokens, lemmas, and Part Of Speech tags we will not need any other NLP tools other than the [rule based pre-configured French PyMUSAS spaCy pipeline](https://github.com/UCREL/pymusas-models/releases/tag/fr_single_upos2usas_contextual-0.3.1) which will output [USAS](https://ucrel.lancs.ac.uk/usas/) semantic tags.

## Download the data

First we are going to download the [French GSD Universal Dependencies version 2.10 development treebank](https://raw.githubusercontent.com/UniversalDependencies/UD_French-GSD/r2.10/fr_gsd-ud-dev.conllu) and save it as `french_gsd_dev_2_10.conllu`


``` bash
curl -o french_gsd_dev_2_10.conllu https://raw.githubusercontent.com/UniversalDependencies/UD_French-GSD/r2.10/fr_gsd-ud-dev.conllu
```

The first 5 lines of the file should contain the following:

``` txt title="french_gsd_dev_2_10.conllu"
# global.columns = ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
# sent_id = fr-ud-dev_00001
# text = Aviator, un film sur la vie de Hughes.
1	Aviator	Aviator	PROPN	_	_	0	root	_	SpaceAfter=No
2	,	,	PUNCT	_	_	4	punct	_	_
```

## Python requirements

:::note

We assume for this guide that you have Python version >= `3.7` already installed.

:::

Now that we have the data we need to download the [French PyMUSAS spaCy pipeline](https://github.com/UCREL/pymusas-models/releases/tag/fr_single_upos2usas_contextual-0.3.1):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/fr_single_upos2usas_contextual-0.3.1/fr_single_upos2usas_contextual-0.3.1-py3-none-any.whl
```

And to easily parse the ConLL-U file we are going to use the Python package [conllu](https://pypi.org/project/conllu/):

``` bash
pip install conllu==4.4.2
```

## Tag a CoNLL-U File

First we are going to load the French PyMUSAS spaCy pipeline:

``` python
import csv
from pathlib import Path
from typing import List

from conllu import parse_incr
import spacy

# Load the French PyMUSAS rule based tagger
nlp = spacy.load("fr_single_upos2usas_contextual")
```

Then we are going to create the TSV file, `french_gsd_dev_2_10.tsv`, and the TSV writer so that we can save the tagged:

``` python
french_gsd_file = Path('french_gsd_dev_2_10.conllu').resolve()
french_output_tsv_file = Path('french_gsd_dev_2_10.tsv').resolve()

with french_output_tsv_file.open('w', encoding='utf-8', newline='') as output_fp:
    field_names = ['Token', 'Lemma', 'UPOS', 'USAS Tags']
    tsv_writer = csv.DictWriter(output_fp, fieldnames=field_names, delimiter='\t')
    tsv_writer.writeheader()
```

Now we are going to read each sentence in the French treebank and extract out the token, lemma, Universal Part Of Speech (UPOS) tag, and if the token contains a space after it or not (default is that there is a space after each token):

``` python
    with french_gsd_file.open('r', encoding='utf-8') as french_gsd_fp:
        for sentence in parse_incr(french_gsd_fp):
            sentence = sentence.filter(id=lambda x: type(x) is int)
            token_text: List[str] = []
            spaces: List[bool] = []
            lemmas: List[str] = []
            upos_tags: List[str] = []
            
            for token_data in sentence:
                token_text.append(token_data['form'])
                lemmas.append(token_data['lemma'])
                upos_tags.append(token_data['upos'])
                space = True
                if isinstance(token_data['misc'], dict):
                    if token_data['misc'].get('SpaceAfter', 'yes').lower() == 'no':
                        space = False
                spaces.append(space)
```

:::note

Notice that we add the filter:

``` python
sentence = sentence.filter(id=lambda x: type(x) is int)
```

This removes all tokens that have an `id` value that is not an integer, in CoNLL-U format the two token types that do not have integer values are: 

1. Tokens that get broken down into multiword tokens, these tokens are represented with an `id` that has an integer range, e.g. `1-2`.
2. Empty nodes, these tokens are represented with an `id` that is a float, e.g. `1.1`.

For more information on this see the [words, tokens and empty nodes section of the CoNLL-U format page.](https://universaldependencies.org/format.html#words-tokens-and-empty-nodes)

:::

:::note

In this example we use the UPOS tag for the POS tag, but some languages like [Welsh](https://ucrel.github.io/pymusas/usage/how_to/tag_text#welsh) require the POS tag to be from a different POS tagset other than the UPOS tagset that the UPOS tag comes from.

To know which POS tagset a PyMUSAS model requires the POS data to come from see the [overview of the models table from the PyMUSAS models repository](https://github.com/UCREL/pymusas-models#overview-of-the-models).

:::

Once we have this data for a sentence we shall use it to semantically tag the text:

``` python
            # As the tagger is a spaCy pipeline that expects tokens, pos, and lemma
            # we need to create a spaCy Doc object that will contain this information
            doc = spacy.tokens.Doc(nlp.vocab, words=token_text, pos=upos_tags,
                                   lemmas=lemmas, spaces=spaces)
            output_doc = nlp(doc)
```

Now we have the token, lemma, UPOS, and USAS semantic tag stored in the spaCy `doc` object we can then save it to a TSV file like so:

``` python
            # Write to TSV file
            for token in output_doc:
                tsv_writer.writerow({'Token': token.text,
                                     'Lemma': token.lemma_,
                                     'UPOS': token.pos_,
                                     'USAS Tags': token._.pymusas_tags})
```

The first 5 lines of the TSV output file should contain the following:

``` tsv title="french_gsd_dev_2_10.tsv"
Token	Lemma	UPOS	USAS Tags
Aviator	Aviator	PROPN	['Z99']
,	,	PUNCT	['PUNCT']
un	un	DET	['Z5']
film	film	NOUN	['Q4.3', 'O2/C1', 'O1.1', 'O1.2', 'B3']
```

The full Python script for this example can be seen below:

<details>
<summary>Python Script</summary>

``` python
import csv
from pathlib import Path
from typing import List

from conllu import parse_incr
import spacy

# Load the French PyMUSAS rule based tagger
nlp = spacy.load("fr_single_upos2usas_contextual")

french_gsd_file = Path('french_gsd_dev_2_10.conllu').resolve()
french_output_tsv_file = Path('french_gsd_dev_2_10.tsv').resolve()

with french_output_tsv_file.open('w', encoding='utf-8', newline='') as output_fp:
    field_names = ['Token', 'Lemma', 'UPOS', 'USAS Tags']
    tsv_writer = csv.DictWriter(output_fp, fieldnames=field_names, delimiter='\t')
    tsv_writer.writeheader()

    with french_gsd_file.open('r', encoding='utf-8') as french_gsd_fp:
        for sentence in parse_incr(french_gsd_fp):
            sentence = sentence.filter(id=lambda x: type(x) is int)
            token_text: List[str] = []
            spaces: List[bool] = []
            lemmas: List[str] = []
            upos_tags: List[str] = []
            
            for token_data in sentence:
                token_text.append(token_data['form'])
                lemmas.append(token_data['lemma'])
                upos_tags.append(token_data['upos'])
                space = True
                if isinstance(token_data['misc'], dict):
                    if token_data['misc'].get('SpaceAfter', 'yes').lower() == 'no':
                        space = False
                spaces.append(space)

            # As the tagger is a spaCy pipeline that expects tokens, pos, and lemma
            # we need to create a spaCy Doc object that will contain this information
            doc = spacy.tokens.Doc(nlp.vocab, words=token_text, pos=upos_tags,
                                lemmas=lemmas, spaces=spaces)
            output_doc = nlp(doc)

            # Write to TSV file
            for token in output_doc:
                tsv_writer.writerow({'Token': token.text,
                                     'Lemma': token.lemma_,
                                     'UPOS': token.pos_,
                                     'USAS Tags': token._.pymusas_tags})
```

</details>