from unittest.mock import patch

import pytest

from inmotion.credentials_client import InMotionCredentialsClient, InMotionCredentialsSession
from inmotion.exceptions import InMotionAuthenticationError
from inmotion.models import AuthenticationSessionModel


def _auth_session(status: str, api_path: str = "/api/v2", requested_version: str = "2.0.0") -> AuthenticationSessionModel:
    return AuthenticationSessionModel(
        token="tok-123",
        copyright="c",
        highestAvailableVersion="2.0.0",
        status=status,
        apiPath=api_path,
        openApiUrl="http://example.test/openapi",
        requestedVersion=requested_version,
        requestedVersionExpiryDate=None,
    )


def _client() -> InMotionCredentialsClient:
    return InMotionCredentialsClient(base_url="http://example.test", dev_key="devkey", dev_secret="devsecret")


def test_connect_active_returns_session_with_token():
    with patch("inmotion.credentials_client.request_json", return_value=_auth_session("active")):
        session = _client().connect("my-account", "user", "pass")

    assert isinstance(session, InMotionCredentialsSession)
    assert session.account == "my-account"
    assert session.is_connected is True


def test_connect_other_status_raises_authentication_error():
    with patch("inmotion.credentials_client.request_json", return_value=_auth_session("revoked")):
        with pytest.raises(InMotionAuthenticationError, match="expired or unavailable"):
            _client().connect("my-account", "user", "pass")


def test_session_build_headers_includes_auth_token_header():
    session = InMotionCredentialsSession("http://example.test", "devkey", "devsecret", "tok-123", "acct", "/api/v2")
    headers = session.build_headers(content="")
    assert headers["X-Auth-Token"] == "tok-123"


def test_session_disconnect_updates_is_connected():
    session = InMotionCredentialsSession("http://example.test", "devkey", "devsecret", "tok-123", "acct", "/api/v2")
    assert session.is_connected is True
    session.disconnect()
    assert session.is_connected is False
