from importlib import reload
import os
from pathlib import Path
import tempfile

from pymusas import config

def test_cache_home() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        home_dir = str(Path.home())
        # Test default home dir
        assert f'{home_dir}/.cache/pymusas' == config.PYMUSAS_CACHE_HOME
        # Test default home dir when the `XDG_CACHE_HOME` environment variable is set.
        os.environ["XDG_CACHE_HOME"] = f'{temp_dir}/.test_data'
        reload(config)
        assert f'{temp_dir}/.test_data/pymusas' == config.PYMUSAS_CACHE_HOME
        # Test default home dir when the `PYMUSAS_HOME` environment variable is set.
        os.environ["PYMUSAS_HOME"] = f'{temp_dir}/.pymusas'
        reload(config)
        assert f'{temp_dir}/.pymusas' == config.PYMUSAS_CACHE_HOME
