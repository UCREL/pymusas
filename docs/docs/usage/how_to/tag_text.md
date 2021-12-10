---
title: Tag Text
sidebar_position: 1
---

In this guide we are going to show you how to tag text using the [USASRuleBasedTagger](/api/spacy_api/taggers/rule_based#usasrulebasedtagger), the guide is broken down into different languages, each language guide is almost identical with the exception of the USAS lexicon used and the spaCy pipeline that is required for lemmatisation and Part Of Speech (POS) tagging. In each of the language examples we will download the small version of the spaCy pipeline, but any version of the spaCy pipeline can be used.

## Chinese
<details>
<summary>Expand</summary>

First download the relevant spaCy pipeline, through the command line, link to [Chinese spaCy models](https://spacy.io/models/zh):

``` bash
python -m spacy download zh_core_web_sm
```

Then create the tagger, in a Python script:

:::note
That we only use the tokeniser of the spaCy pipeline as currently there is not lemmatisation component in the spaCy pipeline and the POS model tagset within the spaCy pipeline is the Chinese Treebank tagset which PyMUSAS does not support currently.
:::

``` python
import spacy

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based

# We exclude all of the components as all we need is the tokeniser. 
nlp = spacy.load('zh_core_web_sm', exclude=['parser', 'ner', 'tagger', 'tok2vec', 'attribute_ruler'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a USAS lexicon
chinese_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Chinese/semantic_lexicon_chi.tsv'
# As we are not using the POS information we exclude it from the lexicon
# NOTE: in this context lemma here means token.
chinese_lemma_lexicon_lookup = LexiconCollection.from_tsv(chinese_usas_lexicon_url, 
                                                          include_pos=False)
# Add the lemma lexicon information to the USAS tagger within the pipeline
usas_tagger.lemma_lexicon_lookup = chinese_lemma_lexicon_lookup
```

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Chinese Wikipedia page on topic the of [`Bank` as a financial institution.](https://zh.wikipedia.org/wiki/%E9%8A%80%E8%A1%8C):

``` python
text = "銀行是吸收公众存款、发放貸款、办理结算等業務的金融機構。"

output_doc = nlp(text)

print(f'Text\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token._.usas_tags}')
```

Output:

``` tsv
Text	USAS Tags
銀行	['Z99']
是	['A3', 'Z5']
吸收	['A1.1.1', 'T1.3+', 'X2.3+', 'X5.2+', 'C1', 'M2', 'A9+', 'X5.1+', 'I1.2', 'O4.2+', 'X2.1', 'K5.1', 'I3.1/A9+', 'S5+', 'N5', 'O4.1', 'A2.1/O1.2', 'A6.1+/A2.1']
公众	['A10+', 'G3/S7.1+/S2mf', 'B3/H1', 'N5+', 'A4.2-', 'S5+', 'S5+c']
存款	['S7.1-/A2.1']
、	['Z99']
发放	['A9-', 'A1.1.1', 'Q2.2', 'S6+', 'I1', 'O4.5']
貸款	['Z99']
、	['Z99']
办理	['A1.1.1', 'S7.1+', 'X9.2+', 'I2.2', 'S1.1.1', 'S7.1+c']
结算	['M2', 'A7+', 'A10+', 'I1.1', 'B4', 'O4.1']
等	['T1.3', 'A3+', 'S1.1.1']
業務	['Z99']
的	['Z5']
金融	['I1']
機構	['Z99']
。	['Z99']
```
</details>

## Dutch

<details>
<summary>Expand</summary>

First download the relevant spaCy pipeline, through the command line, link to [Dutch spaCy models](https://spacy.io/models/nl):

``` bash
python -m spacy download nl_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

# We exclude the following components as we do not need them. 
nlp = spacy.load('nl_core_news_sm', exclude=['parser', 'ner', 'tagger'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a USAS lexicon
dutch_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Dutch/semantic_lexicon_dut.tsv'
# Includes the POS information
dutch_lexicon_lookup = LexiconCollection.from_tsv(dutch_usas_lexicon_url)
# excludes the POS information
dutch_lemma_lexicon_lookup = LexiconCollection.from_tsv(dutch_usas_lexicon_url, 
                                                        include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = dutch_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = dutch_lemma_lexicon_lookup
# Maps from the POS model tagset to the lexicon POS tagset
usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
```

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Dutch Wikipedia page on topic the of [`Bank` as a financial institution.](https://nl.wikipedia.org/wiki/Bank_(financi%C3%ABle_instelling)):

``` python
text = "Een bank of een kredietinstelling is een financieel instituut dat bewaring van geld, leningen, betaalverkeer en diverse andere diensten aanbiedt."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.usas_tags}')
```

Output:

``` tsv
Text	Lemma	POS	USAS Tags
Een	een	DET	['Z5']
bank	bank	NOUN	['Z99']
of	of	CCONJ	['Z5']
een	een	DET	['Z5']
kredietinstelling	kredietinstelling	NOUN	['Z99']
is	is	AUX	['Z99']
een	een	DET	['Z5']
financieel	financieel	ADJ	['I1']
instituut	instituut	NOUN	['P1/S5+c', 'X2.4/S5+c', 'S5+c', 'T2+']
dat	dat	SCONJ	['A13.3', 'A6.1+', 'Z5', 'Z8']
bewaring	bewaring	NOUN	['Z99']
van	van	ADP	['Z5']
geld	geld	NOUN	['I1']
,	,	PUNCT	['PUNCT']
leningen	lening	NOUN	['A9-', 'I1.2']
,	,	PUNCT	['PUNCT']
betaalverkeer	betaalverkeer	PROPN	['Z99']
en	en	CCONJ	['Z5']
diverse	divers	ADJ	['A6.3+']
andere	ander	ADJ	['A6.1-', 'A6.1-/Z8']
diensten	dienst	NOUN	['A1.1.1', 'S8+', 'S7.1-', 'I2.2', 'S9', 'I3.1', 'F1', 'G3@', 'G1.1@', 'G2.1@']
aanbiedt	aanbieden	VERB	['A9-', 'Q2.2']
.	.	PUNCT	['PUNCT']
```
</details>

## French

<details>
<summary>Expand</summary>

First download the relevant spaCy pipeline, through the command line, link to [French spaCy models](https://spacy.io/models/fr):

``` bash
python -m spacy download fr_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

# We exclude the following components as we do not need them. 
nlp = spacy.load('fr_core_news_sm', exclude=['parser', 'ner'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a USAS lexicon
french_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.tsv'
# Includes the POS information
french_lexicon_lookup = LexiconCollection.from_tsv(french_usas_lexicon_url)
# excludes the POS information
french_lemma_lexicon_lookup = LexiconCollection.from_tsv(french_usas_lexicon_url, 
                                                         include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = french_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = french_lemma_lexicon_lookup
# Maps from the POS model tagset to the lexicon POS tagset
usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
```

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the French Wikipedia page on topic the of [`Bank` as a financial institution.](https://fr.wikipedia.org/wiki/Banque):

``` python
text = "Une banque est une institution financière qui fournit des services bancaires, soit notamment de dépôt, de crédit et paiement."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.usas_tags}')
```

Output:

``` tsv
Text	Lemma	POS	USAS Tags
Une	un	DET	['Z5']
banque	banque	NOUN	['I1.1', 'X2.6+', 'M1', 'I1/H1', 'I1.1/I2.1c', 'W3/M4', 'A9+/H1', 'O2', 'M6']
est	être	AUX	['M6']
une	un	DET	['Z5']
institution	institution	NOUN	['S5+c', 'S7.1+', 'H1c', 'S1.1.1', 'T2+']
financière	financier	ADJ	['Z99']
qui	qui	PRON	['Z8']
fournit	fournir	VERB	['Z99']
des	de	ADP	['Z5']
services	service	NOUN	['A1.1.1', 'S8+', 'S7.1-', 'I2.2', 'S9', 'I3.1', 'F1', 'G3@', 'G1.1@', 'G2.1@']
bancaires	bancaire	NOUN	['I1.1', 'X2.6+', 'M1', 'H1']
,	,	PUNCT	['PUNCT']
soit	soit	CCONJ	['Z99']
notamment	notamment	ADV	['A14', 'A13.3']
de	de	ADP	['Z5']
dépôt	dépôt	NOUN	['Z99']
,	,	PUNCT	['PUNCT']
de	de	ADP	['Z5']
crédit	crédit	NOUN	['I1.1', 'A5.1+', 'X2.1', 'P1']
et	et	CCONJ	['Z5']
paiement	paiement	NOUN	['I1.1']
.	.	PUNCT	['PUNCT']
```
</details>

## Italian

<details>
<summary>Expand</summary>

First download the relevant spaCy pipeline, through the command line, link to [Italian spaCy models](https://spacy.io/models/it):

``` bash
python -m spacy download it_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

# We exclude the following components as we do not need them. 
nlp = spacy.load('it_core_news_sm', exclude=['parser', 'ner', 'tagger'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a USAS lexicon
italian_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Italian/semantic_lexicon_ita.tsv'
# Includes the POS information
italian_lexicon_lookup = LexiconCollection.from_tsv(italian_usas_lexicon_url)
# excludes the POS information
italian_lemma_lexicon_lookup = LexiconCollection.from_tsv(italian_usas_lexicon_url, 
                                                          include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = italian_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = italian_lemma_lexicon_lookup
# Maps from the POS model tagset to the lexicon POS tagset
usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
```

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Italian Wikipedia page on topic the of [`Bank` as a financial institution.](https://it.wikipedia.org/wiki/Banca):

``` python
text = "Una banca (detta anche istituto di credito) è un istituto pubblico o privato che esercita congiuntamente l'attività di raccolta del risparmio tra il pubblico e di esercizio del credito (attività bancaria) verso i propri clienti (imprese e privati cittadini); costituisce raccolta del risparmio l'acquisizione di fondi con obbligo di rimborso."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.usas_tags}')
```

Output:

``` tsv
Text	Lemma	POS	USAS Tags
Una	uno	DET	['N1']
banca	banca	NOUN	['I2.1']
(	(	PUNCT	['PUNCT']
detta	dire	VERB	['Q2.2']
anche	anche	ADV	['Z5']
istituto	istituto	NOUN	['P1/S5+c', 'X2.4/S5+c']
di	di	ADP	['Z5']
credito	credito	NOUN	['I1.1', 'A5.1+', 'X2.1', 'P1', 'Q1.2', 'X3.2', 'T1.3', 'L2']
)	)	PUNCT	['PUNCT']
è	essere	AUX	['A5.1', 'S7.1++', 'X3.2', 'Q2.2', 'A8', 'N3.1%']
un	uno	DET	['Z5']
istituto	istituto	NOUN	['P1/S5+c', 'X2.4/S5+c']
pubblico	pubblico	ADJ	['A10+']
o	o	CCONJ	['Z5']
privato	privato	ADJ	['S1.2.1+', 'A1.7-']
che	che	PRON	['Z8']
esercita	esercitare	VERB	['A1.1.1', 'S7.1+', 'X8+', 'X2.4', 'M1', 'A9-', 'K5.1', 'A1.5.1']
congiuntamente	congiuntamente	ADV	['Z99']
l'	il	DET	['Z5']
attività	attività	NOUN	['A1.1.1', 'X8+', 'X2.4', 'M1']
di	di	ADP	['Z5']
raccolta	raccolta	NOUN	['F4', 'N4', 'Q4.3%', 'S9%', 'N5+', 'A9+']
del	del	ADP	['Z5']
risparmio	risparmio	NOUN	['I2.1', 'I1.3-', 'A1.5.1/A1.3+', 'A1.9']
tra	tra	ADP	['Z5']
il	il	DET	['Z5']
pubblico	pubblico	NOUN	['S1.1.3+', 'S5+']
e	e	CCONJ	['Z5']
di	di	ADP	['Z5']
esercizio	esercizio	NOUN	['K5.1', 'P1', 'A1.1.1', 'G3@', 'O2', 'G3', 'B5']
del	del	ADP	['Z5']
credito	credito	NOUN	['I1.1', 'A5.1+', 'X2.1', 'P1', 'Q1.2', 'X3.2', 'T1.3', 'L2']
(	(	PUNCT	['PUNCT']
attività	attività	NOUN	['A1.1.1', 'X8+', 'X2.4', 'M1']
bancaria	bancario	ADJ	['M1', 'M2', 'I1.2']
)	)	PUNCT	['PUNCT']
verso	verso	ADP	['Z5', 'M6']
i	il	DET	['Z5']
propri	proprio	DET	['Z5']
clienti	cliente	NOUN	['I2.2/S2mf']
(	(	PUNCT	['PUNCT']
imprese	impresa	NOUN	['A12-']
e	e	CCONJ	['Z5']
privati	privato	NOUN	['S1.2.1+', 'A1.7-']
cittadini	cittadino	NOUN	['M7/S2mf']
)	)	PUNCT	['PUNCT']
;	;	PUNCT	['PUNCT']
costituisce	costituire	VERB	['A1.1.1', 'A9+', 'A2.2', 'S6+', 'A3+', 'A9-', 'X9.2+', 'X6+']
raccolta	raccolta	NOUN	['F4', 'N4', 'Q4.3%', 'S9%', 'N5+', 'A9+']
del	del	ADP	['Z5']
risparmio	risparmio	NOUN	['I2.1', 'I1.3-', 'A1.5.1/A1.3+', 'A1.9']
l'	il	DET	['Z5']
acquisizione	acquisizione	NOUN	['Z99']
di	di	ADP	['Z5']
fondi	fondo	NOUN	['M6']
con	con	ADP	['Z5']
obbligo	obbligo	NOUN	['S6+']
di	di	ADP	['Z5']
rimborso	rimborso	NOUN	['I1.1', 'I1.1+/A9-', 'I1.2-', 'S1.1.2+', 'S8-']
.	.	PUNCT	['PUNCT']
```
</details>
