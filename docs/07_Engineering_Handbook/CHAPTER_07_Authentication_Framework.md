---

# API Key Authentication Provider

The API Key Authentication Provider is the first concrete implementation of the SupplyMind authentication framework.

It converts an API key into immutable HTTP authentication headers while protecting credentials from accidental exposure.

## Architecture

```text
AuthenticationProviderProtocol
              │
              ▼
ApiKeyAuthenticationProvider
              │
              ▼
AuthenticationHeaders
              │
              ▼
Enterprise HTTP Client
```

The provider implements the common authentication protocol, allowing connectors to remain independent of authentication details.

---

# Supported Authentication Styles

The provider supports multiple enterprise authentication styles.

## Example 1

```http
X-API-Key: abc123
```

---

## Example 2

```http
api-key: abc123
```

---

## Example 3

```http
Authorization: Bearer abc123
```

This flexibility allows a single provider implementation to authenticate against many enterprise APIs.

---

# Security Features

The implementation follows several enterprise security practices.

## Hidden Credentials

API keys never appear in:

- Object representations
- Logging output
- Debugging sessions
- Exception messages

---

## Immutable Headers

Authentication headers are immutable after creation.

This prevents accidental modification before requests are sent.

---

## Configuration Validation

The provider validates configuration before it can be used.

Rejected configurations include:

- Empty API keys
- Empty header names
- Empty authentication prefixes

This follows the **Fail Fast** principle.

---

# Design Principles

This implementation demonstrates:

- Single Responsibility Principle (SRP)
- Dependency Inversion Principle (DIP)
- Protocol-Oriented Design
- Immutable Value Objects
- Defensive Copying
- Fail Fast Validation

---

# Future Authentication Providers

The authentication framework is designed to support additional authentication mechanisms without modifying connector implementations.

Planned providers include:

- Bearer Token Authentication
- OAuth2 Client Credentials
- Microsoft Entra ID
- Azure Managed Identity
- AWS IAM Authentication
- Google Service Account Authentication

Every authentication provider will implement:

```python
AuthenticationProviderProtocol
```

allowing connectors to authenticate without depending on specific implementations.

---

# Bearer Token Authentication Provider

## Overview

The Bearer Token Authentication Provider produces immutable HTTP Authorization headers using the standard Bearer authentication scheme.

Example:

```http
Authorization: Bearer eyJhbGciOi...
```

The provider is intentionally independent from token acquisition.

It accepts a validated bearer token and formats HTTP headers according to the HTTP Authorization standard.

---

## Design Principles

- immutable
- protocol-oriented
- security-first
- standard-compliant
- easily extensible

---

## Authentication Constants

The framework now provides shared constants for authentication providers.

```python
AUTHORIZATION_HEADER = "Authorization"

API_KEY_HEADER = "X-API-Key"

BEARER_PREFIX = "Bearer"
```

Centralizing these values removes duplicated literals and provides a consistent vocabulary across providers.

---

## Relationship to Future Providers

The Bearer Token Provider serves as the foundation for future authentication implementations.

Future providers will include:

- OAuth2 Client Credentials
- Microsoft Entra ID
- Managed Identity
- Token Cache
- Authentication Factory

These providers will focus on obtaining tokens while reusing the Bearer authentication model for HTTP requests.