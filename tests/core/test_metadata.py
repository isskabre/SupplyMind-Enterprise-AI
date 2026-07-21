"""
Tests for application metadata.
"""

from dataclasses import FrozenInstanceError

import pytest

from supplymind.core.config import Settings
from supplymind.core.metadata import (
    ApplicationMetadata,
    build_application_metadata,
)


def test_metadata_is_built_from_settings() -> None:
    """Metadata should combine configuration and runtime values."""

    test_settings = Settings(
        app_name="SupplyMind Test",
        app_version="9.9.9",
        environment="test",
        build_number="142",
        git_commit="fd6e680",
        build_timestamp="2026-07-18T09:30:00Z",
        deployment_name="supplymind-test",
        _env_file=None,
    )

    metadata = build_application_metadata(test_settings)

    assert metadata.application == "SupplyMind Test"
    assert metadata.version == "9.9.9"
    assert metadata.environment == "test"
    assert metadata.build_number == "142"
    assert metadata.git_commit == "fd6e680"
    assert metadata.build_timestamp == "2026-07-18T09:30:00Z"
    assert metadata.deployment_name == "supplymind-test"
    assert metadata.instance_id
    assert metadata.python_version
    assert metadata.uptime_seconds >= 0


def test_metadata_preserves_missing_optional_values() -> None:
    """Optional build metadata should remain absent when not configured."""

    test_settings = Settings(
        _env_file=None,
    )

    metadata = build_application_metadata(test_settings)

    assert metadata.build_number is None
    assert metadata.git_commit is None
    assert metadata.build_timestamp is None
    assert metadata.deployment_name is None


def test_metadata_can_be_converted_to_dictionary() -> None:
    """Metadata should provide a dictionary representation."""

    metadata = ApplicationMetadata(
        application="SupplyMind Test",
        version="1.0.0",
        environment="testing",
        build_number=None,
        git_commit=None,
        build_timestamp=None,
        deployment_name=None,
        instance_id="test-instance",
        python_version="3.12.12",
        uptime_seconds=10.5,
    )

    result = metadata.to_dict()

    assert result["application"] == "SupplyMind Test"
    assert result["instance_id"] == "test-instance"
    assert result["uptime_seconds"] == 10.5


def test_metadata_is_immutable() -> None:
    """Application metadata should not be mutable after creation."""

    metadata = ApplicationMetadata(
        application="SupplyMind Test",
        version="1.0.0",
        environment="testing",
        build_number=None,
        git_commit=None,
        build_timestamp=None,
        deployment_name=None,
        instance_id="test-instance",
        python_version="3.12.12",
        uptime_seconds=10.5,
    )

    with pytest.raises(FrozenInstanceError):
        metadata.version = "2.0.0"
