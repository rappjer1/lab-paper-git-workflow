# ADR 0003: Config And Manifest Schemas

- Status: accepted

## Context

Paper Scaffold relies on YAML files for manuscript config, artifact manifests, and terminology maps. As the CLI grows, these files need clearer validation and stable report output.

## Decision

Use lightweight dataclass-backed schema definitions with explicit manual validation in `src/paper_scaffold/schemas.py`.

Do not add Pydantic in v0.5. Pydantic remains a reasonable future option if schema complexity increases and the dependency cost is acceptable.

## Consequences

Schema validation works without internet access and without installing new runtime dependencies. Unknown fields produce warnings rather than fatal errors, so project-local metadata can coexist with Paper Scaffold fields.

## Alternatives Considered

- Pydantic: excellent error models and type coercion, but adds a runtime dependency.
- JSON Schema: portable, but would need either manual validation or another dependency.
- Manual validation: less expressive, but transparent and sufficient for v0.5.

## What Would Make Us Revisit This?

Revisit if schema logic becomes hard to maintain, if nested validation expands substantially, or if users need stable external JSON Schema documents.
