"""
SupplyMind Enterprise AI

Authentication Model Tests
"""

from dataclasses import FrozenInstanceError

import pytest

from supplymind.authentication.base.models import AuthenticationHeaders


def test_authentication_headers_returns_standard_dictionary() -> None:
    headers = AuthenticationHeaders(
        {
            "Authorization": "Bearer secret-token",
            "Accept": "application/json",
        }
    )

    assert headers.as_dict() == {
        "Authorization": "Bearer secret-token",
        "Accept": "application/json",
    }


def test_authentication_headers_defensively_copies_input() -> None:
    source_headers = {
        "Authorization": "Bearer original-token",
    }

    headers = AuthenticationHeaders(source_headers)

    source_headers["Authorization"] = "Bearer changed-token"

    assert headers.as_dict() == {
        "Authorization": "Bearer original-token",
    }


def test_authentication_headers_returns_independent_copy() -> None:
    headers = AuthenticationHeaders(
        {
            "Authorization": "Bearer secret-token",
        }
    )

    request_headers = headers.as_dict()
    request_headers["Authorization"] = "Bearer modified-token"

    assert headers.as_dict() == {
        "Authorization": "Bearer secret-token",
    }


def test_authentication_headers_hides_secrets_from_representation() -> None:
    headers = AuthenticationHeaders(
        {
            "Authorization": "Bearer highly-sensitive-token",
        }
    )

    representation = repr(headers)

    assert "highly-sensitive-token" not in representation
    assert "Authorization" not in representation


def test_authentication_headers_is_frozen() -> None:
    headers = AuthenticationHeaders(
        {
            "Authorization": "Bearer secret-token",
        }
    )

    with pytest.raises(FrozenInstanceError):
        headers._values = {}  # type: ignore[misc]


def test_authentication_headers_normalizes_values_to_strings() -> None:
    headers = AuthenticationHeaders(
        {
            "X-Client-ID": 12345,  # type: ignore[dict-item]
        }
    )

    assert headers.as_dict() == {
        "X-Client-ID": "12345",
    }