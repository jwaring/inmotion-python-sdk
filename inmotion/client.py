import requests
from inmotion.session import IMSessionImpl
from inmotion.utils import *

INMOTION_API_VERSION = '1.02'


class InMotionClient(object):
    def __init__(self, base_url: str, dev_key: str, dev_secret: str, **kwargs):
        self._base_url = base_url
        self._dev_key = dev_key
        self._dev_secret = dev_secret
        self._api_version = kwargs.pop('api_version', INMOTION_API_VERSION)

    def connect(self, account: str, username: str, password: str):
        """
         Connect to inMotion and create a session for the given account and user
        """
        login_details = stringify({'username': username, 'password': password, 'apiVersion': self._api_version})
        r = requests.post(self._base_url + "/api/authenticate",
                          headers=build_im_headers(
                              dev_key=self._dev_key,
                              dev_secret=self._dev_secret,
                              content=login_details
                          ),
                          data=login_details)
        if r.status_code != 200:
            raise Exception('Failed to authenticate to inmotion')

        data = r.json()

        return IMSessionImpl(self._base_url, self._dev_key, self._dev_secret,
                             account, data['token'], data['api']['apiPath'], data['api'])
