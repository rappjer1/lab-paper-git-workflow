# v0.9 Clean Install Notes

## Clean Clone

```bash
git clone https://github.com/rappjer1/lab-paper-git-workflow.git paper-scaffold-clean
cd paper-scaffold-clean
```

## No-Install Smoke Test

```bash
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py --version
python scripts/paper-scaffold.py self-test
```

## Editable Install Smoke Test

```bash
python -m pip install -e .
paper-scaffold --help
paper-scaffold --version
paper-scaffold self-test
```

## PATH Workaround

On Windows Git Bash, editable install can succeed while `paper-scaffold` is not found because the environment Scripts directory is not on `PATH`.

Call the executable directly:

```bash
<env-root>/Scripts/paper-scaffold.exe --help
```

or add the Scripts directory:

```bash
export PATH="/path/to/env/Scripts:$PATH"
paper-scaffold --help
```

## Module Fallback

The v0.9 fallback avoids the Scripts `PATH` issue after install:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

## Windows Pytest Temp Workaround

Preferred for v0.9.1 and later:

```bash
python scripts/dev/run_tests.py
```

With an explicit Windows environment interpreter:

```powershell
<python> scripts\dev\run_tests.py
```

This runner creates a unique pytest basetemp and `TMP`/`TEMP` directory under `scratch/test-runs/` on every run. Reusing `scratch\pytest-tmp` can fail on Windows if the directory remains locked after a failed or interrupted run.

The older Git Bash style remains valid in Git Bash:

```bash
mkdir -p scratch/tmp scratch/pytest-tmp
TMP="$PWD/scratch/tmp" TEMP="$PWD/scratch/tmp" python -m pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider
```

PowerShell equivalent:

```powershell
New-Item -ItemType Directory -Force -Path scratch/tmp,scratch/pytest-tmp | Out-Null
$env:TMP = (Resolve-Path scratch/tmp).Path
$env:TEMP = (Resolve-Path scratch/tmp).Path
python -m pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider
```

## Recommended Public-User First Commands

```bash
python -m paper_scaffold self-test
paper-scaffold quickstart
paper-scaffold demo --output scratch/demo_manuscript --overwrite
paper-scaffold release-check --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/release_check.md
```
