# Changelog

## v0.9.7

- Added public entry-point docs: `docs/start_here.md`, `docs/common_paths.md`, `docs/one_page_reference.md`, and `docs/glossary.md`.
- Added public walkthroughs for the five-minute demo, Python artifact handoff, existing LaTeX cleanup, pre-submission packaging, and reviewer response rounds.
- Added `scripts/dev/check_docs_links.py` and CI coverage for local Markdown link checks.
- Refreshed README and QUICKSTART as public first-run guides.
- Bumped Paper Scaffold to `0.9.7`.

## v0.9.6

- Added `scripts/dev/build_package.py` for local wheel/sdist builds without publishing.
- Added `scripts/dev/install_matrix_audit.py` for no-install, module fallback, editable install, console script, and optional wheel/sdist checks.
- Documented network-free package build and install-matrix release checks.
- Kept build tooling as an optional extra, not a runtime dependency.
- Bumped Paper Scaffold to `0.9.6`.

## v0.9.5

- Added example artifact integrity checks for synthetic public examples and templates.
- Replaced fake example PDF/PNG placeholders with tiny valid synthetic artifacts.
- Added clean-clone dogfood audit tooling for public-polish validation.
- Linked example integrity guidance from public docs and release-process docs.
- Bumped Paper Scaffold to `0.9.5`.

## v0.9.4

- Polished the README first-run path, Quick Start, and Getting Started guide for public users.
- Added a workflow decision guide and public examples index.
- Added synthetic dogfood scenarios plus a dogfood runner and docs/examples drift checker.
- Updated v1.0 preparation notes and readiness checklist.
- Bumped Paper Scaffold to `0.9.4`.

## v0.9.3

- Added public contract documentation for CLI commands, diagnostics, schemas, exit codes, deprecation policy, versioning policy, and v1.0 readiness.
- Added `contracts/` metadata for CLI commands, diagnostic codes, schema names, and exit codes.
- Added `scripts/dev/check_contracts.py` and CI coverage for contract drift.
- Tightened CLI, schema, and diagnostic references for v1.0 readiness.
- Bumped Paper Scaffold to `0.9.3`.

## v0.9.2

- Added `scripts/dev/clean_install_audit.py` for clone, no-install, editable-install, fallback, text-blob, test-runner, and optional package-build checks.
- Documented clean-install audit expectations for public-user release checks.
- Added tests for audit command construction without network cloning.
- Bumped Paper Scaffold to `0.9.2`.

## v0.9.1

- Added `scripts/dev/run_tests.py` as the preferred shell-independent local pytest runner.
- Created unique repo-local pytest basetemp and `TMP`/`TEMP` directories for each test run.
- Updated CI to use the test runner instead of raw `pytest tests`.
- Documented the Windows locked-basetemp failure mode and the preferred runner command.
- Bumped Paper Scaffold to `0.9.1`.

## v0.9.0

- Added `python -m paper_scaffold` as an installed-use fallback when the console script is not on `PATH`.
- Added global `--version`.
- Added `self-test` for no-network installed-use smoke testing.
- Added `schema list` and `schema show` for metadata and generated-report schema summaries.
- Added install, CLI reference, schema reference, release process, exit-code, and compatibility docs.
- Hardened GitHub Actions for multi-OS, multi-Python checks, module fallback, self-test, text blob guard, and package build.
- Added clean-install notes and stability audit for the v1.0 release-candidate path.

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
