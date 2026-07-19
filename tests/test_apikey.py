from unittest.mock import MagicMock, patch

from inmotion.apikey import InMotionApiKeysImpl
from inmotion.models import AccountAPIKeyCreatorModel, AccountAPIKeyUpdatorModel, AccountPrivilegesModel


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _privs():
    return AccountPrivilegesModel(
        accountOwner=False, viewAccountDetails=True, changeAccountDetails=False,
        viewStreams=True, createStreams=False, changeStreams=False, deleteStreams=False,
    )


def test_find_api_keys_uses_many_true():
    session = _fake_session()
    impl = InMotionApiKeysImpl(session)

    with patch("inmotion.apikey.request_json", return_value=[]) as mock_request_json:
        impl.find_api_keys("acct1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/apikey/acct1"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_create_api_key_posts_creator_body():
    session = _fake_session()
    impl = InMotionApiKeysImpl(session)

    creator = AccountAPIKeyCreatorModel(name="my key", privs=_privs(), expiryOn=None)
    with patch("inmotion.apikey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_api_key("acct1", creator)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/apikey/acct1"
    assert '"name":"my key"' in mock_request_json.call_args.args[3]


def test_update_api_key_posts_updator_body():
    session = _fake_session()
    impl = InMotionApiKeysImpl(session)

    updator = AccountAPIKeyUpdatorModel(name="renamed", privs=None)
    with patch("inmotion.apikey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_api_key("acct1", "key1", updator)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/apikey/acct1/key1"


def test_delete_api_key_issues_a_delete():
    session = _fake_session()
    impl = InMotionApiKeysImpl(session)

    with patch("inmotion.apikey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_api_key("acct1", "key1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/apikey/acct1/key1"


def test_find_api_key_issues_a_get():
    session = _fake_session()
    impl = InMotionApiKeysImpl(session)

    with patch("inmotion.apikey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_api_key("acct1", "key1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/apikey/acct1/key1"
