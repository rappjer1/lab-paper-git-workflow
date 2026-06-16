# v0.9 Release Report

Branch: `v0.9-release-candidate-hardening`

Version: `0.9.0`

## Commands Added

- `paper-scaffold self-test`
- `paper-scaffold schema list`
- `paper-scaffold schema show <schema-name>`
- `paper-scaffold --version`
- `python -m paper_scaffold ...`

## Docs Added

- `docs/cli_reference.md`
- `docs/schema_reference.md`
- `docs/install.md`
- `docs/release_process.md`
- `docs/exit_codes.md`
- `docs/compatibility.md`
- `V0_9_CLEAN_INSTALL_NOTES.md`
- `V0_9_STABILITY_AUDIT.md`

## CI Changes

- GitHub Actions now tests Python 3.10 and 3.11.
- Matrix now covers `ubuntu-latest`, `windows-latest`, and `macos-latest`.
- CI installs `.[dev,build]`.
- CI runs Ruff, pytest, text blob guard, CLI help, CLI version, `python -m paper_scaffold --help`, `paper-scaffold self-test`, demo release-check, artifact checks, and package build.

## Install Hardening

- Added `src/paper_scaffold/__main__.py` for `python -m paper_scaffold`.
- Added global `--version`.
- Added `self-test` as a first installed-use smoke command.
- Updated README, Quick Start, Getting Started, Troubleshooting, Contributing, and install docs with:
  - `python scripts/paper-scaffold.py ...`
  - `paper-scaffold ...`
  - `python -m paper_scaffold ...`

## Schema And Reference Changes

- Added descriptive schema registry in `src/paper_scaffold/schema_reference.py`.
- Added `schema list` and `schema show`.
- Documented user-authored and generated schemas:
  - `artifact_manifest.yaml`
  - `manuscript_config.yaml`
  - `terminology_map.yaml`
  - `provenance_ledger.json`
  - `artifact_lock.json`
  - `validation_report.json`
  - `lock_comparison.json`

## Tests Passed

- Focused v0.9 tests: 12 passed.
- Full suite with fresh repo-local basetemp: 80 passed.
- Ruff: passed.

## Validation Results

Passed:

- `<python> scripts/dev/check_text_blobs.py`
- `<python> scripts/paper-scaffold.py --help`
- `<python> scripts/paper-scaffold.py --version`
- `<python> -m paper_scaffold --help`
- `<python> scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`
- `<python> scripts/paper-scaffold.py schema list`
- `<python> scripts/paper-scaffold.py schema show artifact-manifest`
- `<python> scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite`
- `<python> scripts/paper-scaffold.py release-check --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/release_check.md`

Pytest note:

- The exact documented target `scratch/pytest-tmp` was not usable in this working copy because Windows denied access to that existing folder.
- The same repo-local temp workaround pattern passed with a fresh basetemp:

```powershell
New-Item -ItemType Directory -Force -Path scratch/tmp,scratch/pytest-full-v09 | Out-Null
$env:TMP = (Resolve-Path scratch/tmp).Path
$env:TEMP = (Resolve-Path scratch/tmp).Path
<python> -m pytest tests --basetemp=scratch/pytest-full-v09/run -p no:cacheprovider
```

Result: 80 passed.

## Package Build Result

Local package build was not run because the current environment does not have the `build` frontend installed:

```text
No module named build
```

The `build` optional extra was added to `pyproject.toml`, and GitHub Actions now installs `.[dev,build]` and runs `python -m build`.

## Known Limitations

- v0.9 does not publish to PyPI.
- Some older commands still use pre-1.0 exit-code behavior where blocking findings can return `1`.
- Self-test validates no-network workflow behavior but does not compile LaTeX.
- Schema summaries are descriptive, not full formal JSON Schema documents.
- Paper Scaffold still does not create GitHub repositories or upload to Overleaf.

## Recommended v1.0 Scope

- Freeze CLI command names and global options.
- Freeze required schema/report fields.
- Freeze diagnostic code meanings.
- Decide whether to normalize legacy check exit codes.
- Confirm clean clone and editable install on Windows, Linux, and macOS.
- Confirm GitHub Actions matrix passes before tagging.
- Decide explicitly whether PyPI remains out of scope for v1.0.

## Exact Git Commands

```bash
git status --short
git add .github/workflows/tests.yml CHANGELOG.md CONTRIBUTING.md QUICKSTART.md README.md ROADMAP.md docs/getting_started.md docs/troubleshooting.md docs/cli_reference.md docs/compatibility.md docs/exit_codes.md docs/install.md docs/release_process.md docs/schema_reference.md pyproject.toml src/paper_scaffold/__init__.py src/paper_scaffold/__main__.py src/paper_scaffold/cli.py src/paper_scaffold/schema_reference.py tests/test_v051_hotfix.py tests/test_v08_workflows.py tests/test_v09_release_candidate.py V0_9_CLEAN_INSTALL_NOTES.md V0_9_STABILITY_AUDIT.md V0_9_RELEASE_REPORT.md
git commit -m "Harden release candidate install and schema workflows"
git push -u origin v0.9-release-candidate-hardening
git checkout main
git pull --ff-only
git merge --no-ff v0.9-release-candidate-hardening
git tag -a v0.9.0 -m "Paper Scaffold v0.9.0"
git push origin main
git push origin v0.9.0
```
