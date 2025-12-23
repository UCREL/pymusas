---
title: Hybrid Tagger
sidebar_position: 3
---

:::note
The hybrid tagger requires PyMUSAS with the neural extra installed as shown in the installation [documentation](../../getting_started/installation.md#install-for-neural-or-hybrid-taggers).
:::

In this guide we are going to show you how to tag text with the PyMUSAS [HybridTagger](/api/spacy_api/taggers/hybrid#hybridtagger) so that you can extract token level [USAS semantic tags](https://ucrel.lancs.ac.uk/usas/) from the tagged text. The guide will take you through how to construct the tagger, add it to an existing spaCy pipeline, and then tag text with it. This guide is best read after following the [Rule Based Tagger](./rule_based_tagger.md) and [Neural Tagger](./neural_tagger.md) how to tag text guides as the hybrid tagger is a combination of both taggers.

## Construct the hybrid tagger

The hybrid tagger has no pre-configured spaCy components, it has to be created. The hybrid tagger requires the following resources;
* **A single and/or Multi Word Expression (MWE) lexicon.** We have various lexicons for you to choose for multiple languages which can be found at [Multilingual-USAS repository](https://github.com/UCREL/Multilingual-USAS/tree/master), but we recommend keeping to the 11 languages that we support in the [Rule Based Tagger](./rule_based_tagger.md) as these are also supported with lemma and/or Part Of Speech (POS) tagger from spaCy.
* **A Neural Tagger model.** We have released 2 English, and 2 Multilingual Neural taggers to choose from, see [available taggers](./neural_tagger.md#available-taggers)

In this guide we are going to show how to create the English hybrid tagger using both the [single](https://github.com/UCREL/Multilingual-USAS/blob/2cc9966a3bdcc84bc204d16bdf4318fc28495016/English/semantic_lexicon_en.tsv) and [MWE](https://github.com/UCREL/Multilingual-USAS/blob/2cc9966a3bdcc84bc204d16bdf4318fc28495016/English/mwe-en.tsv) lexicons with the [smallest English Neural Tagger](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM).

We are going to use the [small English spaCy model](https://spacy.io/models/en) as the lemmatizer and POS tagger, thus we need to download it first:

``` bash
python -m spacy download en_core_web_sm
```

Then setup the English spaCy pipeline for lemmatizing and POS tagging:
``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
```

Next we create all of the resources required to create the Rule Based Tagger for the Hybrid Tagger:
``` python
# URLS to the English single and MWE lexicons
english_single_lexicon_url = ('https://raw.githubusercontent.com/UCREL/Multilingual-USAS/'
                              '2cc9966a3bdcc84bc204d16bdf4318fc28495016/'
                              'English/semantic_lexicon_en.tsv')
english_mwe_lexicon_url = ('https://raw.githubusercontent.com/UCREL/Multilingual-USAS/'
                           '2cc9966a3bdcc84bc204d16bdf4318fc28495016/'
                           'English/mwe-en.tsv')
lexicon_lookup = LexiconCollection.from_tsv(english_single_lexicon_url, include_pos=True)
lemma_lexicon_lookup = LexiconCollection.from_tsv(english_single_lexicon_url, include_pos=False)
mwe_lexicon_lookup = MWELexiconCollection.from_tsv(english_mwe_lexicon_url)
# The rules that use the lexicons
single_word_rule = SingleWordRule(lexicon_lookup, lemma_lexicon_lookup)
mwe_word_rule = MWERule(mwe_lexicon_lookup)
word_rules = [single_word_rule, mwe_word_rule]
# The ranker that determines which rule should be used/applied
ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments(word_rules)
ranker = ContextualRuleBasedRanker(*ranker_arguments)
# POS that indicate a Punctuation and Numeric value
default_punctuation_tags = set(['PUNCT'])
default_number_tags = set(['NUM'])
```

We then load a blank Hybrid Tagger that is yet to be initialized with the rule based and neural resources:
``` python
# Initializing the tagger with no resources
tagger = nlp.add_pipe('pymusas_hybrid_tagger', config={"top_n": 10})
```

We then add the resources to the Hybrid tagger like so:
``` python
tagger.initialize(rules=word_rules,
                  ranker=ranker,
                  default_punctuation_tags=default_punctuation_tags,
                  default_number_tags=default_number_tags,
                  pretrained_model_name_or_path="ucrelnlp/PyMUSAS-Neural-English-Small-BEM")
```
Whereby `pretrained_model_name_or_path` is the HuggingFace model id ([ucrelnlp/PyMUSAS-Neural-English-Small-BEM](https://huggingface.co/ucrelnlp/PyMUSAS-Neural-English-Small-BEM)). For more information on the arguments to pass to the Hybrid Tagger see the [HybridTagger class initialize method arguments.](/api/spacy_api/taggers/hybrid#initialize)

We can now run the tagger, we are going to use a sample of text taken from the English Wikipedia page on the topic of [`The Nile River`](https://en.wikipedia.org/wiki/Nile):

``` python
text = "while the Blue Nile begins at Lake Tana in Ethiopia[6] and flows into Sudan from the southeast."

output_doc = nlp(text)

print(f'{"Text":<20}{"Lemma":<20}{"POS":<8}USAS Tags')
for token in output_doc:
    print(f'{token.text:<20}{token.lemma_:<20}{token.pos_:<8}{token._.pymusas_tags}')
```

We can easily see below the words that the neural tagger was required for `Ethiopia[6` and `southeast` as these are the only 2 words with exactly 10 semantic tags which are the number of semantic tags we configured the Hybrid Tagger to output when using the neural tagger.

<details>
<summary>Output</summary>

```tsv
Text                Lemma               POS     USAS Tags
while               while               SCONJ   ['Z5']
the                 the                 DET     ['Z5']
Blue                Blue                PROPN   ['Z1mf', 'Z3c']
Nile                Nile                PROPN   ['Z1mf', 'Z3c']
begins              begin               VERB    ['T2+']
at                  at                  ADP     ['Z5']
Lake                Lake                PROPN   ['Z1mf', 'Z3c']
Tana                Tana                PROPN   ['Z1mf', 'Z3c']
in                  in                  ADP     ['Z5']
Ethiopia[6          ethiopia[6          NOUN    ['Z2', 'Z1', 'Z3', 'T3', 'T1.3', 'N1', 'N3.2', 'T1.2', 'S2', 'S7.1']
]                   ]                   PUNCT   ['PUNCT']
and                 and                 CCONJ   ['Z5']
flows               flow                VERB    ['M4', 'M1']
into                into                ADP     ['Z5']
Sudan               Sudan               PROPN   ['Z2']
from                from                ADP     ['Z5']
the                 the                 DET     ['Z5']
southeast           southeast           NOUN    ['M6', 'Z2', 'Z3', 'M7', 'Z1', 'S2', 'N3.3', 'S7.1', 'M4', 'N5']
.                   .                   PUNCT   ['PUNCT']
```
</details>

We can then compare it to the output from the English Rule based tagger, and as we can see from the output below, indeed the Rule Based tagger generated the unknown tag `Z99` for those two words but apart from that it is the same.

<details>
<summary>Rule Based Tagger Output</summary>

Output:

```tsv
Text                USAS Tags
while               ['Z5']
the                 ['Z5']
Blue                ['Z1mf', 'Z3c']
Nile                ['Z1mf', 'Z3c']
begins              ['T2+']
at                  ['Z5']
Lake                ['Z1mf', 'Z3c']
Tana                ['Z1mf', 'Z3c']
in                  ['Z5']
Ethiopia[6          ['Z99']
]                   ['PUNCT']
and                 ['Z5']
flows               ['M4', 'M1']
into                ['Z5']
Sudan               ['Z2']
from                ['Z5']
the                 ['Z5']
southeast           ['Z99']
.                   ['PUNCT']
```

Code and installable requirements to generate the output:

Install requirements:

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/en_dual_none_contextual_none-0.4.0/en_dual_none_contextual_none-0.4.0-py3-none-any.whl
python -m spacy download en_core_web_sm
```

Code:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
# Load the English PyMUSAS rule-based tagger in a separate spaCy pipeline
english_tagger_pipeline = spacy.load('en_dual_none_contextual_none')
# Adds the English PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=english_tagger_pipeline)

text = "while the Blue Nile begins at Lake Tana in Ethiopia[6] and flows into Sudan from the southeast."

output_doc = nlp(text)

print(f'{"Text":<20}USAS Tags')
for token in output_doc:
    print(f'{token.text:<20}{token._.pymusas_tags}')
```
</details>