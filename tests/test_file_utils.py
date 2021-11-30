import importlib
import os
from pathlib import Path
import tempfile

import pytest
import requests
import responses

from pymusas import config, file_utils


DOWNLOAD_URL = 'https://ucrel-web.lancs.ac.uk/usas/semtags.txt'
EXPECTED_RESPONSE = 'Hello World\nPymusas'


def test_ensure_path() -> None:
    # Test Path type as input
    test_path = Path(__file__)
    assert test_path == file_utils.ensure_path(test_path)
    # Test str type as input
    assert Path(__file__) == file_utils.ensure_path(__file__)


@pytest.mark.parametrize('dir_exists', [True, False])
def test_download_url_file(dir_exists: bool) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        if not dir_exists:
            temp_dir = os.path.join(temp_dir, 'temp_dir')
        os.environ['PYMUSAS_HOME'] = temp_dir
        importlib.reload(config)
        
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, DOWNLOAD_URL, status=500)
            with pytest.raises(requests.exceptions.HTTPError):
                _ = file_utils.download_url_file(DOWNLOAD_URL)
        
        cached_file_path = ''
        with responses.RequestsMock() as rsps:
            req_kwargs = {"stream": True}
            rsps.add(responses.GET, DOWNLOAD_URL, status=200,
                     body=EXPECTED_RESPONSE,
                     match=[responses.matchers.request_kwargs_matcher(req_kwargs)])
            cached_file_path = file_utils.download_url_file(DOWNLOAD_URL)
        assert cached_file_path != ''

        # responses will raise an AssertionError if a request was not called
        # which in this case is what we want as it should be using a cached file
        with pytest.raises(AssertionError):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, DOWNLOAD_URL, status=500)
                expected_cached_file_path = file_utils.download_url_file(DOWNLOAD_URL)
                assert cached_file_path == expected_cached_file_path
        
        with open(cached_file_path, 'r') as cached_response:
            expected_response_lines = EXPECTED_RESPONSE.split('\n')
            cached_lines = []
            for line in cached_response:
                cached_lines.append(line)
            assert len(expected_response_lines) == len(cached_lines)
            for expected_line, cached_line in zip(expected_response_lines, cached_lines):
                assert expected_line == cached_line.rstrip('\n')
