# Contributing

Thanks for helping improve Paper Scaffold.

## Before Larger Changes

Open an issue first for major changes, new commands, or workflow changes. Small documentation fixes can go straight to a pull request.

## Local Checks

```bash
python -m pip install -e ".[dev]"
pytest tests
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py doctor
```

## Contribution Guidelines

- Keep the tool generic for researchers across fields.
- Do not commit private documents, raw data, credentials, model outputs, or large binaries.
- Add tests for CLI behavior changes.
- Update docs when behavior changes.
- Keep dependencies minimal and optional when possible.
- Prefer small, reviewable pull requests.
