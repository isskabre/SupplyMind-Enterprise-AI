"""Central API router configuration."""

from fastapi import APIRouter

from supplymind.api.v1.system import router as system_router
from supplymind.core.constants import API_VERSION

api_router = APIRouter(prefix=f"/api/{API_VERSION}")

api_router.include_router(system_router)
