"""
SupplyMind Enterprise AI

Authentication Models

Shared models used by enterprise authentication providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class AuthenticationHeaders:
    """
    Immutable HTTP headers produced by an authentication provider.

    Header values are excluded from the object's representation to reduce
    the risk of credentials appearing in logs or debugging output.
    """

    _values: Mapping[str, str] = field(
        repr=False,
    )

    def __post_init__(self) -> None:
        """
        Create a defensive, immutable copy of the supplied headers.
        """
        normalized_headers = {
            str(name): str(value)
            for name, value in self._values.items()
        }

        object.__setattr__(
            self,
            "_values",
            MappingProxyType(normalized_headers),
        )

    def as_dict(self) -> dict[str, str]:
        """
        Return a mutable copy suitable for an HTTP request.

        Returns:
            Authentication headers as a standard dictionary.
        """
        return dict(self._values)