# Roadmap

## What v0.4 Provides

v0.4 made Paper Scaffold public-ready with diagnostics, public examples, validation reports, GitHub metadata, and focused checks for figures, citations, labels, privacy, GitHub readiness, and Overleaf readiness.

## v0.5 Architecture Hardening

v0.5 adds architecture decision records, schema validation, JSON validation reports, artifact stale/unused checks, Ruff/pre-commit development hygiene, stronger CI, and a clearer path toward v1.0.

## v0.6 Recipes And Use-Case Workflows

v0.6 added use-case recipes, project archaeology, release checks, and synthetic public examples for common manuscript cleanup workflows.

## v0.7 Provenance Ledger

v0.7 adds generated provenance ledgers, artifact status summaries, and artifact hash locks so manuscript figures/tables have a lightweight bill of materials.

## v0.8 Manuscript CI And Submission Packaging

v0.8 adds dependency-free manuscript CI workflow generation, submission package folders, artifact lock comparison, and reviewer response binders.

## v0.9 Release-Candidate Hardening

v0.9 hardens install paths, module fallback invocation, self-test, schema/reference docs, multi-OS CI, local package build readiness, install-matrix auditing, cross-platform test running, clean-install auditing, public contract metadata, docs/examples usability, dogfood scenarios, example artifact integrity, public docs-freeze walkthroughs, public trust/privacy audits, and the v0.9.9 release-candidate dry run as the final pre-1.0 series.

## v0.10 Reserved Stabilization Window

Use only if v0.9.x contract audits find remaining command, schema, diagnostic, exit-code, or cross-platform issues that should be fixed before v1.0.

## v1.0 Stable CLI And Manifest Schema

Commit to stable command names, stable JSON report shape, and stable artifact manifest fields for normal manuscript workflows.

## v1.0.1 Post-Release Metadata Patch

v1.0.1 fixes package version metadata after the v1.0.0 tag, restores Ruff Python target metadata, and moves historical release reports out of the repository root into `docs/release_reports/`.

## Explicit Non-Goals

- Writing the paper.
- Uploading directly to Overleaf.
- Managing raw research data.
- Replacing scientific review.
- Requiring Pandoc, LaTeX, GitHub CLI, or network access for core validation.
- Publishing private manuscript content or research-specific examples.
