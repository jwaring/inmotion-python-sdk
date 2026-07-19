from unittest.mock import MagicMock, patch

from inmotion.user import InMotionUserImpl
from inmotion.models import UserAttributesModel, UserPasswordRequestModel, UserRegistrationModel


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def test_create_user_against_account_posts_to_account_key_and_privilege_path():
    session = _fake_session()
    impl = InMotionUserImpl(session)

    registration = UserRegistrationModel(
        userKey="u1", userName="jdoe", password="pw", displayName="J Doe", email="j@x.com",
        attrs={}, licenseAccepted=0, publicUserName=False, firstName=None, lastName=None, avatarUrl=None,
    )
    with patch("inmotion.user.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_user_against_account("acct1", "view", registration)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/user/acct1/view"
    assert '"userName":"jdoe"' in mock_request_json.call_args.args[3]


def test_request_password_reset_posts_username_or_email():
    session = _fake_session()
    impl = InMotionUserImpl(session)

    with patch("inmotion.user.request_json", return_value=MagicMock()) as mock_request_json:
        impl.request_password_reset(UserPasswordRequestModel(userNameOrEmail="jdoe"))

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/user/reset-password"
    assert '"userNameOrEmail":"jdoe"' in mock_request_json.call_args.args[3]


def test_find_user_attributes_issues_a_get():
    session = _fake_session()
    impl = InMotionUserImpl(session)

    with patch("inmotion.user.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_user_attributes()

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/user/attributes"


def test_update_user_attributes_posts_and_returns_raw_dict_with_no_model():
    session = _fake_session()
    impl = InMotionUserImpl(session)

    attributes = UserAttributesModel(
        userName="jdoe", displayName="J Doe", email="j@x.com", publicUserName=False,
        firstName=None, lastName=None, avatarUrl=None, attrs={},
    )
    with patch("inmotion.user.request_json", return_value={"message": "Attributes updated for user 'u1'"}) as mock_request_json:
        result = impl.update_user_attributes(attributes)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/user/attributes"
    assert "model" not in mock_request_json.call_args.kwargs
    assert len(mock_request_json.call_args.args) == 5
    assert mock_request_json.call_args.args[4] == 'Failed to update user attributes'
    assert result == {"message": "Attributes updated for user 'u1'"}


def test_unregister_from_account_issues_a_put():
    session = _fake_session()
    impl = InMotionUserImpl(session)

    with patch("inmotion.user.request_json", return_value=MagicMock()) as mock_request_json:
        impl.unregister_from_account("acct1")

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/user/unregister/acct1"
