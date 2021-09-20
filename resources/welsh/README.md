# Welsh Resources

In this directory are all of the Welsh language resources used to either evaluate a semantic tagger or resources used by the semantic tagger.

## Evaluation Resources

### Original Gold Standard Dataset

The gold standard dataset was released within the following [GitHub repository](https://github.com/CorCenCC/welsh_pos_sem_tagger), with the paper [Leveraging Pre-Trained Embeddings for Welsh Taggers](https://aclanthology.org/W19-4332.pdf), this original Gold standard dataset can be found in [./original_gold_standard_data.txt](./original_gold_standard_data.txt). The Part Of Speech (POS) tags that are used within the Gold Standard dataset are from the [CorCenCC basic POS tagset (see table 1)](https://aclanthology.org/L18-1623.pdf).

#### Format and statistics

The dataset is 611 sentences and contains 14,876 tokens. Each sentence is on one line, each token is separated by a whitespace, each token contains the `token`, `POS tag`, and `USAS tag` separated by a `|`. Below we show the first sentence of the dataset:

```txt
A|Rha|Z5 fydd|B|A3+ rhywfaint|E|N5/N5.1- o|Ar|Z5 'r|YFB|Z5 arian|E|I1 hwn|Rha|A3+ yn|U|Z5 cael|B|A9 ei|Rha|Z8 ddefnyddio|B|A1.5.1 i|Ar|Z5 sicrhau|B|A7+ bod|B|A3+ modd|E|X4.2 defnyddio|B|A1.5.1 tocynnau|E|Q1.2 rhatach|Ans|I1.3- yn|Ar|Z5 Lloegr|E|Z2 yn|Ar|Z5 ogystal|Ans|Z99 ag|Ar|Z5 yng|Ar|Z5 Nghymru|E|Z2 ?|Atd|PUNCT
```

#### Differences to the original gold standard dataset

The original gold standard dataset that is within the following [GitHub repository](https://github.com/CorCenCC/welsh_pos_sem_tagger), is slightly different to the one in this repository. The differences are the following, of which these changes were done as we believe these to be POS tag errors that came about when mapping CorCenCC POS tagset to the [core POS tagset that is used by the USAS multilingual lexicon](https://aclanthology.org/N15-1137.pdf). The core POS tagset is best shown in [table 5 of the paper Towards A Welsh Semantic Annotation System](https://aclanthology.org/L18-1158.pdf)

1. The POS tag `pron.demd` was changed to `Rha`
2. The POS tag `pron.demg` was changed to `Rha`
3. The POS tag `pron.demb` was changed to `Rha`
4. The POS tag `unk` was changed to `Gw`

### Enhanced Gold Standard Dataset

The enhanced gold standard dataset, [./enhanced_gold_standard_data.txt](./enhanced_gold_standard_data.txt), contains additional data for each token. Instead of just having the `token`, `POS tag`, and `USAS tag` separated by a `|`. It now contains the following:

1. `token` - same as before
2. `lemma` - lemma that has come from the [CyTag tagger](https://github.com/CorCenCC/CyTag).
3. `core POS tag` - The core POS tag that is used by the USAS multilingual lexicon, this is found through the mapping of basic CorCenCC POS tags to core USAS POS tags, see the [Mapper of basic CorCenCC POS tags to core USAS POS tags section below for more details.](#mapper-of-basic-corcencc-pos-tags-to-core-usas-pos-tags)
4. `basic POS tag` - same as before, but was called the `POS tag`
5. `enriched POS tag` - this has come from running the [CyTag tagger](https://github.com/CorCenCC/CyTag). As this tag has been predicted it may be different to the `basic POS tag`, as the basic tag is gold standard.
6. `USAS tag` - same as before

To re-create this dataset run the following:

``` bash
python convert_welsh_gold_to_text.py # This creates a file called txt_gold_standard_data.txt which contains just the tokenised text.
mkdir -p ./output
sudo chmod -R 777 ./output
docker run --rm -v $(pwd)/txt_gold_standard_data.txt:/tmp/text_file.txt -v $(pwd)/output:/usr/nobody/CyTag-1.0/outputs ghcr.io/ucrel/cytag:1.0.4 -f xml -n example -i /tmp/text_file.txt # Runs the CyTag tagger on the txt_gold_standard_data.txt file.
# Extract XML output from running the CyTag tagger
sudo chown $(id -u):$(id -g) ./output/example/example.xml
sudo mv ./output/example/example.xml ./cytag_output.xml
sudo rm -rf ./output
python create_enhanced_dataset.py
rm txt_gold_standard_data.txt
rm cytag_output.xml
```

### Mapper of basic CorCenCC POS tags to core USAS POS tags

To map between the basic CorCenCC POS tags to the core USAS POS tags we have created a JSON file that contains these mappings, [./basic_cy_tags_to_core_tags.json](./resources/basic_cy_tags_to_core_tags.json). This mapping is based off table A.1 in [Leveraging Pre-Trained Embeddings for Welsh Taggers](https://aclanthology.org/W19-4332.pdf).

Another way of mapping from the CorCenCC POS tags to the core USAS POS tags would be through the rich/enriched tagset rather than the basic. This was not done as the basic POS tags in the Gold dataset are hand annotated, whereas the rich POS tags would be predicted. However for the interested reader the rich to USAS core POS tags mapper can be found in [table 6 of the paper Towards A Welsh Semantic Annotation System](https://aclanthology.org/L18-1158.pdf). 

## Semantic Tagger Resources

The only resource that is used by the Semantic tagger is the single word semantic lexicon, which is within the [./semantic_lexicon_cy.usas.txt](./semantic_lexicon_cy.usas.txt). This lexicon is formatted in TSV format like so:


|lemma/word | POS label |  Semantic Labels/USAS labels  |
|-----------|-----------|-------------------------------|
|apig	    |      noun	|          M6 N2 X9.2+          |

Whereby you can find the semantic labels of a lexeme (lemma, pos label) by looking up that lexeme in the lexicon. The lexeme may result in more than one semantic label as shown above, the most likely semantic label is the first label in the space separated list of labels, in the case above this would be `M6`, for more information on the [USAS tagset see the section in the main README.](../../README.md#usas-tagset)

In the [single word semantic lexicon for Welsh](https://github.com/UCREL/Multilingual-USAS/blob/master/Welsh/semantic_lexicon_cy.usas), some of the lemmas are not lower cased, of which all of these are a type of noun. Some of these names are multi word expression but with a `_` to combine the two words together, in total across all POS tags there are 94 of these, a good example is for the word `Friday` which in the lexicon is `dydd_Gwener`.