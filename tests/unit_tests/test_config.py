from importlib import reload
from pathlib import Path
import tempfile

from pytest import MonkeyPatch

from pymusas import config


def test_cache_home(monkeypatch: MonkeyPatch) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        reload(config)
        home_dir = str(Path.home())
        # Test default home dir
        assert str(Path(f'{home_dir}', '.cache', 'pymusas')) == config.PYMUSAS_CACHE_HOME
        # Test default home dir when the `XDG_CACHE_HOME` environment variable is set.
        monkeypatch.setenv("XDG_CACHE_HOME", str(Path(f'{temp_dir}', '.test_data')))
        reload(config)
        assert str(Path(f'{temp_dir}', '.test_data', 'pymusas')) == config.PYMUSAS_CACHE_HOME
        # Test default home dir when the `PYMUSAS_HOME` environment variable is set.
        monkeypatch.setenv("PYMUSAS_HOME", str(Path(f'{temp_dir}', '.pymusas')))
        reload(config)
        assert str(Path(f'{temp_dir}', '.pymusas')) == config.PYMUSAS_CACHE_HOME
