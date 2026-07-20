# Implementation 19 — Enterprise Authentication Factory

---

# 1. Business Objective

Enterprise connectors should not be responsible for constructing authentication providers directly.

Without a centralized creation mechanism, each connector could duplicate provider construction logic and become coupled to concrete authentication implementations.

This implementation introduces the `AuthenticationFactory`, which centralizes the creation of authentication providers while exposing the common `AuthenticationProviderProtocol` abstraction.

## Business Benefits

- Centralized provider construction
- Reduced duplication across connectors
- Consistent authentication configuration
- Easier testing and maintenance
- Reduced coupling to concrete providers
- Clear extension path for future authentication mechanisms

---

# 2. Enterprise Concepts

## Factory Pattern

The Factory Pattern centralizes object creation behind a dedicated API.

Instead of constructing providers directly:

```python
provider = ApiKeyAuthenticationProvider(
    api_key="secret",
)
```

callers can use:

```python
provider = AuthenticationFactory.create_api_key(
    api_key="secret",
)
```

The factory owns the construction decision while the caller receives an object that satisfies the shared authentication contract.

## Object Creation Responsibility

Object creation is a separate architectural responsibility.

Without a factory, connectors may need to know:

- Which provider class to instantiate
- Which arguments each provider requires
- Which defaults should be used
- How provider construction may evolve

The factory removes those concerns from connector implementations.

---

# 3. Architecture Decision

The first version of the factory exposes two explicit static methods:

```python
AuthenticationFactory.create_api_key(...)
AuthenticationFactory.create_bearer(...)
```

This design was chosen because the authentication framework currently contains two concrete providers.

A generic configuration-driven factory was intentionally deferred until strongly typed authentication configuration models are introduced.

This incremental approach keeps the implementation small while establishing a stable creation layer.

## Architecture

```text
Enterprise Connector
        │
        ▼
AuthenticationFactory
        │
        ├──────────────────────────────┐
        │                              │
        ▼                              ▼
ApiKeyAuthenticationProvider   BearerTokenAuthenticationProvider
        │                              │
        └──────────────┬───────────────┘
                       ▼
         AuthenticationProviderProtocol
                       │
                       ▼
            AuthenticationHeaders
```

---

# 4. Step-by-Step Coding

## Factory Module

Created:

```text
src/supplymind/authentication/factory.py
```

Implemented:

```python
class AuthenticationFactory:
    @staticmethod
    def create_api_key(...) -> AuthenticationProviderProtocol:
        ...

    @staticmethod
    def create_bearer(...) -> AuthenticationProviderProtocol:
        ...
```

## API Key Creation

The API-key factory method supports:

- Secret API key
- Custom HTTP header name
- Optional authentication prefix
- Shared default `API_KEY_HEADER`

## Bearer Token Creation

The bearer-token factory method accepts a token and creates a standard `BearerTokenAuthenticationProvider`.

The provider remains responsible for producing:

```http
Authorization: Bearer <token>
```

---

# 5. Testing

Created:

```text
tests/authentication/test_factory.py
```

The factory tests verify:

- API-key provider creation
- Bearer-token provider creation
- Protocol compatibility
- Provider-specific concrete types
- Configuration forwarding
- Shared API-key header defaults
- Independent provider instances
- Secret-safe provider representations
- Propagation of provider validation errors

## Regression Status

```text
141 automated tests passing
```

---

# 6. Refactoring

The factory remains intentionally thin.

It does not:

- Duplicate provider validation
- Catch and translate provider configuration exceptions
- Store provider instances
- Maintain mutable state
- Build authentication headers itself

Validation remains owned by the concrete provider implementations.

This preserves clear responsibility boundaries.

---

# 7. Git Checkpoint

Recommended commit:

```text
feat(authentication): add enterprise authentication factory
```

Quality checks completed before commit:

```powershell
uv run ruff check
uv run pytest
```

Results:

```text
Ruff clean
141 tests passed
```

---

# 8. Developer Handbook

This implementation adds documentation describing:

- Why factories are used
- Object creation responsibility
- Dependency inversion
- Static factory methods
- Thin factory design
- Future migration to configuration-driven creation

Related Engineering Handbook chapter:

```text
docs/07_Engineering_Handbook/CHAPTER_07_Authentication_Framework.md
```

---

# 9. What We Learned

This implementation reinforced several enterprise engineering concepts:

- Object creation is an architectural responsibility.
- Factories reduce coupling to concrete implementations.
- Callers should depend on protocols rather than provider classes.
- Factories should not duplicate validation owned by constructed objects.
- Incremental architecture is preferable to premature abstraction.
- Stateless factories are naturally expressed through static methods.

---

# 10. Enterprise Best Practices

- Centralize complex or repeated object construction.
- Return abstractions when callers only require contract behavior.
- Keep factories stateless when no lifecycle is required.
- Do not duplicate validation inside the factory.
- Allow domain exceptions to propagate when no translation is needed.
- Use shared constants instead of duplicating default values.
- Introduce generic configuration-driven factories only when justified.
- Keep construction APIs small and explicit during early framework evolution.

---

# Next Implementation

**Implementation 20 — Authentication Configuration Models**

The next implementation will introduce strongly typed, immutable configuration objects for authentication providers.

These models will prepare the factory to evolve from explicit creation methods toward a generic configuration-driven API.