# v0.9.1 Test Runner Report

Branch: `v0.9.1-windows-test-runner-hardening`

Version: `0.9.1`

## Problem Fixed

Local validation used shell-specific pytest commands. Git Bash can use `TMP="$PWD/..."`, CMD needs `set TMP=...`, PowerShell needs `$env:TMP = ...`, and reused `scratch\pytest-tmp` folders can remain locked on Windows. v0.9.1 adds a Python test runner that creates unique repo-local pytest and temp directories for every run.

## Files Changed

- `scripts/dev/run_tests.py`
- `.github/workflows/tests.yml`
- `pyproject.toml`
- `src/paper_scaffold/__init__.py`
- `src/paper_scaffold/schema_reference.py`
- `tests/test_v091_test_runner.py`
- `tests/test_v09_release_candidate.py`
- `README.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `docs/troubleshooting.md`
- `docs/install.md`
- `docs/compatibility.md`
- `docs/release_process.md`
- `docs/schema_reference.md`
- `V0_9_CLEAN_INSTALL_NOTES.md`
- `V0_9_1_TEST_RUNNER_REPORT.md`

## Validation Results

Passed:

- `<python> scripts/dev/check_text_blobs.py`
- `<python> scripts/paper-scaffold.py --version`
- `<python> -m paper_scaffold --help`
- `<python> scripts/dev/run_tests.py`
- `<python> -m ruff check .`

Test result:

- `85 passed in 16.69s`

Focused runner check:

- `<python> scripts/dev/run_tests.py --pytest-args "-q -k run_tests"`
- `5 passed, 80 deselected`

## Known Limitations

- The runner does not replace pytest; it only prepares a safer subprocess environment.
- `--pytest-args` accepts a simple quoted string and is not meant to replace complex shell scripts.
- The runner cleans temp directories by default, but Windows may still prevent cleanup if another process holds a file handle.
- v0.9.1 does not add product workflows, publish to PyPI, or change GitHub/Overleaf behavior.
- The optional `scripts/dev/run_smoke.py` was not added so the release stays focused on the pytest runner.

## Ready Status

v0.9.1 is ready for review.

## Exact Git Commands

```bash
git status --short
git add .github/workflows/tests.yml CHANGELOG.md CONTRIBUTING.md README.md V0_9_CLEAN_INSTALL_NOTES.md V0_9_1_TEST_RUNNER_REPORT.md docs/compatibility.md docs/install.md docs/release_process.md docs/schema_reference.md docs/troubleshooting.md pyproject.toml scripts/dev/run_tests.py src/paper_scaffold/__init__.py src/paper_scaffold/schema_reference.py tests/test_v09_release_candidate.py tests/test_v091_test_runner.py
git commit -m "Harden Windows test runner"
git push -u origin v0.9.1-windows-test-runner-hardening
git checkout main
git pull --ff-only
git merge --no-ff v0.9.1-windows-test-runner-hardening
git tag -a v0.9.1 -m "Paper Scaffold v0.9.1"
git push origin main
git push origin v0.9.1
```
