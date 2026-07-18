"""
Tests for system service diagnostics.
"""

from supplymind.services.system_service import SystemService


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
    assert system_info["uptime_seconds"] >= 0
    assert isinstance(system_info["python_version"], str)
    assert system_info["python_version"]