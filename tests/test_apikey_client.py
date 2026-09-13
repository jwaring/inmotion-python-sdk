from unittest.mock import patch

import pytest

from inmotion.apikey_client import InMotionAPIKeyClient, InMotionAPIKeySession
from inmotion.exceptions import InMotionAuthenticationError
from inmotion.models import APICapabilitiesModel


def _capabilities(status: str, api_path: str = "/api/v2", requested_version: str = "2.0.0") -> APICapabilitiesModel:
    return APICapabilitiesModel(
        copyright="c",
        highestAvailableVersion="2.0.0",
        status=status,
        apiPath=api_path,
        openApiUrl="http://example.test/openapi",
        requestedVersion=requested_version,
    )


def _client() -> InMotionAPIKeyClient:
    return InMotionAPIKeyClient(
        base_url="http://example.test",
        dev_key="devkey",
        dev_secret="devsecret",
        api_key="apikey123",
    )


def test_get_session_active_returns_session_with_discovered_api_path():
    with patch("inmotion.apikey_client.request_json", return_value=_capabilities("active", api_path="/api/discovered")):
        session = _client().get_session("my-account")

    assert isinstance(session, InMotionAPIKeySession)
    assert session.api_path == "/api/discovered"
    assert session.account == "my-account"
    assert session.is_connected is True


def test_get_session_expiring_still_returns_session():
    with patch("inmotion.apikey_client.request_json", return_value=_capabilities("expiring")):
        session = _client().get_session("my-account")
    assert isinstance(session, InMotionAPIKeySession)


def test_get_session_other_status_raises_authentication_error():
    with patch("inmotion.apikey_client.request_json", return_value=_capabilities("expired")):
        with pytest.raises(InMotionAuthenticationError, match="expired or unavailable"):
            _client().get_session("my-account")


def test_session_build_headers_includes_api_key_header():
    session = InMotionAPIKeySession("http://example.test", "devkey", "devsecret", "apikey123", "acct", "/api/v2")
    headers = session.build_headers(content="")
    assert headers["X-API-KEY"] == "apikey123"
