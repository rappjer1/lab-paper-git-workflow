# v0.9.5 Public Polish Audit

## Scope

This audit checked the public-facing documentation and examples that prepare Paper Scaffold for the v1.0 stabilization path.

## Terms Checked

The release audit searched public docs, examples, scripts, tests, and reports for private or project-specific language, including local paths, person names, nonpublic project labels, domain-specific research terms, internal-team wording, chat/tool tokens, and secret-like terms.

Security and privacy words may still appear where they are the subject of user-facing checks, troubleshooting guidance, or this audit report.

## Issues Found

- Several example `.pdf` files were plain-text placeholders despite having a PDF extension.
- Several example `.png` files were plain-text placeholders despite having a PNG extension.
- Public docs did not yet describe how example artifact integrity is checked.

## Fixes

- Added `scripts/dev/generate_example_artifacts.py` to generate deterministic tiny synthetic example PDFs and PNGs.
- Added `scripts/dev/check_example_integrity.py` to verify example/template file signatures, text encoding, size limits, and local-path leakage.
- Added `docs/example_integrity.md` and linked it from public docs and release docs.
- Added CI coverage for example integrity.
- Added `scripts/dev/clean_clone_dogfood_audit.py` for clean-clone dogfood validation of the current release candidate.

## Result

The v0.9.5 public examples are synthetic, small, and mechanically checkable. No private manuscript content, unpublished research content, credentials, or machine-specific paths were added.
