---
title: Autotag Syntax
sidebar_position: 2
---

Some single word lexicon entries are patterns rather than words, e.g. any token ending in `kg` is a measurement, or every punctuation token has the semantic tag `PUNCT`. These pattern entries are not in the single word lexicon files. They are in separate **`autotag`** lexicon files, which in the [Multilingual-USAS GitHub repository](https://github.com/UCREL/Multilingual-USAS) are named `semantic_lexicon_LANG_autotag.tsv`, e.g. `English/semantic_lexicon_en_autotag.tsv`.

An `autotag` file has exactly the same format as a single word lexicon file (`lemma`, `pos`, and `semantic_tags` fields), but its `lemma` and `pos` fields are patterns. In single word lexicon files `*`, `[`, and `]` are always literal, e.g. `2*3`, except for a `pos` value of exactly `*`, which means any POS.

Structure of this documentation page:

1. [Pattern syntax](#pattern-syntax) - the symbols that can be used in an `autotag` pattern.
2. [Matching rules](#matching-rules) - how `autotag` entries are matched to tokens.
3. [Using autotag lexicons in PyMUSAS](#using-autotag-lexicons-in-pymusas).

## Pattern syntax

* `[...]` is a regular expression character class matching exactly one character, e.g. `[0-9]` matches one digit and `[a-z]` one lower case ASCII letter.
* `*` straight after a character class means "zero or more characters from that class", e.g. `[0-9]*ish` matches `9ish` and `10ish`.
* `*` anywhere else means "zero or more of any character", e.g. `*-year-old` matches `10-year-old`. It can appear at any position, not only at the end.
* Within a character class `\[` and `\]` are literal brackets; an unescaped `[` inside a class, or a `]` that does not close a class (e.g. `hello[a-z]]`), is an error.
* Every other character is literal, e.g. `.`, `+`, `?`, and `(`, apart from `[` and `]`, which can only be used as part of a character class.
* A pattern must match the whole token, lemma, or POS tag, not just part of it.

:::warning

`[...]*` also matches **zero** characters, e.g. `[0-9]*ish` matches `ish`. If at least one character from the class is needed, write the class twice, e.g. `[0-9][0-9]*ish`. PyMUSAS applies the pattern as written.

:::

## Matching rules

* **The lemma and POS patterns must both match.** An `autotag` entry only applies to a token when its `lemma` pattern matches the token or lemma, **and** its `pos` pattern matches the token's POS tag. Unlike single word lexicon lookups, there is no match that ignores the POS tag.
* **The `pos` pattern cannot be just `*`**, as this would match any POS tag. A `pos` pattern can still contain `*` alongside other characters, e.g. `N*`. Loading an `autotag` lexicon with an entry whose `pos` is just `*`, or with an invalid pattern, e.g. an unclosed `[` or a `]` that does not close a character class, raises a `ValueError`.
* **Case:** the token, lemma, lower cased token, and lower cased lemma are all matched against the `lemma` pattern, as with single word lexicon lookups. The patterns themselves are not lower cased, so they are case sensitive, e.g. `*MB` matches `10MB` but not `10mb`.
* **Precedence:** a token that matches a single word lexicon entry uses that entry. `autotag` patterns are only tried when there is no single word lexicon match. Multi Word Expression (MWE) matches are also preferred over `autotag` matches.
* **Lexicon order:** if more than one `autotag` entry matches a token, the entry that comes first in the `autotag` lexicon file is used. Put more specific patterns before more general ones, e.g. `*kg` (POS `NUM`) before `*` (POS `NUM`). Lexicon order takes priority over whether the token, lemma, or their lower cased versions matched, e.g. given the entries `*mb` then `*MB` (both with the POS `NOUN`), the token `10MB` is tagged with the `*mb` entry, as it comes first, even though only its lower cased version `10mb` matches `*mb`. Lexicon order also takes priority over the order of the POS tags in a POS mapping. For example, if the token POS tag `CD` is mapped to the lexicon POS tags `noun` and `num` (in that order), and the entries are `*kg` (POS `num`) then `*kg` (POS `noun`), the token `15kg` with the POS tag `CD` matches both entries but is tagged with the `*kg` (POS `num`) entry, as it comes first in the lexicon.
* **Merging `autotag` files:** when `autotag` files are combined with `AutotagLexiconCollection.tsv_merge`, later files take priority over earlier files. The entries of the last file come first, in their file order, followed by the entries of the file before it, and so on. An entry that is in more than one file uses the semantic tags and position from the last file that contains it. For example, merging a published `autotag` file that contains `*` (POS `NUM`) with your own file that contains `*mg` (POS `NUM`), in that order, tags `5mg` with the `*mg` entry.
* `autotag` matches are also used to replace [default (`Df`) semantic tags](/usage/notes/mwe_syntax#default-semantic-tag) in MWE templates, when the token has no single word lexicon match.

:::tip

If you want to customise an `autotag` lexicon, we recommend creating your own `autotag` file, e.g. a copy of the published file that you then edit, rather than merging your changes in with `AutotagLexiconCollection.tsv_merge`. Your own file gives you finer control over the priority order of all of the entries.

:::

### Example

Given the `autotag` lexicon file:

``` tsv
lemma	pos	semantic_tags
*kg	NUM	N3.5
[0-9][0-9]*ish	NUM	N1
*	PUNCT	PUNCT
```

* `15kg` with the POS tag `NUM` is tagged `N3.5`. `15kg` with any other POS tag does not match.
* `10ish` with the POS tag `NUM` is tagged `N1`, but `ish` does not match.
* Any token with the POS tag `PUNCT` is tagged `PUNCT`, unless it matches a single word lexicon entry.

The following entry is **not valid**, because its `pos` pattern is just `*`:

``` tsv
lemma	pos	semantic_tags
*kg	*	N3.5
```

## Using autotag lexicons in PyMUSAS

An `autotag` lexicon is loaded with [`AutotagLexiconCollection.from_tsv`](/api/lexicon_collection#pymusas.lexicon_collection.AutotagLexiconCollection.from_tsv) and given to the [`SingleWordRule`](/api/taggers/rules/single_word) through its `autotag_lexicon_collection` argument:

``` python
from pymusas.lexicon_collection import AutotagLexiconCollection
from pymusas.rankers.lexicon_entry import ContextualRuleBasedRanker
from pymusas.taggers.rule_based import RuleBasedTagger
from pymusas.taggers.rules.single_word import SingleWordRule

autotag_lexicon = AutotagLexiconCollection({'*kg|NUM': ['N3.5'],
                                            '[0-9][0-9]*ish|NUM': ['N1'],
                                            '*|PUNCT': ['PUNCT']}).to_dictionary()
# An `autotag` file would be loaded with:
# autotag_lexicon = AutotagLexiconCollection.from_tsv('semantic_lexicon_en_autotag.tsv')
single_word_rule = SingleWordRule({'!|PUNCT': ['E4.1+']}, {},
                                  autotag_lexicon_collection=autotag_lexicon)
rules = [single_word_rule]
ranker = ContextualRuleBasedRanker(*ContextualRuleBasedRanker.get_construction_arguments(rules))
tagger = RuleBasedTagger(rules, ranker)

tokens = ['15kg', '10ish', 'ish', '!', '?']
pos_tags = ['NUM', 'NUM', 'NUM', 'PUNCT', 'PUNCT']
semantic_tags = [tags for tags, _ in tagger(tokens, tokens, pos_tags)]
assert semantic_tags == [['N3.5'], ['N1'], ['Z99'], ['E4.1+'], ['PUNCT']]
```

In a spaCy config file, use the `pymusas.taggers.rules.SingleWordRule.v2` registered function, which accepts the `autotag_lexicon_collection` argument, and the `pymusas.AutotagLexiconCollection.from_tsv` registered function to load the `autotag` file:

``` cfg
[initialize.components.pymusas_rule_based_tagger.rules]
@misc = "pymusas.taggers.rules.rule_list"

[initialize.components.pymusas_rule_based_tagger.rules.*.single_word_rule]
@misc = "pymusas.taggers.rules.SingleWordRule.v2"

[initialize.components.pymusas_rule_based_tagger.rules.*.single_word_rule.lexicon_collection]
@misc = "pymusas.LexiconCollection.from_tsv"
tsv_file_path = "semantic_lexicon_en.tsv"
include_pos = true

[initialize.components.pymusas_rule_based_tagger.rules.*.single_word_rule.lemma_lexicon_collection]
@misc = "pymusas.LexiconCollection.from_tsv"
tsv_file_path = "semantic_lexicon_en.tsv"
include_pos = false

[initialize.components.pymusas_rule_based_tagger.rules.*.single_word_rule.autotag_lexicon_collection]
@misc = "pymusas.AutotagLexiconCollection.from_tsv"
tsv_file_path = "semantic_lexicon_en_autotag.tsv"

[initialize.components.pymusas_rule_based_tagger.ranker]
@misc = "pymusas.rankers.ContextualRuleBasedRanker.v1"
rules = ${initialize.components.pymusas_rule_based_tagger.rules}
```
