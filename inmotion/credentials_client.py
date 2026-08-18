import marshmallow_dataclass

from inmotion.accounts import InMotionAccountsImpl
from inmotion.activities import InMotionActivitiesImpl
from inmotion.activity_config import InMotionActivityConfigImpl
from inmotion.apikey import InMotionApiKeysImpl
from inmotion.audit import InMotionAuditImpl
from inmotion.datastream import InMotionDataStreamImpl
from inmotion.devkey import InMotionDevKeysImpl
from inmotion.event import InMotionEventsImpl
from inmotion.exceptions import InMotionAuthenticationError, InMotionMfaRequiredError
from inmotion.folio import InMotionFolioImpl
from inmotion.model import InMotionModelImpl
from inmotion.raster_overlay import InMotionRasterOverlayImpl
from inmotion.shape import InMotionShapeImpl
from inmotion.shapegenerator import InMotionShapeGeneratorImpl
from inmotion import (
    InMotionSession,
    InMotionAccounts,
    InMotionActivities,
    InMotionActivityConfig,
    InMotionApiKeys,
    InMotionAudit,
    InMotionDataStream,
    InMotionDevKeys,
    InMotionEvents,
    InMotionFolio,
    InMotionModel,
    InMotionRasterOverlay,
    InMotionShape,
    InMotionShapeGenerator,
    InMotionUpload,
    InMotionUser,
)
from inmotion.models import AuthenticationSessionModel, MfaResendResultModel
from inmotion.upload import InMotionUploadImpl
from inmotion.user import InMotionUserImpl
from inmotion.utils import build_im_headers, request_json, stringify

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

    def shape(self) -> InMotionShape:
        return InMotionShapeImpl(self)

    def shape_generator(self) -> InMotionShapeGenerator:
        return InMotionShapeGeneratorImpl(self)

    def raster_overlay(self) -> InMotionRasterOverlay:
        return InMotionRasterOverlayImpl(self)

    def audit(self) -> InMotionAudit:
        return InMotionAuditImpl(self)

    def model(self) -> InMotionModel:
        return InMotionModelImpl(self)

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
         Connect to inMotion and create a session for the given account and user.

         Raises InMotionMfaRequiredError if the account has MFA enabled - catch it, challenge the
         user for their MFA code, and call verify_mfa(account, error.mfa_token, code) to complete
         the login.
        """
        login_details = stringify({'username': username, 'password': password, 'apiVersion': self._api_version})
        raw = request_json('POST', self._base_url + "/api/latest/authenticate",
                            build_im_headers(
                                dev_key=self._dev_key,
                                dev_secret=self._dev_secret,
                                content=login_details
                            ),
                            login_details,
                            'Failed to authenticate to inMotion')

        if raw.get('mfaPending'):
            raise InMotionMfaRequiredError('MFA challenge required to complete authentication',
                                            mfa_token=raw['mfaToken'],
                                            method=raw['method'],
                                            expires_in_seconds=raw['expiresInSeconds'])

        capabilities = marshmallow_dataclass.class_schema(AuthenticationSessionModel)().load(raw)
        return self._session_from_capabilities(account, capabilities)

    def verify_mfa(self, account: str, mfa_token: str, code: str) -> InMotionCredentialsSession:
        """
         Complete a login that was interrupted by InMotionMfaRequiredError, by submitting the
         user's MFA code against the pending token.
        """
        verify_details = stringify({'code': code, 'apiVersion': self._api_version})
        capabilities = request_json('POST', self._base_url + "/api/latest/authenticate/mfa",
                                     build_im_headers(
                                         dev_key=self._dev_key,
                                         dev_secret=self._dev_secret,
                                         content=verify_details,
                                         extra_name='X-Auth-Token',
                                         extra_value=mfa_token,
                                     ),
                                     verify_details,
                                     'Failed to verify MFA challenge',
                                     AuthenticationSessionModel)
        return self._session_from_capabilities(account, capabilities)

    def resend_mfa(self, mfa_token: str) -> MfaResendResultModel:
        """ Regenerate/resend the MFA challenge code for the account behind a pending token
        (EMAIL/SMS only - TOTP has no resend concept). """
        return request_json('POST', self._base_url + "/api/latest/authenticate/mfa/resend",
                             build_im_headers(
                                 dev_key=self._dev_key,
                                 dev_secret=self._dev_secret,
                                 content='',
                                 extra_name='X-Auth-Token',
                                 extra_value=mfa_token,
                             ),
                             '',
                             'Failed to resend MFA challenge',
                             MfaResendResultModel)

    def _session_from_capabilities(self, account: str, capabilities: AuthenticationSessionModel) -> InMotionCredentialsSession:
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
