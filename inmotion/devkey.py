from inmotion.api import InMotionSession, InMotionDevKeys
from inmotion.models import (
    AccountDevKeyCreatorModel,
    AccountDevKeyModel,
    AccountDevKeyResponseModel,
    AccountDevKeyUpdatorModel,
)
from inmotion.utils import request_json, stringify


class InMotionDevKeysImpl(InMotionDevKeys):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def find_dev_keys(self, account_key: str) -> list[AccountDevKeyModel]:
        return request_json('GET', f"{self._prefix_path}/devkey/{account_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve developer keys',
                             AccountDevKeyModel, many=True)

    def create_dev_key(self, account_key: str, creator: AccountDevKeyCreatorModel) -> AccountDevKeyModel:
        creator_data = stringify(creator)
        return request_json('POST', f"{self._prefix_path}/devkey/{account_key}",
                             self._session.build_headers(content=creator_data),
                             creator_data,
                             'Failed to create developer key',
                             AccountDevKeyModel)

    def update_dev_key(self, account_key: str, dev_key: str, updator: AccountDevKeyUpdatorModel) -> AccountDevKeyModel:
        updator_data = stringify(updator)
        return request_json('POST', f"{self._prefix_path}/devkey/{account_key}/{dev_key}",
                             self._session.build_headers(content=updator_data),
                             updator_data,
                             'Failed to update developer key',
                             AccountDevKeyModel)

    def delete_dev_key(self, account_key: str, dev_key: str) -> AccountDevKeyResponseModel:
        return request_json('DELETE', f"{self._prefix_path}/devkey/{account_key}/{dev_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to delete developer key',
                             AccountDevKeyResponseModel)

    def find_dev_key(self, account_key: str, dev_key: str) -> AccountDevKeyModel:
        return request_json('GET', f"{self._prefix_path}/devkey/{account_key}/{dev_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve developer key',
                             AccountDevKeyModel)
