"""
SupplyMind Enterprise AI

Authentication Protocols

Defines the common contract implemented by authentication providers.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from supplymind.authentication.base.models import AuthenticationHeaders


@runtime_checkable
class AuthenticationProviderProtocol(Protocol):
    """
    Contract implemented by enterprise authentication providers.
    """

    async def get_headers(self) -> AuthenticationHeaders:
        """
        Produce authentication headers for an external request.

        Returns:
            Secure authentication headers for the request.
        """
        ...
