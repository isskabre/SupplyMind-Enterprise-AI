"""System-level API endpoints."""

from fastapi import APIRouter, Depends

from supplymind.api.schemas import (
    ApiResponse,
    HealthData,
    LivenessData,
    ReadinessData,
    RootData,
    SystemInfoData,
    VersionData,
)

from supplymind.core.dependencies import get_system_service
from supplymind.services.system_service import SystemService

router = APIRouter(tags=["System"])


@router.get("/", response_model=ApiResponse[RootData])
def root(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[RootData]:
    """Return versioned API information."""

    return ApiResponse[RootData](
        message="Application information retrieved successfully.",
        data=RootData(**service.get_root()),
    )


@router.get("/health", response_model=ApiResponse[HealthData])
def health(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[HealthData]:
    """Return application health information."""

    return ApiResponse[HealthData](
        message="Health check successful.",
        data=HealthData(**service.get_health()),
    )


@router.get("/live", response_model=ApiResponse[LivenessData])
def live(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[LivenessData]:
    """
    Report whether the application process is alive.

    This endpoint intentionally avoids external dependency checks.
    """

    return ApiResponse[LivenessData](
        message="Liveness check successful.",
        data=LivenessData(**service.get_liveness()),
    )


@router.get("/ready", response_model=ApiResponse[ReadinessData])
def ready(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[ReadinessData]:
    """
    Report whether the application is ready to receive traffic.
    """

    return ApiResponse[ReadinessData](
        message="Readiness check successful.",
        data=ReadinessData(**service.get_readiness()),
    )


@router.get("/info", response_model=ApiResponse[SystemInfoData])
def info(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[SystemInfoData]:
    """
    Return operational metadata about the running application.
    """

    return ApiResponse[SystemInfoData](
        message="System information retrieved successfully.",
        data=SystemInfoData(**service.get_system_info()),
    )


@router.get("/version", response_model=ApiResponse[VersionData])
def version(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[VersionData]:
    """Return the current application version."""

    return ApiResponse[VersionData](
        message="Version retrieved successfully.",
        data=VersionData(**service.get_version()),
    )