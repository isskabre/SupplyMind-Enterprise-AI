"""
Tests for request logging middleware behavior.
"""

import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from supplymind.middleware.correlation_id import CorrelationIdMiddleware
from supplymind.middleware.request_logging import RequestLoggingMiddleware


def create_test_app() -> FastAPI:
    """
    Create an isolated FastAPI application for middleware tests.
    """
    app = FastAPI()

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/success")
    def success() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/client-error")
    def client_error() -> None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    @app.get("/server-error")
    def server_error() -> None:
        raise RuntimeError("Unexpected test failure")

    return app


def test_successful_request_generates_info_log(
    caplog,
) -> None:
    app = create_test_app()
    client = TestClient(app)

    with caplog.at_level(
        logging.INFO,
        logger="supplymind.middleware.request_logging",
    ):
        response = client.get(
            "/success",
            headers={
                "X-Correlation-ID": "middleware-success-001",
            },
        )

    assert response.status_code == 200

    matching_records = [
        record
        for record in caplog.records
        if record.name == "supplymind.middleware.request_logging"
    ]

    assert len(matching_records) == 1

    record = matching_records[0]

    assert record.levelno == logging.INFO
    assert record.http_method == "GET"
    assert record.http_path == "/success"
    assert record.http_status_code == 200
    assert record.duration_ms >= 0


def test_client_error_generates_warning_log(
    caplog,
) -> None:
    app = create_test_app()
    client = TestClient(app)

    with caplog.at_level(
        logging.WARNING,
        logger="supplymind.middleware.request_logging",
    ):
        response = client.get(
            "/client-error",
            headers={
                "X-Correlation-ID": "middleware-warning-001",
            },
        )

    assert response.status_code == 404

    matching_records = [
        record
        for record in caplog.records
        if record.name == "supplymind.middleware.request_logging"
    ]

    assert len(matching_records) == 1

    record = matching_records[0]

    assert record.levelno == logging.WARNING
    assert record.http_method == "GET"
    assert record.http_path == "/client-error"
    assert record.http_status_code == 404
    assert record.duration_ms >= 0


def test_unexpected_exception_generates_error_log(
    caplog,
) -> None:
    app = create_test_app()

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    with caplog.at_level(
        logging.ERROR,
        logger="supplymind.middleware.request_logging",
    ):
        response = client.get(
            "/server-error",
            headers={
                "X-Correlation-ID": "middleware-error-001",
            },
        )

    assert response.status_code == 500

    matching_records = [
        record
        for record in caplog.records
        if record.name == "supplymind.middleware.request_logging"
    ]

    assert len(matching_records) == 1

    record = matching_records[0]

    assert record.levelno == logging.ERROR
    assert record.http_method == "GET"
    assert record.http_path == "/server-error"
    assert record.http_status_code == 500
    assert record.duration_ms >= 0
    assert record.exc_info is not None
