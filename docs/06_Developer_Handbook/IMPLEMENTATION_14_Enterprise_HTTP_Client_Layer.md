# Implementation 14 - Enterprise HTTP Client Layer

---

# 1. Business Objective

SupplyMind Enterprise AI will communicate with many external systems, including AI providers, SharePoint, GitHub, Databricks, internal enterprise APIs, and public data services.

Without a shared HTTP layer, each connector could implement its own:

- HTTP library usage
- Timeout behavior
- Connection management
- Error handling
- Header handling
- Response parsing
- Testing strategy

That would create duplicated code and inconsistent behavior.

The objective of this implementation was to create a reusable, asynchronous, application-owned HTTP client foundation for all future outbound API integrations.

---

# 2. Enterprise Concepts

## Outbound Adapter

An outbound adapter connects SupplyMind to an external system.

Examples include:

- REST API clients
- Database repositories
- Message producers
- Cloud storage clients
- LLM provider clients

The enterprise HTTP client supports REST-based outbound adapters.

## Adapter Pattern

`HttpxClient` adapts the third-party `httpx.AsyncClient` interface into the SupplyMind-owned `HttpClientProtocol`.

```text
SupplyMind Connector
        ↓
HttpClientProtocol
        ↓
HttpxClient
        ↓
httpx.AsyncClient
        ↓
External API
```

## Dependency Inversion

Connectors depend on the SupplyMind abstraction rather than directly on HTTPX.

This reduces coupling and allows fake clients to be substituted in tests.

## Structural Typing

Python `Protocol` supports structural typing.

A client satisfies the protocol when it provides the required methods, even when it does not inherit from a base class.

## Connection Pooling

A long-lived `httpx.AsyncClient` maintains a reusable pool of network connections.

This reduces:

- TCP connection setup
- TLS negotiation
- Request latency
- Resource consumption

## Resource Ownership

The FastAPI application owns the HTTP client.

```text
FastAPI Application
        owns
        ↓
HttpxClient
        owns
        ↓
httpx.AsyncClient
        owns
        ↓
Connection Pool
```

The application creates the client during startup and closes it during shutdown.

## Error Translation

HTTPX transport exceptions are translated into `ConnectorException`.

This prevents third-party infrastructure exceptions from leaking throughout the platform.

---

# 3. Architecture Decision

The implementation introduced:

```text
src/supplymind/connectors/api/
├── __init__.py
├── client.py
├── models.py
└── protocols.py
```

Dependency provider:

```text
src/supplymind/core/dependencies/http.py
```

Lifecycle ownership:

```text
src/supplymind/application/lifespan.py
```

Configuration:

```text
src/supplymind/core/config.py
```

## Key Decisions

### Use HTTPX

`httpx.AsyncClient` was selected because it supports:

- Asynchronous requests
- Connection pooling
- Timeouts
- Custom transports
- Deterministic mock testing

### Do Not Expose `httpx.Response`

SupplyMind exposes its own `HttpResponse` model.

This prevents connectors from becoming coupled to HTTPX.

### Preserve Non-2xx Responses

The generic client does not call `raise_for_status()`.

Responses such as 404, 409, or 429 may have connector-specific meanings.

### Translate Transport Failures

Timeouts and connection failures become `ConnectorException`.

### Do Not Add Retries Yet

Retries require deliberate policy around:

- Idempotency
- Retryable methods
- Retryable status codes
- Backoff
- Jitter
- Maximum attempts

Blind retry behavior could duplicate non-idempotent operations.

---

# 4. Step-by-Step Implementation

## Step 1 - Runtime Dependency

Moved `httpx` from the development dependency group into production runtime dependencies.

This ensures production installations include the library used by application code.

## Step 2 - Normalized Response Model

Created immutable `HttpResponse` with:

- `status_code`
- `headers`
- Raw byte `content`
- `is_success`
- `text`
- `json()`

Raw bytes preserve support for JSON, text, CSV, images, documents, and other binary payloads.

## Step 3 - HTTP Client Protocol

Created `HttpClientProtocol` defining:

- `request()`
- `get()`
- `close()`

This establishes the consumer-facing contract before the concrete implementation.

## Step 4 - Concrete HTTPX Adapter

Created `HttpxClient`.

Responsibilities include:

- Async request execution
- HTTP-method normalization
- Query parameter forwarding
- Request header forwarding
- JSON request bodies
- Response normalization
- Timeout translation
- Request-error translation
- Connection-pool cleanup

## Step 5 - Timeout Configuration

Added:

```python
http_timeout_seconds: float = 10.0
```

The value is validated to ensure it is greater than zero.

It may be overridden using:

```text
HTTP_TIMEOUT_SECONDS
```

## Step 6 - Application Lifecycle Ownership

The FastAPI lifespan creates the client during startup:

```python
http_client = HttpxClient(
    timeout_seconds=settings.http_timeout_seconds,
)
```

It stores the client on application state:

```python
application.state.http_client = http_client
```

During shutdown, it closes and removes the client:

```python
await http_client.close()
del application.state.http_client
```

## Step 7 - Dependency Provider

Created:

```python
get_http_client(request)
```

The provider returns the application-owned client through the `HttpClientProtocol` contract.

It raises a clear `RuntimeError` when lifecycle initialization has not occurred.

---

# 5. Testing

The final test suite contains:

```text
65 passed
```

HTTP model tests cover:

- Successful status detection
- Non-success status detection
- Text decoding
- JSON deserialization
- Invalid JSON

Protocol tests cover:

- Structural substitution

Concrete client tests cover:

- Successful GET requests
- Query parameters
- Request headers
- HTTP-method normalization
- JSON bodies
- Non-2xx responses
- Timeout translation
- Connection-error translation
- Empty methods
- Empty URLs
- Invalid timeout values

Lifecycle and dependency tests cover:

- Client creation during startup
- Client availability during runtime
- Client removal during shutdown
- Dependency-provider resolution
- Missing lifecycle initialization

All HTTP client tests use mock transports and do not access the internet.

---

# 6. Refactoring Review

The design remains intentionally small.

The following features were postponed:

- Automatic retries
- Authentication
- File uploads
- Streaming
- Cookies
- Provider-specific headers
- Multiple timeout profiles
- Circuit breakers
- Rate limiting
- Distributed tracing

These should be introduced only when real connector requirements justify them.

The current `try/finally` lifespan management remains clearer than introducing a resource container or `AsyncExitStack` for one resource.

---

# 7. Git Checkpoint

Recommended commit:

```text
feat: add enterprise HTTP client layer
```

Release gate:

```text
65 passed
```

The commit includes:

- Runtime dependency changes
- HTTP contracts
- HTTP response model
- HTTPX adapter
- Timeout configuration
- Application lifecycle integration
- Dependency provider
- Offline tests
- Developer handbook

---

# 8. Developer Notes

## Why not instantiate a client for every request?

That would repeatedly create connection pools and lose the performance benefit of connection reuse.

## Why not use a module-level global client?

Global mutable infrastructure complicates:

- Tests
- Multiple application instances
- Startup and shutdown
- Configuration isolation
- Resource cleanup

## Why use application state?

It associates the client with one FastAPI application instance.

## Why return a protocol from the provider?

Consumers depend on a stable SupplyMind contract and can receive fake implementations during testing.

## Why preserve raw response bytes?

External services may return many content types beyond JSON.

## Why not translate JSON parsing failures?

Invalid JSON is a content interpretation problem, not necessarily a network transport failure.

---

# 9. What We Learned

- Production imports must be declared as runtime dependencies.
- Third-party types should not leak across architectural boundaries.
- Async clients should be reused to preserve connection pooling.
- Every infrastructure resource requires explicit ownership.
- Lifespan startup and shutdown provide deterministic resource management.
- Protocols enable dependency inversion without mandatory inheritance.
- Transport errors and HTTP status responses represent different failure categories.
- Unit tests should not depend on live external services.

---

# 10. Enterprise Best Practices

- Use a shared async client per application.
- Define explicit timeouts.
- Keep transport logic outside business services.
- Depend on application-owned protocols.
- Preserve raw payloads.
- Translate third-party transport errors.
- Do not log credentials or authorization headers.
- Test HTTP integrations with mock transports.
- Close pooled clients during graceful shutdown.
- Avoid adding retries without an idempotency policy.
- Keep resource ownership explicit.
- Avoid process-global mutable infrastructure.

---

# 11. Common Mistakes

Avoid:

- Calling `httpx.get()` directly throughout services
- Creating a new `AsyncClient` for every request
- Omitting timeout configuration
- Returning `httpx.Response` from internal contracts
- Catching every exception as `ConnectorException`
- Automatically treating every 4xx response as a transport failure
- Retrying POST requests without idempotency guarantees
- Using real websites in unit tests
- Forgetting to close the client
- Logging authorization headers or API tokens

---

# 12. Interview Questions

## Why use `httpx.AsyncClient` with FastAPI?

Network calls are I/O-bound. Async execution allows the event loop to process other work while waiting for external services.

## What is connection pooling?

The reuse of established network connections across multiple requests, reducing connection setup cost and latency.

## Why should connectors depend on a protocol?

It decouples them from the concrete HTTP library and enables fake implementations during testing.

## What is structural typing?

A typing model where compatibility is based on the presence of required behavior rather than explicit inheritance.

## Why not expose `httpx.Response`?

That would couple the entire connector layer to HTTPX and make future replacement more difficult.

## Why distinguish HTTP errors from transport errors?

A 404 or 409 is a successfully received HTTP response with business meaning. A timeout or connection failure means no usable response was obtained.

## Why are retries dangerous?

Retrying non-idempotent operations may produce duplicate side effects.

## Who owns the HTTP client?

The FastAPI application lifecycle creates, stores, and closes it.

## Why not use `lru_cache` for the HTTP client?

Network clients require explicit asynchronous cleanup, which a simple cached function does not manage safely.

## How are HTTP calls tested without the internet?

By injecting HTTPX `MockTransport` handlers that return controlled responses or raise controlled exceptions.

---

# Related ADRs

- ADR-002 - FastAPI API Framework
- ADR-004 - Clean Architecture
- ADR-005 - Provider-Agnostic AI Architecture

---

# Status

**Completed**