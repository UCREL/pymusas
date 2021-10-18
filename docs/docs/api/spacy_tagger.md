<div className="source-div">
 <p><i>pymusas</i><strong>.spacy_tagger</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_tagger.py">[SOURCE]</a></p>
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

