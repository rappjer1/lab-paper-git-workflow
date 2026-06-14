# v0.9.6 Packaging And Install Report

## Purpose

v0.9.6 is a narrow packaging, build, and install-matrix hardening release. It does not add product workflows or change the public CLI contract.

## Scripts Added

- `scripts/dev/build_package.py`
- `scripts/dev/install_matrix_audit.py`

## Install Modes Checked

- Source checkout wrapper: `python scripts/paper-scaffold.py --help`
- Source module fallback: `python -m paper_scaffold --help`
- Editable install in a temporary environment
- Editable installed module fallback
- Editable installed console script
- Editable installed `self-test`
- Optional wheel install when a local wheel exists
- Optional sdist install when a local sdist exists

## Validation Results

- `python scripts/dev/check_text_blobs.py`: passed.
- `python scripts/dev/check_contracts.py`: passed.
- `python scripts/dev/check_docs_examples.py`: passed.
- `python scripts/dev/check_example_integrity.py`: passed with 75 files checked and 0 problems.
- `python scripts/dev/build_package.py`: passed with a clean skip because the optional `build` frontend is not installed; no files were published.
- `python scripts/dev/install_matrix_audit.py`: passed. Required source wrapper, source module fallback, editable install venv, editable install, editable module fallback, editable console script, and editable self-test checks passed. Wheel and sdist checks skipped because no local `dist/` artifacts exist.
- `python scripts/dev/run_tests.py`: passed with 131 tests passed.

## Known Limitations

- `build_package.py` skips package building when the optional `build` frontend is not installed.
- Wheel and sdist install checks run only when local artifacts exist in `dist/`.
- The install matrix defaults to `--no-deps --no-build-isolation` to avoid package-index access.
- No command publishes to PyPI.

## Remaining Before v1.0

- Run one final clean install audit from a fresh checkout.
- Review command, schema, diagnostic, and exit-code contract stability.
- Decide whether package build artifacts should become part of the v1.0 release checklist.

## Ready Status

v0.9.6 is ready. Required validation passed, and skipped optional package checks are recorded.

## Git Commands

```bash
git status --short
git add .
git commit -m "Prepare v0.9.6 packaging install hardening"
git push -u origin v0.9.6-packaging-install-hardening
git checkout main
git merge --no-ff v0.9.6-packaging-install-hardening
git tag -a v0.9.6 -m "Paper Scaffold v0.9.6"
git push origin main
git push origin v0.9.6
```
