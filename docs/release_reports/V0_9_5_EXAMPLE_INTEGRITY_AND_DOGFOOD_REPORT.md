# v0.9.5 Example Integrity And Dogfood Report

## Purpose

v0.9.5 is a narrow public-polish release focused on example integrity, dogfood validation, and v1.0 readiness.

## Files Changed

- Added `scripts/dev/check_example_integrity.py`.
- Added `scripts/dev/generate_example_artifacts.py`.
- Added `scripts/dev/clean_clone_dogfood_audit.py`.
- Added `docs/example_integrity.md`.
- Added `tests/test_v095_example_integrity.py`.
- Added `V0_9_5_PUBLIC_POLISH_AUDIT.md`.
- Regenerated bundled synthetic example PDF and PNG artifacts.
- Updated public docs, example docs, CI, changelog, roadmap, schema docs, and version metadata.

## Checks Added

- Example/template file signature checks for PDFs, PNGs, JPEGs, and text examples.
- Example/template UTF-8, size, and local-path checks.
- Clean-clone dogfood audit script for release-candidate validation.
- CI step for example integrity.

## Validation Results

- `python scripts/dev/check_text_blobs.py`: passed.
- `python scripts/dev/check_contracts.py`: passed.
- `python scripts/dev/check_docs_examples.py`: passed.
- `python scripts/dev/check_example_integrity.py`: passed with 75 files checked and 0 problems.
- `python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output`: passed with 9 steps passed and 0 failed.
- `python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`: passed with 10 steps passed and 0 failed.
- `python scripts/dev/run_tests.py`: passed with 125 tests passed.
- `python scripts/dev/clean_clone_dogfood_audit.py --source . --clone-path scratch/clean-clone-dogfood --overwrite`: passed; text blob guard, contract audit, docs/examples check, example integrity, dogfood, tests, and self-test all exited 0 inside the local clone.
- `python -m ruff check .`: passed.
- `python -m build`: not run because the optional `build` package is not installed in the validation environment.

## Known Limitations

- Example PDFs and PNGs are deliberately tiny synthetic artifacts, not publication figures.
- The clean-clone dogfood audit uses a local clone for release-candidate validation unless a remote source is supplied.
- The audit does not upload to Overleaf, call network services, publish packages, or validate real manuscript science.
- Optional package-build validation requires the `build` package to be installed.

## v1.0 Remaining Tasks

- Review the public contract one final time.
- Freeze command, schema, diagnostic, and exit-code compatibility expectations.
- Run clean install and dogfood validation from a fresh checkout before tagging v1.0.

## Ready Status

v0.9.5 is ready. Required validation passed, and optional package build status is recorded as unavailable in this environment.

## Git Commands

```bash
git status --short
git add .
git commit -m "Prepare v0.9.5 example integrity release"
git push -u origin v0.9.5-example-integrity-and-public-polish
git checkout main
git merge --no-ff v0.9.5-example-integrity-and-public-polish
git tag -a v0.9.5 -m "Paper Scaffold v0.9.5"
git push origin main
git push origin v0.9.5
```
