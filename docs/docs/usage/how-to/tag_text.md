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
# Includes the POS information
chinese_lexicon_lookup = LexiconCollection.from_tsv(chinese_usas_lexicon_url)
# excludes the POS information
chinese_lemma_lexicon_lookup = LexiconCollection.from_tsv(chinese_usas_lexicon_url, 
                                                          include_pos=False)
# Add the lexicon information to the USAS tagger within the pipeline
usas_tagger.lexicon_lookup = chinese_lexicon_lookup
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
