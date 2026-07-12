# ARCH-005: Technology Stack & Architectural Decisions

## Philosophy

-   Local-first development
-   Enterprise-ready architecture
-   Replaceable components
-   Business-driven technology choices

## Technology Stack

  Layer                Technology                Reason
  -------------------- ------------------------- ----------------------------
  Language             Python                    AI ecosystem
  Package Management   pyproject.toml            Modern Python standard
  IDE                  Cursor                    AI-assisted development
  Version Control      Git + GitHub              Professional workflow
  Data Processing      Pandas → Polars → Spark   Scalable evolution
  Storage              Parquet                   Efficient columnar storage
  Machine Learning     Scikit-learn + XGBoost    Forecasting
  Deep Learning        PyTorch                   LSTM and Transformers
  API                  FastAPI                   Modern REST APIs
  UI                   Streamlit                 Rapid dashboards
  Testing              pytest                    Quality assurance
  Configuration        .env + configs            Externalized configuration
  Documentation        Word + Markdown + ADRs    Enterprise documentation

## Approved ADRs

-   ADR-001: Modular Monolith
-   ADR-002: Bronze → Silver → Gold
-   ADR-003: Connector Abstraction
-   ADR-004: Local-First Development
-   ADR-005: Provider-Agnostic AI Copilot
-   ADR-006: Adapter Layer

## Interview Talking Points

The technology stack was selected based on maintainability, scalability,
replaceability, and alignment with enterprise AI engineering practices
rather than popularity alone.
