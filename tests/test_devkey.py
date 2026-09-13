from unittest.mock import MagicMock, patch

from inmotion.devkey import InMotionDevKeysImpl
from inmotion.models import AccountDevKeyCreatorModel, AccountDevKeyUpdatorModel


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def test_find_dev_keys_uses_many_true():
    session = _fake_session()
    impl = InMotionDevKeysImpl(session)

    with patch("inmotion.devkey.request_json", return_value=[]) as mock_request_json:
        impl.find_dev_keys("acct1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/devkey/acct1"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_create_dev_key_posts_creator_body():
    session = _fake_session()
    impl = InMotionDevKeysImpl(session)

    creator = AccountDevKeyCreatorModel(name="my key", hmacEnabled=True, expiryOn=None)
    with patch("inmotion.devkey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_dev_key("acct1", creator)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/devkey/acct1"
    assert '"name":"my key"' in mock_request_json.call_args.args[3]


def test_update_dev_key_posts_updator_body():
    session = _fake_session()
    impl = InMotionDevKeysImpl(session)

    updator = AccountDevKeyUpdatorModel(name="renamed", hmacEnabled=None)
    with patch("inmotion.devkey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_dev_key("acct1", "dev1", updator)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/devkey/acct1/dev1"


def test_delete_dev_key_issues_a_delete():
    session = _fake_session()
    impl = InMotionDevKeysImpl(session)

    with patch("inmotion.devkey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.delete_dev_key("acct1", "dev1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/devkey/acct1/dev1"


def test_find_dev_key_issues_a_get():
    session = _fake_session()
    impl = InMotionDevKeysImpl(session)

    with patch("inmotion.devkey.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_dev_key("acct1", "dev1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/devkey/acct1/dev1"
