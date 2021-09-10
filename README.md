# PymUSAS

PYthon Multilingual Ucrel Semantic Analysis System


## Resources

1. [Multilingual USAS lexicons](https://github.com/UCREL/Multilingual-USAS)
2. [Welsh Semantic Tagger, Java version.](https://github.com/CorCenCC/CySemTagger)
3. [Welsh gold standard dataset](https://github.com/CorCenCC/welsh_pos_sem_tagger/blob/master/data/cy_both_tagged.data), this dataset uses the basic POS tags, see appendix A1 of this [paper](https://aclanthology.org/W19-4332.pdf), from the [CyTag](https://github.com/CorCenCC/CyTag) POS tagger.
4. [Mapping basic CyTag POS tags to core POS tags used by the USAS lexicon.](./resources/basic_cy_tags_to_core_tags.json)

## Semantic Lexicon

In the [single word semantic lexicon for Welsh](https://github.com/UCREL/Multilingual-USAS/blob/master/Welsh/semantic_lexicon_cy.usas), some of the lemmas are not lower cased, of which all of these are a type of noun. Some of these names are multi word expression but with a `_` to combine the two words together, in total across all POS tags there are 94 of these, a good example is for the word `Friday` which in the lexicon is `dydd_Gwener`.