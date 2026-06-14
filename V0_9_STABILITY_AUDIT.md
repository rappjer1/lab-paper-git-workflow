# v0.9 Stability Audit

## Stable Commands For Normal Use

- `doctor`
- `quickstart`
- `self-test`
- `init`
- `demo`
- `validate`
- `overleaf-check`
- `github-check`
- `privacy-check`
- `check-figures`
- `check-citations`
- `check-labels`
- `discover-artifacts`
- `add-artifact`
- `copy-artifacts`
- `stale-artifacts`
- `unused-artifacts`
- `audit-project`
- `release-check`
- `provenance-report`
- `artifact-status`
- `freeze-artifacts`
- `compare-lock`
- `add-manuscript-ci`
- `package-submission`
- `reviewer-binder`
- `schema list`
- `schema show`
- `explain`

## Pre-1.0 Stable Schemas

- `metadata/artifact_manifest.yaml`
- `metadata/manuscript_config.yaml`
- `metadata/terminology_map.yaml`
- `validation_report.json`
- `metadata/provenance_ledger.json`
- `metadata/artifact_lock.json`
- `lock_comparison.json`

These shapes should not receive breaking changes before v1.0 unless a defect requires it.

## Commands That May Still Change Before 1.0

- `import-word`: conversion quality and cleanup guidance may improve.
- `audit-word-conversion`: heuristics may expand.
- `make-slack-summary`: launch messaging may be revised.
- Exit codes for older check commands may be normalized before 1.0.

## Known Limitations

- Paper Scaffold does not compile LaTeX.
- Paper Scaffold does not create GitHub repositories.
- Paper Scaffold does not upload to Overleaf.
- Word conversion still requires Pandoc and manual review.
- Artifact provenance compares files and declared metadata; it does not prove scientific correctness.
- Package builds are local only in v0.9; no PyPI publishing.

## Must Freeze At 1.0

- Command names.
- Required schema fields.
- Generated JSON report field names.
- Diagnostic code meanings.
- Exit-code behavior.
- Public install and invocation docs.

## Recommended 1.0 Checklist

- Confirm clean clone on Windows, Linux, and macOS.
- Confirm editable install and `python -m paper_scaffold`.
- Confirm console script behavior when Scripts/bin is on `PATH`.
- Confirm GitHub Actions passes on all matrix entries.
- Confirm text blob guard after staging.
- Confirm docs match command help.
- Decide whether exit-code normalization is needed before tagging.
- Decide whether PyPI publishing remains out of scope for 1.0.
