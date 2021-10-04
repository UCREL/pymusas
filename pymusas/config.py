import os

# Cache location
# Reference HuggingFace Datasets: 
# https://github.com/huggingface/datasets/blob/d488db2f64f312f88f72bbc57a09b7eddb329182/src/datasets/config.py#L130
DEFAULT_XDG_CACHE_HOME = os.path.join(os.path.expanduser('~'), '.cache')
XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", DEFAULT_XDG_CACHE_HOME)
DEFAULT_PYMUSAS_CACHE_HOME = os.path.join(XDG_CACHE_HOME, "pymusas")
PYMUSAS_CACHE_HOME = os.path.expanduser(os.getenv("PYMUSAS_HOME", DEFAULT_PYMUSAS_CACHE_HOME))

LANG_LEXICON_RESOUCRE_MAPPER = {
    'fr' : {'lexicon': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.usas',
            'lexicon_lemma': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/French/semantic_lexicon_fr.usas'},
    'nl' : {'lexicon': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Dutch/semantic_lexicon_dut.usas',
            'lexicon_lemma': 'https://raw.githubusercontent.com/UCREL/Multilingual-USAS/master/Dutch/semantic_lexicon_dut.usas'}
}