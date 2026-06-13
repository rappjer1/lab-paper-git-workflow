# ADR 0001: Project Scope

- Status: accepted

## Context

Paper Scaffold helps researchers create and validate clean manuscript repositories from existing research work. The project needs clear boundaries so it remains a small workflow tool instead of becoming a manuscript editor, data manager, build system, or publishing platform.

## Decision

Paper Scaffold creates scaffolds, copies selected manuscript artifacts, tracks provenance, checks terminology, and validates repository hygiene for GitHub/Overleaf workflows.

It does not:

- write papers;
- upload to Overleaf;
- manage raw data;
- guarantee LaTeX compilation;
- replace scientific judgment.

## Consequences

The CLI stays lightweight and works without Pandoc, LaTeX, GitHub CLI, Overleaf, or network access. Users remain responsible for scientific content, final copyediting, and publication decisions.

## Alternatives Considered

- Full manuscript authoring environment: too broad and too hard to keep reliable.
- Research data manager: overlaps with domain-specific storage and reproducibility systems.
- LaTeX build orchestrator: would require optional external tools and platform-specific support.

## What Would Make Us Revisit This?

Revisit if users consistently need one additional bounded workflow that fits the clean-manuscript-repo mission without requiring external services or raw-data management.
