# Chapter 6 — Connector Framework

---

# Business Motivation

Modern enterprise applications rarely operate in isolation.

Instead, they integrate with many external systems:

- Microsoft Graph
- SharePoint
- SAP
- Manhattan WMS
- Databricks
- GitHub
- AI providers

Each external platform exposes different APIs, authentication mechanisms, error models, and response formats.

Without a dedicated connector layer, business services become tightly coupled to vendor implementations, making the application difficult to maintain, test, and evolve.

The Connector Framework isolates those concerns behind application-owned abstractions.

---

# Architecture Overview

```
Business Service
        │
        ▼
Connector Protocol
        │
        ▼
Enterprise Connector
        │
        ▼
Enterprise HTTP Client
        │
        ▼
External System
```

Each layer has a single responsibility.

---

# Responsibilities

## Business Service

Responsible for business logic.

Should never know:

- HTTP
- REST endpoints
- Authentication
- Vendor SDKs

---

## Connector

Responsible for:

- Endpoint construction
- Request translation
- Response translation
- Pagination
- Vendor-specific behavior
- Error translation

A connector should never implement business rules.

---

## HTTP Client

Responsible for transport only.

Responsibilities include:

- Sending requests
- Timeouts
- Retries
- Connection pooling
- HTTP error handling

---

# Dependency Inversion

Business services depend on:

```
ConnectorProtocol
```

instead of:

```
GitHubConnector
```

This allows connectors to be replaced during testing without changing application logic.

---

# Connector Health

Every connector implements:

```python
health_check()
```

This provides a lightweight mechanism for verifying that external systems are reachable.

Typical startup checks include:

- SharePoint
- Microsoft Graph
- Databricks
- SAP

---

# Connector Exceptions

The Connector Framework defines a shared exception hierarchy.

Examples include:

- ConnectorTimeoutException
- ConnectorResponseException
- ConnectorRateLimitException
- ConnectorAuthenticationException

This creates consistent behavior across all enterprise integrations.

---

# Design Principles

The Connector Framework follows several engineering principles:

- Dependency Inversion
- Single Responsibility
- Protocol-oriented Design
- Composition over Inheritance
- Testability
- Vendor Isolation

---

# Benefits

The Connector Framework provides:

- Vendor independence
- Easier testing
- Cleaner business services
- Consistent error handling
- Simplified maintenance
- Reusable infrastructure

---

# Common Mistakes

Avoid:

- Business logic inside connectors
- Direct use of httpx in services
- Vendor-specific exceptions escaping connectors
- Duplicate authentication logic
- Connectors calling other connectors directly

---

# Testing Strategy

Connector implementations should be tested using mocked HTTP clients.

Tests should verify:

- Request generation
- Response translation
- Error translation
- Retry behavior
- Health checks

Real external APIs should only be exercised in dedicated integration tests.

---

# Future Extensions

The Connector Framework is designed to support:

- GitHub
- SharePoint
- Microsoft Graph
- SAP
- Manhattan WMS
- Databricks
- OpenAI
- Azure OpenAI
- Ollama

without changing the application architecture.

---

# Key Takeaways

The Connector Framework acts as an Anti-Corruption Layer between SupplyMind Enterprise AI and external enterprise systems.

Business services communicate only with application-owned abstractions, ensuring that vendor-specific implementation details remain isolated within the infrastructure layer.