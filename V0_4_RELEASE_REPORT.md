# v0.4 Release Report

## Scope

v0.4 adds a structured diagnostics layer to Paper Scaffold. The release keeps the repository public-facing and generic while improving the user experience when manuscript repositories are not ready for GitHub/Overleaf sync.

## Added Commands

- `paper-scaffold explain`
- `paper-scaffold overleaf-check`
- `paper-scaffold github-check`
- `paper-scaffold privacy-check`
- `paper-scaffold check-figures`
- `paper-scaffold check-citations`
- `paper-scaffold check-labels`
- `paper-scaffold audit-word-conversion`

## Added Docs

- `docs/error_codes.md`
- Expanded `docs/troubleshooting.md`
- Expanded `docs/validation.md`
- README diagnostics section

## Added Tests

- Diagnostic message registry coverage.
- Known and unknown `explain` code behavior.
- Demo plus focused diagnostics.
- Validation report generation.
- Privacy scan detection and redaction.
- Citation and LaTeX label error detection.
- Word-conversion audit heuristics.
- Duplicate artifact ID discovery behavior.

## Public-Readiness Notes

- The diagnostics are generic and do not depend on any manuscript, research repo, field-specific project, model output, or external service.
- No commands create GitHub repositories, upload to Overleaf, call external APIs, or modify outside the selected manuscript path.
- Large/raw/model/cache outputs remain blocked by validation and discovery filters.
- Privacy previews redact local paths, emails, and secret-like values.

## Manual Steps Before Public Visibility

- Review `git status --short` and `git diff --stat`.
- Run the v0.4 validation commands listed in the final task summary.
- Push the branch and confirm GitHub Actions passes.
- Merge to `main`.
- Tag `v0.4.0`.
- Only then change GitHub visibility if desired.
