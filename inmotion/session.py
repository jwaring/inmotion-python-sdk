from inmotion.activities import IMActivitiesImpl
from inmotion.api import IMSession, IMActivities
from inmotion.utils import *


class IMSessionImpl(IMSession):

    def __init__(self, base_url: str, dev_key: str, dev_secret: str, account: str, token: str, api_path: str, end_points):
        self._is_connected = None
        self._base_url = base_url
        self._account = account
        self._token = token
        self._api_path = api_path
        self._end_points = end_points
        self._dev_key = dev_key
        self._dev_secret = dev_secret

    def disconnect(self):
        if self._is_connected:
            return ''

    def activities(self) -> IMActivities:
        return IMActivitiesImpl(self)

    def build_headers(self, content: str):
        return build_im_headers(dev_key=self._dev_key, dev_secret=self._dev_secret, content=content, token=self._token)

    @property
    def is_connected(self):
        return self._is_connected

    @property
    def base_url(self):
        return self._base_url

    @property
    def api_path(self):
        return self._api_path

    @property
    def account(self):
        return self._account
