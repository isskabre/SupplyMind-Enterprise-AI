"""System response schemas."""

from pydantic import BaseModel


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