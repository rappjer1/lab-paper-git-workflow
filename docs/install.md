# Install

Paper Scaffold can run without installation from a checkout, through an editable install, or through the module fallback.

## No-Install Usage From Checkout

```bash
git clone https://github.com/rappjer1/lab-paper-git-workflow.git
cd lab-paper-git-workflow
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py self-test
```

## Editable Install

```bash
python -m pip install -e .
paper-scaffold --help
paper-scaffold self-test
```

For contributor tools:

```bash
python -m pip install -e ".[dev]"
python scripts/dev/run_tests.py
```

The test runner creates unique repo-local pytest and temp directories under `scratch/test-runs/`, so it works from CMD, PowerShell, and Git Bash without shell-specific `TMP=...` syntax.

For clean-clone release audits:

```bash
python scripts/dev/clean_install_audit.py
```

See [clean_install_audit.md](clean_install_audit.md) for clone source and optional check details.

For local package builds:

```bash
python -m pip install -e ".[build]"
python scripts/dev/build_package.py --clean
```

`scripts/dev/build_package.py` runs `python -m build --no-isolation` only when the optional build frontend is installed, then checks that local `dist/` contains a wheel and an sdist. It does not publish anything.

For local install-matrix release audits:

```bash
python scripts/dev/install_matrix_audit.py
```

The install matrix checks no-install wrapper usage, `python -m paper_scaffold`, editable install, console-script creation, self-test after editable install, and optional wheel/sdist installs when local `dist/` artifacts exist. By default it uses `--no-deps --no-build-isolation` for install checks so it does not need package-index access. Use `--allow-deps` only when you intentionally want dependency resolution.

Do not publish to PyPI from this repository unless the release process explicitly changes.

## Module Fallback

If the console script is not on `PATH`, use:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

This works after an editable install because Python can import the installed package even when the environment's script directory is not on `PATH`.

## Windows CMD

```cmd
python -m pip install -e .
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

If the script directory is on `PATH`:

```cmd
paper-scaffold --help
paper-scaffold self-test
```

## PowerShell

```powershell
python -m pip install -e .
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

Preferred test command on Windows:

```powershell
python scripts/dev/run_tests.py
```

Use the Python executable for the environment you want to test.

## Git Bash

```bash
python -m pip install -e .
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

If `paper-scaffold` is not found after install, add the environment scripts folder:

```bash
export PATH="/path/to/env/Scripts:$PATH"
paper-scaffold --help
```

Or call the executable directly:

```bash
<env-root>/Scripts/paper-scaffold.exe --help
```

The older Git Bash pytest workaround still works in Git Bash, but `scripts/dev/run_tests.py` is preferred because it creates a fresh basetemp for each run and works the same way from CMD and PowerShell.

## First Commands

```bash
python -m paper_scaffold self-test
paper-scaffold quickstart
paper-scaffold demo --output scratch/demo_manuscript --overwrite
```
