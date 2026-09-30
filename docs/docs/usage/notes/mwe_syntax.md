---
title: Multi Word Expression Syntax
sidebar_position: 1
---

These notes explain how to interpret the Multi Word Expression (MWE) syntax that is contained in the MWE lexicon files, which can be found in the [Multilingual-USAS GitHub repository](https://github.com/UCREL/Multilingual-USAS#multi-word-expression-mwe-lexicon-file-format). The MWE syntax has also been defined and used in previous papers on the USAS semantic tagger, e.g. figure 1 of [Extracting Multiword Expressions with A Semantic Tagger by Piao et al. 2003](https://aclanthology.org/W03-1807.pdf) and figure 3 of [The UCREL Semantic Analysis System by Rayson et al. 2004](https://www.lancaster.ac.uk/staff/rayson/publications/usas_lrec04ws.pdf). Within this documentation an example that uses the MWE syntax will be called a **MWE template**. An example of the MWE syntax can be seen below, whereby this pattern would capture words like `Pacific Ocean` and `Atlantic Ocean`.

``` txt title="MWE template example"
*_* Ocean_N*1
```

The MWE syntax is best described as a simplified pattern matching syntax/code, like a regular expression, that is used to capture MWEs that have similar structure.

Structure of this documentation page:

1. [General syntax structure](#general-syntax-structure) - explains the general MWE syntax structure.
2. [Syntax symbol definitions](#syntax-symbol-definitions) - will define special syntax symbols that allow the MWE syntax to capture more complicated MWE, e.g. inflection variants and discontinuous MWE.
3. [Default semantic tag](#default-semantic-tag) - explains the default (`Df`) semantic tag that some MWE templates use.

## General syntax structure

The general syntax can be best seen below, in which the MWE syntax is sequence of words/tokens and Part Of Speech (POS) tags joined together by an underscore and separated by a single whitespace:

``` txt title="MWE general structure"
word1_POS1 word2_POS2 word3_POS3
```

This general syntax allows us to find MWE within text using both the token and the corresponding POS. For instance given the text:

``` txt
I went to the river bank after walking back from the bank.
```

and the following MWE template:

```txt
river_noun bank_noun
```

The MWE `river bank` would be extracted from the given text.

## Syntax symbol definitions

### Wildcard

The wildcard symbol, `*`, states that zero or more characters may appear after the word token and/or Part Of Speech (POS) tag.

This can be most useful for capturing inflectional variants and increasing the recall of your MWE.

#### Examples

To take into account that `Amazon` could be a proper noun (POS tag = `pnoun`) or a common noun (POS tag = `noun`) we can use the `*` at the start of the POS tag `noun` to allow for both `pnoun` or `noun` as the POS tag for the token `Amazon`, whereby in the example MWE template below we are trying to capture the MWE that represents the [Amazon rainforest](https://en.wikipedia.org/wiki/Amazon_rainforest) in a text.

``` txt
Amazon_*noun rainforest_noun
```

<hr/>

We can also use the `*` to state that it can be any token or POS, for instance if we want to capture the text of any type of boot, e.g. `ski boot`, `ski boots`, `walking boot`, etc. we could write the following MWE template:

``` txt
*_noun boot*_noun
```

<hr/>

If the POS tagset you are working with is more fine grained than having just `pnoun` and `noun` for all types of nouns, e.g. for [CLAWS 7 tagset](https://ucrel.lancs.ac.uk/claws7tags.html) which includes `NN1` for a singular common noun and `NN2` for a plural common noun, then you could write the MWE template like so:

``` txt
*_NN1 boot*_NN*
```

### Curly Braces

**Note that this feature is not implemented yet, see [issue #24](https://github.com/UCREL/pymusas/issues/24)**

The curly braces, e.g. `{}` can be used to match discontinuous MWE. 

The only symbols that can be used within a curly brace are: 

- word tokens
- POS tags
- the item "Np"
- The wildcard symbol attached to a word token or POS tag
- A slash (`/`) to separate the words and/or POS tags.

The curly braces format states that word tokens and/or the POS types defined within the curly brace can **optionally** appear, i.e. zero or more times, at that point between the two tokens in the discontinuous MWE. The slash allows you to have more than one type of word and/or POS tag defined within the curly brace. The ordering of the elements between slashes is not significant. Items inside the curly braces are not considered part of the MWE, i.e. not semantically tagged as such, but just as intervening items (and given their semantic tags from other methods).

The item "Np" is interpreted as an intervening noun phrase between two tokens of a MWE if a noun phrase chunker has been used to mark up noun phrases in the text.

A curly brace sequence **cannot** start or end a MWE template, it must appear between tokens, but more than one set of curly braces can appear in an MWE template.

#### Examples

To capture "asked to" as a discontinuous MWE in the following text:

``` txt
I asked David Brown to go over to the house next door.
```

You can use the following MWE template:

``` txt
asked_verb {noun} to_prep
```

<hr/>

To capture "stub out" as a discontinuous expression in the following text:

``` txt
I asked him to stub the cigarette out.
```

You can use the following MWE template:

``` txt
stub_verb {noun/det} out_adv
```

<hr/>

Similarly, the tag "brushed off" as a discontinuous MWE in the following text:

``` txt
She brushed the whole thing off.
```

You can use the following MWE template in conjunction with a noun phrase parser which identifies "the whole thing" as a noun phrase:

``` txt
brush*_* {Np} off_*
```

## Default semantic tag

Some MWE templates, currently only in the English MWE lexicon, have the semantic tag `Df`, which stands for default. The `Df` tag is replaced with the single word semantic tag of the token that matched the **first token in the MWE template that starts with a wildcard (`*`)**. For example, given the following MWE template:

``` tsv
mwe_template	semantic_tags
*_ADJ style_NOUN	C1/Df
```

And the following single word lexicon entry:

``` tsv
lemma	pos	semantic_tags
acting	ADJ	A1/Z3
```

The text `The acting style.` would tag `acting style` as a MWE with the semantic tag `C1/A1`.

When replacing the `Df` tag:

* Only the first semantic tag of the single word match is used, and only the first part of it if it is a slash (`/`) tag, e.g. `A1/Z3` becomes `A1`.
* All affixes (e.g. `+` and `-`), lower case markers (e.g. gender markers such as `m` and `f`), and rarity markers (`%` and `@`) are removed from the single word semantic tag.
* Any affixes, lower case markers, and rarity markers on the `Df` tag, which can appear in any order and independently of each other, are added to the replacement in the same order, e.g. `Df++` becomes `A1++`, `Dfc` becomes `A1c`, `Df-m%` becomes `A1-m%`, and `Dfm+` becomes `A1m+`.
* If the token has no single word match, the `Df` tag is replaced with `Z99`.

MWE templates that contain a `Df` tag but no token that starts with a wildcard are ignored, and a warning is raised.

In PyMUSAS the `Df` tag is replaced by the [`MWERule`](/api/taggers/rules/mwe), which requires a `single_word_rule` to find the single word semantic tags. If no `single_word_rule` is given, all `Df` tags are replaced with `Z99`:

``` python
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.single_word import SingleWordRule

single_word_rule = SingleWordRule({'acting|ADJ': ['A1/Z3']}, {})
mwe_rule = MWERule({'*_ADJ style_NOUN': ['C1/Df']}, single_word_rule=single_word_rule)
assert "C1/A1" == mwe_rule(["acting", "style"], ["act", "style"], ["ADJ", "NOUN"])[0][0].semantic_tags[0]
```
