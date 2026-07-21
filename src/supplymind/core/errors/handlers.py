"""
SupplyMind Enterprise AI

Global Exception Handlers

Transforms application and framework exceptions into consistent,
safe, enterprise API error responses.
"""

import logging
from http import HTTPStatus
from typing import Any

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from supplymind.core.errors.codes import ErrorCode
from supplymind.core.errors.exceptions import SupplyMindException
from supplymind.core.errors.schemas import ErrorDetails, ErrorResponse

logger = logging.getLogger(__name__)


ERROR_STATUS_MAP: dict[ErrorCode, int] = {
    ErrorCode.VALIDATION_ERROR: HTTPStatus.BAD_REQUEST,
    ErrorCode.BAD_REQUEST: HTTPStatus.BAD_REQUEST,
    ErrorCode.RESOURCE_NOT_FOUND: HTTPStatus.NOT_FOUND,
    ErrorCode.RESOURCE_ALREADY_EXISTS: HTTPStatus.CONFLICT,
    ErrorCode.UNAUTHORIZED: HTTPStatus.UNAUTHORIZED,
    ErrorCode.FORBIDDEN: HTTPStatus.FORBIDDEN,
    ErrorCode.DATABASE_ERROR: HTTPStatus.SERVICE_UNAVAILABLE,
    ErrorCode.CONFIGURATION_ERROR: HTTPStatus.INTERNAL_SERVER_ERROR,
    ErrorCode.CONNECTOR_ERROR: HTTPStatus.BAD_GATEWAY,
    ErrorCode.AI_PROVIDER_ERROR: HTTPStatus.BAD_GATEWAY,
    ErrorCode.INTERNAL_SERVER_ERROR: HTTPStatus.INTERNAL_SERVER_ERROR,
}


def _build_error_response(
    *,
    code: ErrorCode,
    message: str,
    details: Any | None = None,
) -> dict[str, Any]:
    """
    Build a JSON-serializable enterprise error response.

    Keeping response construction in one function prevents handlers
    from producing different payload structures.
    """

    response = ErrorResponse(
        error=ErrorDetails(
            code=code,
            message=message,
            details=details,
        ),
    )

    return response.model_dump(mode="json")


def _error_code_from_http_status(status_code: int) -> ErrorCode:
    """Map an HTTP status code to a standardized application error code."""

    status_mapping: dict[int, ErrorCode] = {
        HTTPStatus.BAD_REQUEST: ErrorCode.BAD_REQUEST,
        HTTPStatus.UNAUTHORIZED: ErrorCode.UNAUTHORIZED,
        HTTPStatus.FORBIDDEN: ErrorCode.FORBIDDEN,
        HTTPStatus.NOT_FOUND: ErrorCode.RESOURCE_NOT_FOUND,
        HTTPStatus.CONFLICT: ErrorCode.RESOURCE_ALREADY_EXISTS,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorCode.VALIDATION_ERROR,
    }

    return status_mapping.get(status_code, ErrorCode.BAD_REQUEST)


async def supplymind_exception_handler(
    request: Request,
    exc: SupplyMindException,
) -> JSONResponse:
    """Handle expected SupplyMind application exceptions."""

    status_code = ERROR_STATUS_MAP.get(
        exc.code,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    logger.warning(
        "Application error: code=%s status=%s path=%s message=%s",
        exc.code,
        status_code,
        request.url.path,
        exc.message,
    )

    return JSONResponse(
        status_code=status_code,
        content=_build_error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details,
        ),
    )


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle FastAPI request validation failures."""

    validation_details = jsonable_encoder(exc.errors())

    logger.warning(
        "Request validation failed: path=%s errors=%s",
        request.url.path,
        validation_details,
    )

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=_build_error_response(
            code=ErrorCode.VALIDATION_ERROR,
            message="The request contains invalid data.",
            details=validation_details,
        ),
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Handle FastAPI and Starlette HTTP exceptions."""

    code = _error_code_from_http_status(exc.status_code)

    if isinstance(exc.detail, str):
        message = exc.detail
        details = None
    else:
        message = HTTPStatus(exc.status_code).phrase
        details = jsonable_encoder(exc.detail)

    logger.warning(
        "HTTP error: code=%s status=%s path=%s message=%s",
        code,
        exc.status_code,
        request.url.path,
        message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content=_build_error_response(
            code=code,
            message=message,
            details=details,
        ),
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle unexpected application failures.

    The complete exception is logged internally, while the API client
    receives a safe generic message.
    """

    logger.exception(
        "Unexpected application error: path=%s",
        request.url.path,
        exc_info=exc,
    )

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=_build_error_response(
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            message="An unexpected internal error occurred.",
        ),
    )
