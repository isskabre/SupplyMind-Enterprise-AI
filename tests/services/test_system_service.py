"""
Tests for system service diagnostics.
"""

from supplymind.services.system_service import SystemService
from supplymind.core.metadata import ApplicationMetadata

def create_test_metadata() -> ApplicationMetadata:
    """Return deterministic metadata for service tests."""

    return ApplicationMetadata(
        application="SupplyMind Test",
        version="9.9.9",
        environment="test",
        build_number="142",
        git_commit="abc1234",
        build_timestamp="2026-07-18T12:00:00Z",
        deployment_name="test-deployment",
        instance_id="test-instance",
        python_version="3.12.12",
        uptime_seconds=42.5,
    )

def test_liveness_reports_application_alive() -> None:
    service = SystemService()

    assert service.get_liveness() == {
        "alive": True,
    }


def test_readiness_reports_application_ready() -> None:
    service = SystemService()

    assert service.get_readiness() == {
        "ready": True,
    }


def test_system_info_contains_operational_metadata() -> None:
    service = SystemService()

    system_info = service.get_system_info()

    assert system_info["application"] == "SupplyMind Enterprise AI"
    assert system_info["version"] == "0.1.0"
    assert system_info["environment"] == "development"
    assert system_info["build_number"] is None
    assert system_info["git_commit"] is None
    assert system_info["build_timestamp"] is None
    assert system_info["deployment_name"] is None
    assert isinstance(system_info["instance_id"], str)
    assert system_info["instance_id"]
    assert system_info["uptime_seconds"] >= 0
    assert isinstance(system_info["python_version"], str)
    assert system_info["python_version"]

def test_service_uses_injected_metadata_provider() -> None:
    """System service should use its injected metadata provider."""

    metadata = create_test_metadata()

    service = SystemService(
        metadata_provider=lambda: metadata,
    )

    assert service.get_root() == {
        "application": "SupplyMind Test",
        "version": "9.9.9",
        "status": "running",
    }

    assert service.get_version() == {
        "version": "9.9.9",
    }

    assert service.get_system_info() == metadata.to_dict()