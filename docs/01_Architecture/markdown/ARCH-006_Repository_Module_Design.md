# ARCH-006: Repository Module Design

**Document ID:** ARCH-006  
**Version:** 1.0  
**Status:** Approved  
**Project:** SupplyMind Enterprise AI  
**Architecture Style:** Modular Monolith

## 1. Purpose

Define the responsibility, ownership, dependencies, interfaces, and design rules for every module within SupplyMind Enterprise AI. This document acts as the software architecture contract for the repository.

## 2. Repository Overview

```text
SupplyMind-Enterprise-AI/
├── assets/
├── artifacts/
├── configs/
├── data/
├── docker/
├── docs/
├── logs/
├── models/
├── notebooks/
├── scripts/
├── src/
├── tests/
├── .github/
├── pyproject.toml
├── README.md
└── .gitignore
```

## 3. Dependency Direction

```text
Users → UI → API → Services → AI / Gold / Feature Store
External Systems → Connectors → Bronze → Silver → Gold → Feature Store → AI
```

## 4. Module Contracts

| Module | Primary responsibility | Must not own |
|---|---|---|
| `src/core` | Shared contracts, configuration abstractions, constants, exceptions | Business logic |
| `src/connectors` | Source-specific data acquisition and ingestion metadata | Cleaning, KPIs, model training |
| `src/bronze` | Raw reproducible data and ingestion metadata | Business calculations |
| `src/silver` | Standardization, validation, deduplication | Forecasting and UI logic |
| `src/gold` | Business-ready datasets and KPIs | Model implementation |
| `src/feature_store` | Reusable and versioned model features | Model fitting |
| `src/ai/ml` | Classical ML training and inference | API routing and business recommendations |
| `src/ai/dl` | LSTM, GRU, and Transformer forecasting | Source ingestion |
| `src/ai/llm` | Provider-agnostic LLM integration | Business truth and KPI calculations |
| `src/ai/agents` | Tool-based AI workflow orchestration | Invented business values |
| `src/ai/prompts` | Versioned prompt templates | Data access and business logic |
| `src/ai/evaluation` | Common model and Copilot evaluation | Training orchestration |
| `src/services` | Business orchestration and decision intelligence | HTTP and UI concerns |
| `src/api` | Thin HTTP interface and validation | Forecast algorithms and transformations |
| `src/copilot` | Grounded conversational experience | Raw ingestion and unverified claims |
| `src/ui` | Dashboards, charts, forms, and chat | Direct data storage and model training |
| `src/monitoring` | Data, pipeline, model, API, and service observability | Business-rule ownership |
| `src/adapters` | Isolation of external libraries and infrastructure | Business behavior |
| `tests` | Unit, integration, contract, API, and end-to-end verification | Production business logic |

## 5. Module Interface Contract

Every major module must document:

- **Inputs:** accepted requests, datasets, or configuration.
- **Outputs:** returned datasets, results, artifacts, or events.
- **Dependencies:** modules and contracts it may call.
- **Guarantees:** behavior that consumers may rely on.
- **Prohibitions:** responsibilities it must never assume.

### Connector guarantee

A connector returns raw extracted data and source metadata, reports failures clearly, and never performs business transformations.

### Service guarantee

A service accepts a typed business request, coordinates lower-level modules, and returns a business result without exposing implementation details.

### Copilot guarantee

The Copilot retrieves facts through trusted tools and services. It does not invent business numbers.

## 6. Dependency Rules

Allowed:

```text
UI → API → Services
Connectors → Bronze → Silver → Gold
Services → Feature Store / AI / Gold
Copilot → Services / Agents / LLM
```

Prohibited:

```text
UI → Bronze
API → Connector
AI Model → CSV File
Connector → Gold KPI Logic
Prompt Template → Database
```

Circular dependencies are prohibited. Modules consume public contracts rather than internal implementation details.

## 7. Extension Strategy

- Adding a new connector must not require changes to Silver, Gold, AI, API, or UI.
- Replacing a model must not require changes to API or UI when the model contract remains stable.
- Replacing Pandas with Polars should be isolated through dataframe adapters.
- Replacing an LLM provider should be isolated through provider adapters.

## 8. Design Principles

- Single Responsibility Principle
- Open/Closed Principle
- Dependency Inversion
- Interface-Based Design
- Loose Coupling
- High Cohesion
- Explicit Contracts
- Technology Isolation through Adapters

## 9. Module Lifecycle Checklist

1. Why does the module exist?
2. Which business capability does it support?
3. What are its inputs, outputs, and guarantees?
4. Which modules may depend on it?
5. Which modules must it never depend on?
6. How will it be tested?
7. How could its implementation be replaced later?

## 10. Interview Talking Point

We organized the repository around business capabilities rather than file types. Every module has documented ownership, dependency rules, extension points, and an interface contract. Business orchestration lives in Services, source-specific work is isolated in Connectors and Adapters, AI models are separated from APIs, and the UI consumes stable service or API contracts. This supports maintainability today and future service extraction when scale justifies it.

## 11. Approval

The repository module design and Module Interface Contract approach are approved for implementation in SupplyMind Enterprise AI.
