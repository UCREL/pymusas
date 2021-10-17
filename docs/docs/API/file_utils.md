<div>
 <p className="alignleft"><i>pymusas</i><strong>.file_utils</strong></p>
 <p className="alignright"><a className="sourcelink" href="https://github.com/allenai/allennlp/blob/main/allennlp/file_utils.py">[SOURCE]</a></p>
</div>
<div></div>

---

<a id="pymusas.file_utils.download_url_file"></a>

### download\_url\_file

```python
def download_url_file(url: str) -> str
```

Reference AllenNLP:
https://github.com/allenai/allennlp/blob/e5d332a592a8624e1f4ee7a9a7d30a90991db83c/allennlp/common/file_utils.py#L536

This function will first check if the downloaded content already exists
based on a cached file within the `config.PYMUSAS_CACHE_HOME` directory.
If it does then the cached file path will be returned else the the content
will be downloaded and cached.

**Returns**:

A path to the contents download from the `url`.

