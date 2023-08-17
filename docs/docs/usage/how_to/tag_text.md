---
title: Tag Text
sidebar_position: 1
---

In this guide, we are going to show you how to tag text using the PyMUSAS [RuleBasedTagger](/api/spacy_api/taggers/rule_based#rulebasedtagger) so that you can extract token level [USAS semantic tags](https://ucrel.lancs.ac.uk/usas/) from the tagged text. The guide is broken down into different languages, for each guide we are going to: 

1. Download the relevant pre-configured PyMUSAS `RuleBasedTagger` spaCy component for the language.
2. Download and use a Natural Language Processing (NLP) pipeline that will tokenize, lemmatize, and Part Of Speech (POS) tag. In most cases, this will be a spaCy pipeline. **Note** that the PyMUSAS `RuleBasedTagger` only requires at minimum the data to be tokenized but having the lemma and POS tag will improve the accuracy of the tagging of the text.
3. Run the PyMUSAS `RuleBasedTagger`.
4. Extract token-level linguistic information from the tagged text, which will include USAS semantic tags.
5. For Chinese, Italian, Portuguese, Spanish, Welsh, and English taggers which support Multi Word Expression (MWE) identification and tagging we will show how to extract this information from the tagged text as well.


## Chinese
<details>
<summary>Expand</summary>

First download both the [Chinese PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/cmn_dual_upos2usas_contextual-0.3.3) and the [small Chinese spaCy model](https://spacy.io/models/zh):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/cmn_dual_upos2usas_contextual-0.3.3/cmn_dual_upos2usas_contextual-0.3.3-py3-none-any.whl
python -m spacy download zh_core_web_sm
```

Then create the tagger, in a Python script:

:::note
Currently, there is no lemmatization component in the spaCy pipeline for Chinese.
:::

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('zh_core_web_sm', exclude=['parser', 'ner'])
# Load the Chinese PyMUSAS rule-based tagger in a separate spaCy pipeline
chinese_tagger_pipeline = spacy.load('cmn_dual_upos2usas_contextual')
# Adds the Chinese PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=chinese_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Chinese Wikipedia page on the topic of [`The Nile River`](https://zh.wikipedia.org/wiki/%E5%B0%BC%E7%BD%97%E6%B2%B3):

``` python
text = "尼罗河 是一条流經非洲東部與北部的河流，與中非地區的剛果河、非洲南部的赞比西河以及西非地区的尼日尔河並列非洲最大的四個河流系統。"

output_doc = nlp(text)

print(f'Text\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.pos_}\t{token._.pymusas_tags}')
```

<details>
<summary>Output:</summary>

``` tsv
Text    POS     USAS Tags
尼罗河     PROPN   ['Z2']
是       VERB    ['A3', 'Z5']
一       NUM     ['N1']
条       NUM     ['G2.1/P1', 'S7.4-', 'A1.7+', 'S8-']
流經      ADJ     ['Z99']
非洲      PROPN   ['Z2']
東部      NOUN    ['Z99']
與北部     PROPN   ['Z99']
的       PART    ['Z5']
河流      NOUN    ['W3/M4', 'N5+']
，       PUNCT   ['PUNCT']
與       VERB    ['Z99']
中非      PROPN   ['Z99']
地區      NOUN    ['Z99']
的       PART    ['Z5']
剛果河     PROPN   ['Z99']
、       PUNCT   ['PUNCT']
非洲      PROPN   ['Z2']
南部      NOUN    ['M6']
的       PART    ['Z5']
赞比西河    NOUN    ['Z99']
以及      CCONJ   ['N5++', 'N5.2+', 'A13.3', 'Z5']
西非      PROPN   ['Z99']
地区      NOUN    ['A1.1.1', 'B3/X1', 'G1.1c', 'W3', 'F4/M7', 'K2', 'M7', 'A4.1', 'N3.6', 'B1', 'T1.1', 'O4.4', 'N5.1-', 'S5+c', 'B3', 'Y1', 'C1/H1@']
的       PART    ['Z5']
尼日尔河    NOUN    ['Z99']
並列      VERB    ['Z99']
非洲      PROPN   ['Z2']
最       ADV     ['A11.1+', 'N5+++', 'N3.2+++', 'A11.1+++', 'N5.1+', 'O2/M4', 'O3']
大       VERB    ['A11.1+', 'N5+++', 'N3.2+++', 'A11.1+++', 'N5.1+', 'O2/M4', 'O3']
的       PART    ['Z5']
四       NUM     ['N1']
個       NUM     ['N1']
河流      NOUN    ['W3/M4', 'N5+']
系統      NOUN    ['Z99']
。       PUNCT   ['PUNCT']
```

</details>

For Chinese the tagger also identifies and tags Multi-Word Expressions (MWE), to find these MWE's you can run the following:

``` python
print(f'Text\tPOS\tMWE start and end index\tUSAS Tags')
for token in output_doc:
    start, end = token._.pymusas_mwe_indexes[0]
    if (end - start) > 1:
        print(f'{token.text}\t{token.pos_}\t{(start, end)}\t{token._.pymusas_tags}')
```

Which will output the following:

``` tsv
Text    POS    MWE start and end index    USAS Tags
最       ADV    (28, 30)                   ['A11.1+', 'N5+++', 'N3.2+++', 'A11.1+++', 'N5.1+', 'O2/M4', 'O3']
大       VERB   (28, 30)                   ['A11.1+', 'N5+++', 'N3.2+++', 'A11.1+++', 'N5.1+', 'O2/M4', 'O3']
```


</details>

## Dutch

<details>
<summary>Expand</summary>

First download both the [Dutch PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/nl_single_upos2usas_contextual-0.3.3) and the [small Dutch spaCy model](https://spacy.io/models/nl):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/nl_single_upos2usas_contextual-0.3.3/nl_single_upos2usas_contextual-0.3.3-py3-none-any.whl
python -m spacy download nl_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('nl_core_news_sm', exclude=['parser', 'ner', 'tagger'])
# Load the Dutch PyMUSAS rule-based tagger in a separate spaCy pipeline
dutch_tagger_pipeline = spacy.load('nl_single_upos2usas_contextual')
# Adds the Dutch PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=dutch_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Dutch Wikipedia page on the topic of [`The Nile River`](https://nl.wikipedia.org/wiki/Nijl):

``` python
text = "De Nijl is met een lengte van 5499 tot 6695 km de langste of de op een na langste rivier van de wereld."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
```

<details>

<summary>Output:</summary>

``` tsv
Text    Lemma   POS     USAS Tags
De      de      DET     ['Z5']
Nijl    nijl    PROPN   ['Z99']
is      is      AUX     ['Z99']
met     met     ADP     ['Z5']
een     een     DET     ['Z5']
lengte  lengte  NOUN    ['N3.7', 'T1.3', 'M4']
van     van     ADP     ['Z5']
5499    5499    NUM     ['N1']
tot     tot     ADP     ['Z99']
6695    6695    NUM     ['N1']
km      km      SYM     ['Z99']
de      de      DET     ['Z5']
langste lang    ADJ     ['N3.7+', 'T1.3+', 'N3.3+', 'N3.2+', 'X7+']
of      of      CCONJ   ['Z5']
de      de      DET     ['Z5']
op      op      ADP     ['A5.1+', 'G2.2+', 'A1.1.1', 'M6', 'Z5']
een     e       NUM     ['N1', 'T3', 'T1.2', 'Z8']
na      na      ADP     ['N4', 'Z5']
langste lang    ADJ     ['N3.7+', 'T1.3+', 'N3.3+', 'N3.2+', 'X7+']
rivier  rivier  NOUN    ['W3/M4', 'N5+']
van     van     ADP     ['Z5']
de      de      DET     ['Z5']
wereld  wereld  NOUN    ['W1', 'S5+c', 'A4.1', 'N5+']
.       .       PUNCT   ['PUNCT']
```
</details>

</details>

## French

<details>
<summary>Expand</summary>

First download both the [French PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/fr_single_upos2usas_contextual-0.3.3) and the [small French spaCy model](https://spacy.io/models/fr):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/fr_single_upos2usas_contextual-0.3.3/fr_single_upos2usas_contextual-0.3.3-py3-none-any.whl
python -m spacy download fr_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('fr_core_news_sm', exclude=['parser', 'ner'])
# Load the French PyMUSAS rule-based tagger in a separate spaCy pipeline
french_tagger_pipeline = spacy.load('fr_single_upos2usas_contextual')
# Adds the French PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=french_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the French Wikipedia page on the topic of [`The Nile River`](https://fr.wikipedia.org/wiki/Nil):

``` python
text = "Le Nil est un fleuve d'Afrique. Avec une longueur d'environ 6 700 km, c'est avec le fleuve Amazone, le plus long fleuve du monde."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
```

<details>

<summary>Output:</summary>

``` tsv
Text      Lemma     POS       USAS Tags
Le        le        DET       ['Z5']
Nil       Nil       PROPN     ['Z99']
est       être      AUX       ['M6']
un        un        DET       ['Z5']
fleuve    fleuve    NOUN      ['W3/M4', 'N5+']
d'        de        ADP       ['Z5']
Afrique   Afrique   PROPN     ['Z99']
.         .         PUNCT     ['PUNCT']
Avec      avec      ADP       ['Z5']
une       un        DET       ['Z5']
longueur  longueur  NOUN      ['N3.7', 'T1.3', 'M4']
d'        de        ADP       ['Z5']
environ   environ   ADV       ['Z5']
6         6         DET       ['Z99']
700       700       NUM       ['N1']
km        kilomètre NOUN      ['N3.3', 'N3.7']
,         ,         PUNCT     ['PUNCT']
c'        ce        PRON      ['Z8']
est       être      VERB      ['M6']
avec      avec      ADP       ['Z5']
le        le        DET       ['Z5']
fleuve    fleuve    NOUN      ['W3/M4', 'N5+']
Amazone   amazone   NOUN      ['Z99']
,         ,         PUNCT     ['PUNCT']
le        le        DET       ['Z5']
plus      plus      ADV       ['Z5']
long      long      ADJ       ['Z99']
fleuve    fleuve    NOUN      ['W3/M4', 'N5+']
du        de        ADP       ['Z5']
monde     monde     NOUN      ['Z99']
.         .         PUNCT     ['PUNCT']
```

</details>

</details>

## Italian

<details>
<summary>Expand</summary>

First download both the [Italian PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/it_dual_upos2usas_contextual-0.3.3) and the [small Italian spaCy model](https://spacy.io/models/it):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/it_dual_upos2usas_contextual-0.3.3/it_dual_upos2usas_contextual-0.3.3-py3-none-any.whl
python -m spacy download it_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('it_core_news_sm', exclude=['parser', 'ner', 'tagger'])
# Load the Italian PyMUSAS rule-based tagger in a separate spaCy pipeline
italian_tagger_pipeline = spacy.load('it_dual_upos2usas_contextual')
# Adds the Italian PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=italian_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Italian Wikipedia page on the topic of [`The Nile River`](https://it.wikipedia.org/wiki/Nilo):

``` python
text = "Il Nilo è un fiume africano lungo 6.852 km che attraversa otto stati dell'Africa. Tradizionalmente considerato il fiume più lungo del mondo, contende il primato della lunghezza al Rio delle Amazzoni."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
```

<details>

<summary>Output:</summary>

``` tsv
Text              Lemma             POS     USAS Tags
Il                il                DET     ['Z5']
Nilo              nilo              PROPN   ['Z99']
è                 essere            AUX     ['A5.1', 'S7.1++', 'X3.2', 'Q2.2', 'A8', 'N3.1%']
un                uno               DET     ['Z5']
fiume             fiume             NOUN    ['W3']
africano          africano          ADJ     ['Z2']
lungo             lungo             ADP     ['Z5']
6.852             6.852             NUM     ['N1']
km                km                NOUN    ['N3.3']
che               che               PRON    ['Z8']
attraversa        attraversare      VERB    ['M1', 'M6', 'S8-', 'A1.8+', 'A6.3+', 'F4/L2', 'O4.4', 'Q1.2', 'E3-', 'S1.1.1', 'S9@']
otto              otto              NUM     ['N1']
stati             stato             NOUN    ['G2.1/H1', 'B2', 'A3']
dell'             dell'             ADP     ['Z99']
Africa            Africa            PROPN   ['Z2']
.                 .                 PUNCT   ['PUNCT']
Tradizionalmente  tradizionalmente  ADV     ['Z99']
considerato       considerare       VERB    ['A5.1', 'N2', 'A11.1+', 'Q2.2', 'S1.1.1', 'Q1.3', 'S9%', 'X2.1', 'X2.4', 'X6']
il                il                DET     ['Z5']
fiume             fiume             NOUN    ['W3']
più               molto             ADV     ['N3.3+', 'A13.3']
lungo             lungo             ADJ     ['N3.3+', 'A13.3']
del               del               ADP     ['Z5']
mondo             mondo             NOUN    ['W1']
,                 ,                 PUNCT   ['PUNCT']
contende          contendere        VERB    ['S7.3']
il                il                DET     ['Z5']
primato           primato           NOUN    ['A5.1+++', 'A11.1+']
della             della             ADP     ['Z99']
lunghezza         lunghezza         NOUN    ['N3.7', 'T1.3', 'M4']
al                al                ADP     ['Z5']
Rio               Rio               PROPN   ['Z2']
delle             della             ADP     ['Z5']
Amazzoni          amazzoni          PROPN   ['Z99']
.                 .                 PUNCT   ['PUNCT']
```

</details>

For Italian the tagger also identifies and tags Multi-Word Expressions (MWE), to find these MWE's you can run the following:

``` python
print(f'Text\tPOS\tMWE start and end index\tUSAS Tags')

for token in output_doc:
    start, end = token._.pymusas_mwe_indexes[0]
    if (end - start) > 1:
        print(f'{token.text}\t{token.pos_}\t{(start, end)}\t{token._.pymusas_tags}')
```

Which will output the following:

``` tsv
Text    POS     MWE start and end index    USAS Tags
più     ADV     (20, 22)                   ['N3.3+', 'A13.3']
lungo   ADJ     (20, 22)                   ['N3.3+', 'A13.3']
```

</details>

## Portuguese

<details>
<summary>Expand</summary>

First download both the [Portuguese PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/pt_dual_upos2usas_contextual-0.3.3) and the [small Portuguese spaCy model](https://spacy.io/models/pt):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/pt_dual_upos2usas_contextual-0.3.3/pt_dual_upos2usas_contextual-0.3.3-py3-none-any.whl
python -m spacy download pt_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('pt_core_news_sm', exclude=['parser', 'ner'])
# Load the Portuguese PyMUSAS rule-based tagger in a separate spaCy pipeline
portuguese_tagger_pipeline = spacy.load('pt_dual_upos2usas_contextual')
# Adds the Portuguese PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=portuguese_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Portuguese Wikipedia page on the topic of [`The Nile River`](https://pt.wikipedia.org/wiki/Rio_Nilo):

``` python
text = "Todos estes estudos levam a que o comprimento de ambos os rios permaneça em aberto, continuando por isso o debate e como tal, continuando-se a considerar o Nilo como o rio mais longo."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
```

<details>

<summary>Output:</summary>

``` tsv
Text            Lemma           POS     USAS Tags
Todos           Todos           DET     ['Z8/N5.1+c']
estes           este            DET     ['Z5', 'Z8']
estudos         estudo          NOUN    ['P1', 'X2.4', 'H2', 'Q1.2', 'C1']
levam           levar           VERB    ['A9+', 'T1.3', 'C1', 'A1.1.1', 'M2', 'S7.1-', 'A2.1+', 'X2.4', 'S6+', 'S7.4+', 'N3', 'A2.1+', 'P1', 'M1', 'X2.5+', 'F1@', 'F2@', 'Q1.2@', 'B3@']
a               o               SCONJ   ['M6', 'Z5']
que             que             SCONJ   ['A13.3', 'A6.1+', 'Z5', 'Z8']
o               o               DET     ['Z5']
comprimento     comprimento     NOUN    ['N3.7', 'T1.3', 'M4']
de              de              ADP     ['Z5']
ambos           ambos           DET     ['N5']
os              o               DET     ['Z5']
rios            rio             NOUN    ['W3/M4', 'N5+']
permaneça       permanecer      VERB    ['T2++', 'M8', 'N5.2+']
em              em              SCONJ   ['A5.1+', 'G2.2+', 'A1.1.1', 'M6', 'O4.2+', 'Z5']
aberto          aberto          VERB    ['A10+', 'T2+']
,               ,               PUNCT   ['PUNCT']
continuando     continuar       VERB    ['Z99']
por             por             ADP     ['N4', 'Z5', 'T1.2']
isso            isso            PRON    ['N4', 'Z5', 'T1.2']
o               o               DET     ['Z5']
debate          debater         NOUN    ['Q2.1', 'Q2.1/A6.1-', 'Q2.1/E3-', 'Q2.2']
e               e               CCONJ   ['Z5']
como            comer           ADP     ['Z5']
tal             tal             PRON    ['Z5']
,               ,               PUNCT   ['PUNCT']
continuando-se  continuando-se  VERB    ['Z99']
a               o               SCONJ   ['M6', 'Z5']
considerar      considerar      VERB    ['Z99']
o               o               DET     ['Z5']
Nilo            Nilo            PROPN   ['Z2']
como            comer           ADP     ['Z5']
o               o               DET     ['Z5']
rio             rir             NOUN    ['W3/M4', 'N5+']
mais            mais            ADV     ['T1.3++', 'N3.7++', 'N3.3++', 'N3.2++']
longo           longo           ADJ     ['T1.3++', 'N3.7++', 'N3.3++', 'N3.2++']
.               .               PUNCT   ['PUNCT']
```
</details>

For Portuguese the tagger also identifies and tags Multi-Word Expressions (MWE), to find these MWE's you can run the following:

``` python
print(f'Text\tPOS\tMWE start and end index\tUSAS Tags')

for token in output_doc:
    start, end = token._.pymusas_mwe_indexes[0]
    if (end - start) > 1:
        print(f'{token.text}\t{token.pos_}\t{(start, end)}\t{token._.pymusas_tags}')
```

Which will output the following:

``` tsv
Text    POS     MWE start and end index    USAS Tags
por     ADP     (17, 19)                   ['N4', 'Z5', 'T1.2']
isso    PRON    (17, 19)                   ['N4', 'Z5', 'T1.2']
mais    ADV     (33, 35)                   ['T1.3++', 'N3.7++', 'N3.3++', 'N3.2++']
longo   ADJ     (33, 35)                   ['T1.3++', 'N3.7++', 'N3.3++', 'N3.2++']
```


</details>

## Spanish

<details>
<summary>Expand</summary>

First download both the [Spanish PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/es_dual_upos2usas_contextual-0.3.3) and the [small Spanish spaCy model](https://spacy.io/models/es):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/es_dual_upos2usas_contextual-0.3.3/es_dual_upos2usas_contextual-0.3.3-py3-none-any.whl
python -m spacy download es_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('es_core_news_sm', exclude=['parser', 'ner'])
# Load the Spanish PyMUSAS rule-based tagger in a separate spaCy pipeline
spanish_tagger_pipeline = spacy.load('es_dual_upos2usas_contextual')
# Adds the Spanish PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=spanish_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Spanish Wikipedia page on the topic of [`Países Bajos`](https://es.wikipedia.org/wiki/Pa%C3%ADses_Bajos):

``` python
text = "Los Países Bajos son un país soberano ubicado al noreste de la Europa continental y el país constituyente más grande de los cuatro que, junto con las islas de Aruba, Curazao y San Martín, forman el Reino de los Países Bajos."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
```

<details>

<summary>Output:</summary>

``` tsv
Text            Lemma           POS     USAS Tags
Los             el              DET     ['Z5']
Países          Países          PROPN   ['Z2']
Bajos           Bajos           PROPN   ['Z2']
son             ser             AUX     ['A3+', 'L1', 'Z5']
un              uno             DET     ['Z5', 'N1']
país            país            NOUN    ['G1.1c', 'W3', 'M7']
soberano        soberano        ADJ     ['Z99']
ubicado         ubicado         ADJ     ['Z99']
al              al              ADP     ['Z5']
noreste         noreste         NOUN    ['Z99']
de              de              ADP     ['Z5']
la              el              DET     ['Z5']
Europa          Europa          PROPN   ['Z2', 'S7', 'M7']
continental     continental     ADJ     ['Z99']
y               y               CCONJ   ['Z5', 'A1.8+']
el              el              DET     ['Z5']
país            país            NOUN    ['G1.1c', 'W3', 'M7']
constituyente   constituyente   ADJ     ['Z99']
más             más             ADV     ['A13.3', 'N6++', 'Z5']
grande          grande          ADJ     ['N3.1+/A6.1+/A13.2+', 'A5']
de              de              ADP     ['Z5']
los             el              DET     ['Z5']
cuatro          cuatro          NUM     ['N1']
que             que             PRON    ['Z5', 'Z8']
,               ,               PUNCT   ['PUNCT']
junto           junto           ADJ     ['A2.2', 'S5+', 'A1.8+']
con             con             ADP     ['Z5', 'A4.1']
las             el              DET     ['Z5']
islas           isla            NOUN    ['W3M7']
de              de              ADP     ['Z5']
Aruba           Aruba           PROPN   ['Z99']
,               ,               PUNCT   ['PUNCT']
Curazao         Curazao         PROPN   ['Z99']
y               y               CCONJ   ['Z5', 'A1.8+']
San             San             PROPN   ['S9', 'S2', 'A4.1']
Martín          Martín          PROPN   ['Z1', 'S2']
,               ,               PUNCT   ['PUNCT']
forman          formar          VERB    ['T2+', 'A2.1+', 'A1.8+', 'A3+', 'A1.1.1']
el              el              DET     ['Z5']
Reino           Reino           PROPN   ['M7']
de              de              ADP     ['Z5']
los             el              DET     ['Z5']
Países          Países          PROPN   ['Z2']
Bajos           Bajos           PROPN   ['Z2']
.               .               PUNCT   ['PUNCT']
```
</details>



For Spanish the tagger also identifies and tags Multi-Word Expressions (MWE), to find these MWE's you can run the following:

``` python
print(f'Text\tPOS\tMWE start and end index\tUSAS Tags')

for token in output_doc:
    start, end = token._.pymusas_mwe_indexes[0]
    if (end - start) > 1:
        print(f'{token.text}\t{token.pos_}\t{(start, end)}\t{token._.pymusas_tags}')
```

Which will output the following:

``` tsv
Text    POS     MWE start and end index    USAS Tags
Países  PROPN   (1, 3)                     ['Z2']
Bajos   PROPN   (1, 3)                     ['Z2']
Países  PROPN   (42, 44)                   ['Z2']
Bajos   PROPN   (42, 44)                   ['Z2']
```

</details>

## Finnish

<details>
<summary>Expand</summary>

First download both the [Finnish PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/fi_single_upos2usas_contextual-0.3.3) and the [small Finnish spaCy model](https://spacy.io/models/fi):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/fi_single_upos2usas_contextual-0.3.3/fi_single_upos2usas_contextual-0.3.3-py3-none-any.whl
python -m spacy download fi_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load("fi_core_news_sm", exclude=['tagger', 'parser', 'attribute_ruler', 'ner'])
# Load the Finnish PyMUSAS rule-based tagger in a separate spaCy pipeline
finnish_tagger_pipeline = spacy.load('fi_single_upos2usas_contextual')
# Adds the Finnish PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=finnish_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Finnish Wikipedia page on the topic of [`Bank` as a financial institution](https://fi.wikipedia.org/wiki/Pankki):

``` python
text = "Pankki on instituutio, joka tarjoaa finanssipalveluita, erityisesti maksuliikenteen hoitoa ja luotonantoa."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
print(f'{"Text":<20}{"Lemma":<20}{"POS":<8}USAS Tags')
for token in output_doc:
    print(f'{token.text:<20}{token.lemma_:<20}{token.pos_:<8}{token._.pymusas_tags}')
```

<details>

<summary>Output:</summary>

``` tsv
Text                Lemma               POS     USAS Tags
Pankki              pankki              NOUN    ['I1/H1', 'K5.2/I1.1']
on                  olla                AUX     ['A3+', 'A1.1.1', 'M6', 'Z5']
instituutio         instituutio         NOUN    ['S5+']
,                   ,                   PUNCT   ['PUNCT']
joka                joka                PRON    ['Z8', 'N5.1+']
tarjoaa             tarjota             VERB    ['A9-', 'Q2.2', 'F1', 'S6+', 'A7+', 'I2.2']
finanssipalveluita  finanssipalvelus    NOUN    ['Z99']
,                   ,                   PUNCT   ['PUNCT']
erityisesti         erityisesti         ADV     ['A14']
maksuliikenteen     maksuliikentete     NOUN    ['Z99']
hoitoa              hoito               NOUN    ['B3', 'S4']
ja                  ja                  CCONJ   ['Z5']
luotonantoa         luotonanto          NOUN    ['Z99']
.                   .                   PUNCT   ['PUNCT']
```

</details>

</details>

## Welsh
<details>
<summary>Expand</summary>

In this example, we will not be using spaCy for tokenization, lemmatization, and POS tagging, as we will be using the [CyTag toolkit](https://github.com/UCREL/CyTag) that has been wrapped in a docker container. Therefore, first, you will need to [install docker](https://docs.docker.com/get-docker/).

We assume that you would like to tag the following text, of which this text is stored in the file named `welsh_text_example.txt`. The example text is taken from the Welsh Wikipedia page on the topic of [`Bank` as a financial institution.](https://cy.wikipedia.org/wiki/Banc) With an additional random sentence at the end to demonstrate the Multi-Word Expression (MWE) identification and tagging attributes of the tagger.

``` txt title="welsh_text_example.txt"
Sefydliad cyllidol yw bancwr neu fanc sy'n actio fel asiant talu ar gyfer cwsmeriaid, ac yn rhoi benthyg ac yn benthyg arian. Yn rhai gwledydd, megis yr Almaen a Siapan, mae banciau'n brif berchenogion corfforaethau diwydiannol, tra mewn gwledydd eraill, megis yr Unol Daleithiau, mae banciau'n cael eu gwahardd rhag bod yn berchen ar gwmniau sydd ddim yn rhai cyllidol. Adran Iechyd Cymru.
```

First, we will need to run the CyTag toolkit, more specifically we will run version 1 of the toolkit as we have a mapping from the POS tags produced in version 1 (the [basic CorCencC POS tagset](https://cytag.corcencc.org/tagset?lang=en)) to the POS tags that the USAS lexicon uses (the USAS core POS tagset) within the pre-configured Welsh PyMUSAS `RuleBasedTagger` tagger.

``` bash
cat welsh_text_example.txt | docker run -i --rm ghcr.io/ucrel/cytag:1.0.4 > welsh_text_example.tsv
```

We now have a `tsv` version of the file that has been tokenized, lemmatized, and POS tagged. The `welsh_text_example.tsv` file should contain the following (I have added column headers here to explain what each column represents, these headers should not be in your file, also note that the "Mutation" column is optional):

<details>
<summary>welsh_text_example.tsv:</summary>

``` tsv title="welsh_text_example.tsv"
Line Number	Token	Sentence Index, Token Index	Lemma	Basic POS	Enriched POS	Mutation
1	Sefydliad	1,1	sefydliad	E	Egu	
2	cyllidol	1,2	cyllidol	Ans	Anscadu	
3	yw	1,3	bod	B	Bpres3u	
4	bancwr	1,4	bancwr	E	Egu	
5	neu	1,5	neu	Cys	Cyscyd	
6	fanc	1,6	banc	E	Egu	+sm
7	sy	1,7	bod	B	Bpres3perth	
8	'n	1,8	yn	U	Uberf	
9	actio	1,9	actio	B	Be	
10	fel	1,10	fel	Cys	Cyscyd	
11	asiant	1,11	asiant | asio	E | B	Egu | Bpres3ll	
12	talu	1,12	talu	B	Be	
13	ar	1,13	ar	Ar	Arsym	
14	gyfer	1,14	cyfer	E	Egu	+sm
15	cwsmeriaid	1,15	cwsmer	E	Egll	
16	,	1,16	,	Atd	Atdcan	
17	ac	1,17	a	Cys	Cyscyd	
18	yn	1,18	yn	U	Uberf	
19	rhoi	1,19	rhoi	B	Be	
20	benthyg	1,20	benthyg	E	Egu	
21	ac	1,21	a	Cys	Cyscyd	
22	yn	1,22	yn	U	Uberf	
23	benthyg	1,23	benthyg	B	Be	
24	arian	1,24	arian	E	Egu	
25	.	1,25	.	Atd	Atdt	
26	Yn	2,1	yn	Ar	Arsym	
27	rhai	2,2	rhai	unk	unk	
28	gwledydd	2,3	gwlad	E	Ebll	
29	,	2,4	,	Atd	Atdcan	
30	megis	2,5	megis	Cys	Cyscyd	
31	yr	2,6	y	YFB	YFB	
32	Almaen	2,7	Almaen	E	Epb	
33	a	2,8	a	Cys	Cyscyd	
34	Siapan	2,9	Siapan	E	Epb	
35	,	2,10	,	Atd	Atdcan	
36	mae	2,11	bod	B	Bpres3u	
37	banciau	2,12	banc	E	Egll	
38	'n	2,13	yn	U	Utra	
39	brif	2,14	brif	unk	unk	
40	berchenogion	2,15	berchenogion	unk	unk	
41	corfforaethau	2,16	corfforaeth	E	Ebll	
42	diwydiannol	2,17	diwydiannol	Ans	Anscadu	
43	,	2,18	,	Atd	Atdcan	
44	tra	2,19	tra	Cys	Cyscyd	
45	mewn	2,20	mewn	Ar	Arsym	
46	gwledydd	2,21	gwlad	E	Ebll	
47	eraill	2,22	arall	Ans	Anscadu	
48	,	2,23	,	Atd	Atdcan	
49	megis	2,24	megis	Cys	Cyscyd	
50	yr	2,25	y	YFB	YFB	
51	Unol	2,26	unol	Ans	Anscadu	
52	Daleithiau	2,27	Daleithiau	E	Ep	
53	,	2,28	,	Atd	Atdcan	
54	mae	2,29	bod	B	Bpres3u	
55	banciau	2,30	banc	E	Egll	
56	'n	2,31	yn	U	Uberf	
57	cael	2,32	cael	B	Be	
58	eu	2,33	eu	Rha	Rhadib3ll	
59	gwahardd	2,34	gwahardd	B	Be	
60	rhag	2,35	rhag	Ar	Arsym	
61	bod	2,36	bod	B	Be	
62	yn	2,37	yn	U	Utra	
63	berchen	2,38	perchen	E	Egu	+sm
64	ar	2,39	ar	Ar	Arsym	
65	gwmniau	2,40	gwmniau	unk	unk	
66	sydd	2,41	bod	B	Bpres3perth	
67	ddim	2,42	dim	E	Egu	+sm
68	yn	2,43	yn	U	Utra	
69	rhai	2,44	rhai	unk	unk	
70	cyllidol	2,45	cyllidol	Ans	Anscadu	
71	.	2,46	.	Atd	Atdt	
72	Adran	3,1	adran	E	Ebu	
73	Iechyd	3,2	iechyd	E	Egu	
74	Cymru	3,3	Cymru	E	Epb	
75	.	3,4	.	Atd	Atdt
```

</details>

Now we have the token, lemma, and POS tag information we can run the [Welsh PyMUSAS `RuleBasedTagger`](https://github.com/UCREL/pymusas-models/releases/tag/cy_dual_basiccorcencc2usas_contextual-0.3.3), so first we will download it:

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/cy_dual_basiccorcencc2usas_contextual-0.3.3/cy_dual_basiccorcencc2usas_contextual-0.3.3-py3-none-any.whl
```

Now we can run the tagger over the `tsv` data using the following Python script:

``` python
from pathlib import Path
from typing import List

import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab

# Load the Welsh PyMUSAS rule-based tagger
nlp = spacy.load("cy_dual_basiccorcencc2usas_contextual")

tokens: List[str] = []
spaces: List[bool] = []
basic_pos_tags: List[str] = []
lemmas: List[str] = []

welsh_tagged_file = Path(Path.cwd(), 'welsh_text_example.tsv').resolve()

print('Text\tLemma\tPOS\tUSAS Tags')
with welsh_tagged_file.open('r', encoding='utf-8') as welsh_tagged_data:
    for line in welsh_tagged_data:
        line = line.strip()
        if line:
            line_tags = line.split('\t')
            tokens.append(line_tags[1])
            lemmas.append(line_tags[3])
            basic_pos_tags.append(line_tags[4])
            spaces.append(True)


# As the tagger is a spaCy component that expects tokens, pos, and lemma
# We need to create a spaCy Doc object that will contain this information
doc = Doc(Vocab(), words=tokens, tags=basic_pos_tags, lemmas=lemmas)
output_doc = nlp(doc)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.tag_}\t{token._.pymusas_tags}')
```

<details>
<summary>Output:</summary>

``` tsv
Text            Lemma           POS     USAS Tags
Sefydliad       sefydliad       E       ['S5+c', 'S7.1+', 'H1c', 'S1.1.1', 'T2+']
cyllidol        cyllidol        Ans     ['I1']
yw              bod             B       ['A3+', 'Z5']
bancwr          bancwr          E       ['Z99']
neu             neu             Cys     ['Z5']
fanc            banc            E       ['I1.1', 'X2.6+', 'M1']
sy              bod             B       ['A3+', 'Z5']
'n              yn              U       ['Z5']
actio           actio           B       ['A1.1.1', 'T1.1.2', 'A8', 'K4']
fel             fel             Cys     ['Z5']
asiant          asiant | asio   E | B   ['I2.1/S2mf', 'G3/S2mf', 'K4/S2mf']
talu            talu            B       ['I1.2', 'A9-', 'I1.1/I3.1']
ar              ar              Ar      ['Z5']
gyfer           cyfer           E       ['M6', 'Q2.2', 'Q2.2', 'S7.1+', 'X4.2', 'K4']
cwsmeriaid      cwsmer          E       ['I2.2/S2mf']
,               ,               Atd     ['PUNCT']
ac              a               Cys     ['Z5']
yn              yn              U       ['Z5']
rhoi            rhoi            B       ['A9-', 'A1.1.1']
benthyg         benthyg         E       ['A9-']
ac              a               Cys     ['Z5']
yn              yn              U       ['Z5']
benthyg         benthyg         B       ['A9-']
arian           arian           E       ['I1']
.               .               Atd     ['PUNCT']
Yn              yn              Ar      ['Z5']
rhai            rhai            unk     ['A13.5']
gwledydd        gwlad           E       ['M7']
,               ,               Atd     ['PUNCT']
megis           megis           Cys     ['Z5']
yr              y               YFB     ['Z5']
Almaen          Almaen          E       ['Z2']
a               a               Cys     ['Z5']
Siapan          Siapan          E       ['Z2']
,               ,               Atd     ['PUNCT']
mae             bod             B       ['A3+', 'Z5']
banciau         banc            E       ['I1.1', 'X2.6+', 'M1']
'n              yn              U       ['Z5']
brif            brif            unk     ['Z99']
berchenogion    berchenogion    unk     ['Z99']
corfforaethau   corfforaeth     E       ['I2.1/S5c', 'G1.1c']
diwydiannol     diwydiannol     Ans     ['I4']
,               ,               Atd     ['PUNCT']
tra             tra             Cys     ['Z5']
mewn            mewn            Ar      ['Z5']
gwledydd        gwlad           E       ['M7']
eraill          arall           Ans     ['A6.1-/Z8']
,               ,               Atd     ['PUNCT']
megis           megis           Cys     ['Z5']
yr              y               YFB     ['Z5']
Unol            unol            Ans     ['S5+', 'A1.1.1']
Daleithiau      Daleithiau      E       ['Z99']
,               ,               Atd     ['PUNCT']
mae             bod             B       ['A3+', 'Z5']
banciau         banc            E       ['I1.1', 'X2.6+', 'M1']
'n              yn              U       ['Z5']
cael            cael            B       ['A9+', 'Z5', 'X9.2+', 'A2.1+', 'A2.2', 'M1', 'M2', 'X2.5+', 'E4.1-']
eu              eu              Rha     ['Z8']
gwahardd        gwahardd        B       ['S7.4-']
rhag            rhag            Ar      ['Z5']
bod             bod             B       ['A3+', 'Z5']
yn              yn              U       ['Z5']
berchen         perchen         E       ['A9+/S2mf']
ar              ar              Ar      ['Z5']
gwmniau         gwmniau         unk     ['Z99']
sydd            bod             B       ['A3+', 'Z5']
ddim            dim             E       ['Z6/Z8']
yn              yn              U       ['Z5']
rhai            rhai            unk     ['A13.5']
cyllidol        cyllidol        Ans     ['I1']
.               .               Atd     ['PUNCT']
Adran           adran           E       ['G1.1']
Iechyd          iechyd          E       ['G1.1']
Cymru           Cymru           E       ['Z2', 'Z1mf']
.               .               Atd     ['PUNCT']
```

</details>

For Welsh the tagger also identifies and tags Multi-Word Expressions (MWE), to find these MWE's you can run the following:

``` python
print(f'Text\tPOS\tMWE start and end index\tUSAS Tags')
for token in output_doc:
    start, end = token._.pymusas_mwe_indexes[0]
    if (end - start) > 1:
        print(f'{token.text}\t{token.tag_}\t{(start, end)}\t{token._.pymusas_tags}')
```

Which will output the following:

``` tsv
Text    POS     MWE start and end index    USAS Tags
Adran   E       (71, 73)                   ['G1.1']
Iechyd  E       (71, 73)                   ['G1.1']
```

</details>

## Indonesian
<details>
<summary>Expand</summary>

In this example, we will not be using spaCy for tokenization, lemmatization, and POS tagging, as we will be using the [Indonesian TreeTagger](https://github.com/UCREL/Indonesian-TreeTagger-Docker-Build) that has been wrapped in a docker container. Therefore, first, you will need to [install docker](https://docs.docker.com/get-docker/). After installing docker you will need to build the Indonesian TreeTagger docker container locally, of which by doing this you agree to the [TreeTagger license](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/Tagger-Licence) (this license stops you from re-distributing the TreeTagger code, therefore please do not upload your built docker container to a registry like [Docker Hub](https://hub.docker.com/)), like so (docker container size roughly 139MB):

``` bash
docker build -t indonesian-treetagger:1.0.0 https://github.com/UCREL/Indonesian-TreeTagger-Docker-Build.git#main
```

We assume that you would like to tag the following text, of which this text is stored in the file named `indonesian_text_example.txt`. The example text is taken from the Indonesian Wikipedia page on the topic of [`Bank` as a financial institution.](https://id.wikipedia.org/wiki/Bank)

``` txt title="indonesian_text_example.txt"
Bank adalah sebuah lembaga keuangan intermediasi yang umumnya didirikan dengan kewenangan untuk menerima simpanan uang, meminjamkan uang, dan menerbitkan surat sanggup bayar.
```

First, we will need to run the Indonesian TreeTagger:

``` bash
cat indonesian_text_example.txt | docker run -i --rm indonesian-treetagger:1.0.0 > indonesian_text_example.tsv
```

We now have a `tsv` version of the file that has been tokenized, lemmatized, and POS tagged. The `indonesian_text_example.tsv` file should contain the following (I have added column headers here to explain what each column represents, these headers should not be in your file):

:::note
The POS tagset for Indonesian is not the USAS core or [UPOS](https://universaldependencies.org/u/pos/) tagset, but rather the [UI tagset](https://drive.google.com/file/d/1Pnhj2vVEEP5eIc655Af-WPDXxthyZdwb/view).
:::

<details>
<summary>indonesian_text_example.tsv:</summary>

``` tsv title="indonesian_text_example.tsv"
Token	POS	Lemma
Bank	NNP	bank
adalah	VB	adalah
sebuah	NND	sebuah
lembaga keuangan	NN	lembaga
intermediasi	NN	intermediasi
yang	SC	yang
umumnya	NN	umumnya
didirikan	VB	diri
dengan	IN	dengan
kewenangan	NN	wenang
untuk	SC	untuk
menerima	VB	terima
simpanan	NN	simpan
uang	NN	uang
,	Z	,
meminjamkan	VB	pinjam
uang	NN	uang
,	Z	,
dan	CC	dan
menerbitkan	VB	terbit
surat	NN	surat
sanggup	VB	sanggup
bayar	VB	bayar
.	Z	.
```

</details>

Now we have the token, lemma, and POS tag information we can run the [Indonsian PyMUSAS `RuleBasedTagger`](https://github.com/UCREL/pymusas-models/releases/tag/id_single_none_contextual-0.3.3), so first we will download it:

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/id_single_none_contextual-0.3.3/id_single_none_contextual-0.3.3-py3-none-any.whl
```

Now we can run the tagger over the `tsv` data using the following Python script:

``` python
from pathlib import Path
from typing import List

import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab

# Load the Indonesian PyMUSAS rule based tagger
nlp = spacy.load("id_single_none_contextual")

tokens: List[str] = []
spaces: List[bool] = []
pos_tags: List[str] = []
lemmas: List[str] = []

indonesian_tagged_file = Path(Path.cwd(), 'indonesian_text_example.tsv').resolve()

print('Text\tLemma\tPOS\tUSAS Tags')
with indonesian_tagged_file.open('r', encoding='utf-8') as indonesian_tagged_data:
    for line in indonesian_tagged_data:
        line = line.strip()
        if line:
            line_tags = line.split('\t')
            tokens.append(line_tags[0])
            lemmas.append(line_tags[2])
            pos_tags.append(line_tags[1])
            spaces.append(True)


# As the tagger is a spaCy component that expects tokens, pos, and lemma
# we need to create a spaCy Doc object that will contain this information
doc = Doc(Vocab(), words=tokens, tags=pos_tags, lemmas=lemmas)
output_doc = nlp(doc)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.tag_}\t{token._.pymusas_tags}')
```

<details>
<summary>Output:</summary>

``` tsv
Text                Lemma               POS     USAS Tags
Bank                bank                NNP     ['Z99']
adalah              adalah              VB      ['Z99']
sebuah              sebuah              NND     ['Z99']
lembaga keuangan    lembaga             NN      ['Z99']
intermediasi        intermediasi        NN      ['Z99']
yang                yang                SC      ['Z5']
umumnya             umumnya             NN      ['Z99']
didirikan           diri                VB      ['Z99']
dengan              dengan              IN      ['Z5']
kewenangan          wenang              NN      ['Z99']
untuk               untuk               SC      ['Z5']
menerima            terima              VB      ['Z99']
simpanan            simpan              NN      ['Z99']
uang                uang                NN      ['Z99']
,                   ,                   Z       ['PUNCT']
meminjamkan         pinjam              VB      ['Z99']
uang                uang                NN      ['Z99']
,                   ,                   Z       ['PUNCT']
dan                 dan                 CC      ['Z5']
menerbitkan         terbit              VB      ['Z99']
surat               surat               NN      ['Z99']
sanggup             sanggup             VB      ['Z99']
bayar               bayar               VB      ['Z99']
.                   .                   Z       ['PUNCT']
```

</details>

</details>

## English

<details>
<summary>Expand</summary>

First download both the [English PyMUSAS `RuleBasedTagger` spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/en_dual_none_contextual-0.3.3) and the [small English spaCy model](https://spacy.io/models/en):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/en_dual_none_contextual-0.3.3/en_dual_none_contextual-0.3.3-py3-none-any.whl
python -m spacy download en_core_web_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

# We exclude the following components as we do not need them. 
nlp = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
# Load the English PyMUSAS rule-based tagger in a separate spaCy pipeline
english_tagger_pipeline = spacy.load('en_dual_none_contextual')
# Adds the English PyMUSAS rule-based tagger to the main spaCy pipeline
nlp.add_pipe('pymusas_rule_based_tagger', source=english_tagger_pipeline)
```

The tagger is now set up for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the English Wikipedia page on the topic of [`The Nile River`](https://en.wikipedia.org/wiki/Nile), we capitalised the *n* in `Northeastern`:

``` python
text = "The Nile is a major north-flowing river in Northeastern Africa."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.pymusas_tags}')
```

<details>

<summary>Output:</summary>

``` tsv
Text            Lemma           POS     USAS Tags
The             the             DET     ['Z5']
Nile            Nile            PROPN   ['Z2']
is              be              AUX     ['A3+', 'Z5']
a               a               DET     ['Z5']
major           major           ADJ     ['A11.1+', 'N3.2+']
north           north           NOUN    ['M6']
-               -               PUNCT   ['PUNCT']
flowing         flow            VERB    ['M4', 'M1']
river           river           NOUN    ['W3/M4', 'N5+']
in              in              ADP     ['Z5']
Northeastern    Northeastern    PROPN   ['Z1mf', 'Z3c']
Africa          Africa          PROPN   ['Z1mf', 'Z3c']
.               .               PUNCT   ['PUNCT']
```
</details>

For English, the tagger also identifies and tags Multi-Word Expressions (MWE), to find these MWE's you can run the following:

``` python
print(f'Text\tPOS\tMWE start and end index\tUSAS Tags')

for token in output_doc:
    start, end = token._.pymusas_mwe_indexes[0]
    if (end - start) > 1:
        print(f'{token.text}\t{token.pos_}\t{(start, end)}\t{token._.pymusas_tags}')
```

Which will output the following:

``` tsv
Text            POS             MWE start and end index     USAS Tags
Northeastern    PROPN           (10, 12)                    ['Z1mf', 'Z3c']
Africa          PROPN           (10, 12)                    ['Z1mf', 'Z3c']
```

</details>
