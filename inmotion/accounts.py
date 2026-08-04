from dataclasses import asdict

from inmotion.api import InMotionSession, InMotionAccounts
from inmotion.models import (
    AccountDetailsModel,
    AccountMarkedForDeletionModel,
    AccountModel,
    AccountPrivilegesModel,
    AccountTagsModel,
    AccountUpdateBatchCommandModel,
    AccountUpdateBatchResultsModel,
    AccountUserSummaryModel,
    AccountUserUnregisteredModel,
    DeviceConfigSyncRequestModel,
    DeviceConfigSyncResultModel,
    UserAccountSummaryModel,
)
from inmotion.utils import request_json, request_json_map, stringify


def _text_headers(session: InMotionSession, content: str) -> dict[str, str]:
    headers = session.build_headers(content=content)
    headers['Content-Type'] = 'text/plain'
    return headers


class InMotionAccountsImpl(InMotionAccounts):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def find_account(self, account_key: str) -> AccountDetailsModel:
        return request_json('GET', f"{self._prefix_path}/account/{account_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve account',
                             AccountDetailsModel)

    def find_account_tags(self, account_key: str) -> AccountTagsModel:
        return request_json('GET', f"{self._prefix_path}/account/tags/{account_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve account tags',
                             AccountTagsModel)

    def update_account(self, account_key: str, account: AccountModel) -> AccountDetailsModel:
        account_data = stringify(account)
        return request_json('POST', f"{self._prefix_path}/account/{account_key}",
                             self._session.build_headers(content=account_data),
                             account_data,
                             'Failed to update account',
                             AccountDetailsModel)

    def find_account_users(self, account_key: str) -> list[AccountUserSummaryModel]:
        return request_json('GET', f"{self._prefix_path}/account/{account_key}/users",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve account users',
                             AccountUserSummaryModel, many=True)

    def register_account_user(self, account_key: str, user_key: str, privileges: AccountPrivilegesModel) -> list[AccountUserSummaryModel]:
        privileges_data = stringify(privileges)
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/register/{user_key}",
                             self._session.build_headers(content=privileges_data),
                             privileges_data,
                             'Failed to register account user',
                             AccountUserSummaryModel, many=True)

    def unregister_account_user(self, account_key: str, user_key: str) -> AccountUserUnregisteredModel:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/unregister/{user_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to unregister account user',
                             AccountUserUnregisteredModel)

    def batch_update_account_users(self, account_key: str, commands: list[AccountUpdateBatchCommandModel]) -> AccountUpdateBatchResultsModel:
        batch_data = stringify([asdict(c) for c in commands])
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/batch",
                             self._session.build_headers(content=batch_data),
                             batch_data,
                             'Failed to batch update account users',
                             AccountUpdateBatchResultsModel)

    def create_account_only(self, account: AccountModel) -> AccountDetailsModel:
        account_data = stringify(account)
        return request_json('POST', f"{self._prefix_path}/account/create/only",
                             self._session.build_headers(content=account_data),
                             account_data,
                             'Failed to create account',
                             AccountDetailsModel)

    def mark_account_for_deletion(self, account_key: str, and_user: bool) -> AccountMarkedForDeletionModel:
        and_user_segment = 'true' if and_user else 'false'
        return request_json('DELETE', f"{self._prefix_path}/account/delete/{account_key}/{and_user_segment}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to mark account for deletion',
                             AccountMarkedForDeletionModel)

    def find_my_accounts(self) -> dict[str, UserAccountSummaryModel]:
        return request_json_map('GET', f"{self._prefix_path}/accounts",
                                 self._session.build_headers(content=''),
                                 '',
                                 'Failed to retrieve accounts',
                                 UserAccountSummaryModel)

    def fetch_global_device_configs(self) -> dict:
        return request_json('GET', f"{self._prefix_path}/device-config",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to fetch global device configs')

    def sync_device_configs(self, request: DeviceConfigSyncRequestModel) -> DeviceConfigSyncResultModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/device-config/sync",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to sync device configs',
                             DeviceConfigSyncResultModel)

    def list_standard_data_types(self, account_key: str) -> list[dict]:
        return request_json('GET', f"{self._prefix_path}/account/{account_key}/sdt/data-types",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to list standard data types')

    def create_standard_data_type(self, account_key: str, yaml_document: str) -> dict:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/sdt/data-types",
                             _text_headers(self._session, yaml_document),
                             yaml_document,
                             'Failed to create standard data type')

    def update_standard_data_type(self, account_key: str, key: str, yaml_document: str) -> dict:
        return request_json('PUT', f"{self._prefix_path}/account/{account_key}/sdt/data-types/{key}",
                             _text_headers(self._session, yaml_document),
                             yaml_document,
                             'Failed to update standard data type')

    def delete_standard_data_type(self, account_key: str, key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/account/{account_key}/sdt/data-types/{key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete standard data type')

    def list_standard_data_variant_types(self, account_key: str) -> list[dict]:
        return request_json('GET', f"{self._prefix_path}/account/{account_key}/sdt/data-variant-types",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to list standard data variant types')

    def create_standard_data_variant_type(self, account_key: str, yaml_document: str) -> dict:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/sdt/data-variant-types",
                             _text_headers(self._session, yaml_document),
                             yaml_document,
                             'Failed to create standard data variant type')

    def update_standard_data_variant_type(self, account_key: str, key: str, yaml_document: str) -> dict:
        return request_json('PUT', f"{self._prefix_path}/account/{account_key}/sdt/data-variant-types/{key}",
                             _text_headers(self._session, yaml_document),
                             yaml_document,
                             'Failed to update standard data variant type')

    def delete_standard_data_variant_type(self, account_key: str, key: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/account/{account_key}/sdt/data-variant-types/{key}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete standard data variant type')

    def fetch_device_configs(self, account_key: str, preview: bool = False) -> dict:
        qs = '?preview=true' if preview else ''
        return request_json('GET', f"{self._prefix_path}/account/{account_key}/device-config{qs}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to fetch device configs')

    def list_device_configs(self, account_key: str) -> dict:
        return request_json('GET', f"{self._prefix_path}/account/{account_key}/device-configs",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to list device configs')

    def create_device_config(self, account_key: str, yaml_document: str) -> dict:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/device-configs",
                             _text_headers(self._session, yaml_document),
                             yaml_document,
                             'Failed to create device config')

    def save_device_config(self, account_key: str, name: str, yaml_document: str) -> dict:
        return request_json('PUT', f"{self._prefix_path}/account/{account_key}/device-configs/{name}",
                             _text_headers(self._session, yaml_document),
                             yaml_document,
                             'Failed to save device config')

    def delete_device_config(self, account_key: str, name: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/account/{account_key}/device-configs/{name}",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to delete device config')

    def start_device_config_development(self, account_key: str, name: str) -> dict:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/device-configs/{name}/development",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to start device config development')

    def discard_device_config_development(self, account_key: str, name: str) -> None:
        request_json('DELETE', f"{self._prefix_path}/account/{account_key}/device-configs/{name}/development",
                     self._session.build_headers(content=''),
                     '',
                     'Failed to discard device config development')

    def publish_device_config(self, account_key: str, name: str, semantic_version: str) -> dict:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/device-configs/{name}/publish?semanticVersion={semantic_version}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to publish device config')

    def withdraw_device_config(self, account_key: str, name: str, version: int) -> dict:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/device-configs/{name}/{version}/withdraw",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to withdraw device config')

    def republish_device_config(self, account_key: str, name: str, version: int) -> dict:
        return request_json('POST', f"{self._prefix_path}/account/{account_key}/device-configs/{name}/{version}/republish",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to republish device config')
