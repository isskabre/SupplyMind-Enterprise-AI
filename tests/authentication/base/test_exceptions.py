"""
SupplyMind Enterprise AI

Authentication Exception Tests
"""

import pytest

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
    AuthenticationException,
    CredentialUnavailableException,
    TokenAcquisitionException,
)
from supplymind.core.errors.codes import ErrorCode
from supplymind.core.errors.exceptions import SupplyMindException


@pytest.mark.parametrize(
    ("exception_type", "expected_code"),
    [
        (
            AuthenticationConfigurationException,
            ErrorCode.AUTHENTICATION_CONFIGURATION_ERROR,
        ),
        (
            CredentialUnavailableException,
            ErrorCode.CREDENTIAL_UNAVAILABLE_ERROR,
        ),
        (
            TokenAcquisitionException,
            ErrorCode.TOKEN_ACQUISITION_ERROR,
        ),
    ],
)
def test_authentication_exception_assigns_expected_error_code(
    exception_type: type[AuthenticationException],
    expected_code: ErrorCode,
) -> None:
    exception = exception_type(
        message="Authentication operation failed.",
        details={"provider": "example"},
    )

    assert exception.code == expected_code
    assert exception.message == "Authentication operation failed."
    assert exception.details == {"provider": "example"}
    assert str(exception) == "Authentication operation failed."


def test_base_authentication_exception_uses_generic_code() -> None:
    exception = AuthenticationException(
        message="Unexpected authentication failure.",
    )

    assert exception.code == ErrorCode.AUTHENTICATION_PROVIDER_ERROR
    assert exception.message == ("Unexpected authentication failure.")
    assert exception.details is None


def test_authentication_exception_inherits_from_supplymind_exception() -> None:
    exception = TokenAcquisitionException(
        message="Unable to acquire token.",
    )

    assert isinstance(exception, SupplyMindException)
    assert isinstance(exception, AuthenticationException)
    assert isinstance(exception, Exception)
