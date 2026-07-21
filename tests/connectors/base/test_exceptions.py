"""
SupplyMind Enterprise AI

Connector Exception Tests

Tests the shared enterprise connector exception hierarchy.
"""

import pytest

from supplymind.connectors.base.exceptions import (
    ConnectorAuthenticationException,
    ConnectorAuthorizationException,
    ConnectorException,
    ConnectorRateLimitException,
    ConnectorResponseException,
    ConnectorTimeoutException,
    ConnectorUnavailableException,
)
from supplymind.core.errors.codes import ErrorCode
from supplymind.core.errors.exceptions import SupplyMindException


@pytest.mark.parametrize(
    ("exception_type", "expected_code"),
    [
        (
            ConnectorAuthenticationException,
            ErrorCode.CONNECTOR_AUTHENTICATION_ERROR,
        ),
        (
            ConnectorAuthorizationException,
            ErrorCode.CONNECTOR_AUTHORIZATION_ERROR,
        ),
        (
            ConnectorTimeoutException,
            ErrorCode.CONNECTOR_TIMEOUT_ERROR,
        ),
        (
            ConnectorRateLimitException,
            ErrorCode.CONNECTOR_RATE_LIMIT_ERROR,
        ),
        (
            ConnectorUnavailableException,
            ErrorCode.CONNECTOR_UNAVAILABLE_ERROR,
        ),
        (
            ConnectorResponseException,
            ErrorCode.CONNECTOR_RESPONSE_ERROR,
        ),
    ],
)
def test_connector_exception_assigns_expected_error_code(
    exception_type: type[ConnectorException],
    expected_code: ErrorCode,
) -> None:
    exception = exception_type(
        message="Connector operation failed.",
        details={"system": "example"},
    )

    assert exception.code == expected_code
    assert exception.message == "Connector operation failed."
    assert exception.details == {"system": "example"}
    assert str(exception) == "Connector operation failed."


def test_base_connector_exception_uses_generic_connector_code() -> None:
    exception = ConnectorException(
        message="Unexpected connector failure.",
    )

    assert exception.code == ErrorCode.CONNECTOR_ERROR
    assert exception.message == "Unexpected connector failure."
    assert exception.details is None


def test_connector_exception_inherits_from_supplymind_exception() -> None:
    exception = ConnectorTimeoutException(
        message="Connector request timed out.",
    )

    assert isinstance(exception, SupplyMindException)
    assert isinstance(exception, ConnectorException)
    assert isinstance(exception, Exception)
