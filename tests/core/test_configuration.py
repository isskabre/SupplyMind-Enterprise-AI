"""Tests for application configuration and startup policies."""

import pytest
from pydantic import ValidationError

from supplymind.core.config import Settings
from supplymind.core.configuration_validator import validate_configuration
from supplymind.core.enums import Environment
from supplymind.core.errors.codes import ErrorCode
from supplymind.core.errors.exceptions import ConfigurationException


def test_default_configuration_is_valid() -> None:
    """Default development settings should satisfy startup policies."""

    settings = Settings()

    validate_configuration(settings)

    assert settings.environment == Environment.DEVELOPMENT
    assert settings.is_development is True
    assert settings.is_testing is False
    assert settings.is_production is False


def test_log_level_is_normalized_to_uppercase() -> None:
    """Logging levels should be normalized during settings creation."""

    settings = Settings(log_level="warning")

    assert settings.log_level == "WARNING"


def test_invalid_log_level_is_rejected() -> None:
    """Unsupported logging levels should fail immediately."""

    with pytest.raises(ValidationError):
        Settings(log_level="LOUD")


def test_testing_environment_helper() -> None:
    """Testing settings should expose the correct helper properties."""

    settings = Settings(
        environment=Environment.TEST,
        debug=False,
    )

    assert settings.is_development is False
    assert settings.is_testing is True
    assert settings.is_production is False


def test_production_debug_mode_is_rejected() -> None:
    """Production configuration must not enable debug mode."""

    settings = Settings(
        environment=Environment.PRODUCTION,
        debug=True,
    )

    with pytest.raises(ConfigurationException) as exception_info:
        validate_configuration(settings)

    exception = exception_info.value

    assert exception.code == ErrorCode.CONFIGURATION_ERROR
    assert exception.message == (
        "Application configuration validation failed."
    )
    assert exception.details == {
        "errors": [
            "debug must be disabled when running in production.",
        ]
    }


def test_valid_production_configuration_passes() -> None:
    """Production settings should pass when debug mode is disabled."""

    settings = Settings(
        environment=Environment.PRODUCTION,
        debug=False,
    )

    validate_configuration(settings)

    assert settings.is_production is True