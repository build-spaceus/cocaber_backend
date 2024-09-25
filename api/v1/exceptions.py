from rest_framework.exceptions import APIException
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from api.v1.constants import (
    API_DEFAULT_ERROR_CODE,
    AUTH_BASE_EXCEPTION_CODE,
    FIELD_BLANK_ERROR_CODE,
    FIELD_BLANK_ERROR_MSG,
    FIELD_INVALID_ERROR_CODE,
    FIELD_INVALID_ERROR_MSG,
    FIELD_NULL_ERROR_CODE,
    FIELD_NULL_ERROR_MSG,
    FIELD_REQUIRED_ERROR_CODE,
    FIELD_REQUIRED_ERROR_MSG,
    FORBIDDEN_ACTION_CODE,
    INTERNAL_ERROR_CODE,
    INVALID_OTP_CODE,
    INVALID_REQUEST_TOKEN_CODE,
    UNAUTHORIZED_USER_CODE,
)


class APIBaseException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    detail = ""

    def __init__(self, message="", code=API_DEFAULT_ERROR_CODE):
        """
        :param message:
        :param code:
        """
        self.message = "API error occurred"
        if message:
            self.message = message

        if code:
            self.code = code

        self.errors = {
            "status": "failure",
            "errors": {
                "message": self.message,
                "error_code": self.code,
            },
        }
        self.detail = self.errors


class UnauthorizedUserException(APIBaseException):
    status_code = HTTP_401_UNAUTHORIZED

    def __init__(self, message=""):
        self.message = "You are not authorized to perform this action."
        if message:
            self.message = message
        self.code = UNAUTHORIZED_USER_CODE

        super().__init__(message=self.message, code=self.code)


class ForbiddenActionException(APIBaseException):
    status_code = HTTP_403_FORBIDDEN

    def __init__(self, message=""):
        self.message = "This action is forbidden."
        if message:
            self.message = message
        self.code = FORBIDDEN_ACTION_CODE

        super().__init__(message=self.message, code=self.code)


class AuthBaseException(APIBaseException):
    def __init__(self, message=""):
        self.message = "Authentication failed."
        if message:
            self.message = message
        self.code = AUTH_BASE_EXCEPTION_CODE

        super().__init__(message=self.message, code=self.code)


class FieldRequiredException(APIBaseException):
    def __init__(self, entity=""):
        self.message = FIELD_REQUIRED_ERROR_MSG.format(entity=entity)
        self.code = FIELD_REQUIRED_ERROR_CODE
        super().__init__(message=self.message, code=self.code)


class FieldBlankException(APIBaseException):
    def __init__(self, entity=""):
        self.message = FIELD_BLANK_ERROR_MSG.format(entity=entity)
        self.code = FIELD_BLANK_ERROR_CODE
        super().__init__(message=self.message, code=self.code)


class FieldNullException(APIBaseException):
    def __init__(self, entity=""):
        self.message = FIELD_NULL_ERROR_MSG.format(entity=entity)
        self.code = FIELD_NULL_ERROR_CODE
        super().__init__(message=self.message, code=self.code)


class FieldInvalidException(APIBaseException):
    def __init__(self, entity=""):
        self.message = FIELD_INVALID_ERROR_MSG.format(entity=entity)
        self.code = FIELD_INVALID_ERROR_CODE
        super().__init__(message=self.message, code=self.code)


class InternalException(APIBaseException):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message=""):
        self.message = (
            "Something went wrong. Please contact the team "
            "if the failure persists."
        )
        if message:
            self.message = message
        self.code = INTERNAL_ERROR_CODE

        super().__init__(message=self.message, code=self.code)


class InvalidRequestTokenException(APIBaseException):
    def __init__(self, message=""):
        self.message = "Invalid request token or request timed out."
        if message:
            self.message = message
        self.code = INVALID_REQUEST_TOKEN_CODE

        super().__init__(message=self.message, code=self.code)


class InvalidOTPException(APIBaseException):
    def __init__(self, message=""):
        self.message = "Invalid otp or otp expired."
        if message:
            self.message = message
        self.code = INVALID_OTP_CODE

        super().__init__(message=self.message, code=self.code)
