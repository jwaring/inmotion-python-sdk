from dataclasses import asdict

from inmotion.api import InMotionSession, InMotionAccounts
from inmotion.models import *
from inmotion.utils import *


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
