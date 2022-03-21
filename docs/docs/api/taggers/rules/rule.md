<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><i>.rules</i><strong>.rule</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rules/rule.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.rules.rule.Rule"></a>

## Rule

```python
class Rule(ABC)
```

An **abstract class** that defines the basic method, `__call__`, that is
required for all [`Rule`](#rule)s.

A Rule when called, `__call__`, creates a `List` of rules matches for each
token, whereby each rule matched is defined by the
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object. These
rules matches per token can then be, optionally, combined with other rule
matches per token from other [`Rule`](#rule) classes to then be ranked by a
[`pymusas.rankers.lexicon_entry.LexiconEntryRanker`](/pymusas/api/rankers/lexicon_entry/#lexiconentryranker).

<a id="pymusas.taggers.rules.rule.Rule.__call__"></a>

### \_\_call\_\_

```python
class Rule(ABC):
 | ...
 | @abstractmethod
 | def __call__(
 |     self,
 |     tokens: List[str],
 |     lemmas: List[str],
 |     pos_tags: List[str]
 | ) -> List[List[RankingMetaData]]
```

For each token it returns a `List` of rules matches defined by the
[`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object.

Each `List` of `tokens`, `lemmas`, and `pos_tags` are assumed to be of
equal length.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `List[str]` <br/>
    The tokens that are within the text.
- __lemmas__ : `List[str]` <br/>
    The lemmas of the tokens.
- __pos\_tags__ : `List[str]` <br/>
    The Part Of Speech tags of the tokens.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `List[List[RankingMetaData]]` <br/>

<a id="pymusas.taggers.rules.rule.Rule.to_bytes"></a>

### to\_bytes

```python
class Rule(ABC):
 | ...
 | @abstractmethod
 | def to_bytes() -> bytes
```

Serialises the [`Rule`](#rule) to a bytestring.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.taggers.rules.rule.Rule.from_bytes"></a>

### from\_bytes

```python
class Rule(ABC):
 | ...
 | @staticmethod
 | @abstractmethod
 | def from_bytes(bytes_data: bytes) -> "Rule"
```

Loads [`Rule`](#rule) from the given bytestring and returns it.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`Rule`](#rule) <br/>

