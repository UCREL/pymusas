from hashlib import sha256
import os
from pathlib import Path
from typing import Union

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

from . import config


def ensure_path(path: Union[str, Path]) -> Path:
    """
    Ensure string is converted to a Path.
    
    This is a more restrictive version of spaCy's [ensure_path](https://github.com/explosion/spaCy/blob/ac05de2c6c708e33ebad6c901e674e1e8bdc0688/spacy/util.py#L358)
    
    # Parameters

    path : `Union[str, Path]`
        If string, it's converted to Path.
    
    # Returns

    `Path`
    """
    if isinstance(path, str):
        return Path(path)
    return path


def _session_with_backoff() -> requests.Session:
    """
    We ran into an issue where http requests to s3 were timing out,
    possibly because we were making too many requests too quickly.
    This helper function returns a requests session that has retry-with-backoff
    built in. See this [Stack Overflow post.](https://stackoverflow.com/questions/23267409/how-to-implement-retry-mechanism-into-python-requests-library>.)
    
    Code reference [AllenNLP](https://github.com/allenai/allennlp/blob/e5d332a592a8624e1f4ee7a9a7d30a90991db83c/allennlp/common/file_utils.py#L510)

    # Returns

    `requests.Session`
    """
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    return session


def _resource_to_filename(resource: str) -> str:
    """
    Converts a `resource` into a hashed filename in a repeatable way.

    Code reference [AllenNLP](https://github.com/allenai/allennlp/blob/e5d332a592a8624e1f4ee7a9a7d30a90991db83c/allennlp/common/file_utils.py#L121)
    
    # Parameters

    resource: `str`
        The filename to be hashed.

    # Returns

    `str`
    """
    resource_bytes = resource.encode("utf-8")
    resource_hash = sha256(resource_bytes)
    filename = resource_hash.hexdigest()

    return filename


def download_url_file(url: str) -> str:
    '''
    Returns a path to the contents download from the `url`.

    This function will first check if the downloaded content already exists
    based on a cached file within the :var:`pymusas.config.PYMUSAS_CACHE_HOME` directory.
    If it does then the cached file path will be returned else the the content
    will be downloaded and cached.

    Code reference [AllenNLP](https://github.com/allenai/allennlp/blob/e5d332a592a8624e1f4ee7a9a7d30a90991db83c/allennlp/common/file_utils.py#L536)

    # Parameters

    url: `str`
        The URL address to the file to be downloaded.
 
    # Returns

    `str`
    '''
    cache_dir = config.PYMUSAS_CACHE_HOME
    os.makedirs(cache_dir, exist_ok=True)
    filename = _resource_to_filename(url)
    download_file_path = Path(cache_dir, filename)
    if download_file_path.exists():
        return str(download_file_path)
    
    with _session_with_backoff() as session:
        req = session.get(url, stream=True, timeout=5)
        req.raise_for_status()
        content_length = req.headers.get("Content-Length")
        total = int(content_length) if content_length is not None else None
        with download_file_path.open('wb') as download_file:
            with tqdm(unit="B", unit_scale=True, total=total, desc="downloading") as progress:
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        progress.update(len(chunk))
                        download_file.write(chunk)
    return str(download_file_path)
