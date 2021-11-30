<div className="source-div">
 <p><i>pymusas</i><strong>.file_utils</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/file_utils.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.file_utils.ensure_path"></a>

### ensure\_path

```python
def ensure_path(path: Union[str, Path]) -> Path
```

Ensure string is converted to a Path.

This is a more restrictive version of spaCy's [ensure_path](https://github.com/explosion/spaCy/blob/ac05de2c6c708e33ebad6c901e674e1e8bdc0688/spacy/util.py#L358)

<h4 id="ensure_path.parameters">Parameters<a className="headerlink" href="#ensure_path.parameters" title="Permanent link">&para;</a></h4>


- __path__ : `Union[str, Path]` <br/>
    If string, it's converted to Path.

<h4 id="ensure_path.returns">Returns<a className="headerlink" href="#ensure_path.returns" title="Permanent link">&para;</a></h4>


- `Path` <br/>

<a id="pymusas.file_utils.download_url_file"></a>

### download\_url\_file

```python
def download_url_file(url: str) -> str
```

Returns a path to the contents download from the `url`.

This function will first check if the downloaded content already exists
based on a cached file within the [`pymusas.config.PYMUSAS_CACHE_HOME`](/pymusas/api/config/#pymusas_cache_home) directory.
If it does then the cached file path will be returned else the the content
will be downloaded and cached.

Code reference [AllenNLP](https://github.com/allenai/allennlp/blob/e5d332a592a8624e1f4ee7a9a7d30a90991db83c/allennlp/common/file_utils.py#L536)

<h4 id="download_url_file.parameters">Parameters<a className="headerlink" href="#download_url_file.parameters" title="Permanent link">&para;</a></h4>


- __url__ : `str` <br/>
    The URL address to the file to be downloaded.

<h4 id="download_url_file.returns">Returns<a className="headerlink" href="#download_url_file.returns" title="Permanent link">&para;</a></h4>


- `str` <br/>

