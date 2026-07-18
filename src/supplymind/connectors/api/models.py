"""
SupplyMind Enterprise AI

HTTP Connector Models

Defines framework-independent models used by the enterprise HTTP
client layer.
"""

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class HttpResponse:
    """
    Represent a normalized response from an external HTTP service.

    Attributes:
        status_code: HTTP status code returned by the external service.
        headers: Response headers represented as a string mapping.
        content: Raw response body as bytes.
    """

    status_code: int
    headers: dict[str, str] = field(default_factory=dict)
    content: bytes = b""

    @property
    def is_success(self) -> bool:
        """
        Return whether the response has a successful HTTP status code.

        Returns:
            True for HTTP status codes from 200 through 299.
        """

        return 200 <= self.status_code < 300

    @property
    def text(self) -> str:
        """
        Decode the response body as UTF-8 text.

        Returns:
            The decoded response body.
        """

        return self.content.decode("utf-8")

    def json(self) -> Any:
        """
        Deserialize the response body as JSON.

        Returns:
            The deserialized JSON-compatible Python value.

        Raises:
            json.JSONDecodeError: If the response body is not valid JSON.
        """

        return json.loads(self.content)