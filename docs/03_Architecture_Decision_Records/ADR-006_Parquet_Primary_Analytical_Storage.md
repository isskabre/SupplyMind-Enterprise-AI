# ADR-006: Adopt Parquet as the Primary Analytical Storage Format

## Status

**Accepted**

## Date

2026-07-12

---

# Context

SupplyMind Enterprise AI requires an efficient and portable storage format for the Bronze, Silver, Gold, and Feature Store layers.

The selected format must preserve data types, support analytical processing, reduce unnecessary storage and input/output operations, and remain compatible with local and cloud-based data technologies.

The platform may ingest data from CSV, JSON, APIs, databases, and other enterprise sources, but it requires a consistent internal format for trusted analytical datasets.

---

# Decision

SupplyMind Enterprise AI will use **Apache Parquet** as its primary internal analytical storage format.

Parquet will be used for persisted datasets across the Bronze, Silver, Gold, and Feature Store layers unless a specific use case requires another technology.

Source formats such as CSV and JSON may be accepted by the connector framework, but ingested data will be converted into governed Parquet datasets as it enters the platform.

---

# Alternatives Considered

## Option 1 — CSV

### Advantages

- Human-readable
- Universally supported
- Easy to inspect manually
- Simple for data exchange

### Disadvantages

- Weak schema enforcement
- Data types are not reliably preserved
- Larger file sizes
- Inefficient for analytical queries
- Limited support for nested data

**Decision**

Rejected as the primary internal format.

CSV will remain supported as an ingestion and export format where appropriate.

---

## Option 2 — JSON

### Advantages

- Human-readable
- Supports nested structures
- Commonly used by APIs

### Disadvantages

- Larger storage footprint
- Slower analytical processing
- Inconsistent schema handling
- Inefficient for tabular analytics

**Decision**

Rejected as the primary analytical storage format.

JSON will remain appropriate for API payloads, configuration, and selected metadata use cases.

---

## Option 3 — Relational Database

### Advantages

- Strong transactional capabilities
- Mature query support
- Constraints and indexing
- Concurrent access

### Disadvantages

- Additional infrastructure
- Less suitable as the default portable file format
- Greater operational complexity for local-first development
- Potential vendor and platform dependency

**Decision**

Rejected as the initial primary analytical storage mechanism.

Databases may be introduced later for transactional, metadata, serving, or operational requirements.

---

## Option 4 — Apache Parquet

### Advantages

- Columnar storage
- Strong data-type preservation
- Efficient compression
- Column pruning
- Broad analytical ecosystem support
- Compatible with Pandas, Polars, Spark, DuckDB, and cloud platforms
- Suitable for local-first and cloud-ready development

### Disadvantages

- Not designed for manual editing
- Less convenient for direct human inspection
- Not suitable for high-frequency transactional updates

**Decision**

Accepted.

---

# Consequences

## Positive

- Analytical datasets require less storage.
- Data types and schemas are preserved more reliably.
- Pipelines can read only the columns they require.
- The same datasets can be processed by multiple analytical engines.
- Local development remains compatible with future cloud and distributed processing.
- Bronze, Silver, Gold, and Feature Store layers use a consistent storage standard.

## Negative

- Files are not directly human-readable.
- Specialized tools or libraries are required for inspection.
- Parquet is not appropriate for transactional record-by-record updates.
- Schema evolution must be managed deliberately.

---

# Future Considerations

SupplyMind may introduce additional storage technologies as requirements evolve.

Examples include:

- relational databases for operational metadata;
- object storage for cloud deployment;
- Delta Lake or Apache Iceberg for transactional lakehouse capabilities;
- vector databases for semantic retrieval;
- model registries and artifact stores for machine learning assets.

These technologies may complement Parquet without changing its role as the initial analytical storage standard.

---

# Lessons Learned

A source format and an internal analytical format serve different purposes.

CSV and JSON are useful for exchanging and ingesting data, while Parquet provides stronger performance, schema preservation, and interoperability for governed analytical pipelines.

The platform should standardize internal storage without unnecessarily restricting the formats accepted from external systems.

---

# Related Architecture Documents

- ARCH-005 — Technology Stack and Architectural Decisions
- ARCH-007 — Enterprise Data Platform Architecture
- ARCH-010 — Enterprise Implementation Roadmap