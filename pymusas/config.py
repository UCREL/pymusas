'''
This module has various attributes, of which the most important of these
are listed below:

# Attributes

PYMUSAS_CACHE_HOME: `str`
       The directory that by default we store any downloaded data too. This
       attribute by default is set to `~/.cache/pymusas`. This attribute can be
       set through the `PYMUSAS_HOME` environment variable.

The creation of the `PYMUSAS_CACHE_HOME` attribute and how to set a default value
for it came from the [HuggingFace Datasets codebase
(reference to their code)](https://github.com/huggingface/datasets/blob/d488db2f64f312f88f72bbc57a09b7eddb329182/src/datasets/config.py#L130).
'''
import os


DEFAULT_XDG_CACHE_HOME: str = os.path.join(os.path.expanduser('~'), '.cache')
XDG_CACHE_HOME: str = os.getenv("XDG_CACHE_HOME", DEFAULT_XDG_CACHE_HOME)
DEFAULT_PYMUSAS_CACHE_HOME: str = os.path.join(XDG_CACHE_HOME, "pymusas")
PYMUSAS_CACHE_HOME: str = os.path.expanduser(os.getenv("PYMUSAS_HOME", DEFAULT_PYMUSAS_CACHE_HOME))

LANG_LEXICON_RESOUCRE_MAPPER = {
    'fr': {'lexicon': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.usas',
           'lexicon_lemma': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.usas'},
    'nl': {'lexicon': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Dutch/semantic_lexicon_dut.usas',
           'lexicon_lemma': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Dutch/semantic_lexicon_dut.usas'}
}
