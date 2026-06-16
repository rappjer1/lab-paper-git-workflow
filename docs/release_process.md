# Release Process

This project is not published to PyPI in v0.9. Releases are GitHub branch, merge, and tag events only.

## v0.9.9 Release-Candidate Dry Run

v0.9.9 adds a maintainer-only release-candidate audit that composes the v1.0 checks without publishing, pushing, tagging, creating remote resources, or uploading anything.

Run it from the release-candidate branch:

```bash
python scripts/dev/release_candidate_audit.py --output scratch/release-candidate
```

Use `--allow-dirty` while developing the release branch. Use a clean working tree before relying on the result for a tag:

```bash
python scripts/dev/release_candidate_audit.py --output scratch/release-candidate --allow-dirty
```

The audit runs text-blob, contract, docs/examples, docs-link, example-integrity, public-safety, dogfood, self-test, test-runner, install-matrix, clean-clone dogfood, version consistency, and Git-status checks. It runs the package build script when available; if the Python build frontend is not installed, the package build is recorded as a skip rather than a release failure.

Interpret skips explicitly:

- Package build skipped: install the optional build extra and rerun if local wheel/sdist artifacts are part of the release decision.
- Clean install skipped on a dirty tree: commit or stash local changes, then rerun from a clean branch.
- Clean clone dogfood skipped by flag: rerun without `--skip-clean-clone` before tagging v1.0.

For a command plan without expensive checks:

```bash
python scripts/dev/release_candidate_audit.py --plan
```

Do not use this audit to publish to PyPI, create GitHub releases, push branches, create tags, upload to Overleaf, or introduce credentials. It is a local readiness dry run.

## Local Validation

Run from a clean working tree:

```bash
python scripts/dev/check_text_blobs.py
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py --version
python -m paper_scaffold --help
python scripts/dev/check_root_layout.py
python scripts/dev/check_contracts.py
python scripts/dev/check_docs_examples.py
python scripts/dev/check_docs_links.py
python scripts/dev/check_example_integrity.py
python scripts/dev/check_public_safety.py
python scripts/dev/release_candidate_audit.py --plan
python scripts/dev/build_package.py
python scripts/dev/install_matrix_audit.py
python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output
python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
python scripts/paper-scaffold.py schema list
python scripts/paper-scaffold.py schema show artifact-manifest
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py release-check --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/release_check.md
python scripts/dev/run_tests.py
```

`scripts/dev/run_tests.py` is the preferred local test command on all shells. It creates unique repo-local pytest temp directories and avoids reusing locked Windows basetemp folders.

## Package Build

Install the build extra, then build locally:

```bash
python -m pip install -e ".[build]"
python scripts/dev/build_package.py --clean
```

Inspect `dist/` locally. The script validates that local wheel and sdist artifacts exist when build succeeds. Do not publish to PyPI in v0.9.

## Install Matrix

Run the install matrix before a release candidate:

```bash
python scripts/dev/install_matrix_audit.py
```

It checks no-install source usage, `python -m paper_scaffold`, editable install, console script help, self-test after editable install, and optional local wheel/sdist installs. These are local checks only; they are not PyPI publishing.

## Clean Clone Test

```bash
git clone https://github.com/rappjer1/lab-paper-git-workflow.git paper-scaffold-clean
cd paper-scaffold-clean
python scripts/paper-scaffold.py --help
python -m pip install -e .
python -m paper_scaffold self-test
```

Also check the console script when the environment scripts directory is on `PATH`:

```bash
paper-scaffold self-test
```

## GitHub Actions

Before tagging, confirm Actions pass for supported operating systems and Python versions. CI should not require secrets, Overleaf, GitHub CLI, Pandoc, LaTeX, or network services beyond package installation and normal GitHub Actions setup.

Review [github_repo_settings.md](github_repo_settings.md) before changing repository settings. Paper Scaffold does not change GitHub settings automatically.

## Tag Process

After review and merge:

```bash
git checkout main
git pull --ff-only
git tag -a v<version> -m "Paper Scaffold v<version>"
git push origin main
git push origin v<version>
```

For v1.0, prepare [V1_0_RELEASE_NOTES_DRAFT.md](release_reports/V1_0_RELEASE_NOTES_DRAFT.md), complete [V1_0_FINAL_CHECKLIST.md](release_reports/V1_0_FINAL_CHECKLIST.md), confirm the release-candidate audit report has no required failures, then review tag commands before execution:

```bash
git checkout main
git pull --ff-only
git tag -a v1.0.0 -m "Paper Scaffold v1.0.0"
git push origin main
git push origin v1.0.0
```

## What Not To Publish Accidentally

- Do not publish to PyPI.
- Do not upload generated demo manuscript outputs.
- Do not commit private manuscript text, credentials, local paths, raw data, or model outputs.
- Do not tag until tests and Actions pass.

Historical release reports are listed in [release_reports.md](release_reports.md).
