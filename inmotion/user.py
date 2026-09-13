from inmotion.api import InMotionSession, InMotionUser
from inmotion.models import (
    AccountUserSummaryModel,
    MessageResponseModel,
    MfaBackupCodesModel,
    MfaDisableRequestModel,
    MfaEnrollRequestModel,
    MfaStatusModel,
    OTCModel,
    TotpBackupCodesRegenerateRequestModel,
    TotpConfirmRequestModel,
    TotpEnrollBeginRequestModel,
    TotpEnrollmentBeginResultModel,
    UserAttributesModel,
    UserPasswordRequestModel,
    UserRegistrationModel,
    UserUnregisteredResponseModel,
)
from inmotion.utils import request_json, stringify


class InMotionUserImpl(InMotionUser):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}"

    def create_user_against_account(self, account_key: str, privilege_label: str, registration: UserRegistrationModel) -> AccountUserSummaryModel:
        registration_data = stringify(registration)
        return request_json('POST', f"{self._prefix_path}/user/{account_key}/{privilege_label}",
                             self._session.build_headers(content=registration_data),
                             registration_data,
                             'Failed to create user against account',
                             AccountUserSummaryModel)

    def request_password_reset(self, request: UserPasswordRequestModel) -> MessageResponseModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/user/reset-password",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to request password reset',
                             MessageResponseModel)

    def find_user_attributes(self) -> UserAttributesModel:
        return request_json('GET', f"{self._prefix_path}/user/attributes",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve user attributes',
                             UserAttributesModel)

    def update_user_attributes(self, attributes: UserAttributesModel) -> dict:
        attributes_data = stringify(attributes)
        return request_json('POST', f"{self._prefix_path}/user/attributes",
                             self._session.build_headers(content=attributes_data),
                             attributes_data,
                             'Failed to update user attributes')

    def unregister_from_account(self, account_key: str) -> UserUnregisteredResponseModel:
        return request_json('PUT', f"{self._prefix_path}/user/unregister/{account_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to unregister from account',
                             UserUnregisteredResponseModel)

    def create_otc(self) -> OTCModel:
        return request_json('GET', f"{self._prefix_path}/otc",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to create one-time code',
                             OTCModel)

    def find_mfa_status(self) -> MfaStatusModel:
        return request_json('GET', f"{self._prefix_path}/user/mfa",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to retrieve MFA status',
                             MfaStatusModel)

    def enroll_mfa(self, request: MfaEnrollRequestModel) -> MfaStatusModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/user/mfa/enroll",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to begin MFA enrollment',
                             MfaStatusModel)

    def confirm_mfa_email(self, request: TotpConfirmRequestModel) -> MfaStatusModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/user/mfa/email/confirm",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to confirm EMAIL MFA enrollment',
                             MfaStatusModel)

    def begin_totp_enrollment(self, request: TotpEnrollBeginRequestModel) -> TotpEnrollmentBeginResultModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/user/mfa/totp/enroll",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to begin TOTP enrollment',
                             TotpEnrollmentBeginResultModel)

    def confirm_totp_enrollment(self, request: TotpConfirmRequestModel) -> MfaStatusModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/user/mfa/totp/confirm",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to confirm TOTP enrollment',
                             MfaStatusModel)

    def regenerate_totp_backup_codes(self, request: TotpBackupCodesRegenerateRequestModel) -> MfaBackupCodesModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/user/mfa/totp/backup-codes/regenerate",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to regenerate TOTP backup codes',
                             MfaBackupCodesModel)

    def disable_mfa(self, request: MfaDisableRequestModel) -> MfaStatusModel:
        request_data = stringify(request)
        return request_json('POST', f"{self._prefix_path}/user/mfa/disable",
                             self._session.build_headers(content=request_data),
                             request_data,
                             'Failed to disable MFA',
                             MfaStatusModel)
