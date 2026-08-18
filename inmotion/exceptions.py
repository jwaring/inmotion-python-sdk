from typing import Optional


class InMotionError(Exception):
    pass


class InMotionConnectionError(InMotionError):
    pass


class InMotionAPIError(InMotionError):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class InMotionAuthenticationError(InMotionAPIError):
    pass


class InMotionMfaRequiredError(InMotionAuthenticationError):
    """ Raised by InMotionCredentialsClient.get_session when the account has MFA enabled -
    `/authenticate` returned an MfaChallengeModel in place of a full session. `mfa_token` must be
    passed back to verify_mfa/resend_mfa. """
    def __init__(self, message: str, mfa_token: str, method: str, expires_in_seconds: int):
        super().__init__(message)
        self.mfa_token = mfa_token
        self.method = method
        self.expires_in_seconds = expires_in_seconds
