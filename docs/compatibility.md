# Compatibility

## Python

Paper Scaffold supports Python 3.10 and 3.11 in v0.9. The package uses only the Python standard library for core workflows.

Optional extras:

- `dev`: pytest, Ruff, pre-commit.
- `test`: pytest.
- `build`: Python build frontend.
- `docs`: currently empty placeholder for future documentation tooling.

## Operating Systems

CI covers:

- Linux
- Windows
- macOS

Windows is a first-class target because manuscript workflows often run from PowerShell, CMD, or Git Bash.

## Optional Tools

These are optional and not required for normal validation, self-test, packaging, or provenance workflows:

- Pandoc
- LaTeX
- GitHub CLI
- Overleaf

Word conversion needs Pandoc. Local PDF compilation needs LaTeX. GitHub/Overleaf sync still happens outside Paper Scaffold.

## Known Windows Issues

Editable install can succeed even when `paper-scaffold.exe` is not on Git Bash `PATH`. Use:

```bash
python -m paper_scaffold --help
```

or add the scripts directory:

```bash
export PATH="/path/to/env/Scripts:$PATH"
```

Pytest can fail if Windows blocks the default user temp directory. Use repo-local temp folders:

```bash
mkdir -p scratch/tmp scratch/pytest-tmp
TMP="$PWD/scratch/tmp" TEMP="$PWD/scratch/tmp" python -m pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider
```

## GitHub And Overleaf Limits

Paper Scaffold does not create GitHub repositories, upload to Overleaf, or push tags. It prepares clean manuscript repos and reports so humans can make those publishing decisions.
