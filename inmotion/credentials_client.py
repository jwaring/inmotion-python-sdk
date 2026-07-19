from inmotion.accounts import InMotionAccountsImpl
from inmotion.activities import InMotionActivitiesImpl
from inmotion.activity_config import InMotionActivityConfigImpl
from inmotion.exceptions import InMotionAuthenticationError
from inmotion import InMotionSession, InMotionActivities, InMotionAccounts, InMotionActivityConfig
from inmotion.utils import *
from inmotion.models import AuthenticationSessionModel

INMOTION_API_VERSION = '2.0.0'

class InMotionCredentialsSession(InMotionSession):

    def __init__(self, base_url: str, dev_key: str, dev_secret: str,
                 token: str, account: str, api_path: str):
        self._is_connected = True
        self._base_url = base_url
        self._account = account
        self._token = token
        self._api_path = api_path
        self._dev_key = dev_key
        self._dev_secret = dev_secret

    def disconnect(self) -> None:
        if self._is_connected:
            self._is_connected = False

    def activities(self) -> InMotionActivities:
        return InMotionActivitiesImpl(self)

    def accounts(self) -> InMotionAccounts:
        return InMotionAccountsImpl(self)

    def activity_config(self) -> InMotionActivityConfig:
        return InMotionActivityConfigImpl(self)

    def build_headers(self, content: str) -> dict[str, str]:
        return build_im_headers(dev_key=self._dev_key,
                                dev_secret=self._dev_secret,
                                content=content,
                                extra_name='X-Auth-Token',
                                extra_value=self._token)

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def api_path(self) -> str:
        return self._api_path

    @property
    def account(self) -> str:
        return self._account


class InMotionCredentialsClient(object):
    def __init__(self, base_url: str, dev_key: str, dev_secret: str, **kwargs):
        self._base_url = base_url
        self._dev_key = dev_key
        self._dev_secret = dev_secret
        self._api_version = kwargs.pop('api_version', INMOTION_API_VERSION)

    def get_session(self, account: str, username: str, password: str) -> InMotionCredentialsSession:
        """
         Connect to inMotion and create a session for the given account and user
        """
        login_details = stringify({'username': username, 'password': password, 'apiVersion': self._api_version})
        capabilities = request_json('POST', self._base_url + "/api/latest/authenticate",
                                     build_im_headers(
                                         dev_key=self._dev_key,
                                         dev_secret=self._dev_secret,
                                         content=login_details
                                     ),
                                     login_details,
                                     'Failed to authenticate to inMotion',
                                     AuthenticationSessionModel)

        match capabilities.status:
            case 'active':
                return InMotionCredentialsSession(self._base_url,
                                                 self._dev_key,
                                                 self._dev_secret,
                                                 capabilities.token,
                                                 account,
                                                 capabilities.apiPath)

            case 'expiring':
                print(f'Warning: API version {capabilities.requestedVersion} is expiring on {capabilities.requestedVersionExpiryDate}. ')
                return InMotionCredentialsSession(self._base_url,
                                                  self._dev_key,
                                                  self._dev_secret,
                                                  capabilities.token,
                                                  account,
                                                  capabilities.apiPath)

            case _:
                raise InMotionAuthenticationError(f'API version {capabilities.requestedVersion} expired or unavailable')
