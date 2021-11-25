<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><i>.taggers</i><strong>.rule_based</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/taggers/rule_based.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.spacy_api.taggers.rule_based.logger"></a>

#### logger

```python
logger = logging.getLogger(__name__)
```

<a id="pymusas.spacy_api.taggers.rule_based.USASRuleBasedTagger"></a>

## USASRuleBasedTagger

```python
class USASRuleBasedTagger:
 | ...
 | def __init__(
 |     self,
 |     lexicon_lookup: Optional[Dict[str, List[str]]] = None,
 |     lemma_lexicon_lookup: Optional[Dict[str, List[str]]] = None,
 |     pos_mapper: Optional[Dict[str, List[str]]] = None,
 |     usas_tags_token_attr: str = 'usas_tags',
 |     pos_attribute: str = 'pos_',
 |     lemma_attribute: str = 'lemma_'
 | ) -> None
```

