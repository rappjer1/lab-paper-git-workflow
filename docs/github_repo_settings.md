# GitHub Repository Settings

These are recommended maintainer settings for the public Paper Scaffold repository. They are guidance only; Paper Scaffold does not change GitHub settings automatically.

## Description

Use a concise description:

```text
Lightweight CLI and docs for clean manuscript Git/Overleaf workflows.
```

## Topics

Recommended topics:

- `manuscript`
- `latex`
- `overleaf`
- `research-software`
- `reproducibility`
- `python`
- `workflow`

## Visibility

Public visibility is appropriate only after the public release checklist passes. Do not store secrets, private documents, unpublished data, raw data, or sensitive research material in the repository.

## Branch Protection

Recommended for `main`:

- require pull request review before merge;
- require status checks to pass;
- require branches to be up to date before merge if practical;
- prevent force pushes;
- restrict deletion of the protected branch.

## Actions

GitHub Actions should be enabled. CI should not require secrets, Overleaf, GitHub CLI, Pandoc, LaTeX, or network services beyond normal package installation.

## Issues And Discussions

- Issues: enabled for bug reports and documentation feedback.
- Discussions: optional.
- Issue templates should remind users not to post private documents, credentials, raw data, or confidential manuscript text.

## Dependabot

Dependabot is optional. Core runtime has no third-party dependencies, but development and packaging extras may still benefit from dependency alerts.

## Security Policy

Security policy location:

```text
SECURITY.md
```

## Releases And Tags

Use annotated tags:

```bash
git tag -a v<version> -m "Paper Scaffold v<version>"
git push origin v<version>
```

Do not publish to PyPI unless the release process explicitly changes.

## Secrets

Do not store secrets in the repository. Do not add repository secrets unless a future workflow explicitly needs them and has maintainer approval.
