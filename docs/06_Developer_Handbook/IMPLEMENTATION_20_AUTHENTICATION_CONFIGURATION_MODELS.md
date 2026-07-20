# Implementation 20 — Authentication Configuration Models

---

# 1. Business Objective

Separate authentication configuration from authentication behavior.

Instead of storing API keys and tokens directly inside providers, providers now receive validated immutable configuration objects.

This architecture mirrors enterprise SDKs and prepares the authentication framework for OAuth2 and Microsoft Entra ID.

---

# 2. Enterprise Concepts

This implementation introduces an important enterprise architecture concept:

Configuration Objects.

Instead of mixing:

- configuration
- validation
- behavior

inside a single class, responsibilities are separated.

Configuration models own:

- validation
- normalization
- immutability

Providers own:

- behavior

---

# 3. Architecture Decision

Previous architecture:

```text
Provider

├── validation

├── normalization

└── header creation
```

New architecture:

```text
Configuration

├── validation

├── normalization

└── immutable settings

↓

Provider

└── HTTP header creation
```

This greatly simplifies provider implementations.

---

# 4. Step-by-Step Implementation

Implemented:

## Authentication Configuration package

```text
authentication/
    configuration/
```

---

Created:

- ApiKeyAuthenticationConfiguration
- BearerTokenAuthenticationConfiguration

---

Updated:

- AuthenticationFactory

Factory now constructs:

Configuration

↓

Provider

instead of constructing providers directly.

---

Updated Providers

Providers no longer perform validation.

They now receive validated configuration.

Responsibilities became significantly smaller.

---

# 5. Testing

Added dedicated configuration tests.

Coverage includes:

- default values
- whitespace normalization
- empty API key rejection
- empty bearer token rejection
- empty header rejection
- repr security
- export tests

Provider tests were simplified to verify only behavior.

Factory tests were updated to verify configuration forwarding.

All tests remain green.

---

# 6. Refactoring

Responsibilities moved:

Before:

Provider

- validation
- normalization
- behavior

After:

Configuration

- validation
- normalization

Provider

- behavior only

This significantly improved cohesion.

---

# 7. Git Checkpoint

```bash
git add .

git commit -m "feat(authentication): add authentication configuration models"

git push
```

---

# 8. What We Learned

Enterprise applications frequently separate:

Configuration

↓

Behavior

Benefits include:

- reusable configuration
- easier dependency injection
- easier testing
- cleaner APIs
- lower coupling

This implementation demonstrates the "Tell, Don't Ask" design principle.

Providers no longer inspect or validate raw input.

They trust validated configuration objects.

---

# 9. Enterprise Best Practices

✔ Immutable configuration

✔ Validation at construction time

✔ Fail Fast

✔ Single Responsibility Principle

✔ Composition over inheritance

✔ Strong typing

✔ Provider simplicity

✔ Reusable configuration

---

# 10. Interview Questions

## Why separate configuration from providers?

To isolate validation from runtime behavior.

---

## What enterprise pattern is demonstrated?

Configuration Object Pattern.

---

## Why validate during construction?

To guarantee every instance is always valid.

---

## Why are providers now smaller?

They have a single responsibility:

Generate authentication headers.

---

## How does this prepare for OAuth2?

Future providers will receive validated OAuth configuration instead of validating raw client credentials themselves.

---

# Final Architecture

```text
AuthenticationFactory
            │
            ▼
AuthenticationConfiguration
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

Implementation 20 completes the separation of configuration and behavior, resulting in a cleaner, more maintainable, and enterprise-grade authentication architecture.