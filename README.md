# PyMUSAS 

**Py**thon **M**ultilingual **U**crel **S**emantic **A**nalysis **S**ystem, it currently is a rule based token level semantic tagger which can be added to any spaCy pipeline. The current tagger system is flexible enough to support any semantic tagset, however the tagset we have concentrated on and give examples for throughout the documentation is the [Ucrel Semantic Analysis System (USAS)](https://ucrel.lancs.ac.uk/usas/).

<hr/>

<p align="center">
    <a href="https://github.com/UCREL/pymusas/actions/workflows/ci.yml">
        <img alt="CI" src="https://github.com/UCREL/pymusas/actions/workflows/ci.yml/badge.svg?branch=main&event=push"/>
    </a>
    <a href="https://github.com/UCREL/pymusas/blob/main/LICENSE">
        <img alt="License" src="https://img.shields.io/pypi/l/pymusas"/>
    </a>
    <a href="https://codecov.io/gh/UCREL/pymusas">
        <img alt="Code coverage" src="https://codecov.io/gh/UCREL/pymusas/branch/main/graph/badge.svg" />
    </a>

</p>
<p align="center">
    <a href="https://pypi.org/project/pymusas/">
        <img alt="PyPI Version" src="https://img.shields.io/pypi/v/pymusas"/>
    </a>
    <img alt="Supported Python Versions" src="https://img.shields.io/pypi/pyversions/pymusas" />
</p>
<p align="center">
    <img alt="Number of PyMUSAS PyPI downloads for the last month" 
         src="https://img.shields.io/pypi/dm/pymusas" />
    <a href="https://mybinder.org/v2/gh/UCREL/pymusas/binder-main?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252FUCREL%252Fpymusas%26urlpath%3Dlab%252Ftree%252Fpymusas%252F%26branch%3Dmain">
        <img alt="Launch Binder" src="https://static.mybinder.org/badge_logo.svg">
    </a>
</p>

## Documentation

* 📚 [Usage Guides](https://ucrel.github.io/pymusas/) - What the package is, tutorials, how to guides, and explanations.
* 🔎 [API Reference](https://ucrel.github.io/pymusas/api/spacy_api/taggers/rule_based) - The docstrings of the library, with minimum working examples.

## Install PyMUSAS

Can be installed on all operating systems and supports Python version >= `3.7`, to install run:

```
pip install pymusas
```

## Quick example

Here is a quick example of what PyMUSAS can do using the [USASRuleBasedTagger](https://ucrel.github.io/pymusas/api/spacy_api/taggers/rule_based), from now on called the USAS tagger, for a full tutorial, which explains all of the steps in this example, see the [Using PyMUSAS tutorial in the documentation](https://ucrel.github.io/pymusas/using).

This example will semantically tag, at the token level, some Portuguese text. We do first need to download a [spaCy Portuguese model](https://spacy.io/models/pt) (any version will do, but we choose the small version)

``` bash
python -m spacy download pt_core_news_sm
```

Then we load the Portuguese spaCy tagger, add the USAS tagger, and apply it to the Portuguese text:

``` python
import spacy

from pymusas.file_utils import download_url_file
from pymusas.lexicon_collection import LexiconCollection
from pymusas.spacy_api.taggers import rule_based
from pymusas.pos_mapper import UPOS_TO_USAS_CORE

# We exclude ['parser', 'ner'] as these components are typically not needed
# for the USAS tagger
nlp = spacy.load('pt_core_news_sm', exclude=['parser', 'ner'])
# Adds the tagger to the pipeline and returns the tagger 
usas_tagger = nlp.add_pipe('usas_tagger')

# Rule based tagger requires a lexicon
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
# Maps from the POS model tagset to the lexicon POS tagset
usas_tagger.pos_mapper = UPOS_TO_USAS_CORE

text = "O Parque Nacional da Peneda-Gerês é uma área protegida de Portugal, com autonomia administrativa, financeira e capacidade jurídica, criada no ano de 1971, no meio ambiente da Peneda-Gerês."

output_doc = nlp(text)

print(f'Text\tLemma\tPOS\tUSAS Tags')
for token in output_doc:
    print(f'{token.text}\t{token.lemma_}\t{token.pos_}\t{token._.usas_tags}')
```

This will output the following, whereby the USAS tags are a list of the most likely semantic tags, the first tag in the list is the most likely semantic tag. For more information on the USAS tagset see the [USAS website](https://ucrel-web.lancs.ac.uk/usas/).

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

### Development

When developing on the project you will want to install the Python package locally in editable format with all the extra requirements, this can be done like so:

```bash
pip install -e .[tests]
```

For a `zsh` shell, which is the default shell for the new Macs you will need to escape with `\` the brackets:

```zsh
pip install -e .\[tests\]
```

#### Running linters and tests

This code base uses flake8 and mypy to ensure that the format of the code is consistent and contain type hints. The flake8 settings can be found in [./setup.cfg](./setup.cfg) and the mypy settings within [./pyproject.toml](./pyproject.toml). To run these linters:

``` bash
isort pymusas tests scripts
flake8
mypy
```

To run the tests with code coverage (**NOTE** these are the code coverage tests that the Continuos Integration (CI) reports at the top of this README, the doc tests are not part of this report):

``` bash
coverage run # Runs the tests (uses pytest)
coverage report # Produces a report on the test coverage
```

To run the [doc tests](https://docs.python.org/3/library/doctest.html), these are tests to ensure that examples within the documentation run as expected:

``` bash
coverage run -m pytest --doctest-modules pymusas/ # Runs the doc tests
coverage report # Produces a report on the doc tests coverage
```

## Team

PyMUSAS is an open-source project that has been created and funded by the [University Centre for Computer Corpus Research on Language](https://ucrel.lancs.ac.uk/) (UCREL) at [Lancaster University](https://www.lancaster.ac.uk/). For more information on who has contributed to this code base see the [contributions page.](https://github.com/UCREL/pymusas/graphs/contributors) 