"""Shared pytest fixtures for SupplyMind tests."""

from collections.abc import Callable, Generator
from supplymind.core.dependencies import get_system_service
from supplymind.services.system_service import SystemService

import pytest
from fastapi.testclient import TestClient

from supplymind.app import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client."""

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def override_system_service() -> Generator[
    Callable[[SystemService], None],
    None,
    None,
]:
    """
    Provide a helper for overriding the SystemService dependency.
    """

    def apply_override(service: SystemService) -> None:
        app.dependency_overrides[get_system_service] = lambda: service

    yield apply_override

    app.dependency_overrides.pop(
        get_system_service,
        None,
    )
