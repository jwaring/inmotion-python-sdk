from types import SimpleNamespace
from typing import cast

import requests

from inmotion.activities import InMotionActivitiesImpl
from inmotion import InMotionSession, InMotionActivities
from inmotion.utils import *
from inmotion.models import *

INMOTION_API_VERSION = '2.0.0'

class InMotionAPIKeySession(InMotionSession):

    def __init__(self, base_url: str, dev_key: str, dev_secret: str,
                 api_key: str, account: str, api_path: str):
        self._base_url = base_url
        self._dev_key = dev_key
        self._dev_secret = dev_secret
        self._api_key = api_key
        self._account = account
        self._api_path = api_path

    def disconnect(self) -> None:
        pass

    def activities(self) -> InMotionActivities:
        return InMotionActivitiesImpl(self)

    def build_headers(self, content: str) -> dict[str, str]:
        return build_im_headers(dev_key=self._dev_key,
                                dev_secret=self._dev_secret,
                                content=content,
                                extra_name='X-API-KEY',
                                extra_value=self._api_key)

    @property
    def is_connected(self) -> bool:
        return True

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def api_path(self) -> str:
        return self._api_path

    @property
    def account(self) -> str:
        return self._account

class InMotionAPIKeyClient(object):
    def __init__(self, base_url: str, dev_key: str, dev_secret: str, api_key: str, **kwargs):
        self._base_url = base_url
        self._dev_key = dev_key
        self._dev_secret = dev_secret
        self._api_key = api_key
        self._api_version = kwargs.pop('api_version', INMOTION_API_VERSION)

    def get_session(self, account: str) -> InMotionAPIKeySession:
        """
         Validate connectivity and extract tha API path by using the capabilities endpoint.
        """
        capabilitiesRequired = stringify({
            'requiredApiVersion': self._api_version,
            'withMasterData': True
        })
        r = requests.post(self._base_url + "/api/latest/authenticate/capabilities",
                          headers=build_im_headers(
                              dev_key=self._dev_key,
                              dev_secret=self._dev_secret,
                              content=capabilitiesRequired,
                              extra_name='X-API-KEY',
                              extra_value=self._api_key,
                          ),
                          data=capabilitiesRequired)

        if r.status_code != 200:
            raise Exception('Failed to authenticate to inMotion')

        try:
            capabilities = APICapabilitiesModel(**r.json())
            match capabilities.status:
                case 'active':
                    return InMotionAPIKeySession(self._base_url,
                                                 self._dev_key,
                                                 self._dev_secret,
                                                 self._api_key,
                                                 account,
                                                 capabilities.apiPath)

                case 'expiring':
                    print(f'Warning: API version {capabilities.requestedVersion} is expiring on {capabilities.requestedVersionExpiryDate}. ')
                    return InMotionAPIKeySession(self._base_url,
                                                 self._dev_key,
                                                 self._dev_secret,
                                                 self._api_key,
                                                 account,
                                                 capabilities.apiPath)

                case _:
                    raise Exception(f'API version {capabilities.requestedVersion} expired or unavailable')

        except:
            raise Exception('Malformed capabilities model received from inMotion')
