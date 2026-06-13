# Roadmap

## What v0.4 Provides

v0.4 made Paper Scaffold public-ready with diagnostics, public examples, validation reports, GitHub metadata, and focused checks for figures, citations, labels, privacy, GitHub readiness, and Overleaf readiness.

## v0.5 Architecture Hardening

v0.5 adds architecture decision records, schema validation, JSON validation reports, artifact stale/unused checks, Ruff/pre-commit development hygiene, stronger CI, and a clearer path toward v1.0.

## v0.6 Docs Site And Template Engine Evaluation

Evaluate MkDocs Material for documentation and Copier for versioned template updates. Adopt only if the workflow benefit outweighs dependency and maintenance cost.

## v0.7 Word/Pandoc Conversion Quality

Improve Word conversion audits, section splitting guidance, equation/citation cleanup checks, and examples for converted drafts.

## v0.8 Manuscript CI Templates And Release Packaging

Add optional manuscript-repo CI templates and prepare PyPI release mechanics. Prefer PyPI Trusted Publishing when packaging is ready.

## v0.9 Schema Freeze And Cross-Platform Hardening

Stabilize the manifest/config/report schemas, broaden Windows/macOS/Linux path tests, and tighten error messages before v1.0.

## v1.0 Stable CLI And Manifest Schema

Commit to stable command names, stable JSON report shape, and stable artifact manifest fields for normal manuscript workflows.

## Explicit Non-Goals

- Writing the paper.
- Uploading directly to Overleaf.
- Managing raw research data.
- Replacing scientific review.
- Requiring Pandoc, LaTeX, GitHub CLI, or network access for core validation.
- Publishing private manuscript content or research-specific examples.
