from unittest.mock import MagicMock, patch

import pytest

from inmotion.credentials_client import InMotionCredentialsClient, InMotionCredentialsSession
from inmotion.exceptions import InMotionAuthenticationError


def _auth_session(status: str, api_path: str = "/api/v2", requested_version: str = "2.0.0") -> dict:
    """A raw JSON dict, matching what request_json(model=None) actually returns - get_session
    inspects this dict for 'mfaPending' before loading it as an AuthenticationSessionModel, so it
    can't be mocked as an already-loaded model instance."""
    return {
        "token": "tok-123",
        "copyright": "c",
        "highestAvailableVersion": "2.0.0",
        "status": status,
        "apiPath": api_path,
        "openApiUrl": "http://example.test/openapi",
        "requestedVersion": requested_version,
        "requestedVersionExpiryDate": None,
    }


def _client() -> InMotionCredentialsClient:
    return InMotionCredentialsClient(base_url="http://example.test", dev_key="devkey", dev_secret="devsecret")


def test_get_session_active_returns_session_with_token():
    with patch("inmotion.credentials_client.request_json", return_value=_auth_session("active")) as mock_request_json:
        session = _client().get_session("my-account", "user", "pass")

    assert isinstance(session, InMotionCredentialsSession)
    assert session.account == "my-account"
    assert session.is_connected is True
    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/latest/authenticate"


def test_get_session_accepts_expiry_and_device_trust_fields():
    raw = {**_auth_session("active"), "expiresInSeconds": 1800, "deviceTrustToken": "trust-1"}
    with patch("inmotion.credentials_client.request_json", return_value=raw) as mock_request_json:
        session = _client().get_session("my-account", "user", "pass")

    assert session.is_connected is True
    assert '"requiredApiVersion"' in mock_request_json.call_args.args[3]


def test_get_session_other_status_raises_authentication_error():
    with patch("inmotion.credentials_client.request_json", return_value=_auth_session("revoked")):
        with pytest.raises(InMotionAuthenticationError, match="expired or unavailable"):
            _client().get_session("my-account", "user", "pass")


def test_session_build_headers_includes_auth_token_header():
    session = InMotionCredentialsSession("http://example.test", "devkey", "devsecret", "tok-123", "acct", "/api/v2")
    headers = session.build_headers(content="")
    assert headers["X-Auth-Token"] == "tok-123"


def test_session_disconnect_updates_is_connected():
    session = InMotionCredentialsSession("http://example.test", "devkey", "devsecret", "tok-123", "acct", "/api/v2")
    assert session.is_connected is True
    session.disconnect()
    assert session.is_connected is False


def test_switch_mfa_method_posts_method_with_the_pending_token():
    with patch("inmotion.credentials_client.request_json", return_value=MagicMock()) as mock_request_json:
        _client().switch_mfa_method("pending-tok", "EMAIL")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/latest/authenticate/mfa/switch"
    assert mock_request_json.call_args.args[2]["X-Auth-Token"] == "pending-tok"
    assert mock_request_json.call_args.args[3] == '{"method":"EMAIL"}'


def test_get_session_ignores_fields_the_sdk_does_not_know():
    raw = {**_auth_session("active"), "someFutureField": {"nested": 1}}
    with patch("inmotion.credentials_client.request_json", return_value=raw):
        assert _client().get_session("my-account", "user", "pass").is_connected is True


def test_disconnect_logs_out_with_the_session_token():
    session = InMotionCredentialsSession("http://example.test", "devkey", "devsecret", "tok-123", "acct", "/api/v2")
    with patch("inmotion.credentials_client.request_json", return_value=MagicMock()) as mock_request_json:
        session.disconnect()
        session.disconnect()

    assert mock_request_json.call_count == 1
    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/latest/authenticate/logout"
    assert mock_request_json.call_args.args[2]["X-Auth-Token"] == "tok-123"
    assert session.is_connected is False


def test_disconnect_closes_locally_when_the_server_cannot_be_reached():
    from inmotion.exceptions import InMotionConnectionError
    session = InMotionCredentialsSession("http://example.test", "devkey", "devsecret", "tok-123", "acct", "/api/v2")
    with patch("inmotion.credentials_client.request_json", side_effect=InMotionConnectionError("down")):
        session.disconnect()
    assert session.is_connected is False


@pytest.mark.parametrize("method,step", [("complete_mfa_enrollment", "complete"), ("skip_mfa_enrollment", "skip")])
def test_mfa_enrollment_exchanges_the_enroll_token_for_a_session(method, step):
    from inmotion.models import AuthenticationSessionModel
    session_model = AuthenticationSessionModel(**_auth_session("active"))
    with patch("inmotion.credentials_client.request_json", return_value=session_model) as mock_request_json:
        session = getattr(_client(), method)("my-account", "enroll-1")

    assert isinstance(session, InMotionCredentialsSession)
    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == f"http://example.test/api/latest/authenticate/enrollment/{step}"
    assert mock_request_json.call_args.args[2]["X-Auth-Token"] == "enroll-1"


def test_register_account_posts_the_registration_unauthenticated():
    from inmotion.models import AccountRegistrationModel, UserRegistrationModel
    owner = UserRegistrationModel(userKey="u", userName="u", password="p", displayName="U", email="u@example.test",
                                  attrs={}, licenseAccepted=0, publicUserName=False)
    registration = AccountRegistrationModel(owner=owner, name="Acme", accountType="FREE_PERSONAL", address=None, profiles=[], attrs={})
    with patch("inmotion.credentials_client.request_json", return_value=MagicMock()) as mock_request_json:
        _client().register_account(registration)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/latest/account"
    assert "X-Auth-Token" not in mock_request_json.call_args.args[2]
    assert '"accountType":"FREE_PERSONAL"' in mock_request_json.call_args.args[3]
