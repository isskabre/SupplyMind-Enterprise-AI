"""Tests for system API endpoints."""

from collections.abc import Callable

from fastapi.testclient import TestClient

from supplymind.app import app
from supplymind.core.dependencies import get_system_service
from supplymind.core.metadata import ApplicationMetadata
from supplymind.services.system_service import SystemService


def test_application_root_endpoint(client: TestClient) -> None:
    """Application root should return basic platform information."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "SupplyMind Enterprise AI",
        "version": "0.1.0",
        "status": "running",
    }


def test_versioned_root_endpoint(client: TestClient) -> None:
    """Versioned root should return the enterprise response contract."""

    response = client.get("/api/v1/")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Application information retrieved successfully."
    assert body["data"]["application"] == "SupplyMind Enterprise AI"
    assert body["data"]["version"] == "0.1.0"
    assert body["data"]["status"] == "running"


def test_health_endpoint(client: TestClient) -> None:
    """Health endpoint should report a healthy application."""

    response = client.get("/api/v1/health")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Health check successful."
    assert body["data"] == {"status": "healthy"}


def test_liveness_endpoint(client: TestClient) -> None:
    """Liveness endpoint should report that the process is alive."""

    response = client.get("/api/v1/live")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Liveness check successful."
    assert body["data"] == {
        "alive": True,
    }


def test_readiness_endpoint(client: TestClient) -> None:
    """Readiness endpoint should report that traffic can be accepted."""

    response = client.get("/api/v1/ready")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Readiness check successful."
    assert body["data"] == {
        "ready": True,
    }


def test_system_info_endpoint(client: TestClient) -> None:
    """System information endpoint should expose runtime metadata."""

    response = client.get("/api/v1/info")

    assert response.status_code == 200

    body = response.json()
    data = body["data"]

    assert body["success"] is True
    assert body["message"] == "System information retrieved successfully."
    assert data["application"] == "SupplyMind Enterprise AI"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "development"
    assert data["uptime_seconds"] >= 0
    assert isinstance(data["python_version"], str)
    assert data["python_version"]
    assert data["build_number"] is None
    assert data["git_commit"] is None
    assert data["build_timestamp"] is None
    assert data["deployment_name"] is None
    assert isinstance(data["instance_id"], str)
    assert data["instance_id"]


def test_version_endpoint(client: TestClient) -> None:
    """Version endpoint should return the current application version."""

    response = client.get("/api/v1/version")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Version retrieved successfully."
    assert body["data"] == {"version": "0.1.0"}


def test_unknown_endpoint_returns_enterprise_error(
    client: TestClient,
) -> None:
    """Unknown routes should use the enterprise error contract."""

    response = client.get("/api/v1/does-not-exist")

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert body["error"]["message"] == "Not Found"
    assert body["error"]["details"] is None
    assert body["meta"] is None


def test_system_service_dependency_can_be_overridden(
    client: TestClient,
) -> None:
    """System endpoints should support FastAPI dependency overrides."""

    metadata = ApplicationMetadata(
        application="SupplyMind Override",
        version="8.8.8",
        environment="test",
        build_number="9001",
        git_commit="override123",
        build_timestamp="2026-07-18T15:00:00Z",
        deployment_name="override-deployment",
        instance_id="override-instance",
        python_version="3.12.12",
        uptime_seconds=123.45,
    )

    def override_system_service() -> SystemService:
        return SystemService(
            metadata_provider=lambda: metadata,
        )

    app.dependency_overrides[get_system_service] = override_system_service

    try:
        response = client.get("/api/v1/info")
    finally:
        app.dependency_overrides.pop(
            get_system_service,
            None,
        )

    assert response.status_code == 200

    body = response.json()
    data = body["data"]

    assert data["application"] == "SupplyMind Override"
    assert data["version"] == "8.8.8"
    assert data["environment"] == "test"
    assert data["build_number"] == "9001"
    assert data["git_commit"] == "override123"
    assert data["deployment_name"] == "override-deployment"
    assert data["instance_id"] == "override-instance"
    assert data["uptime_seconds"] == 123.45


def test_system_service_override_fixture(
    client: TestClient,
    override_system_service: Callable[[SystemService], None],
) -> None:
    """The shared fixture should install and clean up an override."""

    metadata = ApplicationMetadata(
        application="Fixture Override",
        version="7.7.7",
        environment="test",
        build_number=None,
        git_commit=None,
        build_timestamp=None,
        deployment_name=None,
        instance_id="fixture-instance",
        python_version="3.12.12",
        uptime_seconds=77.7,
    )

    service = SystemService(
        metadata_provider=lambda: metadata,
    )

    override_system_service(service)

    response = client.get("/api/v1/version")

    assert response.status_code == 200
    assert response.json()["data"] == {
        "version": "7.7.7",
    }
