"""
SupplyMind Enterprise AI

Authentication Foundations

Public exports for shared authentication contracts, models, and exceptions.
"""

from supplymind.authentication.base.exceptions import (
    AuthenticationConfigurationException,
    AuthenticationException,
    CredentialUnavailableException,
    TokenAcquisitionException,
)
from supplymind.authentication.base.models import AuthenticationHeaders
from supplymind.authentication.base.protocols import (
    AuthenticationProviderProtocol,
)

__all__ = [
    "AuthenticationConfigurationException",
    "AuthenticationException",
    "AuthenticationHeaders",
    "AuthenticationProviderProtocol",
    "CredentialUnavailableException",
    "TokenAcquisitionException",
]