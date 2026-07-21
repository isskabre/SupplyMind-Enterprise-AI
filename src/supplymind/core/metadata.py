"""
SupplyMind Enterprise AI

Application Metadata

Defines immutable application, build, deployment, and runtime metadata.
"""

import platform
import socket
from dataclasses import asdict, dataclass
from typing import Any

from supplymind.core.config import Settings, settings
from supplymind.core.runtime import get_uptime_seconds


@dataclass(frozen=True, slots=True)
class ApplicationMetadata:
    """
    Immutable metadata describing the running application instance.
    """

    application: str
    version: str
    environment: str
    build_number: str | None
    git_commit: str | None
    build_timestamp: str | None
    deployment_name: str | None
    instance_id: str
    python_version: str
    uptime_seconds: float

    def to_dict(self) -> dict[str, Any]:
        """
        Return metadata as a dictionary.
        """
        return asdict(self)


def get_instance_id() -> str:
    """
    Return a stable identifier for the current host or container.

    In local development this is usually the computer hostname.
    In container platforms it commonly resolves to the container
    or pod hostname.
    """
    return socket.gethostname()


def build_application_metadata(
    application_settings: Settings = settings,
) -> ApplicationMetadata:
    """
    Build metadata for the running application instance.
    """
    return ApplicationMetadata(
        application=application_settings.app_name,
        version=application_settings.app_version,
        environment=application_settings.environment.value,
        build_number=application_settings.build_number,
        git_commit=application_settings.git_commit,
        build_timestamp=application_settings.build_timestamp,
        deployment_name=application_settings.deployment_name,
        instance_id=get_instance_id(),
        python_version=platform.python_version(),
        uptime_seconds=get_uptime_seconds(),
    )
