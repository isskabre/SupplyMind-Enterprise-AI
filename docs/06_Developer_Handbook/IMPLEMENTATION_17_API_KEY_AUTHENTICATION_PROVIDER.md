# Implementation 17 — API Key Authentication Provider

---

# 1. Business Objective

Many enterprise services authenticate API requests using API keys.

Instead of allowing every connector to build authentication headers independently, SupplyMind centralizes this responsibility into reusable authentication providers.

This implementation introduces the first concrete authentication provider based on the common `AuthenticationProviderProtocol`.

## Business Benefits

- Consistent authentication behavior
- Reduced code duplication
- Improved security
- Easier testing
- Reusable authentication across enterprise connectors

---

# 2. Enterprise Concepts

API Key authentication is one of the most common authentication mechanisms used by enterprise APIs.

Examples include:

- OpenAI
- Anthropic
- Pinecone
- Azure Cognitive Services
- Internal Enterprise REST APIs

Instead of embedding authentication logic inside every connector, connectors delegate authentication to an authentication provider.

```text
Connector
      │
      ▼
AuthenticationProvider
      │
      ▼
AuthenticationHeaders
      │
      ▼
Enterprise HTTP Client
```

This keeps authentication independent from connector implementations.

---

# 3. Architecture Decision

The API Key Authentication Provider has a single responsibility:

> Produce authentication headers.

The provider does **not**:

- Send HTTP requests
- Refresh access tokens
- Communicate with external services
- Know anything about connectors

This follows the **Single Responsibility Principle (SRP)** and **Dependency Inversion Principle (DIP)**.

---

# 4. Implementation

## New Package

```text
src/supplymind/authentication/providers/
```

## Implemented

- `ApiKeyAuthenticationProvider`
- Provider package exports
- Unit test package

The provider:

- Implements `AuthenticationProviderProtocol`
- Produces immutable `AuthenticationHeaders`
- Supports configurable header names
- Supports optional authentication prefixes
- Validates configuration during construction
- Prevents credential leakage through object representations

Examples:

```http
Authorization: Bearer <token>
```

```http
X-API-Key: <key>
```

```http
api-key: <key>
```

---

# 5. Validation Rules

The provider validates:

- API key cannot be empty
- Header name cannot be empty
- Prefix cannot contain only whitespace

Configuration values are normalized by trimming surrounding whitespace.

The provider follows a **Fail Fast** approach by rejecting invalid configuration during construction.

---

# 6. Security Considerations

Several design decisions reduce accidental credential exposure.

## Secret-safe representation

The API key is excluded from object representations.

```python
repr(provider)
```

does not reveal credentials.

---

## Immutable headers

Returned authentication headers are immutable.

This prevents accidental modification after creation.

---

## Defensive copying

Header dictionaries are copied before storage.

External code cannot modify the provider's internal state.

---

# 7. Testing

The implementation includes comprehensive unit tests covering:

- Default header generation
- Custom header names
- Prefix support
- Configuration normalization
- Protocol implementation
- Configuration validation
- Secret-safe object representation
- Secret-safe exception messages

Regression status:

```
115 automated tests passing
```

---

# 8. Files Added

```text
src/supplymind/authentication/providers/
    __init__.py
    api_key.py

tests/authentication/providers/
    __init__.py
    test_api_key.py
```

---

# 9. What We Learned

This implementation reinforced several enterprise engineering concepts:

- Protocol-oriented programming
- Dependency inversion
- Immutable value objects
- Defensive copying
- Secure handling of secrets
- Fail Fast validation
- Enterprise testing practices

---

# 10. Enterprise Best Practices

✔ Keep authentication separate from connectors

✔ Never expose credentials through object representations

✔ Validate configuration during object construction

✔ Return immutable authentication headers

✔ Depend on protocols rather than concrete implementations

✔ Keep authentication providers focused on a single responsibility

---

# Next Implementation

**Implementation 18 — Bearer Token Authentication Provider**

This implementation will introduce bearer-token authentication while preparing the framework for OAuth2, Microsoft Entra ID, and cloud identity providers.