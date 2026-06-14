# Clean Install Audit

`scripts/dev/clean_install_audit.py` verifies that Paper Scaffold works for a public user starting from a fresh clone.

This is a release-audit tool for maintainers. It is slower than normal local checks because it creates a clone, installs the package in editable mode, and runs the full test suite through `scripts/dev/run_tests.py`.

## What It Checks

- Fresh clone into `scratch/clean-install/` or a path passed with `--clone-path`.
- No-install wrapper usage:
  - `python scripts/paper-scaffold.py --help`
  - `python scripts/paper-scaffold.py self-test`
- Editable install:
  - `python -m pip install -e ".[dev]"`
- Installed console script when `paper-scaffold` is available on `PATH`.
- Module fallback:
  - `python -m paper_scaffold --help`
- Installed-use self-test:
  - `python -m paper_scaffold self-test`
- Text blob guard:
  - `python scripts/dev/check_text_blobs.py`
- Full tests through the shell-independent runner:
  - `python scripts/dev/run_tests.py`
- Optional package build when the `build` frontend is installed.

## Basic Use

```bash
python scripts/dev/clean_install_audit.py
```

In the lab Windows environment:

```powershell
R:\Code\Envs\nh_quantum\python.exe scripts\dev\clean_install_audit.py
```

By default, the audit clones from `origin` when available and otherwise clones from the current checkout path. Generated clone folders are placed under:

```text
scratch/clean-install/
```

## Custom Clone Path

```bash
python scripts/dev/clean_install_audit.py --clone-path scratch/clean-install/manual-audit
```

The clone path must not already exist unless you pass `--overwrite`:

```bash
python scripts/dev/clean_install_audit.py --clone-path scratch/clean-install/manual-audit --overwrite
```

## Custom Source

Use `--source` to audit a specific local path, branch URL, or public repository URL:

```bash
python scripts/dev/clean_install_audit.py --source https://github.com/<owner>/<repo>.git
```

For release candidates, run this after the branch has been pushed or from a local source that contains the exact committed state you intend to audit. Git clones do not include uncommitted working-tree edits.

## Expected Optional Skips

The installed console-script check is optional. On Windows Git Bash, editable install can succeed while the environment `Scripts` directory is not on `PATH`; in that case the audit still verifies `python -m paper_scaffold --help`.

The package build check is optional. If `python -m build --version` fails because the build frontend is not installed, the audit reports a skip rather than failing the release audit.
