# v0.9.8 Public Trust Audit

Branch: `v0.9.8-public-trust-release-audit`

Purpose: evaluate whether a public user can clone, inspect, run, and trust Paper Scaffold without being misled by claims or exposed to private paths, data, credentials, project-specific research material, invalid examples, or tracked generated outputs.

## Scope

Audited:

- README, QUICKSTART, public docs, and walkthroughs
- examples and templates
- contracts and package metadata
- GitHub metadata under `.github/`
- top-level historical reports and public release checklist
- security, contribution, citation, license, and conduct files

Not changed:

- command contract
- schema contract
- diagnostic contract
- normal CLI behavior
- publishing or repository visibility

## Audit Categories

The audit covered:

- privacy and local path leakage;
- secret-like values and credential wording;
- project-specific research leakage;
- misleading automation claims;
- public repository hygiene, including badges, stale versions, historical reports, scratch outputs, oversized tracked files, and invalid example artifacts.

The exact sensitive search strings are not repeated in this report so the report does not reintroduce them into the public repository.

## Findings Fixed

- Added `scripts/dev/check_public_safety.py`, a dependency-free public-repo safety checker.
- Added `contracts/public_safety_allowlist.yaml` for intentionally retained generic safety wording.
- Generalized concrete local interpreter paths in historical release reports.
- Rewrote the historical public-readiness audit so it describes categories instead of preserving local paths or project-specific search terms.
- Rewrote `PUBLIC_RELEASE_CHECKLIST.md` as an actionable v1.0 public release checklist.
- Hardened `SECURITY.md` with public issue guidance, synthetic example notes, heuristic-check limitations, and no-network core-check language.
- Added `docs/privacy_and_data_safety.md`.
- Added `docs/github_repo_settings.md`.
- Added `docs/release_reports.md`.
- Added CI coverage for the public-safety audit.

## Findings Intentionally Retained

- Generic privacy/security words remain in security docs, troubleshooting docs, diagnostics, the public release checklist, and the public-safety allowlist.
- The legacy launch-summary command name remains in CLI and contract references because command names are under contract freeze review.
- Historical release reports are retained, but paths and sensitive search strings were generalized where low-risk.
- Real public repository URLs, badges, and citation metadata are retained.

## Follow-Up Items

- Before v1.0, decide whether the legacy launch-summary command should remain under its current exact name or enter a deprecation path after the contract freeze.
- Review GitHub repository settings manually using `docs/github_repo_settings.md`.
- Run a clean clone audit from a committed branch or tag during v0.9.9.
- Draft v1.0 release notes after the release-candidate dry run.

## Public Safety Check Result

`scripts/dev/check_public_safety.py` scans public-facing files, examples, templates, contracts, GitHub metadata, package metadata, and historical reports.

Current result:

- blocked high-risk findings: 0
- generated scratch outputs tracked: 0
- oversized tracked files: 0
- invalid example artifacts: 0

Allowed findings are generic privacy/security terms documented in `contracts/public_safety_allowlist.yaml`.

## Conclusion

v0.9.8 improves public trust and release hygiene without adding major product workflows. The repository is safer to inspect publicly, and the new checker gives maintainers a repeatable guard before v0.9.9 and v1.0.
