from unittest.mock import MagicMock, patch

from inmotion.accounts import InMotionAccountsImpl
from inmotion.models import (
    AccountModel,
    AccountPrivilegesModel,
    AccountUpdateBatchCommandModel,
    DeviceConfigSyncRequestModel,
)


def _fake_session():
    session = MagicMock()
    session.base_url = "http://example.test"
    session.api_path = "/api/v2"
    session.account = "my-account"
    session.build_headers.return_value = {"im-hmac": "sig"}
    return session


def _privileges():
    return AccountPrivilegesModel(
        accountOwner=False, viewAccountDetails=True, changeAccountDetails=False,
        viewStreams=True, createStreams=False, changeStreams=False, deleteStreams=False,
    )


def test_find_account_issues_a_get():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_account("acct1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1"


def test_find_account_tags_issues_a_get():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.find_account_tags("acct1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/tags/acct1"


def test_update_account_posts_the_account_body():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    account = AccountModel(name="Acme", address=None, accountType="1", attrs={}, profiles=[])
    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.update_account("acct1", account)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1"
    assert '"name":"Acme"' in mock_request_json.call_args.args[3]


def test_find_account_users_uses_many_true():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=[]) as mock_request_json:
        impl.find_account_users("acct1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/users"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_register_account_user_posts_privileges():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=[]) as mock_request_json:
        impl.register_account_user("acct1", "user1", _privileges())

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/register/user1"
    assert mock_request_json.call_args.kwargs["many"] is True


def test_unregister_account_user_posts_no_body():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.unregister_account_user("acct1", "user1")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/unregister/user1"


def test_batch_update_account_users_posts_command_list():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    commands = [AccountUpdateBatchCommandModel(action="register", userName="jdoe", privileges=None)]
    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.batch_update_account_users("acct1", commands)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/batch"
    assert '"action":"register"' in mock_request_json.call_args.args[3]


def test_create_account_only_posts_to_create_only_path():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    account = AccountModel(name="Acme", address=None, accountType="1", attrs={}, profiles=[])
    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.create_account_only(account)

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/create/only"


def test_mark_account_for_deletion_issues_a_delete_with_stringified_bool():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.mark_account_for_deletion("acct1", True)

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/delete/acct1/true"

    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.mark_account_for_deletion("acct1", False)

    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/delete/acct1/false"


def test_find_my_accounts_uses_root_level_path_and_map():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json_map", return_value={}) as mock_request_json_map:
        impl.find_my_accounts()

    assert mock_request_json_map.call_args.args[0] == "GET"
    assert mock_request_json_map.call_args.args[1] == "http://example.test/api/v2/accounts"


def test_fetch_global_device_configs_issues_a_get():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.fetch_global_device_configs()

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/device-config"


def test_sync_device_configs_posts_the_request_body():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=MagicMock()) as mock_request_json:
        impl.sync_device_configs(DeviceConfigSyncRequestModel(accountKeys=["acct1"]))

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/device-config/sync"
    assert '"acct1"' in mock_request_json.call_args.args[3]


def test_list_standard_data_types_issues_a_get():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value=[]) as mock_request_json:
        impl.list_standard_data_types("acct1")

    assert mock_request_json.call_args.args[0] == "GET"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/sdt/data-types"


def test_create_standard_data_type_sends_text_plain_body():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.create_standard_data_type("acct1", "key: my-sdt")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/sdt/data-types"
    assert mock_request_json.call_args.args[3] == "key: my-sdt"


def test_update_standard_data_type_puts_to_key_path():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.update_standard_data_type("acct1", "sdt1", "key: sdt1")

    assert mock_request_json.call_args.args[0] == "PUT"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/sdt/data-types/sdt1"


def test_delete_standard_data_type_issues_a_delete():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.delete_standard_data_type("acct1", "sdt1")

    assert mock_request_json.call_args.args[0] == "DELETE"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/sdt/data-types/sdt1"


def test_fetch_device_configs_includes_preview_flag():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.fetch_device_configs("acct1", preview=True)

    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/device-config?preview=true"


def test_create_device_config_sends_text_plain_body():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.create_device_config("acct1", "profile:\n  name: my-config")

    assert mock_request_json.call_args.args[0] == "POST"
    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/device-configs"


def test_publish_device_config_includes_semantic_version_query_param():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.publish_device_config("acct1", "my-config", "1.0.0")

    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/device-configs/my-config/publish?semanticVersion=1.0.0"


def test_withdraw_device_config_includes_version_path_segment():
    session = _fake_session()
    impl = InMotionAccountsImpl(session)

    with patch("inmotion.accounts.request_json", return_value={}) as mock_request_json:
        impl.withdraw_device_config("acct1", "my-config", 1)

    assert mock_request_json.call_args.args[1] == "http://example.test/api/v2/account/acct1/device-configs/my-config/1/withdraw"
