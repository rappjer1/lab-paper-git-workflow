# ADR 0004: CLI Framework Strategy

- Status: accepted

## Context

The current CLI uses `argparse`. Typer and Rich could improve command organization, help output, and terminal formatting.

## Decision

Keep `argparse` for v0.5. Defer Typer/Rich migration until command complexity or output readability clearly warrants it.

## Consequences

The `paper-scaffold` command remains dependency-free and stable. Existing commands and tests continue to work. Output stays plain text and easy to capture in reports.

## Alternatives Considered

- Typer: good command ergonomics, but adds dependency and migration work.
- Rich: better display tables and colors, but plain output is more portable for CI and logs.
- `argparse`: enough for current command count and avoids dependency churn.

## What Would Make Us Revisit This?

Revisit if command nesting grows, help output becomes hard to navigate, or users need richer interactive terminal output.
