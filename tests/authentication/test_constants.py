"""
SupplyMind Enterprise AI

Authentication Constants Tests
"""

from supplymind.authentication.constants import (
    API_KEY_HEADER,
    AUTHORIZATION_HEADER,
    BEARER_PREFIX,
)


def test_authentication_constants() -> None:
    """
    Verify the shared authentication constant values.
    """
    assert API_KEY_HEADER == "X-API-Key"
    assert AUTHORIZATION_HEADER == "Authorization"
    assert BEARER_PREFIX == "Bearer"