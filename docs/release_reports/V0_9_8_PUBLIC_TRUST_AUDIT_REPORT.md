# v0.9.8 Public Trust Audit Report

Branch: `v0.9.8-public-trust-release-audit`

Version: `0.9.8`

## Purpose

v0.9.8 is a narrow public trust, privacy, security, and release-hygiene audit release. It does not add major product workflows or change the public command contract.

## Privacy, Security, And Public-Safety Checks Added

- Added `scripts/dev/check_public_safety.py`.
- Added `contracts/public_safety_allowlist.yaml`.
- Added CI coverage for `python scripts/dev/check_public_safety.py`.
- Added tests for the checker, allowlist, docs, checklist, security guidance, and existing drift guards.

The public-safety checker detects:

- private local paths and machine-specific names;
- secret-like assignments and cloud key-like strings;
- project-specific research leakage terms;
- misleading automation claims;
- generated scratch outputs tracked by Git;
- oversized tracked files;
- invalid example artifact files.

Allowed generic safety language is documented in the allowlist.

## Files And Docs Updated

Added:

- `docs/privacy_and_data_safety.md`
- `docs/github_repo_settings.md`
- `docs/release_reports.md`
- `scripts/dev/check_public_safety.py`
- `contracts/public_safety_allowlist.yaml`
- `tests/test_v098_public_trust.py`
- `V0_9_8_PUBLIC_TRUST_AUDIT.md`
- `V0_9_8_PUBLIC_TRUST_AUDIT_REPORT.md`

Updated:

- `.github/workflows/tests.yml`
- `README.md`
- `PUBLIC_RELEASE_CHECKLIST.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/start_here.md`
- `docs/common_paths.md`
- `docs/troubleshooting.md`
- `docs/compatibility.md`
- `docs/release_process.md`
- `docs/v1_0_readiness.md`
- `docs/contract.md`
- `docs/schema_reference.md`
- `scripts/dev/check_docs_examples.py`
- `src/paper_scaffold/__init__.py`
- `src/paper_scaffold/schema_reference.py`
- `tests/test_v09_release_candidate.py`

Historical reports generalized:

- `PUBLIC_READINESS_AUDIT.md`
- `V0_4_RELEASE_REPORT.md`
- `V0_5_1_CLEAN_CLONE_REPORT.md`
- `V0_6_RELEASE_REPORT.md`
- `V0_9_1_TEST_RUNNER_REPORT.md`
- `V0_9_2_CLEAN_INSTALL_AUDIT_REPORT.md`
- `V0_9_5_PUBLIC_POLISH_AUDIT.md`
- `V0_9_CLEAN_INSTALL_NOTES.md`

## Findings Fixed

- Historical reports no longer contain concrete local interpreter paths.
- Historical audit language no longer preserves exact sensitive search strings.
- Public release checklist now includes v1.0 public safety, clean clone, install matrix, dogfood, contract, text-blob, docs-link, example-integrity, and GitHub Actions checks.
- Security policy now explicitly warns users not to post private documents, credentials, sensitive data, raw data, model outputs, or confidential text in public issues or pull requests.
- Public docs now point to privacy/data-safety guidance and GitHub repository setting guidance.

## Findings Intentionally Retained

- Generic privacy/security terminology remains where it is the subject of safety docs and diagnostics.
- The legacy launch-summary command name remains because command names are under contract freeze review.
- Historical release reports remain in the repository and are indexed in `docs/release_reports.md`.
- Public repository URLs and badges remain.

## Validation Results

Passed:

- `<python> scripts/dev/check_text_blobs.py`
- `<python> scripts/dev/check_contracts.py`
- `<python> scripts/dev/check_docs_examples.py`
- `<python> scripts/dev/check_docs_links.py`
- `<python> scripts/dev/check_example_integrity.py`
- `<python> scripts/dev/check_public_safety.py`
- `<python> scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output`
- `<python> scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`
- `<python> scripts/dev/run_tests.py`

Observed results:

- Public safety check: 0 blocked high-risk findings.
- Example integrity: 75 files checked, 0 problems.
- Dogfood: 9 passed, 0 failed.
- Self-test: 10 passed, 0 failed.
- Full test suite: 147 passed.
- Version output: `paper-scaffold 0.9.8`.

Optional package build:

- `<python> -m build` was unavailable in this environment because the build frontend was not installed.

## Known Limitations

- Public safety checks are heuristic and do not replace manual review.
- The checker intentionally allows generic privacy/security wording in documented safety contexts.
- The optional package build requires the build frontend.
- Paper Scaffold still does not create remote repositories, upload to Overleaf, compile LaTeX, publish to PyPI, manage raw data, write the science, or replace manual review.

## Remaining v0.9.9/v1.0 Tasks

- Run v0.9.9 release-candidate dry run from a committed branch.
- Run clean clone and install matrix audits from committed source.
- Confirm GitHub Actions are green after push.
- Review repository settings manually.
- Draft v1.0 release notes.

## Readiness

v0.9.8 is ready for commit and review as a public trust, privacy, security, and release-hygiene audit release.

## Exact Git Commands

```bash
git status --short --branch
git add .
git commit -m "Add v0.9.8 public trust audit"
git push -u origin v0.9.8-public-trust-release-audit
git checkout main
git pull --ff-only origin main
git merge --ff-only v0.9.8-public-trust-release-audit
git tag -a v0.9.8 -m "Paper Scaffold v0.9.8"
git push origin main
git push origin v0.9.8
```
