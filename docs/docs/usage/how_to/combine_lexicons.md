---
title: Combine/Merge Lexicons
sidebar_position: 3
---

In this guide we will show how to combine two lexicons together, both for single word and Multi Word Expression (MWE), so that the combined lexicon can be used in a single PyMUSAS [RuleBasedTagger](/api/spacy_api/taggers/rule_based#rulebasedtagger).

This approach is useful if you want the coverage of the existing lexicons that are available for the given language but you want to customize them. You might want to customize them because;
* Want to add domain specific language to the lexicons, e.g. `flat_* white_*` = `F2/Z3` (type of coffee)
* Want to override/change an existing lexicon with a different semantic tag, e.g. in the [English semantic lexicon](https://github.com/UCREL/Multilingual-USAS/blob/6b305509016b21cd9062c5f77c1f29313ca9cc53/English/semantic_lexicon_en.tsv#L586C1-L586C18) `Amazon PROPN` is associated with `Z2 M7` a semantic tag associated with *Geographical names* and *Places* but perhaps in your corpus you would like it to be associated with the company therefore change the semantic tag to `Z3`.

All of the existing lexicons for different language can be found at the [Multilingual-USAS repository](https://github.com/UCREL/Multilingual-USAS/tree/master), in this guide we will only use the [English lexicons](https://github.com/UCREL/Multilingual-USAS/tree/master/English).

This guide is going to show how to create a PyMUSAS [RuleBasedTagger](/api/spacy_api/taggers/rule_based#rulebasedtagger) that uses the existing [English lexicons](https://github.com/UCREL/Multilingual-USAS/tree/master/English) with additional custom lexicons that both extend the existing as well as override them. The guide will be broken down into:

1. Setup
2. How the existing tagger performs
3. How to customize the tagger through combining the existing lexicon with a custom lexicon

## Setup

Download both the [English PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/en_dual_none_contextual-0.3.3) and the [small English spaCy model](https://spacy.io/models/en):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/en_dual_none_contextual-0.3.3/en_dual_none_contextual-0.3.3-py3-none-any.whl
python -m spacy download en_core_web_sm
```

We are going to use 2 example custom lexicons, this is for example purposes only as we assume the custom lexicons you will use contain different/more lexicons and you don't need to have both a single and MWE lexicon.

The custom single word lexicon, that we assume is saved to a file at `./custom_semantic_lexicon.tsv`
```tsv title="custom_semantic_lexicon.tsv"
lemma	pos	semantic_tags
Amazon	PROPN	Z3
broligarchy	NOUN	S5
```

The custom MWE lexicon, that we assume is saved to a file at `./custom_mwe.tsv`
``` tsv title="custom_mwe.tsv"
mwe_template	semantic_tags
battery_NOUN farm_NOUN	Z3/Y1/W3
flat_* white_*	F2/Z3
```

These files can be saved anywhere locally or even at a URL, just change the file path in the code to the location of these files.

The example sentence we are going to use throughout is:

``` python
sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy")
```

Using this sentence and the custom lexicons we will show that we can netter reflect the meaning in this sentence.

## How the existing tagger performs

Using the off the shelf [English PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/en_dual_none_contextual-0.3.3) with the single and MWE lexicons we get the following tags for the example sentence:

``` tsv
Text    Lemma   POS     USAS Tags
While   while   SCONJ   ['Z5']
drinking        drink   VERB    ['A5.4+']
my      my      PRON    ['A5.4+']
flat    flat    ADJ     ['O4.4', 'O3', 'O4.1', 'K2', 'A5.3+']
white   white   NOUN    ['O4.3', 'O4.3/S2mf', 'F2', 'F1', 'B1']
I       I       PRON    ['Z8mf']
was     be      AUX     ['A3+', 'Z5']
reading read    VERB    ['Q3', 'Q1.2', 'X3.2+', 'X2.5+', 'P1', 'A10+']
about   about   ADP     ['Z5']
the     the     DET     ['Z5']
new     new     ADJ     ['T3-']
battery battery NOUN    ['F4']
farm    farm    NOUN    ['F4']
that    that    SCONJ   ['Z5', 'Z8']
Amazon  Amazon  PROPN   ['Z2', 'M7']
is      be      AUX     ['A3+', 'Z5']
creating        create  VERB    ['A1.1.1', 'A2.2', 'E1']
which   which   DET     ['Z5', 'Z8']
is      be      AUX     ['A3+', 'Z5']
owned   own     VERB    ['A9+']
by      by      ADP     ['Z5']
one     one     NUM     ['N1', 'T3', 'T1.2']
of      of      ADP     ['Z5']
the     the     DET     ['Z5']
broligarchy     broligarchy     NOUN    ['Z99']
```

As you can see `flat white` is not recognised as a drink, `broligarchy` is not recognised at all as it is a new word according to [collins dictionary](https://www.collinsdictionary.com/dictionary/english/brollies), `Amazon` is assumed to be the rain forest in Brazil, and `battery farm` is recognised as a farm with livestock rather than a farm with batteries.

This was created using the following code:

<details>
<summary>Python Script</summary>

``` python
import spacy


sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy")

# We exclude the following components as we do not need them. 
nlp = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
# Load the English PyMUSAS rule-based tagger in a separate spaCy pipeline
english_tagger_pipeline = spacy.load('en_dual_none_contextual')
# Adds the English PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=english_tagger_pipeline)

output_doc = nlp(sentence)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
```

</details>

## How to customize the tagger through combining the existing lexicon with a custom lexicon

In the code below we show that we first need to create a combined/merged single word lexicon from the existing single word lexicon in the Multilingual USAS GitHub repository, this is done through the [RuleBasedTagger](/api/spacy_api/taggers/rule_based#rulebasedtagger) function which downloads/loads the TSV files and then merges them whereby the last TSV file in the list overrides any lexicon entries that come before it thus the custom lexicon(s) should come after the existing/general lexicon:

``` python
# Get the existing single word lexicon from the Multilingual USAS repository
existing_single_lexicon_url = ("https://raw.githubusercontent.com/UCREL/"
                               "Multilingual-USAS/refs/heads/master/"
                               "English/semantic_lexicon_en.tsv")
custom_single_lexicon_path = Path("/workspaces/pymusas/scripts/combine_lexicon_example/custom_semantic_lexicon.tsv")

# Download and merge with only lemma/word information
combined_single_lexicon_data = LexiconCollection.tsv_merge(*[existing_single_lexicon_url,
                                                             custom_single_lexicon_path],
                                                           include_pos=False)

# Download and merge with POS information
combined_single_pos_lexicon_data = LexiconCollection.tsv_merge(*[existing_single_lexicon_url,
                                                                 custom_single_lexicon_path],
                                                               include_pos=True)
```

Then do the same for MWE lexicon:

``` python
# Get the existing MWE lexicon from the Multilingual USAS repository
existing_mwe_lexicon_url = ("https://raw.githubusercontent.com/UCREL/"
                            "Multilingual-USAS/refs/heads/master/"
                            "English/mwe-en.tsv")
custom_mwe_lexicon_path = Path("/workspaces/pymusas/scripts/combine_lexicon_example/custom_mwe.tsv")
combined_mwe_lexicon_data = MWELexiconCollection.tsv_merge(*[existing_mwe_lexicon_url,
                                                             custom_mwe_lexicon_path])
```

After this we need to setup the rest of the tagger and add it to the English spaCy pipeline, the full code for this can be found below:

<details>
<summary>Python Script</summary>

``` python
from pathlib import Path

import spacy
from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.taggers.rules.mwe import MWERule

# Get the existing single word lexicon from the Multilingual USAS repository
existing_single_lexicon_url = ("https://raw.githubusercontent.com/UCREL/"
                               "Multilingual-USAS/refs/heads/master/"
                               "English/semantic_lexicon_en.tsv")
custom_single_lexicon_path = Path("custom_semantic_lexicon.tsv")

# Download and merge with only lemma/word information
combined_single_lexicon_data = LexiconCollection.tsv_merge(*[existing_single_lexicon_url,
                                                             custom_single_lexicon_path],
                                                           include_pos=False)

# Download and merge with POS information
combined_single_pos_lexicon_data = LexiconCollection.tsv_merge(*[existing_single_lexicon_url,
                                                               custom_single_lexicon_path],
                                                               include_pos=True)

# Get the existing MWE lexicon from the Multilingual USAS repository
existing_mwe_lexicon_url = ("https://raw.githubusercontent.com/UCREL/"
                               "Multilingual-USAS/refs/heads/master/"
                               "English/mwe-en.tsv")
custom_mwe_lexicon_path = Path("custom_mwe.tsv")
combined_mwe_lexicon_data = MWELexiconCollection.tsv_merge(*[existing_mwe_lexicon_url,
                                                             custom_mwe_lexicon_path])

# Creating the PyMUSAS tagger resources
single_word_rule = SingleWordRule(lexicon_collection=combined_single_pos_lexicon_data,
                                  lemma_lexicon_collection=combined_single_lexicon_data,
                                  pos_mapper=None)
mwe_word_rule = MWERule(mwe_lexicon_lookup=combined_mwe_lexicon_data,
                        pos_mapper=None)
rules = [single_word_rule, mwe_word_rule]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))

# Loading the English spaCy pipeline
# We exclude the following components as we do not need them. 
nlp = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
# Adding a blank PyMUSAS tagger
pymusas_tagger = nlp.add_pipe('pymusas_rule_based_tagger')
# Adding our custom resources to the tagger
pymusas_tagger.initialize(rules=rules,
                          ranker=ranker,
                          default_punctuation_tags=["PUNCT"],
                          default_number_tags=["NUM"])

sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy")
output_doc = nlp(sentence)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')

```

</details>

Of which when ran on the same sentence it produces the following:

``` tsv
Text    Lemma   POS     USAS Tags
While   while   SCONJ   ['Z5']
drinking        drink   VERB    ['A5.4+']
my      my      PRON    ['A5.4+']
flat    flat    ADJ     ['F2/Z3']
white   white   NOUN    ['F2/Z3']
I       I       PRON    ['Z8mf']
was     be      AUX     ['A3+', 'Z5']
reading read    VERB    ['Q3', 'Q1.2', 'X3.2+', 'X2.5+', 'P1', 'A10+']
about   about   ADP     ['Z5']
the     the     DET     ['Z5']
new     new     ADJ     ['T3-']
battery battery NOUN    ['Z3/Y1/W3']
farm    farm    NOUN    ['Z3/Y1/W3']
that    that    SCONJ   ['Z5', 'Z8']
Amazon  Amazon  PROPN   ['Z3']
is      be      AUX     ['A3+', 'Z5']
creating        create  VERB    ['A1.1.1', 'A2.2', 'E1']
which   which   DET     ['Z5', 'Z8']
is      be      AUX     ['A3+', 'Z5']
owned   own     VERB    ['A9+']
by      by      ADP     ['Z5']
one     one     NUM     ['N1', 'T3', 'T1.2']
of      of      ADP     ['Z5']
the     the     DET     ['Z5']
broligarchy     broligarchy     NOUN    ['S5']
```

As you can see `flat white` is recognised as a drink and a proper noun, `broligarchy` is recognised as a group, `Amazon` is linked to a company, and `battery farm` is recognised more to do with proper noun/science and technology/green issues.


:::note

At the moment we assume when you are merging lexicons together they are using the same Part Of Speech (POS) tagset.

:::