<div className="source-div">
 <p><i>pymusas</i><strong>.config</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/config.py">[SOURCE]</a></p>
</div>
<div></div>

---

This module has various attributes, of which the most important of these
are listed below:

<h4 id="pymusas.config.attributes">Attributes<a className="headerlink" href="#pymusas.config.attributes" title="Permanent link">&para;</a></h4>


- __PYMUSAS\_CACHE\_HOME__ : `str` <br/>
       The directory that by default we store any downloaded data too. This
       attribute by default is set to `~/.cache/pymusas`. This attribute can be
       set through the `PYMUSAS_HOME` environment variable.

The creation of the `PYMUSAS_CACHE_HOME` attribute and how to set a default value
for it came from the [HuggingFace Datasets codebase
(reference to their code)](https://github.com/huggingface/datasets/blob/d488db2f64f312f88f72bbc57a09b7eddb329182/src/datasets/config.py#L130).

<a id="pymusas.config.DEFAULT_XDG_CACHE_HOME"></a>

#### DEFAULT\_XDG\_CACHE\_HOME

```python
DEFAULT_XDG_CACHE_HOME: str = os.path.join(os.path.expanduser('~'), '.cache')
```

<a id="pymusas.config.XDG_CACHE_HOME"></a>

#### XDG\_CACHE\_HOME

```python
XDG_CACHE_HOME: str = os.getenv("XDG_CACHE_HOME", DEFAULT_XDG_CACHE_HOME)
```

<a id="pymusas.config.DEFAULT_PYMUSAS_CACHE_HOME"></a>

#### DEFAULT\_PYMUSAS\_CACHE\_HOME

```python
DEFAULT_PYMUSAS_CACHE_HOME: str = os.path.join(XDG_CACHE_HOME, "pymusas")
```

<a id="pymusas.config.PYMUSAS_CACHE_HOME"></a>

#### PYMUSAS\_CACHE\_HOME

```python
PYMUSAS_CACHE_HOME: str = os.path.expanduser(os.getenv("PYMUSAS_HOME", DEFAULT_PYMUSAS_CACHE_HOME))
```

<a id="pymusas.config.LANG_LEXICON_RESOUCRE_MAPPER"></a>

#### LANG\_LEXICON\_RESOUCRE\_MAPPER

```python
LANG_LEXICON_RESOUCRE_MAPPER = {
    'fr': {'lexicon': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/sem ...
```

