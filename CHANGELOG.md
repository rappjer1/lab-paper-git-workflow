# Changelog

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
