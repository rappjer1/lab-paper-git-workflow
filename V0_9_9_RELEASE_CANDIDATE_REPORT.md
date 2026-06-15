# v0.9.9 Release Candidate Report

Branch: `v0.9.9-release-candidate-dry-run`

Version: `0.9.9`

## Purpose

v0.9.9 is the final release-candidate dry run before v1.0.0. It adds a maintainer-only audit script that composes the existing public-safety, contract, docs, example, dogfood, test, install, clean-clone, package-build, version, and Git-status checks without adding user-facing workflows.

## Checks Run

The release-candidate audit covers:

- Text blob guard.
- Contract audit.
- Docs/examples check.
- Docs link check.
- Example integrity check.
- Public safety audit.
- Dogfood scenarios.
- Self-test.
- Full test suite through `scripts/dev/run_tests.py`.
- Install matrix audit when available.
- Clean install audit when it can represent the current tree.
- Clean clone dogfood audit when not skipped.
- Optional local package build.
- Version consistency across `pyproject.toml`, package `__version__`, CLI `--version`, and module help.
- Git status, branch, HEAD, and tags at HEAD.

## Summary

Local validation passed for the v0.9.9 release-candidate dry run.

- Release-candidate audit: passed.
- Required audit checks: 13 passed, 0 failed.
- Optional audit checks: 2 skipped.
- Full test suite: 155 passed.
- Dogfood scenarios: 9 passed, 0 failed.
- Self-test: passed.
- Version consistency: `0.9.9` across package metadata, package `__version__`, CLI version output, and module help.

## Package Build Status

Package build was skipped by the audit because the Python build frontend was not installed in the validation environment. The skip is acceptable for this dirty-tree dry run, but maintainers should install the optional build extra and rerun before using local wheel/sdist artifacts for a final v1.0 decision.

## Clean Install Status

Clean install audit was skipped because the working tree was dirty. That avoids a misleading local-source clone that would omit uncommitted v0.9.9 files. Run the audit again from a clean branch before tagging v1.0.

## Clean Clone And Dogfood

Clean clone dogfood passed using the local source with the working tree overlaid into the clone. The clone ran text-blob, contract, docs/examples, example-integrity, dogfood, tests, and self-test checks successfully.

## GitHub Actions Manual Check

Before v1.0.0, confirm that GitHub Actions are green on supported operating systems and Python versions. This report does not create remote releases or modify repository settings.

## Limitations

- v0.9.9 does not add product workflows.
- v0.9.9 does not publish to PyPI.
- v0.9.9 does not create GitHub releases or remote repositories.
- v0.9.9 does not compile LaTeX or require Pandoc, LaTeX, GitHub CLI, Overleaf, or network services for normal local checks.
- A dirty-tree audit can validate local files but should not be treated as the final tag audit.

## Remaining v1.0 Tasks

- Run the release-candidate audit from a clean branch.
- Install the optional build extra and rerun local package build if wheel/sdist inspection is required.
- Review and finalize `V1_0_RELEASE_NOTES_DRAFT.md`.
- Complete `V1_0_FINAL_CHECKLIST.md`.
- Confirm GitHub Actions are green.
- Bump version to `1.0.0` on the v1.0 branch.
- Review tag commands before execution.

## Exact Git Commands For v0.9.9

```bash
git status --short
git add .
git commit -m "Add v0.9.9 release candidate dry run"
git push -u origin v0.9.9-release-candidate-dry-run
git checkout main
git pull --ff-only
git merge --ff-only v0.9.9-release-candidate-dry-run
git tag -a v0.9.9 -m "Paper Scaffold v0.9.9"
git push origin main
git push origin v0.9.9
```

## Proposed Git Commands For v1.0.0

```bash
git checkout main
git pull --ff-only
git checkout -b v1.0.0-release
git status --short
git add .
git commit -m "Prepare Paper Scaffold v1.0.0"
git push -u origin v1.0.0-release
git checkout main
git pull --ff-only
git merge --ff-only v1.0.0-release
git tag -a v1.0.0 -m "Paper Scaffold v1.0.0"
git push origin main
git push origin v1.0.0
```
