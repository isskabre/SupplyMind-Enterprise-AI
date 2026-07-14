"""Shared pytest fixtures for SupplyMind tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from supplymind.app import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client."""

    with TestClient(app) as test_client:
        yield test_client