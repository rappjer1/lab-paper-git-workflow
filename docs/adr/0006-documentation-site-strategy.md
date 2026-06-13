# ADR 0006: Documentation Site Strategy

- Status: proposed

## Context

The project now has enough docs that README-only navigation may become limiting. MkDocs Material could provide a searchable documentation site.

## Decision

Keep Markdown docs in the repository for v0.5. Recommend evaluating MkDocs Material in v0.6 if the docs continue to grow.

Do not add a documentation site in v0.5.

## Consequences

Docs remain easy to read on GitHub and do not require site build tooling. Navigation pressure is handled through README links and a roadmap for now.

## Alternatives Considered

- README-only: simple, but insufficient for all workflow details.
- MkDocs Material: strong public docs experience, but adds configuration and dependency surface.
- Sphinx: powerful, but heavier than needed for this workflow-focused project.

## What Would Make Us Revisit This?

Revisit if users need search, versioned docs, a documentation landing page, or a clearer tutorial/reference split.
