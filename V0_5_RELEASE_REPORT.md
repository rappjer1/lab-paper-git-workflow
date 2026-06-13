# v0.5 Release Report

## Scope

v0.5 is an architecture-hardening release. It adds maintainability structure, schema validation, stronger reports, artifact workflow checks, development hygiene, CI hardening, and a public roadmap toward v1.0.

## Files Changed

- Core code: `src/paper_scaffold/schemas.py`, `src/paper_scaffold/checks.py`, `src/paper_scaffold/cli.py`, `src/paper_scaffold/validation.py`, `src/paper_scaffold/discovery.py`, `src/paper_scaffold/messages.py`, `src/paper_scaffold/artifact_manifest.py`.
- Project metadata: `pyproject.toml`, `.pre-commit-config.yaml`, `.github/workflows/tests.yml`, `CHANGELOG.md`.
- Docs: `README.md`, `CONTRIBUTING.md`, `docs/error_codes.md`, `docs/artifact_manifest.md`, `docs/validation.md`, `docs/adr/*.md`, `ROADMAP.md`.
- Tests: `tests/test_v05_architecture.py`.

## ADRs Created

- `docs/adr/0001-project-scope.md`
- `docs/adr/0002-template-engine-strategy.md`
- `docs/adr/0003-config-and-manifest-schemas.md`
- `docs/adr/0004-cli-framework-strategy.md`
- `docs/adr/0005-packaging-and-release-strategy.md`
- `docs/adr/0006-documentation-site-strategy.md`

## Schema Strategy Chosen

v0.5 uses dependency-free dataclass-backed schema definitions and explicit validation in `src/paper_scaffold/schemas.py`.

Schemas cover:

- `artifact_manifest.yaml`
- `terminology_map.yaml`
- `manuscript_config.yaml`
- `validation_report.json`

Unknown metadata fields are warnings. Structural problems and missing required fields are errors.

## Dependencies Added Or Avoided

Runtime dependencies avoided:

- Pydantic was evaluated and deferred.
- Typer/Rich were evaluated and deferred.
- Copier was evaluated and deferred.
- MkDocs Material was evaluated and deferred.
- uv was evaluated and deferred.
- Hatch was evaluated and deferred.

Development dependencies added:

- Ruff
- pre-commit

## Commands Added

- `paper-scaffold stale-artifacts`
- `paper-scaffold unused-artifacts`

Command improved:

- `paper-scaffold validate --write-json`

## Tests Added

- Schema validation for valid and invalid manifests.
- JSON validation report generation and schema validation.
- Stale artifact detection.
- Unused artifact detection.
- Discovery destination suggestions.
- CLI help surface for v0.5 commands.
- ADR and roadmap existence.
- README workflow and roadmap checks.

## Validation Results

```text
syntax compile: passed
pytest tests -p no:cacheprovider: 36 passed
paper-scaffold --help: passed
paper-scaffold doctor: passed
paper-scaffold explain E003: passed
paper-scaffold demo --output scratch/demo_manuscript --overwrite: passed
paper-scaffold validate --write-report --write-json: passed
paper-scaffold stale-artifacts: passed, no stale demo artifacts
paper-scaffold unused-artifacts: passed, expected demo warnings for unreferenced example artifacts
paper-scaffold overleaf-check: passed, expected demo warnings for unreferenced figures
paper-scaffold privacy-check --path .: passed, expected warnings only in audit/checklist search strings
paper-scaffold github-check --repo .: passed, expected warnings for uncommitted work, no upstream, and audit/checklist search strings
ruff check .: not run locally because Ruff is not installed in the current environment; CI installs dev dependencies and runs it
```

## Known Limitations

- Schema validation is intentionally lightweight and not a full JSON Schema export.
- `stale-artifacts` only compares files when both source and manuscript copies exist.
- `unused-artifacts` is heuristic and may warn on files referenced indirectly by custom LaTeX macros.
- Ruff is a contributor/dev dependency, not a normal user dependency.

## Recommended Next Release

v0.6 should evaluate MkDocs Material and Copier with small prototypes, then adopt only if they simplify real maintenance work.

## Exact Git Commands

```bash
git add .
git commit -m "Add v0.5 architecture hardening"
git push -u origin v0.5-architecture-hardening

git checkout main
git pull --ff-only origin main
git merge --no-ff v0.5-architecture-hardening
git push origin main

git tag v0.5.0
git push origin v0.5.0
```
