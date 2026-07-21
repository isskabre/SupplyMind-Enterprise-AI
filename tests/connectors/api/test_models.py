"""
Tests for enterprise HTTP connector models.
"""

import json

import pytest

from supplymind.connectors.api.models import HttpResponse


def test_http_response_exposes_success_status() -> None:
    """A 2xx response should be identified as successful."""

    response = HttpResponse(status_code=200)

    assert response.is_success is True


def test_http_response_rejects_non_success_status() -> None:
    """A non-2xx response should not be identified as successful."""

    response = HttpResponse(status_code=404)

    assert response.is_success is False


def test_http_response_decodes_text_content() -> None:
    """Text should be decoded from the raw response bytes."""

    response = HttpResponse(
        status_code=200,
        content=b"SupplyMind",
    )

    assert response.text == "SupplyMind"


def test_http_response_deserializes_json_content() -> None:
    """JSON content should deserialize into Python values."""

    response = HttpResponse(
        status_code=200,
        content=b'{"status": "healthy"}',
    )

    assert response.json() == {
        "status": "healthy",
    }


def test_http_response_rejects_invalid_json() -> None:
    """Invalid JSON content should preserve the standard JSON error."""

    response = HttpResponse(
        status_code=200,
        content=b"not-json",
    )

    with pytest.raises(json.JSONDecodeError):
        response.json()
