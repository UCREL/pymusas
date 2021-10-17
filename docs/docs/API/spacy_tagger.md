<div>
 <p className="alignleft"><i>pymusas</i><strong>.spacy_tagger</strong></p>
 <p className="alignright"><a className="sourcelink" href="https://github.com/allenai/allennlp/blob/main/allennlp/spacy_tagger.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.spacy_tagger.RuleBasedTagger"></a>

## RuleBasedTagger

```python
class RuleBasedTagger:
 | ...
 | def __init__(
 |     self,
 |     nlp: Language,
 |     lexicon_lookup: Optional[Dict[str, List[str]]] = None,
 |     lexicon_lemma_lookup: Optional[Dict[str, List[str]]] = None,
 |     usas_tags_token_attr: str = 'usas_tags'
 | ) -> None
```

