<div className="source-div">
 <p><i>pymusas</i><i>.taggers</i><i>.rules</i><strong>.mwe</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/taggers/rules/mwe.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.taggers.rules.mwe.MWERule"></a>

## MWERule

```python
class MWERule(Rule):
 | ...
 | def __init__(
 |     self,
 |     mwe_lexicon_lookup: dict[str, list[str]],
 |     pos_mapper: dict[str, list[str]] | None = None,
 |     single_word_rule: SingleWordRule | None = None
 | ) -> None
```

A Multi Word Expression (MWE) rule match can be one of the following matches:

1. `MWE_NON_SPECIAL` match - whereby the combined token/lemma and POS
is found within the given MWE Lexicon Collection (`self.mwe_lexicon_collection`).
2. `MWE_WILDCARD` match - whereby the combined token/lemma and POS matches
a wildcard MWE template that is within the MWE Lexicon Collection
(`self.mwe_lexicon_collection`).

All rule matches use the
`pymusas.lexicon_collection.MWELexiconCollection.mwe_match`
method for matching. Matches are found based on the original token/lemma and
lower cased versions of the token/lemma.

**Default (`Df`) semantic tags**

A MWE template can contain a default (`Df`) semantic tag, e.g. the
template `*_ADJ style_NOUN` with the semantic tags `C1/Df`. The `Df` tag is
replaced with the single word semantic tag of the token that matched the
first token in the MWE template that starts with a wildcard (`*`), in
this example the adjective. The single word semantic tag is found using the
`single_word_rule`, whereby the best single word match is found using
the [`pymusas.taggers.rules.single_word.best_match`](/pymusas/api/taggers/rules/single_word/#best_match) method of
[`pymusas.taggers.rules.single_word.SingleWordRule`](/pymusas/api/taggers/rules/single_word/#singlewordrule). From
this single word match the first semantic tag is used, and of that
semantic tag only the first part of any slash tag, with all affixes and
lower case markers removed, e.g. `A1+/Z3` becomes `A1`. Any affixes and
lower case markers on the `Df` tag are added to it, e.g. `Df++` becomes
`A1++`. For more details see [`pymusas.utils.resolve_default_tags`](/pymusas/api/utils/#resolve_default_tags).

If the `single_word_rule` is `None` or the token has no single word match
then the `Df` tag is replaced with `Z99`.

<h4 id="mwerule.parameters">Parameters<a className="headerlink" href="#mwerule.parameters" title="Permanent link">&para;</a></h4>


- __mwe\_lexicon\_lookup__ : `dict[str, list[str]]` <br/>
    The data to create `mwe_lexicon_collection` instance attribute. A
    Dictionary where the keys are MWE templates, of any
    [`pymusas.lexicon_collection.LexiconType`](/pymusas/api/lexicon_collection/#lexicontype),
    and the values are a list of associated semantic tags.
- __pos\_mapper__ : `dict[str, list[str]]`, optional (default = `None`) <br/>
    If not `None`, maps from the `mwe_lexicon_lookup` POS tagset to the
    desired POS tagset,whereby the mapping is a `list` of tags,
    at the moment there is no preference order in this list of POS tags.
    **Note** the longer the `list[str]` for
    each POS mapping the slower the tagger, a one to one mapping will have
    no speed impact on the tagger. A selection of POS mappers can be found in
    [`pymusas.pos_mapper`](/pymusas/api/pos_mapper).
- __single\_word\_rule__ : `pymusas.taggers.rules.single_word.SingleWordRule`, optional (default = `None`) <br/>
    The single word rule used to find the semantic tags that replace
    default (`Df`) semantic tags, see the default semantic tags section
    above. If `None` all `Df` tags will be replaced with `Z99`.

<h4 id="mwerule.instance_attributes">Instance Attributes<a className="headerlink" href="#mwerule.instance_attributes" title="Permanent link">&para;</a></h4>


- __mwe\_lexicon\_collection__ : `pymusas.lexicon_collection.MWELexiconCollection` <br/>
    A [`pymusas.lexicon_collection.MWELexiconCollection`](/pymusas/api/lexicon_collection/#mwelexiconcollection) instance that
    has been initialised using the `mwe_lexicon_lookup` and `pos_mapper`
    parameters. This collection is used to find MWE rule matches.
- __single\_word\_rule__ : `pymusas.taggers.rules.single_word.SingleWordRule`, optional (default = `None`) <br/>
    The given `single_word_rule`.

<h4 id="mwerule.examples">Examples<a className="headerlink" href="#mwerule.examples" title="Permanent link">&para;</a></h4>

``` python
from pymusas.taggers.rules.mwe import MWERule
from pymusas.taggers.rules.single_word import SingleWordRule
single_word_rule = SingleWordRule({'acting|ADJ': ['A1/Z3']}, {})
mwe_rule = MWERule({'*_ADJ style_NOUN': ['C1/Df']},
                   single_word_rule=single_word_rule)
ranking_meta_data = mwe_rule(['The', 'acting', 'style'],
                             ['the', 'acting', 'style'],
                             ['DET', 'ADJ', 'NOUN'])
assert ('C1/A1',) == ranking_meta_data[1][0].semantic_tags
```

<a id="pymusas.taggers.rules.mwe.MWERule.__call__"></a>

### \_\_call\_\_

```python
class MWERule(Rule):
 | ...
 | def __call__(
 |     self,
 |     tokens: list[str],
 |     lemmas: list[str],
 |     pos_tags: list[str]
 | ) -> list[list[RankingMetaData]]
```

Given the tokens, lemmas, and POS tags for each word in a text,
it returns for each token a `list` of rules matches defined by
the [`pymusas.rankers.ranking_meta_data.RankingMetaData`](/pymusas/api/rankers/ranking_meta_data/#rankingmetadata) object based on
the rule matches stated in the class docstring above.

<h4 id="__call__.parameters">Parameters<a className="headerlink" href="#__call__.parameters" title="Permanent link">&para;</a></h4>


- __tokens__ : `list[str]` <br/>
    The tokens that are within the text.
- __lemmas__ : `list[str]` <br/>
    The lemmas of the tokens.
- __pos\_tags__ : `list[str]` <br/>
    The Part Of Speech tags of the tokens.

<h4 id="__call__.returns">Returns<a className="headerlink" href="#__call__.returns" title="Permanent link">&para;</a></h4>


- `list[list[RankingMetaData]]` <br/>

<a id="pymusas.taggers.rules.mwe.MWERule.to_bytes"></a>

### to\_bytes

```python
class MWERule(Rule):
 | ...
 | def to_bytes() -> bytes
```

Serialises the [`MWERule`](#mwerule) to a bytestring.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.taggers.rules.mwe.MWERule.from_bytes"></a>

### from\_bytes

```python
class MWERule(Rule):
 | ...
 | @staticmethod
 | def from_bytes(bytes_data: bytes) -> "MWERule"
```

Loads [`MWERule`](#mwerule) from the given bytestring and returns it.

Bytestrings created before the `single_word_rule` was added, which
only contain the serialised `mwe_lexicon_collection`, can also be
loaded.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`MWERule`](#mwerule) <br/>

<a id="pymusas.taggers.rules.mwe.MWERule.__eq__"></a>

### \_\_eq\_\_

```python
class MWERule(Rule):
 | ...
 | def __eq__(other: object) -> bool
```

Given another object to compare too it will return `True` if the other
object is the same class and initialised using with the same argument
values.

<h4 id="__eq__.parameters">Parameters<a className="headerlink" href="#__eq__.parameters" title="Permanent link">&para;</a></h4>


- __other__ : `object` <br/>
    The object to compare too.

<h4 id="__eq__.returns">Returns<a className="headerlink" href="#__eq__.returns" title="Permanent link">&para;</a></h4>


- `True` <br/>

