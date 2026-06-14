# Contributing

Thanks for helping improve Paper Scaffold.

## Before Larger Changes

Open an issue first for major changes, new commands, or workflow changes. Small documentation fixes can go straight to a pull request.

## Local Checks

```bash
python -m pip install -e ".[dev]"
python scripts/dev/run_tests.py
ruff check .
python scripts/paper-scaffold.py --help
python -m paper_scaffold --help
python scripts/paper-scaffold.py doctor
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/validation_report.md --write-json scratch/demo_manuscript/validation_report.json
python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
python scripts/dev/check_text_blobs.py
python scripts/dev/build_package.py
python scripts/dev/install_matrix_audit.py
```

With an explicit environment interpreter, the same test runner can be called as:

```powershell
<env-python> scripts\dev\run_tests.py
```

`scripts/dev/run_tests.py` creates a unique repo-local pytest basetemp and `TMP`/`TEMP` directory under `scratch/test-runs/` on every run. This avoids shell-specific environment-variable syntax and avoids reusing a stale `scratch\pytest-tmp` directory that Windows may keep locked after a failed or interrupted run.

Before release candidates, run a clean-install audit from a committed state:

```bash
python scripts/dev/clean_install_audit.py
```

With an explicit environment interpreter:

```powershell
<env-python> scripts\dev\clean_install_audit.py
```

The audit clones into `scratch/clean-install/`, checks no-install usage, performs `python -m pip install -e ".[dev]"`, verifies the module fallback, runs `self-test`, runs the text blob guard, and runs tests through `scripts/dev/run_tests.py`. The console-script and package-build checks are optional because PATH and installed build tooling differ by machine.

For packaging release checks, `scripts/dev/build_package.py` builds local wheel/sdist artifacts when the optional `build` frontend is installed, and `scripts/dev/install_matrix_audit.py` checks source, editable, fallback, console-script, and optional wheel/sdist install modes. These scripts do not publish to PyPI and default to network-free install checks.

On Git Bash for Windows, editable install can succeed while `paper-scaffold` is still not on `PATH`. Either call the installed executable directly:

```bash
<env-root>/Scripts/paper-scaffold.exe --help
```

or add the environment Scripts directory:

```bash
export PATH="/path/to/env/Scripts:$PATH"
paper-scaffold --help
```

The install-safe fallback is:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

If pytest cannot access the default Windows temp directory, prefer the shell-independent runner:

```bash
python scripts/dev/run_tests.py
```

The older Git Bash style is still fine in Git Bash when a one-off command is useful:

```bash
mkdir -p scratch/tmp scratch/pytest-tmp
TMP="$PWD/scratch/tmp" TEMP="$PWD/scratch/tmp" python -m pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider
```

Pre-commit is optional for normal users but recommended for contributors:

```bash
pre-commit install
pre-commit run --all-files
```

## Text Blob Line Endings

GitHub raw view reads committed Git blobs, not the local working tree. A local checkout can show normal line counts while the committed blob is stored with CR-only or otherwise collapsed line endings. That makes public raw files look like one very long line.

Run this guard before release branches:

```bash
python scripts/dev/check_text_blobs.py
```

If it reports CR bytes or collapsed blobs, normalize tracked text files and the index:

```bash
python scripts/dev/normalize_text_blobs.py --apply
```

`.gitattributes` is present to make Git store common text files with LF endings. The normalization utility also writes exact LF bytes to the Git index with `git hash-object -w --no-filters` and `git update-index`, which is the part that fixes the blob GitHub raw will display after commit.

## Contribution Guidelines

- Keep the tool generic for researchers across fields.
- Do not commit private documents, raw data, credentials, model outputs, or large binaries.
- Add tests for CLI behavior changes.
- Update docs when behavior changes.
- Keep dependencies minimal and optional when possible.
- Prefer small, reviewable pull requests.
