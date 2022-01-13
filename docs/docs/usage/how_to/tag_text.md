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
Currently there is no lemmatisation component in the spaCy pipeline for Chinese.
:::

``` python
import spacy

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

# We exclude the following components as we do not need them. 
nlp = spacy.load('zh_core_web_sm', exclude=['parser', 'ner'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a USAS lexicon
chinese_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Chinese/semantic_lexicon_chi.tsv'
# Includes the POS information
chinese_lexicon_lookup = LexiconCollection.from_tsv(chinese_usas_lexicon_url)
# excludes the POS information
chinese_lemma_lexicon_lookup = LexiconCollection.from_tsv(chinese_usas_lexicon_url, 
                                                          include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = chinese_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = chinese_lemma_lexicon_lookup
# Maps from the POS model tagset to the lexicon POS tagset
usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
```

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Chinese Wikipedia page on the topic of [`Bank` as a financial institution.](https://zh.wikipedia.org/wiki/%E9%8A%80%E8%A1%8C):

``` python
text = "銀行是吸收公众存款、发放貸款、办理结算等業務的金融機構。"

output_doc = nlp(text)

print(f'Text\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.pos_}\t{token._.usas_tags}')
```

Output:

``` tsv
Text	POS	USAS Tags
銀行	NOUN	['Z99']
是	VERB	['A3', 'Z5']
吸收	VERB	['A1.1.1', 'T1.3+', 'X2.3+', 'X5.2+', 'C1', 'M2', 'A9+', 'X5.1+', 'I1.2', 'O4.2+', 'X2.1', 'K5.1', 'I3.1/A9+', 'S5+', 'N5', 'O4.1', 'A2.1/O1.2', 'A6.1+/A2.1']
公众	NOUN	['A10+', 'G3/S7.1+/S2mf', 'B3/H1', 'N5+', 'A4.2-', 'S5+', 'S5+c']
存款	NOUN	['I1.1', 'O1.1', 'S7.1-/A2.1']
、	PUNCT	['PUNCT']
发放	VERB	['A9-', 'A1.1.1', 'Q2.2', 'S6+', 'I1', 'O4.5']
貸款	NOUN	['Z99']
、	PUNCT	['PUNCT']
办理	VERB	['A1.1.1', 'S7.1+', 'X9.2+', 'I2.2', 'S1.1.1', 'S7.1+c']
结算	NOUN	['L3', 'M2', 'A7+', 'A10+', 'I1.1', 'B4', 'O4.1']
等	PART	['T1.3', 'A3+', 'S1.1.1']
業務	VERB	['Z99']
的	PART	['Z5']
金融	NOUN	['I1', 'I1.1', 'X2.6+', 'M1', 'H1']
機構	NOUN	['Z99']
。	PUNCT	['PUNCT']
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

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Dutch Wikipedia page on the topic of [`Bank` as a financial institution.](https://nl.wikipedia.org/wiki/Bank_(financi%C3%ABle_instelling)):

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

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the French Wikipedia page on the topic of [`Bank` as a financial institution.](https://fr.wikipedia.org/wiki/Banque):

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

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Italian Wikipedia page on the topic of [`Bank` as a financial institution.](https://it.wikipedia.org/wiki/Banca):

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

## Portuguese

<details>
<summary>Expand</summary>

First download the relevant spaCy pipeline, through the command line, link to [Portuguese spaCy models](https://spacy.io/models/pt):

``` bash
python -m spacy download pt_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

# We exclude the following components as we do not need them. 
nlp = spacy.load('pt_core_news_sm', exclude=['parser', 'ner'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a USAS lexicon
portuguese_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Portuguese/semantic_lexicon_pt.tsv'
# Includes the POS information
portuguese_lexicon_lookup = LexiconCollection.from_tsv(portuguese_usas_lexicon_url)
# excludes the POS information
portuguese_lemma_lexicon_lookup = LexiconCollection.from_tsv(portuguese_usas_lexicon_url, 
                                                             include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = portuguese_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = portuguese_lemma_lexicon_lookup
# Maps from the POS model tagset to the lexicon POS tagset
usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
```

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Portuguese Wikipedia page on the topic of [`Bank` as a financial institution.](https://pt.wikipedia.org/wiki/Banco):

``` python
text = "Banco (do germânico banki, através do latim vulgar) é uma instituição financeira intermediária entre agentes superavitários e agentes deficitários."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.usas_tags}')
```

Output:

``` tsv
Text	Lemma	POS	USAS Tags
Banco	Banco	PROPN	['H5', 'B1%', 'I1/H1', 'I1.1/I2.1c', 'W3/M4', 'A9+/H1', 'O2', 'M6', 'G2.1c']
(	(	PUNCT	['PUNCT']
do	do	ADP	['Z5']
germânico	germânico	ADJ	['Z2', 'Z2/Q3']
banki	banki	ADJ	['Z99']
,	,	PUNCT	['PUNCT']
através	através	ADV	['M6', 'Z5']
do	do	ADP	['Z5']
latim	latim	NOUN	['Z2/Q3', 'Z2/S2mf']
vulgar	vulgar	VERB	['A6.2+', 'A5.1', 'N2', 'N5++', 'S5+', 'O4.2-', 'M7', 'S1.2.4-']
)	)	PUNCT	['PUNCT']
é	ser	AUX	['A3+', 'Z5']
uma	umar	DET	['Z99']
instituição	instituição	NOUN	['S5+c', 'S7.1+', 'H1c', 'S1.1.1', 'T2+']
financeira	financeiro	ADJ	['I1', 'I1/G1.1']
intermediária	intermediário	ADJ	['N5', 'N4', 'S8+/S2mf']
entre	entrar	ADP	['M1', 'S5+', 'T2+', 'A1.8+', 'Y2']
agentes	agente	NOUN	['I2.1/S2mf', 'G1.1/X2.2+/S2mf', 'K4/S2mf', 'I2.2/S2.2m', 'S8+/S2.2m']
superavitários	superavitários	ADJ	['Z99']
e	e	CCONJ	['Z5']
agentes	agente	NOUN	['I2.1/S2mf', 'G1.1/X2.2+/S2mf', 'K4/S2mf', 'I2.2/S2.2m', 'S8+/S2.2m']
deficitários	deficitário	ADJ	['Z99']
.	.	PUNCT	['PUNCT']
```
</details>

## Spanish

<details>
<summary>Expand</summary>

First download the relevant spaCy pipeline, through the command line, link to [Spanish spaCy models](https://spacy.io/models/es):

``` bash
python -m spacy download es_core_news_sm
```

Then create the tagger, in a Python script:

``` python
import spacy

from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

# We exclude the following components as we do not need them. 
nlp = spacy.load('es_core_news_sm', exclude=['parser', 'ner'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a USAS lexicon
spanish_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Spanish/semantic_lexicon_es.tsv'
# Includes the POS information
spanish_lexicon_lookup = LexiconCollection.from_tsv(spanish_usas_lexicon_url)
# excludes the POS information
spanish_lemma_lexicon_lookup = LexiconCollection.from_tsv(spanish_usas_lexicon_url, 
                                                          include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = spanish_lexicon_lookup
usas_tagger.lemma_lexicon_lookup = spanish_lemma_lexicon_lookup
# Maps from the POS model tagset to the lexicon POS tagset
usas_tagger.pos_mapper = UPOS_TO_USAS_CORE
```

The tagger is now setup for tagging text through the spaCy pipeline like so (this example follows on from the last). The example text is taken from the Spanish Wikipedia page on the topic of [`Bank` as a financial institution.](https://es.wikipedia.org/wiki/Banco):

``` python
text = "Un banco, también conocido como entidad de crédito o entidad de depósito es una empresa financiera que acepta depósitos del público y crea depósitos a la vista, lo que coloquialmente se denominan cuentas bancarias; así mismo proveen otro tipo de servicios financieros, como créditos."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.usas_tags}')
```

Output:

``` tsv
Text	Lemma	POS	USAS Tags
Un	uno	DET	['Z5', 'N1']
banco	banco	NOUN	['I2', 'M7']
,	,	PUNCT	['PUNCT']
también	también	ADV	['N5++', 'Z5']
conocido	conocido	ADJ	['Z99']
como	como	SCONJ	['Z5']
entidad	entidad	NOUN	['I2.1.3', 'G1', 'A3', 'S7.2+', 'S5+']
de	de	ADP	['Z5']
crédito	crédito	NOUN	['I2.1']
o	o	CCONJ	['Z5', 'A1.8-']
entidad	entidad	NOUN	['I2.1.3', 'G1', 'A3', 'S7.2+', 'S5+']
de	de	ADP	['Z5']
depósito	depósito	NOUN	['Z99']
es	ser	AUX	['Z5', 'A3+']
una	uno	DET	['Z5', 'Z8', 'N1']
empresa	empresa	NOUN	['I1.2.1.3', 'X6/X7']
financiera	financiero	ADJ	['I1', 'S2mf', 'S7']
que	que	PRON	['Z5', 'Z8']
acepta	aceptar	VERB	['A9+', 'X2.5+', 'S7.4+', 'S9@']
depósitos	depósito	NOUN	['Z99']
del	del	ADP	['Z5']
público	público	NOUN	['K1/S2mfc', 'S2mfc', 'S1.1.3+', 'S5+c', 'A10+']
y	y	CCONJ	['Z5', 'A1.8+']
crea	crea	VERB	['Z99']
depósitos	depósito	NOUN	['Z99']
a	a	ADP	['Z5']
la	el	DET	['Z5']
vista	vista	NOUN	['X3.4', 'M5', 'B2', 'G2.1']
,	,	PUNCT	['PUNCT']
lo	él	PRON	['Z5', 'Z8']
que	que	PRON	['Z5', 'Z8']
coloquialmente	coloquialmentar	VERB	['Z99']
se	él	PRON	['Z5', 'Z8', 'S1.1']
denominan	denominar	VERB	['Z99']
cuentas	cuenta	NOUN	['I1.1/N2/Y2', 'N5', 'N5.1+', 'I1.3.1', 'O2']
bancarias	bancario	ADJ	['Z99']
;	;	PUNCT	['PUNCT']
así	así	ADV	['Z5', 'A8', 'N3']
mismo	mismo	PRON	['A6']
proveen	proveer	VERB	['A9+', 'S6+']
otro	otro	DET	['Z8', 'A6.1-m', 'N5++']
tipo	tipo	NOUN	['A4.1', 'A6.1', 'S2.2m', 'Y2', 'I1.2', 'I1.3']
de	de	ADP	['Z5']
servicios	servicio	NOUN	['I1', 'S8+', 'G1']
financieros	financiero	ADJ	['I1', 'S2mf', 'S7']
,	,	PUNCT	['PUNCT']
como	como	SCONJ	['Z5']
créditos	crédito	NOUN	['I2.1']
.	.	PUNCT	['PUNCT']
```
</details>


## Welsh
<details>
<summary>Expand</summary>

In this example we will not be using spaCy for tokenisation, lemmatisation, and POS tagging, as we will be using the [CyTag toolkit](https://github.com/UCREL/CyTag) that has been wrapped in a docker container. Therefore, first you will need to [install docker](https://docs.docker.com/get-docker/).

We assume that you would like to tag the following text, of which this text is stored in the file named `welsh_text_example.txt`. The example text is taken from the Welsh Wikipedia page on the topic of [`Bank` as a financial institution.](https://cy.wikipedia.org/wiki/Banc)

``` txt title="welsh_text_example.txt"
Sefydliad cyllidol yw bancwr neu fanc sy'n actio fel asiant talu ar gyfer cwsmeriaid, ac yn rhoi benthyg ac yn benthyg arian. Yn rhai gwledydd, megis yr Almaen a Siapan, mae banciau'n brif berchenogion corfforaethau diwydiannol, tra mewn gwledydd eraill, megis yr Unol Daleithiau, mae banciau'n cael eu gwahardd rhag bod yn berchen ar gwmniau sydd ddim yn rhai cyllidol.
```

First we will need to run the CyTag toolkit, more specifically we will run version 1 of the toolkit as we have a mapping from the POS tags produced in version 1 (the [basic CorCencC POS tagset](https://cytag.corcencc.org/tagset?lang=en)) to the POS tags that the USAS lexicon uses (the USAS core POS tagset)

``` bash
cat welsh_text_example.txt | docker run -i --rm ghcr.io/ucrel/cytag:1.0.4 > welsh_text_example.tsv
```

We now have a `tsv` version of the file that has been tokenised, lemmatised, and POS tagged. The `welsh_text_example.tsv` file should contain the following (I have added column headers here to explain what each column represents, these headers should not be in your file, also note that the "Mutation" column is optional):

``` tsv title="welsh_text_example.tsv"
Line Number       Token       Sentence Index, Token Index     Lemma       Basic POS       Enriched POS       Mutation
1       Sefydliad       1,1     sefydliad       E       Egu
2       cyllidol        1,2     cyllidol        Ans     Anscadu
3       yw      1,3     bod     B       Bpres3u
4       bancwr  1,4     bancwr  E       Egu
5       neu     1,5     neu     Cys     Cyscyd
6       fanc    1,6     banc    E       Egu     +sm
7       sy      1,7     bod     B       Bpres3perth
8       'n      1,8     yn      U       Uberf
9       actio   1,9     actio   B       Be
10      fel     1,10    fel     Cys     Cyscyd
11      asiant  1,11    asiant | asio   E | B   Egu | Bpres3ll
12      talu    1,12    talu    B       Be
13      ar      1,13    ar      Ar      Arsym
14      gyfer   1,14    cyfer   E       Egu     +sm
15      cwsmeriaid      1,15    cwsmer  E       Egll
16      ,       1,16    ,       Atd     Atdcan
17      ac      1,17    a       Cys     Cyscyd
18      yn      1,18    yn      U       Uberf
19      rhoi    1,19    rhoi    B       Be
20      benthyg 1,20    benthyg E       Egu
21      ac      1,21    a       Cys     Cyscyd
22      yn      1,22    yn      U       Uberf
23      benthyg 1,23    benthyg B       Be
24      arian   1,24    arian   E       Egu
25      .       1,25    .       Atd     Atdt
26      Yn      2,1     yn      Ar      Arsym
27      rhai    2,2     rhai    unk     unk
28      gwledydd        2,3     gwlad   E       Ebll
29      ,       2,4     ,       Atd     Atdcan
30      megis   2,5     megis   Cys     Cyscyd
31      yr      2,6     y       YFB     YFB
32      Almaen  2,7     Almaen  E       Epb
33      a       2,8     a       Cys     Cyscyd
34      Siapan  2,9     Siapan  E       Epb
35      ,       2,10    ,       Atd     Atdcan
36      mae     2,11    bod     B       Bpres3u
37      banciau 2,12    banc    E       Egll
38      'n      2,13    yn      U       Utra
39      brif    2,14    brif    unk     unk
40      berchenogion    2,15    berchenogion    unk     unk
41      corfforaethau   2,16    corfforaeth     E       Ebll
42      diwydiannol     2,17    diwydiannol     Ans     Anscadu
43      ,       2,18    ,       Atd     Atdcan
44      tra     2,19    tra     Cys     Cyscyd
45      mewn    2,20    mewn    Ar      Arsym
46      gwledydd        2,21    gwlad   E       Ebll
47      eraill  2,22    arall   Ans     Anscadu
48      ,       2,23    ,       Atd     Atdcan
49      megis   2,24    megis   Cys     Cyscyd
50      yr      2,25    y       YFB     YFB
51      Unol    2,26    unol    Ans     Anscadu
52      Daleithiau      2,27    Daleithiau      E       Ep
53      ,       2,28    ,       Atd     Atdcan
54      mae     2,29    bod     B       Bpres3u
55      banciau 2,30    banc    E       Egll
56      'n      2,31    yn      U       Uberf
57      cael    2,32    cael    B       Be
58      eu      2,33    eu      Rha     Rhadib3ll
59      gwahardd        2,34    gwahardd        B       Be
60      rhag    2,35    rhag    Ar      Arsym
61      bod     2,36    bod     B       Be
62      yn      2,37    yn      U       Utra
63      berchen 2,38    perchen E       Egu     +sm
64      ar      2,39    ar      Ar      Arsym
65      gwmniau 2,40    gwmniau unk     unk
66      sydd    2,41    bod     B       Bpres3perth
67      ddim    2,42    dim     E       Egu     +sm
68      yn      2,43    yn      U       Utra
69      rhai    2,44    rhai    unk     unk
70      cyllidol        2,45    cyllidol        Ans     Anscadu
71      .       2,46    .       Atd     Atdt
```

Now we have the token, lemma, and POS tag information we can now create a [USASRuleBasedTagger](https://ucrel.github.io/pymusas/api/taggers/rule_based#usasrulebasedtagger) and run the tagger over this `tsv` data using the following Python script:

``` python
from pathlib import Path
import csv

from pymusas.lexicon_collection import LexiconCollection
from pymusas.taggers.rule_based import USASRuleBasedTagger

# Rule based tagger requires a USAS lexicon
welsh_usas_lexicon_url = 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Welsh/semantic_lexicon_cy.tsv'
# Includes the POS information
welsh_lexicon_lookup = LexiconCollection.from_tsv(welsh_usas_lexicon_url)
# excludes the POS information
welsh_lemma_lexicon_lookup = LexiconCollection.from_tsv(welsh_usas_lexicon_url, 
                                                        include_pos=False)
usas_tagger = USASRuleBasedTagger(welsh_lexicon_lookup, welsh_lemma_lexicon_lookup)

welsh_tagged_file = Path(Path.cwd(), 'welsh_text_example.tsv').resolve()

print(f'Text\tLemma\tPOS\tUSAS Tags')
with welsh_tagged_file.open('r', encoding='utf-8') as welsh_tagged_data:
    for line in welsh_tagged_data:
        line = line.strip()
        if line:
            line_tags = line.split('\t')
            token = line_tags[1]
            lemma = line_tags[3]
            basic_pos = line_tags[4]
            usas_tags = usas_tagger.tag_token((token, lemma, basic_pos))
            print(f'{token}\t{lemma}\t{basic_pos}\t{usas_tags}')
```

Output:

``` tsv
Text       Lemma       POS       USAS Tags
Sefydliad       sefydliad       E       ['S5+c', 'S7.1+', 'H1c', 'S1.1.1', 'T2+']
cyllidol        cyllidol        Ans     ['I1']
yw      bod     B       ['A3+', 'Z5']
bancwr  bancwr  E       ['Z99']
neu     neu     Cys     ['Z5']
fanc    banc    E       ['I1.1', 'X2.6+', 'M1']
sy      bod     B       ['A3+', 'Z5']
'n      yn      U       ['Z5']
actio   actio   B       ['A1.1.1', 'T1.1.2', 'A8', 'K4']
fel     fel     Cys     ['Z5']
asiant  asiant | asio   E | B   ['I2.1/S2mf', 'G3/S2mf', 'K4/S2mf']
talu    talu    B       ['I1.2', 'A9-', 'I1.1/I3.1']
ar      ar      Ar      ['Z5']
gyfer   cyfer   E       ['M6', 'Q2.2', 'Q2.2', 'S7.1+', 'X4.2', 'K4']
cwsmeriaid      cwsmer  E       ['I2.2/S2mf']
,       ,       Atd     ['Z99']
ac      a       Cys     ['Z5']
yn      yn      U       ['Z5']
rhoi    rhoi    B       ['A9-', 'A1.1.1']
benthyg benthyg E       ['A9-']
ac      a       Cys     ['Z5']
yn      yn      U       ['Z5']
benthyg benthyg B       ['A9-']
arian   arian   E       ['I1']
.       .       Atd     ['Z99']
Yn      yn      Ar      ['Z5']
rhai    rhai    unk     ['A13.5']
gwledydd        gwlad   E       ['M7']
,       ,       Atd     ['Z99']
megis   megis   Cys     ['Z5']
yr      y       YFB     ['Z5']
Almaen  Almaen  E       ['Z2']
a       a       Cys     ['Z5']
Siapan  Siapan  E       ['Z2']
,       ,       Atd     ['Z99']
mae     bod     B       ['A3+', 'Z5']
banciau banc    E       ['I1.1', 'X2.6+', 'M1']
'n      yn      U       ['Z5']
brif    brif    unk     ['Z99']
berchenogion    berchenogion    unk     ['Z99']
corfforaethau   corfforaeth     E       ['I2.1/S5c', 'G1.1c']
diwydiannol     diwydiannol     Ans     ['I4']
,       ,       Atd     ['Z99']
tra     tra     Cys     ['Z5']
mewn    mewn    Ar      ['Z5']
gwledydd        gwlad   E       ['M7']
eraill  arall   Ans     ['A6.1-/Z8']
,       ,       Atd     ['Z99']
megis   megis   Cys     ['Z5']
yr      y       YFB     ['Z5']
Unol    unol    Ans     ['S5+', 'A1.1.1']
Daleithiau      Daleithiau      E       ['Z99']
,       ,       Atd     ['Z99']
mae     bod     B       ['A3+', 'Z5']
banciau banc    E       ['I1.1', 'X2.6+', 'M1']
'n      yn      U       ['Z5']
cael    cael    B       ['A9+', 'Z5', 'X9.2+', 'A2.1+', 'A2.2', 'M1', 'M2', 'X2.5+', 'E4.1-']
eu      eu      Rha     ['Z8']
gwahardd        gwahardd        B       ['S7.4-']
rhag    rhag    Ar      ['Z5']
bod     bod     B       ['A3+', 'Z5']
yn      yn      U       ['Z5']
berchen perchen E       ['A9+/S2mf']
ar      ar      Ar      ['Z5']
gwmniau gwmniau unk     ['Z99']
sydd    bod     B       ['A3+', 'Z5']
ddim    dim     E       ['Z6/Z8']
yn      yn      U       ['Z5']
rhai    rhai    unk     ['A13.5']
cyllidol        cyllidol        Ans     ['I1']
.       .       Atd     ['Z99']
```
</details>