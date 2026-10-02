# Tag and export to TSV for manual annotation

In this example we are going to show how to tag the text from a file and then export that tagged text to TSV format for manual annotation/checking purposes. Once in TSV format it can be used in applications like Microsoft Excel or another spreadsheet editor, e.g. Google Sheets.

The TSV file we will create will have the following headers:

- "Token" - The predicted word or token text, e.g. "Bank". The word or token is not generated but the PyMUSAS tool does determine how to break the text up into tokens, this is what we mean by predicted and therefore this breaking up of the text into tokens could be incorrect.
- "POS" - The predicted Part Of Speech of the token, e.g. "NOUN".
- "Predicted-USAS" - The semicolon list of predicted USAS tags, whereby the first USAS tag in the list should be the most probable, e.g. "H4;I1.2"
- "Corrected-USAS" - The semicolon list of corrected USAS tags, whereby the first USAS tag in the list should be the most probable, e.g. "H1;I1.1" 
- "Errors" - A semicolon list of errors, e.g. "WRONG-POS;WRONG-TOKEN" whereby the list of errors is best to be pre-defined so that when analysing the dataset error statistics can be generated, e.g. 10% of samples have POS tag errors.
- "Notes" - Any additional notes you may want to add that is relevant to annotating this sample. These notes can be anything but should be useful for another annotator or colleague that is currently or in the future working on this project.

Only the first three headers will have content, "Token", "POS", and "Predicted-USAS", as the rest of the headers have to be filled in by an annotator.


## Chinese Example

This example shows how to create this TSV format when given a Chinese text, we are assuming the text file is at the following path [./data/zh_text.txt](./data/zh_text.txt)

First download both the [Chinese PyMUSAS RuleBasedTagger spaCy component](https://github.com/UCREL/pymusas-models/releases/tag/cmn_dual_upos2usas_contextual-0.3.3) and the [Transformer Chinese spaCy model](https://spacy.io/models/zh#zh_core_web_trf) (**Note** you can use any spaCy model but we are choosing the most powerful model so that we can get the most accurate tokenizer and POS tagger):

``` bash
pip install https://github.com/UCREL/pymusas-models/releases/download/cmn_dual_upos2usas_contextual-0.3.3/cmn_dual_upos2usas_contextual-0.3.3-py3-none-any.whl
pip install zh_core_web_trf@https://github.com/explosion/spacy-models/releases/download/zh_core_web_trf-3.8.0/zh_core_web_trf-3.8.0.tar.gz
```

Then we can tag the text and export the generated TSV file to `./zh_tagged_text.tsv`, the text we are tagging is the introduction to the ["Bank" Wikipedia page](https://zh.wikipedia.org/wiki/%E9%8A%80%E8%A1%8C).

``` bash
python tag_and_export.py zh_core_web_trf ./data/zh_text.txt ./zh_tagged_text.tsv
```

**Note** - `zh_core_web_trf` is the name of the SpaCy model we have installed and want to use.

**Note** - The POS tags are from the [Universal Dependency POS tagset.](https://universaldependencies.org/u/pos/)

### Excel specific

If you would like to export specifically to excel format.

First install the following Python dependency:

``` bash
pip install XlsxWriter
```

Then run the following to get an excel version:

``` bash
python tag_and_export.py zh_core_web_trf ./data/zh_text.txt ./zh_tagged_text.xlsx --excel-format
```

**Note** - the file extension different the output file name extension is `.xlsx` which is the extension used by Excel.