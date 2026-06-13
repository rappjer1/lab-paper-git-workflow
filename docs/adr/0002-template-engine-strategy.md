# ADR 0002: Template Engine Strategy

- Status: accepted

## Context

Paper Scaffold currently uses a small custom scaffold function and a static template tree. Template engines such as Cookiecutter and Copier could add richer prompts and updates.

## Decision

Keep the current custom scaffold for v0.5. Evaluate Copier later, but do not adopt it yet.

Copier is the stronger future candidate because it supports updating generated projects from versioned templates when `.copier-answers.yml` exists and the generated project satisfies Copier's Git safety conditions.

## Consequences

The project keeps no new runtime dependency for scaffolding. Generated manuscript repos remain simple folders with normal files. Template updates remain manual for now.

## Alternatives Considered

- Cookiecutter: mature and familiar, but update workflows are less central.
- Copier: better long-term update story, but adds dependency and workflow complexity.
- Current custom scaffold: small, understandable, and enough for v0.5.

## What Would Make Us Revisit This?

Revisit in v0.6 if users need template update workflows, more template variants, or repeated project generation from versioned templates.
