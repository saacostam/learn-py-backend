import sys
import traceback

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from lab.shared.errors.domain import DomainError, ErrorType

MAP_DOMAIN_ERROR_TO_STATUS_CODE = {
    ErrorType.BAD_REQUEST: status.HTTP_400_BAD_REQUEST,
    ErrorType.CONFLICT: status.HTTP_409_CONFLICT,
    ErrorType.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    ErrorType.FORBIDDEN: status.HTTP_403_FORBIDDEN,
    ErrorType.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorType.SERVER_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorType.UNKNOWN: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorType.INVALID_RESPONSE: status.HTTP_502_BAD_GATEWAY,
}

MAP_DOMAIN_ERROR_TO_GENERIC_ERROR = {
    ErrorType.BAD_REQUEST: "Invalid request",
    ErrorType.CONFLICT: "Conflict",
    ErrorType.UNAUTHORIZED: "Unauthorized",
    ErrorType.FORBIDDEN: "Forbidden",
    ErrorType.NOT_FOUND: "Not found",
    ErrorType.SERVER_ERROR: "Something went wrong",
    ErrorType.UNKNOWN: "Something went wrong",
    ErrorType.INVALID_RESPONSE: "Invalid response",
}


class FieldError(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    message: str
    status: int
    errors: list[FieldError] | None = None


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Equivalent to ZodError handling in Express"""
    assert isinstance(exc, RequestValidationError)
    print(exc, file=sys.stderr)

    status_code = status.HTTP_400_BAD_REQUEST
    base_message = MAP_DOMAIN_ERROR_TO_GENERIC_ERROR[ErrorType.BAD_REQUEST]

    field_specific_errors: list[FieldError] = []
    root_validation_messages: list[str] = []

    for error in exc.errors():
        loc = error.get("loc", ())
        path_parts = [
            str(p) for p in loc if p not in ("body", "query", "path", "header")
        ]
        msg = error.get("msg", "Invalid input")

        if path_parts:
            field_specific_errors.append(
                FieldError(field=".".join(path_parts), message=msg)
            )
        else:
            root_validation_messages.append(msg)

    message = base_message
    if root_validation_messages:
        message = f"{message}: {', '.join(root_validation_messages)}"

    error_response = ErrorResponse(
        message=message,
        status=status_code,
        errors=field_specific_errors if field_specific_errors else None,
    )
    return JSONResponse(status_code=status_code, content=error_response.model_dump())


async def domain_error_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Equivalent to BaseDomainError handling in Express"""
    assert isinstance(exc, DomainError)
    print(exc, file=sys.stderr)

    status_code = MAP_DOMAIN_ERROR_TO_STATUS_CODE.get(
        exc.type, status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    generic_msg = MAP_DOMAIN_ERROR_TO_GENERIC_ERROR.get(
        exc.type, "Something went wrong"
    )
    message = exc.user_msg or generic_msg

    formatted_errors: list[FieldError] | None = None
    if exc.fields:
        formatted_errors = [
            FieldError(field=f.get("field", ""), message=f.get("message", ""))
            for f in exc.fields
        ]

    error_response = ErrorResponse(
        message=message, status=status_code, errors=formatted_errors
    )
    return JSONResponse(status_code=status_code, content=error_response.model_dump())


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Equivalent to standard Error / catch-all handling in Express"""
    traceback.print_exc()

    status_code = getattr(exc, "status_code", 500)
    message = (
        str(exc)
        if status_code != 500
        else MAP_DOMAIN_ERROR_TO_GENERIC_ERROR[ErrorType.SERVER_ERROR]
    )

    error_response = ErrorResponse(
        message=message,
        status=status_code,
    )
    return JSONResponse(status_code=status_code, content=error_response.model_dump())
