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
python -m pytest tests
```

For local package builds:

```bash
python -m pip install -e ".[build]"
python -m build
```

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

Temporary pytest folders on Windows:

```powershell
New-Item -ItemType Directory -Force -Path scratch/tmp,scratch/pytest-tmp | Out-Null
$env:TMP = (Resolve-Path scratch/tmp).Path
$env:TEMP = (Resolve-Path scratch/tmp).Path
python -m pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider
```

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

## First Commands

```bash
python -m paper_scaffold self-test
paper-scaffold quickstart
paper-scaffold demo --output scratch/demo_manuscript --overwrite
```
