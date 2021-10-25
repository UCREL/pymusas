<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><strong>.tagger</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/tagger.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.spacy_api.tagger.RuleBasedTagger"></a>

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

