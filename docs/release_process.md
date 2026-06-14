# Release Process

This project is not published to PyPI in v0.9. Releases are GitHub branch, merge, and tag events only.

## Local Validation

Run from a clean working tree:

```bash
python scripts/dev/check_text_blobs.py
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py --version
python -m paper_scaffold --help
python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
python scripts/paper-scaffold.py schema list
python scripts/paper-scaffold.py schema show artifact-manifest
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py release-check --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/release_check.md
python -m pytest tests
```

On Windows, use the repo-local pytest temp workaround documented in `docs/install.md`.

## Package Build

Install the build extra, then build locally:

```bash
python -m pip install -e ".[build]"
python -m build
```

Inspect `dist/` locally. Do not publish to PyPI in v0.9.

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

## Tag Process

After review and merge:

```bash
git checkout main
git pull --ff-only
git tag -a v0.9.0 -m "Paper Scaffold v0.9.0"
git push origin main
git push origin v0.9.0
```

## What Not To Publish Accidentally

- Do not publish to PyPI.
- Do not upload generated demo manuscript outputs.
- Do not commit private manuscript text, credentials, local paths, raw data, or model outputs.
- Do not tag until tests and Actions pass.
