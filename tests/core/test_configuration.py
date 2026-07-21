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
    assert exception.message == ("Application configuration validation failed.")
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


def test_build_metadata_defaults_to_none() -> None:
    """Optional build metadata should not be invented locally."""

    test_settings = Settings(
        _env_file=None,
    )

    assert test_settings.build_number is None
    assert test_settings.git_commit is None
    assert test_settings.build_timestamp is None
    assert test_settings.deployment_name is None


def test_build_metadata_can_be_configured() -> None:
    """Build metadata should accept values supplied by a pipeline."""

    test_settings = Settings(
        build_number="142",
        git_commit="fd6e680",
        build_timestamp="2026-07-18T09:30:00Z",
        deployment_name="supplymind-development",
        _env_file=None,
    )

    assert test_settings.build_number == "142"
    assert test_settings.git_commit == "fd6e680"
    assert test_settings.build_timestamp == "2026-07-18T09:30:00Z"
    assert test_settings.deployment_name == "supplymind-development"


def test_http_timeout_uses_default_value() -> None:
    """HTTP timeout should have a safe platform default."""

    settings = Settings()

    assert settings.http_timeout_seconds == 10.0


def test_http_timeout_rejects_non_positive_value() -> None:
    """HTTP timeout must be greater than zero."""

    with pytest.raises(
        ValueError,
        match="http_timeout_seconds must be greater than zero",
    ):
        Settings(http_timeout_seconds=0)
