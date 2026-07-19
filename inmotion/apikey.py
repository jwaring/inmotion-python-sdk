from inmotion.api import InMotionSession, InMotionApiKeys
from inmotion.models import (
    AccountAPIKeyCreatorModel,
    AccountAPIKeyModel,
    AccountAPIKeyResponseModel,
    AccountAPIKeyUpdatorModel,
)
from inmotion.utils import request_json, stringify


class InMotionApiKeysImpl(InMotionApiKeys):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def find_api_keys(self, account_key: str) -> list[AccountAPIKeyModel]:
        return request_json('GET', f"{self._prefix_path}/apikey/{account_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve API keys',
                             AccountAPIKeyModel, many=True)

    def create_api_key(self, account_key: str, creator: AccountAPIKeyCreatorModel) -> AccountAPIKeyModel:
        creator_data = stringify(creator)
        return request_json('POST', f"{self._prefix_path}/apikey/{account_key}",
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to create API key',
                             AccountAPIKeyModel)

    def update_api_key(self, account_key: str, api_key: str, updator: AccountAPIKeyUpdatorModel) -> AccountAPIKeyModel:
        updator_data = stringify(updator)
        return request_json('POST', f"{self._prefix_path}/apikey/{account_key}/{api_key}",
                             self._session.build_headers(content=updator_data),
                             updator_data,
                             'Failed to update API key',
                             AccountAPIKeyModel)

    def delete_api_key(self, account_key: str, api_key: str) -> AccountAPIKeyResponseModel:
        return request_json('DELETE', f"{self._prefix_path}/apikey/{account_key}/{api_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to delete API key',
                             AccountAPIKeyResponseModel)

    def find_api_key(self, account_key: str, api_key: str) -> AccountAPIKeyModel:
        return request_json('GET', f"{self._prefix_path}/apikey/{account_key}/{api_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve API key',
                             AccountAPIKeyModel)
