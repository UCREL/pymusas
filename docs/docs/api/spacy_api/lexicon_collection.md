<div className="source-div">
 <p><i>pymusas</i><i>.spacy_api</i><strong>.lexicon_collection</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/spacy_api/lexicon_collection.py">[SOURCE]</a></p>
</div>
<div></div>

---

spaCy registered functions for reading in a
[`pymusas.lexicon_collection.LexiconCollection`](/pymusas/api/lexicon_collection/#lexiconcollection),
[`pymusas.lexicon_collection.MWELexiconCollection`](/pymusas/api/lexicon_collection/#mwelexiconcollection), or
[`pymusas.lexicon_collection.AutotagLexiconCollection`](/pymusas/api/lexicon_collection/#autotaglexiconcollection) from a TSV file.

<a id="pymusas.spacy_api.lexicon_collection.lexicon_collection_from_tsv"></a>

### lexicon\_collection\_from\_tsv

```python
@spacy.util.registry.misc('pymusas.LexiconCollection.from_tsv')
def lexicon_collection_from_tsv(
    tsv_file_path: PathLike | str,
    include_pos: bool = True
) -> dict[str, list[str]]
```

`pymusas.LexiconCollection.from_tsv` is a registered function under the
`@misc` function register. Given a `tsv_file_path` it will return a
dictionary object that can be used to create a
[`pymusas.lexicon_collection.LexiconCollection`](/pymusas/api/lexicon_collection/#lexiconcollection).

<h4 id="lexicon_collection_from_tsv.parameters">Parameters<a className="headerlink" href="#lexicon_collection_from_tsv.parameters" title="Permanent link">&para;</a></h4>


- __tsv\_file\_path__ : `PathLike | str` <br/>
    A file path or URL to a TSV file that contains at least two
    fields, with an optional third, with the following headings:

    1. `lemma`,
    2. `semantic_tags`
    3. `pos` (Optional)

    All other fields will be ignored.
- __include\_pos__ : `bool`, optional (default = `True`) <br/>
    Whether to include the POS information, if the information is available,
    or not. See [`pymusas.lexicon_collection.add_lexicon_entry`](/pymusas/api/lexicon_collection/#add_lexicon_entry)
    for more information on this parameter.

<h4 id="lexicon_collection_from_tsv.returns">Returns<a className="headerlink" href="#lexicon_collection_from_tsv.returns" title="Permanent link">&para;</a></h4>


- `dict[str, list[str]]` <br/>

<a id="pymusas.spacy_api.lexicon_collection.mwe_lexicon_collection_from_tsv"></a>

### mwe\_lexicon\_collection\_from\_tsv

```python
@spacy.util.registry.misc('pymusas.MWELexiconCollection.from_tsv')
def mwe_lexicon_collection_from_tsv(
    tsv_file_path: PathLike | str
) -> dict[str, list[str]]
```

`pymusas.MWELexiconCollection.from_tsv` is a registered function under the
`@misc` function register. Given a `tsv_file_path` it will return a
dictionary object that can be used to create a
[`pymusas.lexicon_collection.MWELexiconCollection`](/pymusas/api/lexicon_collection/#mwelexiconcollection).

<h4 id="mwe_lexicon_collection_from_tsv.parameters">Parameters<a className="headerlink" href="#mwe_lexicon_collection_from_tsv.parameters" title="Permanent link">&para;</a></h4>


- __tsv\_file\_path__ : `PathLike | str` <br/>
    A file path or URL to a TSV file that contains at least these two
    fields:

    1. `mwe_template`,
    2. `semantic_tags`

    All other fields will be ignored.

<h4 id="mwe_lexicon_collection_from_tsv.returns">Returns<a className="headerlink" href="#mwe_lexicon_collection_from_tsv.returns" title="Permanent link">&para;</a></h4>


- `dict[str, list[str]]` <br/>

<a id="pymusas.spacy_api.lexicon_collection.autotag_lexicon_collection_from_tsv"></a>

### autotag\_lexicon\_collection\_from\_tsv

```python
@spacy.util.registry.misc('pymusas.AutotagLexiconCollection.from_tsv')
def autotag_lexicon_collection_from_tsv(
    tsv_file_path: PathLike | str
) -> dict[str, list[str]]
```

`pymusas.AutotagLexiconCollection.from_tsv` is a registered function under
the `@misc` function register. Given a `tsv_file_path` to an `autotag`
lexicon file it will return a dictionary object that can be used to create
a [`pymusas.lexicon_collection.AutotagLexiconCollection`](/pymusas/api/lexicon_collection/#autotaglexiconcollection).

<h4 id="autotag_lexicon_collection_from_tsv.parameters">Parameters<a className="headerlink" href="#autotag_lexicon_collection_from_tsv.parameters" title="Permanent link">&para;</a></h4>


- __tsv\_file\_path__ : `PathLike | str` <br/>
    A file path or URL to a TSV file that contains at least these three
    fields:

    1. `lemma`,
    2. `pos`,
    3. `semantic_tags`

    All other fields will be ignored.

<h4 id="autotag_lexicon_collection_from_tsv.returns">Returns<a className="headerlink" href="#autotag_lexicon_collection_from_tsv.returns" title="Permanent link">&para;</a></h4>


- `dict[str, list[str]]` <br/>

<h4 id="autotag_lexicon_collection_from_tsv.raises">Raises<a className="headerlink" href="#autotag_lexicon_collection_from_tsv.raises" title="Permanent link">&para;</a></h4>


- `ValueError` <br/>
    See the `from_tsv` method of [`pymusas.lexicon_collection.AutotagLexiconCollection`](/pymusas/api/lexicon_collection/#autotaglexiconcollection).

