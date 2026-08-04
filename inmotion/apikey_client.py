from inmotion.accounts import InMotionAccountsImpl
from inmotion.activities import InMotionActivitiesImpl
from inmotion.activity_config import InMotionActivityConfigImpl
from inmotion.apikey import InMotionApiKeysImpl
from inmotion.datastream import InMotionDataStreamImpl
from inmotion.devkey import InMotionDevKeysImpl
from inmotion.event import InMotionEventsImpl
from inmotion.exceptions import InMotionAuthenticationError
from inmotion.folio import InMotionFolioImpl
from inmotion import (
    InMotionSession,
    InMotionActivities,
    InMotionAccounts,
    InMotionActivityConfig,
    InMotionApiKeys,
    InMotionDataStream,
    InMotionDevKeys,
    InMotionEvents,
    InMotionFolio,
    InMotionUpload,
    InMotionUser,
)
from inmotion.models import APICapabilitiesModel
from inmotion.upload import InMotionUploadImpl
from inmotion.user import InMotionUserImpl
from inmotion.utils import build_im_headers, request_json, stringify

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

    def accounts(self) -> InMotionAccounts:
        return InMotionAccountsImpl(self)

    def events(self) -> InMotionEvents:
        return InMotionEventsImpl(self)

    def dev_keys(self) -> InMotionDevKeys:
        return InMotionDevKeysImpl(self)

    def api_keys(self) -> InMotionApiKeys:
        return InMotionApiKeysImpl(self)

    def user(self) -> InMotionUser:
        return InMotionUserImpl(self)

    def activity_config(self) -> InMotionActivityConfig:
        return InMotionActivityConfigImpl(self)

    def upload(self) -> InMotionUpload:
        return InMotionUploadImpl(self)

    def folio(self) -> InMotionFolio:
        return InMotionFolioImpl(self)

    def data_stream(self) -> InMotionDataStream:
        return InMotionDataStreamImpl(self)

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
        capabilities_request = stringify({
            'requiredApiVersion': self._api_version,
            'withMasterData': True
        })
        capabilities = request_json('POST', self._base_url + "/api/latest/authenticate/capabilities",
                                     build_im_headers(
                                         dev_key=self._dev_key,
                                         dev_secret=self._dev_secret,
                                         content=capabilities_request,
                                         extra_name='X-API-KEY',
                                         extra_value=self._api_key,
                                     ),
                                     capabilities_request,
                                     f'Failed to authenticate to inMotion at {self._base_url}',
                                     APICapabilitiesModel)

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
                raise InMotionAuthenticationError(f'API version {capabilities.requestedVersion} expired or unavailable')
