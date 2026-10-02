import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIInvalidResponseError,
    AIRateLimitError,
    AIServiceError,
    AITimeoutError,
    AIUpstreamError,
)


logger = logging.getLogger(__name__)


def get_request_id(request: Request) -> str:
    return getattr(
        request.state,
        "request_id",
        "unknown",
    )


def register_exception_handlers(
    app: FastAPI,
) -> None:

    @app.exception_handler(AIRateLimitError)
    async def handle_rate_limit(
        request: Request,
        exc: AIRateLimitError,
    ):
        return JSONResponse(
            status_code=503,
            content={
                "code": exc.code,
                "message": exc.message,
                "request_id": get_request_id(request),
            },
        )

    @app.exception_handler(AITimeoutError)
    async def handle_timeout(
        request: Request,
        exc: AITimeoutError,
    ):
        return JSONResponse(
            status_code=503,
            content={
                "code": exc.code,
                "message": exc.message,
                "request_id": get_request_id(request),
            },
        )

    @app.exception_handler(AIAuthenticationError)
    async def handle_authentication_error(
        request: Request,
        exc: AIAuthenticationError,
    ):
        return JSONResponse(
            status_code=503,
            content={
                "code": exc.code,
                "message": exc.message,
                "request_id": get_request_id(request),
            },
        )

    @app.exception_handler(AIServiceError)
    async def handle_ai_service_error(
        request: Request,
        exc: AIServiceError,
    ):
        return JSONResponse(
            status_code=503,
            content={
                "code": exc.code,
                "message": exc.message,
                "request_id": get_request_id(request),
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exc: Exception,
    ):
        request_id = get_request_id(request)

        logger.exception(
            "Unhandled application error request_id=%s",
            request_id,
        )

        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_SERVER_ERROR",
                "message": (
                    "An unexpected error occurred."
                ),
                "request_id": request_id,
            },
        )