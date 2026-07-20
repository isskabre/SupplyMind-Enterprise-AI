# Chapter 07 — Authentication Framework

---

# Authentication Framework Overview

The SupplyMind Authentication Framework provides a consistent, secure, and extensible mechanism for authenticating outbound requests to enterprise services.

Rather than embedding authentication logic directly inside connectors, authentication responsibilities are delegated to dedicated provider implementations that all conform to a common protocol.

This design follows the Dependency Inversion Principle (DIP), allowing connectors to depend only on abstractions while remaining independent of specific authentication mechanisms.

Current authentication providers include:

- API Key Authentication Provider
- Bearer Token Authentication Provider

Future implementations will extend the framework with OAuth2, Microsoft Entra ID, Azure Managed Identity, AWS IAM, and other enterprise authentication mechanisms without requiring changes to connector implementations.

---

# Authentication Framework Architecture

```text
                    Enterprise Connector
                            │
                            ▼
              AuthenticationProviderProtocol
                            ▲
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
ApiKeyAuthenticationProvider   BearerTokenAuthenticationProvider
              │                           │
              └─────────────┬─────────────┘
                            ▼
                 AuthenticationHeaders
                            │
                            ▼
                 Enterprise HTTP Client
```

The connector depends only on the `AuthenticationProviderProtocol`.

Each provider is responsible for producing immutable authentication headers, allowing the HTTP client to remain completely independent of authentication details.

---

# API Key Authentication Provider

The API Key Authentication Provider is the first concrete implementation of the SupplyMind Authentication Framework.

It converts an API key into immutable HTTP authentication headers while protecting credentials from accidental exposure.

---

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

## Standard API Key

```http
X-API-Key: abc123
```

---

## Custom Header

```http
api-key: abc123
```

---

## Authorization Header

```http
Authorization: Bearer abc123
```

Although bearer authentication now has its own dedicated provider, this flexibility remains useful for enterprise APIs that expect API keys inside the Authorization header.

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

# Bearer Token Authentication Provider

## Overview

The Bearer Token Authentication Provider produces immutable HTTP Authorization headers using the standard Bearer authentication scheme.

Example:

```http
Authorization: Bearer eyJhbGciOi...
```

The provider is intentionally independent of token acquisition.

Its sole responsibility is to transform an already validated bearer token into immutable HTTP Authorization headers.

This separation of concerns allows OAuth2 providers, Microsoft Entra ID providers, Azure Managed Identity providers, and future authentication mechanisms to focus exclusively on obtaining tokens while reusing the same HTTP authentication implementation.

---

## Architecture

```text
AuthenticationProviderProtocol
              │
              ▼
BearerTokenAuthenticationProvider
              │
              ▼
AuthenticationHeaders
              │
              ▼
Enterprise HTTP Client
```

---

## Security Features

The Bearer Token Authentication Provider follows the same enterprise security principles as the API Key provider.

Bearer tokens are never exposed through:

- Object representations
- Logging output
- Exception messages
- Debugging sessions

Configuration is validated during construction, ensuring invalid providers cannot be instantiated.

---

## Design Principles

The implementation emphasizes:

- Immutable design
- Protocol-oriented architecture
- Security-first implementation
- Standard-compliant HTTP authentication
- Separation of concerns
- Future extensibility

---

# Authentication Constants

The authentication framework provides shared constants to eliminate duplicated string literals across authentication providers.

```python
AUTHORIZATION_HEADER = "Authorization"

API_KEY_HEADER = "X-API-Key"

BEARER_PREFIX = "Bearer"
```

Centralizing these values improves consistency, readability, and maintainability while establishing a common authentication vocabulary across the framework.

---

# Future Authentication Providers

The authentication framework is designed to support additional enterprise authentication mechanisms without modifying connector implementations.

Planned providers include:

- OAuth2 Client Credentials
- Microsoft Entra ID
- Azure Managed Identity
- AWS IAM Authentication
- Google Service Account Authentication

Every authentication provider implements:

```python
AuthenticationProviderProtocol
```

allowing connectors to authenticate without depending on specific implementations.

---

---

# Authentication Factory

## Overview

The `AuthenticationFactory` centralizes the creation of authentication provider implementations.

Instead of allowing connectors to instantiate concrete providers directly, the factory provides a stable construction API and returns objects that satisfy the shared `AuthenticationProviderProtocol`.

Example:

```python
provider = AuthenticationFactory.create_api_key(
    api_key="secret",
)
```

or:

```python
provider = AuthenticationFactory.create_bearer(
    token="access-token",
)
```

---

## Architecture

```text
                 Enterprise Connector
                          │
                          ▼
              AuthenticationFactory
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
ApiKeyAuthenticationProvider   BearerTokenAuthenticationProvider
              │                       │
              └───────────┬───────────┘
                          ▼
         AuthenticationProviderProtocol
                          │
                          ▼
             AuthenticationHeaders
                          │
                          ▼
             Enterprise HTTP Client
```

The connector does not need to understand how providers are constructed.

It only requires the behavior defined by:

```python
AuthenticationProviderProtocol
```

---

## Supported Creation Methods

The current factory provides:

```python
AuthenticationFactory.create_api_key(...)
```

and:

```python
AuthenticationFactory.create_bearer(...)
```

The explicit method design keeps the current implementation simple and easy to understand.

A future implementation will introduce strongly typed authentication configuration models and may evolve the factory toward a generic API:

```python
AuthenticationFactory.create(configuration)
```

---

## Factory Responsibilities

The factory is responsible for:

- Selecting the correct concrete provider
- Forwarding provider configuration
- Applying shared defaults
- Returning the common authentication abstraction

The factory is not responsible for:

- Validating credentials
- Producing authentication headers
- Acquiring OAuth2 tokens
- Caching access tokens
- Sending HTTP requests
- Managing connector lifecycle

These responsibilities remain in their appropriate layers.

---

## Stateless Design

The factory maintains no internal state.

Its methods are implemented as static methods because provider creation does not require:

- Factory configuration
- Dependency injection
- Mutable state
- Resource lifecycle
- Instance-level behavior

Each factory call creates a new independent provider instance.

---


## Why Use a Factory?

Without a factory, every connector would need to know which authentication provider to instantiate.

```python
provider = ApiKeyAuthenticationProvider(...)
```

or

```python
provider = BearerTokenAuthenticationProvider(...)
```

As the number of authentication mechanisms grows, connector implementations would become tightly coupled to concrete authentication classes.

Instead, connectors delegate provider creation to the Authentication Factory:

```python
provider = AuthenticationFactory.create_api_key(...)
```

or

```python
provider = AuthenticationFactory.create_bearer(...)
```

This keeps authentication creation centralized and allows connectors to depend only on the shared `AuthenticationProviderProtocol`.

The result is a cleaner architecture with lower coupling and improved extensibility.

## Error Handling

---

The factory allows provider configuration exceptions to propagate directly.

For example, an invalid API key continues to raise:

```python
AuthenticationConfigurationException
```

The factory does not catch and recreate the exception because doing so would duplicate validation logic and reduce diagnostic clarity.

---

## Design Principles

The Authentication Factory demonstrates:

- Factory Pattern
- Dependency Inversion Principle
- Separation of Concerns
- Single Responsibility Principle
- Stateless Design
- Incremental Architecture
- Protocol-Oriented Programming

---

## Future Evolution

The factory will evolve alongside the authentication framework.

Planned improvements include:

- Authentication Configuration Models
- Generic configuration-driven provider creation
- OAuth2 Client Credentials Provider creation
- Microsoft Entra ID Provider creation
- Azure Managed Identity Provider creation
- Dependency injection integration

The factory will remain the centralized construction boundary while provider implementations continue to own authentication behavior.

---

# Current Framework Status

## Implemented

- Authentication protocol
- Authentication models
- Authentication exception hierarchy
- Authentication constants
- API Key Authentication Provider
- Bearer Token Authentication Provider
- Authentication Factory
---

## Planned

- Authentication Configuration Models
- OAuth2 Client Credentials Provider
- Access Token Model
- OAuth2 Token Cache
- Microsoft Entra ID Provider
- Azure Managed Identity Provider
- AWS IAM Authentication
- Google Service Account Authentication

---

# Enterprise Best Practices

The SupplyMind Authentication Framework follows several enterprise engineering principles:

- Keep authentication independent from connectors.
- Separate token acquisition from request authentication.
- Prefer immutable authentication models.
- Never expose credentials through object representations or exceptions.
- Validate configuration during construction.
- Depend on protocols rather than concrete implementations.
- Centralize shared authentication constants.
- Keep providers focused on a single responsibility.

These practices make the framework easier to test, easier to extend, and significantly more secure.

---