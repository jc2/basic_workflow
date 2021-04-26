import json
from unittest.mock import patch

import pytest
import requests

from clients.currconv import convert, CorrConvError


@patch('clients.currconv.requests.get')
def test_convertmock_get(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 200
    mock_resp._content = json.dumps({"USD_COP": 12345}).encode()
    mock_get.return_value = mock_resp

    response = convert("usd", "cop")
    assert response == 12345


@patch('clients.currconv.requests.get')
def test_convertmock_get_400(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 400
    mock_get.return_value = mock_resp

    with pytest.raises(CorrConvError):
        convert("usd", "cop")


@patch('clients.currconv.requests.get')
def test_convertmock_get_500(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 500
    mock_get.return_value = mock_resp

    with pytest.raises(CorrConvError):
        convert("usd", "cop")


@patch('clients.currconv.requests.get')
def test_convertmock_get_badbody(mock_get):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 200
    mock_resp._content = "Hello :)".encode()
    mock_get.return_value = mock_resp

    with pytest.raises(CorrConvError):
        convert("usd", "cop")
