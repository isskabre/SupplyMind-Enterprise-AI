"""System response schemas."""

from pydantic import BaseModel


# ------------------------------------------------------------------
# Existing Response Models
# ------------------------------------------------------------------


class HealthData(BaseModel):
    """Health endpoint response."""

    status: str


class VersionData(BaseModel):
    """Version endpoint response."""

    version: str


class RootData(BaseModel):
    """Root endpoint response."""

    application: str
    version: str
    status: str


# ------------------------------------------------------------------
# Enterprise Diagnostics Models
# ------------------------------------------------------------------


class LivenessData(BaseModel):
    """
    Indicates whether the application process is alive.
    """

    alive: bool


class ReadinessData(BaseModel):
    """
    Indicates whether the application is ready
    to receive production traffic.
    """

    ready: bool


class SystemInfoData(BaseModel):
    """
    Operational metadata about the running application.
    """

    application: str
    version: str
    environment: str
    uptime_seconds: float
    python_version: str