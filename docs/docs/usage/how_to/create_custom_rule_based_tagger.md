---
title: Create a Custom Rule Based Tagger
sidebar_position: 2
---

In this guide we are going to create a custom rule based tagger whereby the Single and Multi Word Expression (MWE) lexicons are different to those that are in the [standard rule based tagger(s)](/usage/how_to/tag_text_with/rule_based_tagger) (all lexicons for the standard rule based taggers can be found in the [Multilingual USAS GitHub repository](https://github.com/UCREL/Multilingual-USAS), i.e. for English both single and MWE lexicons can be found [here](https://github.com/UCREL/Multilingual-USAS/tree/master/English)).


When customising the rule based taggers, you can only change the lexicons that are used within the tagger. The rules that govern the tagger itself cannot be changed, but the rules themselves are heavily based around the lexicons. For more information about the rules used in the tagger please see [the ranking rules section in the Context Rule Based Ranker class documentation.](/api/rankers/lexicon_entry#contextualrulebasedranker).

Custom rule based taggers are useful when you want to create a tagger;
* For a language that the standard taggers do not cover. 
* For a specific domain - medical, legal, etc.
* For a different time period - 17th century etc. (meanings can change over time hence the need for a custom lexicon).

You may think to yourself that you might want to combine standard lexicons we already have with your custom lexicon, in this case we have a different guide for that [Combine/Merge Lexicons guide](/usage/how_to/combine_lexicons), this guide will introduce many of the same concepts as [Combine/Merge Lexicons guide](/usage/how_to/combine_lexicons), but with the addition of showing you how to setup a rule based tagger with custom POS tagger and lemmatiser, as well as creating a custom tagger whereby the POS tagset of the lexicons is different to the POS tagger.

1. [Setup](#setup)
2. [How to create a custom tagger](#how-to-create-a-custom-tagger)
3. [Setup a custom tagger with custom POS tagger and lemmatiser](#setup-a-custom-tagger-with-custom-pos-tagger-and-lemmatiser)
4. [Setup the custom tagger whereby the tagset of the lexicons is different to the tagset of the POS tagger](#custom-tagger-with-different-pos-tagset-for-lexicons-and-pos-tagger)

## Setup

Download the [small English spaCy model](https://spacy.io/models/en), this will be used in [How to create a custom tagger section](#how-to-create-a-custom-tagger) to tokenize, lemmatise, and POS tag the data.

``` bash
python -m spacy download en_core_web_sm
```

We are going to use two example custom lexicons, this is for example purposes only as we assume the custom lexicon you will use contains different/more lexicons and you don't need to have both a single and MWE lexicon.

The custom single word lexicon, that we assume is saved to a file at `./custom_semantic_lexicon.tsv`

``` tsv title="custom_semantic_lexicon.tsv"
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

These file can be saved anywhere locally or even at a URL, just change the file path in the code to the location of these files.

You may have noticed that the POS tags used in both lexicons have come from the [Universal POS (UPOS) tagset](https://universaldependencies.org/u/pos/), of which this aligns with the coarse grained POS tags that the English spaCy model provides (the English spaCy model POS tags with a finer grained tagset but then [maps to the coarser UPOS tagset using the attribute ruler](https://spacy.io/models#design-cnn)).

The example sentence we are going to use throughout is:

``` python
sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy.")
```

We will show how the custom lexicon can be used to semantically tag the tokens in this sentence with the custom lexicons provided, later we will show how to do this with a custom lemmatiser and POS tagger.


## How to create a custom tagger

First we load the single and MWE lexicons into Python dictionary format that the Single and MWE rule classes accept as arguments;

``` python
from pathlib import Path

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection

sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy.")

# File path to the custom semantic lexicon TSV file
single_lexicon_path = Path("custom_semantic_lexicon.tsv")

# Load the single lexicon data without POS information
single_lexicon_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=False)
# Load the single lexicon data with POS information
single_lexicon_pos_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=True)

# File path to the custom MWE lexicon TSV file
mwe_lexicon_path = Path("custom_mwe.tsv")

# Load the MWE lexicon data
mwe_lexicon_data = MWELexiconCollection.from_tsv(mwe_lexicon_path)
```

We then create the [Single](/api/taggers/rules/single_word#singlewordrule) and [MWE](/api/taggers/rules/mwe#mwerule) rules, these rules when called on tokens create a list of lexicon matches with ranking data that is then used later on by the ranker.

:::note

A rule can create more than one match per token, for instance the token `Amazon` can be matched with a lexicon entry either by it's token and POS tag, token without POS, lemma (not all tokens have a different lemma form), or lower cased `amazon`. Thus, `Amazon` could be matched to multiple lexicon entries, hence why you need ranking data for the ranker to determine which is the best lexicon entry match.

:::

``` python
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.taggers.rules.mwe import MWERule

single_word_rule = SingleWordRule(lexicon_collection=single_lexicon_pos_data,
                                  lemma_lexicon_collection=single_lexicon_data,
                                  pos_mapper=None)
mwe_rule = MWERule(mwe_lexicon_lookup=mwe_lexicon_data,
                   pos_mapper=None)
rules = [single_word_rule, mwe_rule]
```

:::info

If your Single word lexicon does not contain any POS tag information then pass an empty dictionary as an argument for `lexicon_collection` to `SingleWordRule` like so;

``` python
single_word_rule = SingleWordRule(lexicon_collection={},
                                  lemma_lexicon_collection=single_lexicon_data,
                                  pos_mapper=None)
```

:::

We can then create the ranker, this takes the ranking data from the rules and ranks the matches whereby the semantic tag that is first in the output list from the tagger has been ranked highest by this ranker. The ranker, [Contextual Rule Based Ranker](/api/rankers/lexicon_entry#contextualrulebasedranker), requires information about the lexicons specifically; maximum n-gram length and maximum number of wildcards of which these can be easily found by passing the rules as a list to [ContextualRuleBasedRaker.get_construction_arguments method](/api/rankers/lexicon_entry#get_construction_arguments) like so;

``` python
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker

ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments([single_word_rule])
ranker = ContextualRuleBasedRanker(*ranker_arguments)
```

:::note
If you only use a Single word lexicon and thus only a Single word rule the return from [ContextualRuleBasedRaker.get_construction_arguments method](/api/rankers/lexicon_entry#get_construction_arguments) will always be `1` and `0` for maximum n-gram length and maximum number of wildcards even if you have wildcards in your single word lexicon. This is because we assume wildcard symbols `*` will never match a POS tag value and thus can be ignored when performing a lookup.
:::

We now have all of the components to create the PyMUSAS rule based tagger, but first we need to setup the tokeniser, lemmatiser, and POS tagger pipeline with the small spaCy English model;

``` python
import spacy

# Loading the English spaCy pipeline
# We exclude the following components as we do not need them. 
nlp = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
```

We next need to add a blank PyMUSAS tagger (a tagger that contains no lexicons);

``` python
import pymusas
# Adding a blank PyMUSAS tagger
pymusas_tagger = nlp.add_pipe('pymusas_rule_based_tagger')
```

We can now add our rules and ranker to the [Rule Based Tagger](/api/spacy_api/taggers/rule_based#rulebasedtagger) that we created earlier, and we can select which POS tags from the POS tagset of the POS tagger, in our case the [UPOS tagset](https://universaldependencies.org/u/pos/), should be used to determine if a token is punctuation or a number through the `default_punctuation_tags` and `default_number_tags` arguments. The list of POS tags passed to `default_punctuation_tags` and `default_number_tags` can be empty if you do not have a lemmatiser or POS tagger and will only be used if the lexicons provided could not find a match for the given token. The USAS tags assigned to punctuation and number tokens are `PUNCT` and `N1` respectively. Any token that cannot be assigned a USAS tag based off the lexicons or `default_punctuation_tags` and `default_number_tags` will be assigned the `Z99` tag, the unmatched tag. Full list of tags and their meanings can be found in the [introduction to the USAS category system.](https://ucrel.lancs.ac.uk/usas/usas_guide.pdf)

``` python
# Adding our custom resources to the tagger
pymusas_tagger.initialize(rules=rules,
                          ranker=ranker,
                          default_punctuation_tags=["PUNCT"],
                          default_number_tags=["NUM"])
```

We can now run the tagger like so;

``` python
output_doc = nlp(sentence)

print(f'{"Text":<15}{"lemma":<15}{"POS":<10}{"USAS Tags":<15}Is MWE')
for token in output_doc:
    is_mwe = False
    mwe_indexes = token._.pymusas_mwe_indexes
    all_mwe_indexes = [index for indexes in mwe_indexes for index in indexes]
    lowest_index, highest_index = min(all_mwe_indexes), max(all_mwe_indexes)
    if highest_index >= (lowest_index + 2):
        is_mwe = True 

    print(f'{token.text:<15}{token.lemma_:<15}{token.pos_:<10}{token._.pymusas_tags!r:<15}{is_mwe}')
```

Which produces the following;

``` bash
Text           lemma          POS       USAS Tags      Is MWE
While          while          SCONJ     ['Z99']        False
drinking       drink          VERB      ['Z99']        False
my             my             PRON      ['Z99']        False
flat           flat           ADJ       ['F2/Z3']      True
white          white          NOUN      ['F2/Z3']      True
I              I              PRON      ['Z99']        False
was            be             AUX       ['Z99']        False
reading        read           VERB      ['Z99']        False
about          about          ADP       ['Z99']        False
the            the            DET       ['Z99']        False
new            new            ADJ       ['Z99']        False
battery        battery        NOUN      ['Z3/Y1/W3']   True
farm           farm           NOUN      ['Z3/Y1/W3']   True
that           that           SCONJ     ['Z99']        False
Amazon         Amazon         PROPN     ['Z3']         False
is             be             AUX       ['Z99']        False
creating       create         VERB      ['Z99']        False
which          which          DET       ['Z99']        False
is             be             AUX       ['Z99']        False
owned          own            VERB      ['Z99']        False
by             by             ADP       ['Z99']        False
one            one            NUM       ['N1']         False
of             of             ADP       ['Z99']        False
the            the            DET       ['Z99']        False
broligarchy    broligarchy    NOUN      ['S5']         False
.              .              PUNCT     ['PUNCT']      False
```

As we can see the tokens in the lexicon like `flat white`, `battery farm`, `Amazon`, and `broligarchy` all have non `Z99` USAS tags that have come from the custom lexicons. In addition we can see that both `battery farm` and `flat white` are identified as MWEs. Both `one` and `.` have the `N1` and `PUNCT` tags from the assigned default punctuation and number POS tag lists set when creating the Rule Based tagger. All of the other tokens have the unmatched USAS tag, `Z99`, as expected as they do not match any token in the custom lexicon or default punctuation and number POS tag lists.

The full Python code for this example can be found below:

<details>

<summary>Python Script</summary>

``` python
from pathlib import Path

import spacy

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.mwe import MWERule

sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy.")

# File path to the custom semantic lexicon TSV file
single_lexicon_path = Path("custom_semantic_lexicon.tsv")

# Load the single lexicon data without POS information
single_lexicon_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=False)
# Load the single lexicon data with POS information
single_lexicon_pos_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=True)

# File path to the custom MWE lexicon TSV file
mwe_lexicon_path = Path("custom_mwe.tsv")

# Load the MWE lexicon data
mwe_lexicon_data = MWELexiconCollection.from_tsv(mwe_lexicon_path)

single_word_rule = SingleWordRule(lexicon_collection=single_lexicon_pos_data,
                                           lemma_lexicon_collection=single_lexicon_data,
                                           pos_mapper=None)
mwe_rule = MWERule(mwe_lexicon_lookup=mwe_lexicon_data,
                            pos_mapper=None)
rules = [single_word_rule, mwe_rule]

ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments([single_word_rule, mwe_rule])
ranker = ContextualRuleBasedRanker(*ranker_arguments)

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


output_doc = nlp(sentence)

print(f'{"Text":<15}{"lemma":<15}{"POS":<10}{"USAS Tags":<15}Is MWE')
for token in output_doc:
    is_mwe = False
    mwe_indexes = token._.pymusas_mwe_indexes
    all_mwe_indexes = [index for indexes in mwe_indexes for index in indexes]
    lowest_index, highest_index = min(all_mwe_indexes), max(all_mwe_indexes)
    if highest_index >= (lowest_index + 2):
        is_mwe = True 

    print(f'{token.text:<15}{token.lemma_:<15}{token.pos_:<10}{token._.pymusas_tags!r:<15}{is_mwe}')
```

</details>

## Setup a custom tagger with custom POS tagger and lemmatiser

It might be the case you already have a tokeniser, lemmatiser, and POS tagger pipeline and only need the PyMUSAS tagger. Below we show you how to set this up using a non-spaCy pipeline and in this specific case we are going to use [Stanza](https://stanfordnlp.github.io/stanza/) as the tokeniser, lemmatiser, and POS tagger; however you can use any NLP processing pipeline.

:::note

In this setup we are assuming that the POS tagger tagset and the tagset of your (custom) lexicons are the same, i.e. in the last example the tagset of the custom lexicon was [UPOS](https://universaldependencies.org/u/pos/) and the spaCy POS tagger's tagset was also UPOS.

If there is a mis-match between the POS tagger's tagset and the lexicons then the POS tag information in the lexicons will never be used as POS tags assigned to the tokens from the POS tagger will never match.

:::

First we need to install [Stanza](https://stanfordnlp.github.io/stanza/index.html#getting-started) and download an English pipeline;

``` bash
# install stanza
pip install stanza
# download the stanza pipeline for English
python -c "import stanza; stanza.Pipeline('en', processors='tokenize,pos,lemma', use_gpu=False)"
```

We create the PyMUSAS rule based tagger like we did in the previous [section](#how-to-create-a-custom-tagger);

``` python
from pathlib import Path

import spacy

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.mwe import MWERule

sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy.")

# File path to the custom semantic lexicon TSV file
single_lexicon_path = Path("custom_semantic_lexicon.tsv")

# Load the single lexicon data without POS information
single_lexicon_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=False)
# Load the single lexicon data with POS information
single_lexicon_pos_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=True)

# File path to the custom MWE lexicon TSV file
mwe_lexicon_path = Path("custom_mwe.tsv")

# Load the MWE lexicon data
mwe_lexicon_data = MWELexiconCollection.from_tsv(mwe_lexicon_path)

single_word_rule = SingleWordRule(lexicon_collection=single_lexicon_pos_data,
                                           lemma_lexicon_collection=single_lexicon_data,
                                           pos_mapper=None)
mwe_rule = MWERule(mwe_lexicon_lookup=mwe_lexicon_data,
                            pos_mapper=None)
rules = [single_word_rule, mwe_rule]

ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments([single_word_rule, mwe_rule])
ranker = ContextualRuleBasedRanker(*ranker_arguments)

# Create a blank non-trained spacy pipeline (multilingual code is xx to replace en)
# all language code can be found https://spacy.io/usage/models#languages
nlp = spacy.blank("en")

# Adding a blank PyMUSAS tagger
pymusas_tagger = nlp.add_pipe('pymusas_rule_based_tagger')

# Adding our custom resources to the tagger
pymusas_tagger.initialize(rules=rules,
                          ranker=ranker,
                          default_punctuation_tags=["PUNCT"],
                          default_number_tags=["NUM"])
```

You may have noticed that we still created a spaCy pipeline (`spacy.blank("en")`), this is so that we can use the PyMUSAS tagger within the spaCy pipeline framework, that blank pipeline does not load any external resources and will in our use case not perform any function other than USAS tagging.

We can run the Stanza pipeline and add the output (tokens, lemmas, and POS tags) to a spaCy Document as shown below;

:::note
You could run any NLP pipeline and add it's token, lemma, and POS tag output to a spaCy document.
:::

``` python
from spacy.tokens import Doc
import stanza

stanza_pipeline = stanza.Pipeline('en', processors='tokenize,pos,lemma', use_gpu=False)
stanza_doc = stanza_pipeline(sentence)

spacy_vocab = nlp.vocab
words = []
pos = []
lemmas = []
for stanza_word in stanza_doc.iter_words():
    words.append(stanza_word.text)
    lemmas.append(stanza_word.lemma)
    pos.append(stanza_word.upos)
spacy_doc = Doc(spacy_vocab, words=words, lemmas=lemmas, pos=pos)
```

Once we have this spaCy document we can run the PyMUSAS tagger over it like so;

``` python
output_doc = nlp(spacy_doc)

print(f'{"Text":<15}{"lemma":<15}{"POS":<10}{"USAS Tags":<15}Is MWE')
for token in output_doc:
    is_mwe = False
    mwe_indexes = token._.pymusas_mwe_indexes
    all_mwe_indexes = [index for indexes in mwe_indexes for index in indexes]
    lowest_index, highest_index = min(all_mwe_indexes), max(all_mwe_indexes)
    if highest_index >= (lowest_index + 2):
        is_mwe = True 

    print(f'{token.text:<15}{token.lemma_:<15}{token.pos_:<10}{token._.pymusas_tags!r:<15}{is_mwe}')
```

Which produces the following;

``` bash
Text           lemma          POS       USAS Tags      Is MWE
While          while          SCONJ     ['Z99']        False
drinking       drink          VERB      ['Z99']        False
my             my             PRON      ['Z99']        False
flat           flat           ADJ       ['F2/Z3']      True
white          white          NOUN      ['F2/Z3']      True
I              I              PRON      ['Z99']        False
was            be             AUX       ['Z99']        False
reading        read           VERB      ['Z99']        False
about          about          ADP       ['Z99']        False
the            the            DET       ['Z99']        False
new            new            ADJ       ['Z99']        False
battery        battery        NOUN      ['Z3/Y1/W3']   True
farm           farm           NOUN      ['Z3/Y1/W3']   True
that           that           PRON      ['Z99']        False
Amazon         Amazon         PROPN     ['Z3']         False
is             be             AUX       ['Z99']        False
creating       create         VERB      ['Z99']        False
which          which          PRON      ['Z99']        False
is             be             AUX       ['Z99']        False
owned          own            VERB      ['Z99']        False
by             by             ADP       ['Z99']        False
one            one            NUM       ['N1']         False
of             of             ADP       ['Z99']        False
the            the            DET       ['Z99']        False
broligarchy    broligarchy    NOUN      ['S5']         False
.              .              PUNCT     ['PUNCT']      False
```

The full Python code for this example can be found below:

<details>

<summary>Python Script</summary>

``` python
from pathlib import Path

import spacy
from spacy.tokens import Doc
import stanza

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.mwe import MWERule

sentence = ("While drinking my flat white I was reading about the "
            "new battery farm that Amazon is creating which is owned by "
            "one of the broligarchy.")

# File path to the custom semantic lexicon TSV file
single_lexicon_path = Path("custom_semantic_lexicon.tsv")

# Load the single lexicon data without POS information
single_lexicon_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=False)
# Load the single lexicon data with POS information
single_lexicon_pos_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=True)

# File path to the custom MWE lexicon TSV file
mwe_lexicon_path = Path("custom_mwe.tsv")

# Load the MWE lexicon data
mwe_lexicon_data = MWELexiconCollection.from_tsv(mwe_lexicon_path)

single_word_rule = SingleWordRule(lexicon_collection=single_lexicon_pos_data,
                                           lemma_lexicon_collection=single_lexicon_data,
                                           pos_mapper=None)
mwe_rule = MWERule(mwe_lexicon_lookup=mwe_lexicon_data,
                            pos_mapper=None)
rules = [single_word_rule, mwe_rule]

ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments([single_word_rule, mwe_rule])
ranker = ContextualRuleBasedRanker(*ranker_arguments)

# Create a blank non-trained spacy pipeline (multilingual code is xx to replace en)
# all language code can be found https://spacy.io/usage/models#languages
nlp = spacy.blank("en")

# Adding a blank PyMUSAS tagger
pymusas_tagger = nlp.add_pipe('pymusas_rule_based_tagger')

# Adding our custom resources to the tagger
pymusas_tagger.initialize(rules=rules,
                          ranker=ranker,
                          default_punctuation_tags=["PUNCT"],
                          default_number_tags=["NUM"])

stanza_pipeline = stanza.Pipeline('en', processors='tokenize,pos,lemma', use_gpu=False)
stanza_doc = stanza_pipeline(sentence)

spacy_vocab = nlp.vocab
words = []
pos = []
lemmas = []
for stanza_word in stanza_doc.iter_words():
    words.append(stanza_word.text)
    lemmas.append(stanza_word.lemma)
    pos.append(stanza_word.upos)
spacy_doc = Doc(spacy_vocab, words=words, lemmas=lemmas, pos=pos)

output_doc = nlp(spacy_doc)

print(f'{"Text":<15}{"lemma":<15}{"POS":<10}{"USAS Tags":<15}Is MWE')
for token in output_doc:
    is_mwe = False
    mwe_indexes = token._.pymusas_mwe_indexes
    all_mwe_indexes = [index for indexes in mwe_indexes for index in indexes]
    lowest_index, highest_index = min(all_mwe_indexes), max(all_mwe_indexes)
    if highest_index >= (lowest_index + 2):
        is_mwe = True 

    print(f'{token.text:<15}{token.lemma_:<15}{token.pos_:<10}{token._.pymusas_tags!r:<15}{is_mwe}')
```

</details>

:::info
In our example the POS tagset is UPOS for both the lexicons and the POS tagger, it might be the case that the lexicons and POS tagger use a different POS tagset. In this case even if they are the same this tagset between lexicons and POS tagger some adjustments to this code is required as you are likely to have run into this error;
``` bash
is not a valid Universal Dependencies tag. Non-UD tags should use the `tag` property.`
```
This can be overcome by assigning the POS tags to the `tags` attribute in the spaCy Doc, i.e.;
``` python
spacy_doc = Doc(spacy_vocab, words=words, lemmas=lemmas, tags=pos)
```
and when creating the `pymusas_tagger` using a config file stating that POS attribute to use is the `tag_` attribute like so;
``` python
# Adding a blank PyMUSAS tagger
pymusas_tagger = nlp.add_pipe('pymusas_rule_based_tagger', config={"pos_attribute": "tag_"})
```
:::

## Custom tagger with different POS tagset for lexicons and POS tagger

It might be the case that the POS tagset in the lexicon you have created is different to the tagset that the POS tagger you want to use, or in many cases might be the only POS tagger available for the language you are working in, this is the case for a few of the off-the-shelf PyMUSAS taggers we support, e.g. [Welsh](/usage/how_to/tag_text_with/rule_based_tagger#welsh) the POS tagger uses the [basic CorCenCC tagset](https://cytag.corcencc.org/tagset?lang=en) (reference paper; [LREC 2018](https://aclanthology.org/L18-1623.pdf)) whereas the lexicons use the USAS core tagset (reference papers; [NAACL 2015 paper](https://aclanthology.org/N15-1137.pdf) and [LREC 2018](https://aclanthology.org/L18-1158.pdf)) thus we have the Basic CorCenCC to USAS core and vice versa POS mappers, of which all supported POS mappers can be found [here](/api/pos_mapper).

The reason this POS tagset mis-alignment is important is when your lexicon contains two words with different meanings based on their POS tags;

``` tsv title="pos_example_custom_semantic_lexicon.tsv"
lemma	pos	semantic_tags
book	NOUN	Q4.1
book	VERB	A9
```

`book` can have many different meanings but with just the two in the lexicon we can see how important it is in disambiguating the following sentence *"He read a **book** on the train while I will **book** the table for the restaurant."*, the first `book` should be tagged with `Q4.1` while the second should be tagged `A9`. Without the correct POS tag information this would not be possible to disambiguate, if the tagger cannot match the token text and POS tag in the text with the lexicon entries then it will match just on the token text, if there is more than one entry (in the non-POS lexicon) with the same text it will use at random one of the entries.

As mentioned to resolve this issue of POS tagset mismatch between lexicon and POS tagger we have the POS mapper feature which maps from one POS tagset to another.

As an example we are going to use the following two lexicons as the Single and MWE lexicons, of which both use the [UPOS tagset](https://universaldependencies.org/u/pos/).

``` tsv title="pos_example_custom_semantic_lexicon.tsv"
lemma	pos	semantic_tags
book	NOUN	Q4.1
book	VERB	A9
```

``` tsv title="pos_example_custom_mwe.tsv"
mwe_template	semantic_tags
check_NOUN up_*	T1.1
check_VERB up_*	X2.4
```

and the following sentence:

``` text
He read a **book** on the train while I will **book** the table for the restaurant, a **check up** at the dentist, and ask Dave to **check** up on the children.
```

For the MWE `check up` could be the verb form *checking up on someone* or the noun form to *make an appointment*.

For this example we are going to use [Stanza](https://stanfordnlp.github.io/stanza/) as our tokeniser, lemmatiser, and POS tagger pipeline. However, instead of using the UPOS POS tags that it outputs we are going to use the [Penn Treebank tags](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) which are language specific POS tags. The reason for using the Penn Treebank tags is so that we have a mismatch between the lexicons and POS tagger, purely for example purposes.

First we are going to show what happens when you have a [mismatch in POS tagsets between lexicon and POS tagger](#the-pos-tagset-mismatch-issue) and then we are going to show [how to fix this mis-match](#the-pos-tagset-mismatch-fix).

### The POS tagset mismatch issue

Below is the code that when ran outputs the following, which can be seen below, as you can see almost all of the tokens are the unmatched tag, `Z99`, the only reason `book` has a semantic tag (`A9`) is due to matching on the token level, but as you can see for the first instance of `book`, `book` as a `NOUN`, it has been labelled incorrectly. All of this is because the tagger cannot match the token text and POS tags to their lexicon entiries because of the tagset mis-match.

``` txt title="mismatch issue output"
Text           lemma          POS       USAS Tags      Is MWE
He             he             PRP       ['Z99']        False
read           read           VBD       ['Z99']        False
a              a              DT        ['Z99']        False
book           book           NN        ['A9']         False
on             on             IN        ['Z99']        False
the            the            DT        ['Z99']        False
train          train          NN        ['Z99']        False
while          while          IN        ['Z99']        False
I              I              PRP       ['Z99']        False
will           will           MD        ['Z99']        False
book           book           VB        ['A9']         False
the            the            DT        ['Z99']        False
table          table          NN        ['Z99']        False
for            for            IN        ['Z99']        False
the            the            DT        ['Z99']        False
restaurant     restaurant     NN        ['Z99']        False
,              ,              ,         ['Z99']        False
a              a              DT        ['Z99']        False
check          check          NN        ['Z99']        False
up             up             RP        ['Z99']        False
at             at             IN        ['Z99']        False
the            the            DT        ['Z99']        False
dentist        dentist        NN        ['Z99']        False
,              ,              ,         ['Z99']        False
and            and            CC        ['Z99']        False
ask            ask            VB        ['Z99']        False
Dave           Dave           NNP       ['Z99']        False
to             to             TO        ['Z99']        False
check          check          VB        ['Z99']        False
up             up             RP        ['Z99']        False
on             on             IN        ['Z99']        False
the            the            DT        ['Z99']        False
children       child          NNS       ['Z99']        False
.              .              .         ['Z99']        False
```

<details>

<summary>Python Script</summary>

``` python
from pathlib import Path

import spacy
from spacy.tokens import Doc
import stanza

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.mwe import MWERule

sentence = ("He read a book on the train while I will book the table "
            "for the restaurant, a check up at the dentist, "
            "and ask Dave to check up on the children.")

# File path to the custom semantic lexicon TSV file
single_lexicon_path = Path("pos_example_custom_semantic_lexicon.tsv")

# Load the single lexicon data without POS information
single_lexicon_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=False)
# Load the single lexicon data with POS information
single_lexicon_pos_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=True)

# File path to the custom MWE lexicon TSV file
mwe_lexicon_path = Path("pos_example_custom_mwe.tsv")

# Load the MWE lexicon data
mwe_lexicon_data = MWELexiconCollection.from_tsv(mwe_lexicon_path)

single_word_rule = SingleWordRule(lexicon_collection=single_lexicon_pos_data,
                                           lemma_lexicon_collection=single_lexicon_data,
                                           pos_mapper=None)
mwe_rule = MWERule(mwe_lexicon_lookup=mwe_lexicon_data,
                            pos_mapper=None)
rules = [single_word_rule, mwe_rule]

ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments([single_word_rule, mwe_rule])
ranker = ContextualRuleBasedRanker(*ranker_arguments)

# Create a blank non-trained spacy pipeline (multilingual code is xx to replace en)
# all language code can be found https://spacy.io/usage/models#languages
nlp = spacy.blank("en")

# Adding a blank PyMUSAS tagger
pymusas_tagger = nlp.add_pipe('pymusas_rule_based_tagger', config={"pos_attribute": "tag_"})

# Adding our custom resources to the tagger
pymusas_tagger.initialize(rules=rules,
                          ranker=ranker,
                          default_punctuation_tags=["PUNCT"],
                          default_number_tags=["NUM"])

stanza_pipeline = stanza.Pipeline('en', processors='tokenize,pos,lemma', use_gpu=False)
stanza_doc = stanza_pipeline(sentence)

spacy_vocab = nlp.vocab
words = []
lemmas = []
x_pos = [] # language specific POS tags
for stanza_word in stanza_doc.iter_words():
    words.append(stanza_word.text)
    lemmas.append(stanza_word.lemma)
    x_pos.append(stanza_word.xpos)
spacy_doc = Doc(spacy_vocab, words=words, lemmas=lemmas, tags=x_pos)

output_doc = nlp(spacy_doc)

print(f'{"Text":<15}{"lemma":<15}{"POS":<10}{"USAS Tags":<15}Is MWE')
for token in output_doc:
    is_mwe = False
    mwe_indexes = token._.pymusas_mwe_indexes
    all_mwe_indexes = [index for indexes in mwe_indexes for index in indexes]
    lowest_index, highest_index = min(all_mwe_indexes), max(all_mwe_indexes)
    if highest_index >= (lowest_index + 2):
        is_mwe = True 

    print(f'{token.text:<15}{token.lemma_:<15}{token.tag_:<10}{token._.pymusas_tags!r:<15}{is_mwe}')

```

</details>

### The POS tagset mismatch fix

We are going to go step-by-step to fix this POS tagset mis-match issue introduced in the last sub-section.

First we need a POS mapper from the language specific tagset, [Penn Treebank tags](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html), to the lexicon tagset, [UPOS tags](https://universaldependencies.org/u/pos/) and vice versa, i.e.;

``` bash
POS tagger tagset -> Lexicon POS tagset
Lexicon POS tagset -> POS tagger tagset
```

For example purposes we are only going to create the most minimal POS mapper tagset to make this example work;

``` python
UPOS_TO_PENN = {
    "NOUN": ["NN"],
    "VERB": ["VB"]
}
PENN_TO_UPOS = {
    "NN": ["NOUN"],
    "VB": ["VERB"]
}
```

As you can see the POS mapper has to be of type; `dict[str, list[str]]` whereby each POS map can be matched to one or more POS tags in the desired tagset, i.e. `NOUN` could be mapped to `NN`, `NNS`, `NNP`, and `NNPS` in the [Penn Treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html), but for this example to keep things simple we only use `NN`.

:::info
We do have existing POS mappers for a few POS tagset which can be found [here](/api/pos_mapper)
:::

First lets fix the single word lexicon POS tagset mis-match, this can be achieved by assigning `PENN_TO_UPOS` POS mapper to the `single_word_rule` as the single word rule maps the token's POS tags (Penn Treebank) to the lexicon's POS tagset (UPOS);

``` python
single_word_rule = SingleWordRule(lexicon_collection=single_lexicon_pos_data,
                                  lemma_lexicon_collection=single_lexicon_data,
                                  pos_mapper=PENN_TO_UPOS)
```

Now we can fix the MWE lexicon POS tagset mis-match, this can be achieved by assigning `UPOS_TO_PENN` POS mapper to the `mwe_rule` as the MWE word rule maps the lexicon's POS tagset (UPOS) to the token's POS tags (Penn Treebank);

``` python
mwe_rule = MWERule(mwe_lexicon_lookup=mwe_lexicon_data,
                   pos_mapper=UPOS_TO_PENN)
```

As the POS tags for the `default_punctuation_tags` and `default_number_tags` are associated with the tagset of the tokens these also need to change to reflect the [Penn Treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html), like so;

``` python
pymusas_tagger.initialize(rules=rules,
                          ranker=ranker,
                          default_punctuation_tags=[".", ",", "!"],
                          default_number_tags=["CD"])
```

:::note
As we have no numbers in the test sentence no semantic tags are assigned to the default numbers semantic tag `N1`; however you can add a number into the test sentence to test if this works, which it should.

The [Penn Treebank tagset](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) does not have a punctuation tag, rather it uses the punctuation tokens themselevs hence why `default_punctuation_tags` is equal to a non-exhaustive list of potential punctuation tokens.
:::

Now that we have made these changes (full script can be found below the output) we can see the output is as expected with the different meanings of `book` and `check up` disambiguated according to our lexicon and punctuation labelled as well;

``` txt title="mismatch fixed output"
Text           lemma          POS       USAS Tags      Is MWE
He             he             PRP       ['Z99']        False
read           read           VBD       ['Z99']        False
a              a              DT        ['Z99']        False
book           book           NN        ['Q4.1']       False
on             on             IN        ['Z99']        False
the            the            DT        ['Z99']        False
train          train          NN        ['Z99']        False
while          while          IN        ['Z99']        False
I              I              PRP       ['Z99']        False
will           will           MD        ['Z99']        False
book           book           VB        ['A9']         False
the            the            DT        ['Z99']        False
table          table          NN        ['Z99']        False
for            for            IN        ['Z99']        False
the            the            DT        ['Z99']        False
restaurant     restaurant     NN        ['Z99']        False
,              ,              ,         ['PUNCT']      False
a              a              DT        ['Z99']        False
check          check          NN        ['T1.1']       True
up             up             RP        ['T1.1']       True
at             at             IN        ['Z99']        False
the            the            DT        ['Z99']        False
dentist        dentist        NN        ['Z99']        False
,              ,              ,         ['PUNCT']      False
and            and            CC        ['Z99']        False
ask            ask            VB        ['Z99']        False
Dave           Dave           NNP       ['Z99']        False
to             to             TO        ['Z99']        False
check          check          VB        ['X2.4']       True
up             up             RP        ['X2.4']       True
on             on             IN        ['Z99']        False
the            the            DT        ['Z99']        False
children       child          NNS       ['Z99']        False
.              .              .         ['PUNCT']      False
```

<details>

<summary>Python Script</summary>

``` python
from pathlib import Path

import spacy
from spacy.tokens import Doc
import stanza

from pymusas.lexicon_collection import LexiconCollection, MWELexiconCollection
from pymusas.taggers.rules.single_word import SingleWordRule
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rules.mwe import MWERule

UPOS_TO_PENN = {
    "NOUN": ["NN"],
    "VERB": ["VB"]
}
PENN_TO_UPOS = {
    "NN": ["NOUN"],
    "VB": ["VERB"]
}

sentence = ("He read a book on the train while I will book the table "
            "for the restaurant, a check up at the dentist, "
            "and ask Dave to check up on the children.")

# File path to the custom semantic lexicon TSV file
single_lexicon_path = Path("pos_example_custom_semantic_lexicon.tsv")

# Load the single lexicon data without POS information
single_lexicon_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=False)
# Load the single lexicon data with POS information
single_lexicon_pos_data = LexiconCollection.from_tsv(single_lexicon_path, include_pos=True)

# File path to the custom MWE lexicon TSV file
mwe_lexicon_path = Path("pos_example_custom_mwe.tsv")

# Load the MWE lexicon data
mwe_lexicon_data = MWELexiconCollection.from_tsv(mwe_lexicon_path)

single_word_rule = SingleWordRule(lexicon_collection=single_lexicon_pos_data,
                                           lemma_lexicon_collection=single_lexicon_data,
                                           pos_mapper=PENN_TO_UPOS)
mwe_rule = MWERule(mwe_lexicon_lookup=mwe_lexicon_data,
                            pos_mapper=UPOS_TO_PENN)
rules = [single_word_rule, mwe_rule]

ranker_arguments = ContextualRuleBasedRanker.get_construction_arguments([single_word_rule, mwe_rule])
ranker = ContextualRuleBasedRanker(*ranker_arguments)

# Create a blank non-trained spacy pipeline (multilingual code is xx to replace en)
# all language code can be found https://spacy.io/usage/models#languages
nlp = spacy.blank("en")

# Adding a blank PyMUSAS tagger
pymusas_tagger = nlp.add_pipe('pymusas_rule_based_tagger', config={"pos_attribute": "tag_"})

# Adding our custom resources to the tagger
pymusas_tagger.initialize(rules=rules,
                          ranker=ranker,
                          default_punctuation_tags=[".", ",", "!"],
                          default_number_tags=["CD"])

stanza_pipeline = stanza.Pipeline('en', processors='tokenize,pos,lemma', use_gpu=False)
stanza_doc = stanza_pipeline(sentence)

spacy_vocab = nlp.vocab
words = []
lemmas = []
x_pos = [] # language specific POS tags
for stanza_word in stanza_doc.iter_words():
    words.append(stanza_word.text)
    lemmas.append(stanza_word.lemma)
    x_pos.append(stanza_word.xpos)
spacy_doc = Doc(spacy_vocab, words=words, lemmas=lemmas, tags=x_pos)

output_doc = nlp(spacy_doc)

print(f'{"Text":<15}{"lemma":<15}{"POS":<10}{"USAS Tags":<15}Is MWE')
for token in output_doc:
    is_mwe = False
    mwe_indexes = token._.pymusas_mwe_indexes
    all_mwe_indexes = [index for indexes in mwe_indexes for index in indexes]
    lowest_index, highest_index = min(all_mwe_indexes), max(all_mwe_indexes)
    if highest_index >= (lowest_index + 2):
        is_mwe = True 

    print(f'{token.text:<15}{token.lemma_:<15}{token.tag_:<10}{token._.pymusas_tags!r:<15}{is_mwe}')

```

</details>