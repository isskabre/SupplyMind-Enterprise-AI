# SupplyMind Enterprise AI

Enterprise-grade AI platform for supply chain decision intelligence.

> A modular, local-first enterprise AI platform for supply chain intelligence, demand forecasting, workload planning, decision support, and AI-assisted business insights.
[Python]
[FastAPI]
[PyTorch]
[CI]
[Version]
[License]
[Status]
[Architecture Complete]

## Project Status

**Current release:** `v0.1.0`  
**Current phase:** Sprint 0 — Enterprise Architecture  
**Implementation status:** Architecture complete; platform implementation begins in Sprint 1.

SupplyMind Enterprise AI is designed as an enterprise platform rather than a single forecasting application. The first implemented business domain will be **Supply Chain Intelligence**, while the architecture remains extensible to manufacturing, quality, procurement, finance, and other enterprise functions.

## Current Progress

| Component | Status |
|-----------|--------|
| Enterprise Architecture | ✅ Complete |
| Repository Structure | ✅ Complete |
| Engineering Standards | ✅ Complete |
| Platform Foundation | 🚧 In Progress |
| Data Platform | ⏳ Planned |
| Machine Learning | ⏳ Planned |
| AI Copilot | ⏳ Planned |
| Dashboard | ⏳ Planned |

## Platform Vision

Enable enterprise teams to transform fragmented operational data into trusted insights, forecasts, recommendations, and conversational decision support through a modular and extensible AI platform.

## Platform Goals

The platform is designed around the following engineering goals:

- Build reusable AI services that can support multiple business domains.
- Maintain a modular architecture that allows components to evolve independently.
- Apply enterprise governance through standardized data pipelines and architecture.
- Deliver explainable AI that business users can trust.
- Support local-first development while remaining cloud-ready.
- Emphasize production-quality engineering practices from the beginning.
- Transform predictions into actionable business decisions.

## Business Problem

Enterprise supply chain and operations teams often face:

- data distributed across APIs, files, databases, cloud storage, and enterprise systems;
- inconsistent business definitions and KPI calculations;
- forecasting workflows that depend on manual spreadsheets;
- disconnected AI models built for only one use case;
- limited explanation of predictions and recommendations;
- delayed operational insights.

SupplyMind Enterprise AI addresses these challenges by creating a governed, reusable platform that connects data engineering, analytics, machine learning, deep learning, APIs, dashboards, and an AI Copilot.

## Why This Project Exists
SupplyMind Enterprise AI was created to demonstrate how enterprise AI systems should be engineered, not merely how machine learning models are trained. The platform emphasizes software architecture, reusable components, governed data pipelines, explainable AI, and production-ready engineering practices that mirror the expectations of modern enterprise organizations.

## Core Capabilities

### Data Intelligence

- Multi-source connector framework
- Automated ingestion
- Landing, Bronze, Silver, and Gold data layers
- Data quality validation
- Metadata, lineage, and data contracts
- Dataset catalog and specification sheets

### Predictive Intelligence

- Baseline forecasting
- Classical machine learning
- XGBoost
- LSTM and GRU
- Transformer-based forecasting
- Shared model evaluation framework

### Decision Intelligence

- Workload estimation
- Labor planning
- Capacity recommendations
- Scenario analysis
- Operational risk assessment

### Conversational Intelligence

- Tool-based AI Copilot
- Grounded KPI and forecast explanations
- Natural-language business questions
- Trusted service invocation
- Provider-agnostic LLM architecture

### Enterprise Platform Services

- FastAPI-based service layer
- Streamlit-based initial user experience
- Configuration management
- Logging and monitoring
- Automated testing
- Docker and CI/CD readiness

## Enterprise Platform Architecture

SupplyMind Enterprise AI follows a modular monolith architecture designed for future service extraction.

<p align="center">
  <img src="assets/architecture/platform-architecture.png"
       alt="SupplyMind Enterprise AI Platform Architecture"
       width="900">
</p>

The architecture separates presentation, business logic, AI services, and the data platform into independent layers that evolve without affecting one another.

### Architectural Principles

- Business logic remains independent of the user interface.
- Pipeline logic remains independent of the original data source.
- Models are replaceable.
- APIs remain thin.
- Services coordinate business capabilities.
- Raw data remains reproducible.
- AI responses must be grounded in trusted data.
- Monitoring and testing are part of the platform from the beginning.
- Complexity must be justified by business value.

## Data Architecture

```text
Landing
   ↓
Bronze
   ↓
Silver
   ↓
Gold
   ↓
Feature Store
```

- **Landing:** temporary recovery zone immediately after ingestion
- **Bronze:** raw, immutable, auditable source data
- **Silver:** cleaned, standardized, validated enterprise data
- **Gold:** business-ready KPIs and analytical datasets
- **Feature Store:** reusable, versioned features for AI models

## Technology Stack

| Area | Selected Technology |
|---|---|
| Language | Python 3.12 |
| Packaging | `pyproject.toml` |
| Data Processing | Pandas initially, with a path to Polars and Spark |
| Storage | Parquet |
| Machine Learning | scikit-learn and XGBoost |
| Deep Learning | PyTorch |
| API | FastAPI |
| User Interface | Streamlit |
| Testing | pytest |
| Formatting | Black |
| Linting | Ruff |
| Type Checking | Pyright |
| Local Quality Automation | pre-commit |
| Version Control | Git and GitHub |
| Documentation | Markdown, Word, ADRs, and Developer Handbook |

## Repository Structure

```text
SupplyMind-Enterprise-AI/
docs/
src/
tests/
configs/
docker/
data/
models/
artifacts/
```

See ARCH-006 Repository Design for the complete structure.

## Architecture Documentation

- `ARCH-001` — Executive Summary
- `ARCH-002` — Business Vision and Capability Map
- `ARCH-003` — Personas and Business Use Cases
- `ARCH-004` — Enterprise Solution Architecture
- `ARCH-005` — Technology Stack and Architectural Decisions
- `ARCH-006` — Repository Module Design
- `ARCH-007` — Enterprise Data Platform Architecture
- `ARCH-008` — Engineering Standards and Development Playbook
- `ARCH-009` — Git Workflow and Release Strategy
- `ARCH-010` — Enterprise Implementation Roadmap

See **docs/01_Architecture/** for the complete architecture documentation.

## Implementation Roadmap

| Sprint | Focus |
|---|---|
| 0 | Enterprise Architecture |
| 1 | Platform Foundation |
| 2 | Connector Framework |
| 3 | Bronze Data Platform |
| 4 | Silver Data Platform |
| 5 | Gold Data Platform |
| 6 | Feature Store |
| 7 | Machine Learning |
| 8 | Deep Learning |
| 9 | Decision Intelligence |
| 10 | Enterprise APIs |
| 11 | AI Copilot |
| 12 | Enterprise Dashboard |
| 13 | Production Readiness |
| 14 | Documentation and Handover |

## Engineering Workflow

```text
Create Branch
    ↓
Implement Change
    ↓
Format with Black
    ↓
Lint with Ruff
    ↓
Type-check with Pyright
    ↓
Test with pytest
    ↓
Run pre-commit Checks
    ↓
Review
    ↓
Commit and Merge
```

Commit messages follow a Conventional Commit-style format:

```text
feat: add connector framework
fix: correct workload calculation
docs: add architecture decision record
test: add connector contract tests
chore: configure project tooling
```

## Release Strategy

The project uses Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

Current milestone:

```text
v0.1.0 — Sprint 0 architecture foundation
```

Planned final portfolio release:

```text
v1.0.0 — Complete enterprise AI platform
```

## Target Roles

This project is designed to develop and demonstrate competencies relevant to:

- AI Engineer
- AI Transformation Specialist
- Machine Learning Engineer
- Data and AI Engineer
- Analytics Engineer
- Enterprise AI Solution Architect

## Development Setup

The implementation environment will be configured during Sprint 1.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

The approved quality toolchain will then be installed and configured through `pyproject.toml`.

## Engineering Principles
- Enterprise-first
- Modular
- Maintainable
- Explainable
- Business-driven
- Testable
- Replaceable
- Documentation-as-Code

## Documentation Strategy

- **Markdown** is the maintainable technical source tracked in Git.
- **Word documents** support formal stakeholder communication.
- **Architecture Decision Records** explain why major decisions were made.
- A complete **Developer Handbook** will be delivered at the end of the project.

## License

MIT License (coming in Sprint 1)

## Author

**Issouf Kabre**

Senior Quality Auditor at Schneider Electric and Master of Data Science candidate, building SupplyMind Enterprise AI as an end-to-end portfolio project to demonstrate enterprise AI engineering, software architecture, machine learning, and decision intelligence.

This project reflects my commitment to designing AI systems that are not only accurate, but also maintainable, explainable, and production-ready.

- LinkedIn: [Issouf Kabre](https://www.linkedin.com/in/issouf-kabre-5b9682373/)
- GitHub: [SupplyMind Enterprise AI Repository](https://github.com/isskabre/SupplyMind-Enterprise-AI)

