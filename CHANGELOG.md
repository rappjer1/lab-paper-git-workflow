# Changelog

## v0.8.0

- Added `add-manuscript-ci` for dependency-free manuscript repository hygiene workflows.
- Added `package-submission` for clean manuscript source and artifact packages.
- Added `compare-lock` for artifact lock drift reports.
- Added `reviewer-binder` for response-round checklists, provenance snapshots, and release snapshots.
- Added workflow docs, examples, diagnostics, and tests for CI, submission packages, artifact locks, and reviewer binders.

## v0.7.0

- Added generated artifact provenance ledgers for manuscript figures and tables.
- Added `provenance-report` with Markdown and JSON output.
- Added `artifact-status` for compact current/stale/missing/untracked counts.
- Added `freeze-artifacts` to write submission or revision hash locks.
- Added provenance diagnostics for missing manuscript artifacts, missing referenced artifacts, missing sources, stale artifacts, untracked artifacts, and unreferenced manifest artifacts.
- Added provenance ledger documentation and tests.

## v0.6.0

- Added workflow recipes with `paper-scaffold recipes list` and `paper-scaffold recipes show <recipe-id>`.
- Added the use-case gallery in `docs/use_cases/` for paper archaeology, Overleaf ZIP rehab, reviewer response binders, pre-submission checks, undergraduate artifact harvesting, and multi-paper splits.
- Added `audit-project` for read-only triage of messy project folders.
- Added `release-check` for consolidated manuscript pre-submission checks.
- Added synthetic examples for messy project archaeology, reviewer response binders, and multi-paper project splits.
- Added audit diagnostics for suspicious final filenames, LaTeX build artifacts, raw/generated outputs, and likely manuscript artifact candidates.

## v0.5.1

- Clean-clone public-user hardening.
- Documented the Windows/Git Bash installed CLI PATH workaround.
- Documented a Windows pytest temp-directory workaround.
- Made the demo manuscript reference its included PDF figure and bibliography entry so validation is warning-free.

## v0.5.0

- Added architecture decision records and a public v1.0 roadmap.
- Added dependency-free schema validation for manuscript config, artifact manifests, terminology maps, and validation JSON reports.
- Added `validate --write-json`.
- Added `stale-artifacts` and `unused-artifacts`.
- Added development hygiene with Ruff, pre-commit configuration, and stronger CI smoke checks.

## v0.4.0

- Added structured diagnostic codes with `paper-scaffold explain`.
- Added focused readiness checks: `overleaf-check`, `github-check`, `privacy-check`, `check-figures`, `check-citations`, `check-labels`, and `audit-word-conversion`.
- Improved validation reports with diagnostic summaries and Git status context.
- Added public troubleshooting and error-code documentation for common GitHub/Overleaf manuscript failures.
- Expanded tests and CI coverage for the public demo and diagnostics workflow.

## v0.3.0

- Public-facing Paper Scaffold positioning.
- Added public getting-started, FAQ, validation, design-principles, and cleanup docs.
- Added demo workflow and public examples.
- Added GitHub community files and CI.
- Improved `doctor`, `discover-artifacts`, and `validate --write-report`.

## v0.2.0

- Added Word/docx to Overleaf workflow docs.
- Added Python-output to Overleaf workflow docs.
- Added `doctor`, `import-word`, `discover-artifacts`, and Slack summary commands.

## v0.1.0

- Initial manuscript Git/Overleaf workflow toolkit.
- Added scaffold template, artifact manifest, terminology map, validation, and core CLI commands.
