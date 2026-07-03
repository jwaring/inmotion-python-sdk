import dataclasses
import re
from unittest.mock import MagicMock, patch

import pytest
import requests

from inmotion.exceptions import InMotionAPIError, InMotionConnectionError
from inmotion.utils import build_im_headers, create_signature, request_json, stringify


@dataclasses.dataclass
class _Sample:
    name: str
    value: int


def test_stringify_dataclass_is_compact_json():
    assert stringify(_Sample(name="a", value=1)) == '{"name":"a","value":1}'


def test_stringify_dict_is_compact_json():
    assert stringify({"b": 2, "a": [1, 2]}) == '{"b":2,"a":[1,2]}'


def test_create_signature_is_deterministic_base64():
    sig1 = create_signature(b"secret", "hello")
    sig2 = create_signature(b"secret", "hello")
    assert sig1 == sig2
    assert create_signature(b"other-secret", "hello") != sig1


def test_build_im_headers_shape_and_date_format():
    headers = build_im_headers(dev_key="devkey", dev_secret="devsecret", content='{"a":1}')

    assert set(headers.keys()) == {"im-content-md5", "im-hmac", "im-request-date"}
    assert headers["im-hmac"].startswith("devkey:")
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", headers["im-request-date"])


def test_build_im_headers_content_md5_changes_with_content():
    h1 = build_im_headers(dev_key="k", dev_secret="s", content="one")
    h2 = build_im_headers(dev_key="k", dev_secret="s", content="two")
    assert h1["im-content-md5"] != h2["im-content-md5"]


def test_build_im_headers_includes_extra_header_when_both_provided():
    headers = build_im_headers(dev_key="k", dev_secret="s", extra_name="X-API-KEY", extra_value="abc123")
    assert headers["X-API-KEY"] == "abc123"


def test_build_im_headers_omits_extra_header_when_only_name_given():
    headers = build_im_headers(dev_key="k", dev_secret="s", extra_name="X-API-KEY", extra_value="")
    assert "X-API-KEY" not in headers


def test_request_json_returns_raw_json_when_no_model():
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"foo": "bar"}
    with patch("inmotion.utils._http_session.post", return_value=mock_response):
        result = request_json("http://example.test/x", {}, "", "error")
    assert result == {"foo": "bar"}


def test_request_json_raises_connection_error_on_network_failure():
    with patch("inmotion.utils._http_session.post", side_effect=requests.ConnectionError("boom")):
        with pytest.raises(InMotionConnectionError, match="unable to reach inMotion"):
            request_json("http://example.test/x", {}, "", "Failed to connect")


def test_request_json_raises_api_error_on_non_2xx_with_server_detail():
    mock_response = MagicMock(status_code=400)
    mock_response.json.return_value = {"error": "bad input"}
    with patch("inmotion.utils._http_session.post", return_value=mock_response):
        with pytest.raises(InMotionAPIError, match="bad input") as exc_info:
            request_json("http://example.test/x", {}, "", "Failed to do thing")
    assert exc_info.value.status_code == 400


def test_request_json_raises_api_error_on_non_2xx_without_json_body():
    mock_response = MagicMock(status_code=500)
    mock_response.json.side_effect = ValueError("not json")
    with patch("inmotion.utils._http_session.post", return_value=mock_response):
        with pytest.raises(InMotionAPIError, match=r"HTTP 500"):
            request_json("http://example.test/x", {}, "", "Failed to do thing")


def test_request_json_raises_api_error_on_malformed_model_response():
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"unexpected": "shape"}

    @dataclasses.dataclass
    class _StrictModel:
        required_field: str

    with patch("inmotion.utils._http_session.post", return_value=mock_response):
        with pytest.raises(InMotionAPIError, match="Malformed response"):
            request_json("http://example.test/x", {}, "", "Failed to load", _StrictModel)
