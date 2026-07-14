"""
SupplyMind Enterprise AI

Correlation ID Middleware Tests
"""

from uuid import UUID

from fastapi.testclient import TestClient

from supplymind.app import app


client = TestClient(app)


def test_correlation_id_is_generated() -> None:
    """
    Verify that the API generates a correlation ID when none is supplied.
    """
    response = client.get("/")

    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers

    generated_correlation_id = response.headers["X-Correlation-ID"]

    UUID(generated_correlation_id)


def test_incoming_correlation_id_is_preserved() -> None:
    """
    Verify that an incoming correlation ID is returned unchanged.
    """
    expected_correlation_id = "supplymind-test-123"

    response = client.get(
        "/",
        headers={
            "X-Correlation-ID": expected_correlation_id,
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["X-Correlation-ID"]
        == expected_correlation_id
    )