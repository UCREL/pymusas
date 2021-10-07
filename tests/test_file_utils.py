import importlib
import os
import tempfile

import responses
import requests
import pytest

from pymusas import config
from pymusas import file_utils

DOWNLOAD_URL = 'https://ucrel-web.lancs.ac.uk/usas/semtags.txt'
EXPECTED_RESPONSE = 'Hello World\nPymusas'

def test_download_url_file() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['PYMUSAS_HOME'] = temp_dir
        importlib.reload(config)
        
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, DOWNLOAD_URL, status=500)
            with pytest.raises(requests.exceptions.HTTPError):
                _ = file_utils.download_url_file(DOWNLOAD_URL)
        
        cached_file_path = ''
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, DOWNLOAD_URL, status=200, 
                     body=EXPECTED_RESPONSE, stream=True)
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


