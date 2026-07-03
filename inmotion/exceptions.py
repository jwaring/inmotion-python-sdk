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
