---
slug: /using
title: Using PyMUSAS
sidebar_position: 3
---

# Using PyMUSAS

PyMUSAS, currently, is most effective when used with one of the [spaCy models](https://spacy.io/models) and a Ucrel Semantic Analysis System (USAS) single word lexicon, of which the [Multilingual USAS repository](https://github.com/UCREL/Multilingual-USAS) contains USAS lexicons for 14 languages. 

In this guide we are going to go over the main features of the [USASRuleBasedTagger](/api/spacy_api/taggers/rule_based), from now on called the USAS tagger, which are:

1. Background information on the tagger
2. Adding the tagger to an existing spaCy pipeline
3. Applying it to some text
4. Saving the tagger. 

The example use case will be tagging the the first sentence of a Portuguese Wikipedia article on the [Peneda-Gerês national park](https://pt.wikipedia.org/wiki/Parque_Nacional_da_Peneda-Ger%C3%AAs) ([English link](https://en.wikipedia.org/wiki/Peneda-Ger%C3%AAs_National_Park) to the Wikipedia article).

## Background information on the tagger

The UCREL tagger is a rule based token level semantic tagger, it has been specifically developed for the [USAS tagset](https://ucrel.lancs.ac.uk/usas/), but has been created so that it can be used with any other semantic tagset. For more information on the UCREL tagger see the [USASRuleBasedTagger class docstring in the API pages](/api/spacy_api/taggers/rule_based#usasrulebasedtagger) which includes the list of rules the tagger applies. The rest of this guide can be read without any of this background knowledge.

## Adding the tagger to an existing spaCy pipeline

As the Wikipedia article is in Portuguese we will need to download the Portuguese spaCy pipeline, in this case we downloaded the small version, but any version can be used:

``` bash
python -m spacy download pt_core_news_sm
``` 

To add the [USAS tagger](/api/spacy_api/taggers/rule_based) to this existing pipeline:

``` python
import spacy
from pymusas.spacy_api.taggers import rule_based
# We exclude ['parser', 'ner'] as these components are typically not needed
# for the USAS tagger
nlp = spacy.load('pt_core_news_sm', exclude=['parser', 'ner'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')
_ = nlp.analyze_pipes(pretty=True)
```

The output from `nlp.analyze_pipes(pretty=True)` is shown below:

``` bash
============================= Pipeline Overview =============================

#   Component         Assigns             Requires      Scores           Retokenizes
-   ---------------   -----------------   -----------   --------------   -----------
0   tok2vec           doc.tensor                                         False      
                                                                                    
1   morphologizer     token.morph                       pos_acc          False      
                      token.pos                         morph_acc                   
                                                        morph_per_feat              
                                                                                    
2   attribute_ruler                                                      False      
                                                                                    
3   lemmatizer        token.lemma                       lemma_acc        False      
                                                                                    
4   usas_tagger       token._.usas_tags   token.lemma                    False      
                                          token.pos                                 

✔ No problems found.
```

As we can see the [USAS tagger](/api/spacy_api/taggers/rule_based) has been added and is called `usas_tagger`. We can see from this pipeline overview that the tagger requires both the `token.lemma`, which comes from the `lemmatizer`, and the `token.pos`, which comes from the `morphologizer`, attributes. In general the USAS tagger is more effective when it has access to Part Of Speech (POS) and the lemma of each token. However the USAS tagger can be used without either of these components, but it might make the tagger less accurate.

## Applying it to some text

Before using the added tagger we need to add the single word Portuguese USAS lexicon to the tagger, to do this we first need to download the lexicon form the [Multilingual USAS repository](https://github.com/UCREL/Multilingual-USAS) and then add the lexicon with and without the POS information (the code example below carries on from the previous).

:::note
When it downloads the lexicon it will be saved within the [PYMUSAS_CACHE_HOME](/api/config) directory for caching, which by default is set to `~/.cache/pymusas`, this can be changed either by setting `pymusas.config.PYMUSAS_CACHE_HOME` within the code you are writing or by setting the `PYMUSAS_HOME` environment variable.
:::

``` python
from pymusas.file_utils import download_url_file
from pymusas.lexicon_collection import LexiconCollection

portuguese_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/semantic_lexicon_pt.tsv'
portuguese_usas_lexicon_file = download_url_file(portuguese_usas_lexicon_url)
# Includes the POS information
portuguese_lexicon_lookup = LexiconCollection.from_tsv(portuguese_usas_lexicon_file)
# excludes the POS information
portuguese_lemma_lexicon_lookup = LexiconCollection.from_tsv(portuguese_usas_lexicon_file, 
                                                             include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = portuguese_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = portuguese_lemma_lexicon_lookup
```

In addition we need to add a POS mapper for the [USAS tagger](/api/spacy_api/taggers/rule_based), as currently all of the USAS lexicons use the USAS core tagset whereas the spaCy POS models uses the UPOS tagset, therefore we need to add a mapping dictionary, [UPOS_TO_USAS_CORE](/api/pos_mapper), which will convert the POS tags outputted from the POS model from the UPOS tagset to the USAS core tagset. This is done by adding the following:

``` python
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
```

We can now apply the tagger to the first sentence from the [Peneda-Gerês national park](https://pt.wikipedia.org/wiki/Parque_Nacional_da_Peneda-Ger%C3%AAs) Wikipedia article using the standard spaCy syntax:

``` python
text = "O Parque Nacional da Peneda-Gerês é uma área protegida de Portugal, com autonomia administrativa, financeira e capacidade jurídica, criada no ano de 1971, no meio ambiente da Peneda-Gerês."

output_doc = nlp(text)
```

We can then output the token, lemma, POS, and USAS tags for each token as follows:

``` python
print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.usas_tags}')
```

Output:

``` tsv
Text    Lemma   POS     USAS Tags
O       O       DET     ['Z5']
Parque  Parque  PROPN   ['M2']
Nacional        Nacional        PROPN   ['M7/S2mf']
da      da      ADP     ['Z5']
Peneda-Gerês    Peneda-Gerês    PROPN   ['Z99']
é       ser     AUX     ['A3+', 'Z5']
uma     umar    DET     ['Z99']
área    área    NOUN    ['H2/S5+c', 'X2.2', 'M7', 'A4.1', 'N3.6']
protegida       protegido       ADJ     ['O4.5/A2.1', 'S1.2.5+']
de      de      ADP     ['Z5']
Portugal        Portugal        PROPN   ['Z2', 'Z3c']
,       ,       PUNCT   ['PUNCT']
com     com     ADP     ['Z5']
autonomia       autonomia       NOUN    ['A1.7-', 'G1.1/S7.1+', 'X6+/S5-', 'S5-']
administrativa  administrativo  ADJ     ['S7.1+']
,       ,       PUNCT   ['PUNCT']
financeira      financeiro      ADJ     ['I1', 'I1/G1.1']
e       e       CCONJ   ['Z5']
capacidade      capacidade      NOUN    ['N3.2', 'N3.4', 'N5.1+', 'X9.1+', 'I3.1', 'X9.1']
jurídica        jurídico        ADJ     ['G2.1']
,       ,       PUNCT   ['PUNCT']
criada  criar   VERB    ['I3.1/B4/S2.1f', 'S2.1f%', 'S7.1-/S2mf']
no      o       ADP     ['Z5']
ano     ano     NOUN    ['T1.3', 'P1c']
de      de      ADP     ['Z5']
1971    1971    NUM     ['N1']
,       ,       PUNCT   ['PUNCT']
no      o       ADP     ['Z5']
meio    mear    ADJ     ['M6', 'N5', 'N4', 'T1.2', 'N2', 'X4.2', 'I1.1', 'M3/H3', 'N3.3', 'A4.1', 'A1.1.1', 'T1.3']
ambiente        ambientar       NOUN    ['W5', 'W3', 'E1', 'Y2', 'O4.1']
da      da      ADP     ['Z5']
Peneda-Gerês    Peneda-Gerês    PROPN   ['Z99']
.       .       PUNCT   ['PUNCT']
```

We can see above the USAS tags are outputted as a `List`, of which the first tag in the `List` is always the most likely tag.

## Saving the tagger

To save yourself from having to add the lexicon to the tagger, and then add the POS mapper you may wish to instead save this spaCy pipeline as it is currently to then load back up. To save the pipeline to disk you can use the standard spaCy method of `to_disk` as follows:

``` python
nlp.to_disk('PATH TO DIRECTORY')
```

And then to load the pipeline back up

``` python
import spacy

nlp = spacy.load('PATH TO DIRECTORY')
```