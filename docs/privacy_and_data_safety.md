# Privacy And Data Safety

Paper Scaffold helps structure, validate, and package manuscript repositories. It does not write the science, guarantee LaTeX compilation, upload to Overleaf, create GitHub repositories, manage raw data, or replace manual review.

## What Not To Commit

Do not commit:

- private documents or confidential manuscript text;
- raw data, sensitive data, or broad external data exports;
- model checkpoints, prediction caches, or generated run folders;
- access credentials, secret values, environment files, or cloud keys;
- machine-local absolute paths;
- full output folders when only selected figures or tables are needed;
- LaTeX build files such as `.aux`, `.log`, `.out`, and `.synctex.gz`.

Keep those files in the research repository, a controlled archive, or another appropriate storage location. The manuscript repository should contain source text, selected publication artifacts, bibliography files, metadata, and small reports.

## User Privacy Check

Run this on a manuscript repository before sharing or syncing:

```bash
python scripts/paper-scaffold.py privacy-check --path ./paper
```

The check looks for common local paths, email addresses, credential-like assignments, and private markers in text files. It redacts likely sensitive values in output.

## Maintainer Public-Safety Audit

Run this before public releases:

```bash
python scripts/dev/check_public_safety.py
```

The audit scans public repository docs, examples, templates, contracts, GitHub metadata, package metadata, and historical release reports. It checks for local paths, secret-like strings, project-specific leakage terms, misleading automation claims, generated scratch outputs, oversized tracked files, and invalid example artifacts.

Allowed generic privacy/security wording is documented in `contracts/public_safety_allowlist.yaml`.

## Risky Examples To Look For

Before making a manuscript repository public, search for:

- absolute paths into user home folders or mounted drives;
- key names such as `password`, `secret`, `token`, and `api_key`;
- environment files and copied configuration files;
- private notes, review correspondence, or unpublished manuscript text;
- raw data folders, model output folders, and cache folders;
- claims that imply the tool performs scientific review or external publishing actions.

Use generic placeholders in public docs, such as `<python>`, `<repo>`, `<output-folder>`, and `<env-root>`.

## Manual Review Checklist

- Run `privacy-check` on the manuscript repo.
- Run `release-check` on the manuscript repo.
- Inspect `git status --short`.
- Inspect every staged file before commit.
- Confirm figures and tables are selected publication artifacts.
- Confirm metadata contains useful provenance without private paths.
- Confirm no generated scratch or build output is tracked.
- Confirm public claims are accurate and conservative.

## Limitations

Privacy and public-safety checks are heuristic. They can catch common mistakes, but they cannot prove a repository is safe to publish. Manual review remains required.
