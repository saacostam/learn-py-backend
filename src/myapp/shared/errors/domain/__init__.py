from enum import Enum


class ErrorType(str, Enum):
    UNKNOWN = "Unknown"
    NOT_FOUND = "Not Found"
    BAD_REQUEST = "Bad Request"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    INVALID_RESPONSE = "Invalid Response"


class DomainError(Exception):
    def __init__(
        self,
        *,
        msg: str,
        type: ErrorType,
        user_msg: str,
        fields: list[dict[str, str]] | None = None,
    ) -> None:
        super().__init__(msg)

        self.msg = msg
        self.type = type
        self.user_msg = user_msg
        self.fields = fields
