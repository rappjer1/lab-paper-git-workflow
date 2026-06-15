# v1.0 Final Checklist

Complete this checklist before tagging v1.0.0.

## Release-Candidate Audit

- [ ] Working tree is clean.
- [ ] `python scripts/dev/release_candidate_audit.py --output scratch/release-candidate` passes.
- [ ] Release-candidate audit report has no required failures.
- [ ] Optional skips are understood and accepted.
- [ ] Clean clone dogfood was not skipped.
- [ ] Clean install audit was run from a clean branch.

## Local Validation

- [ ] `python scripts/dev/check_text_blobs.py`
- [ ] `python scripts/dev/check_contracts.py`
- [ ] `python scripts/dev/check_docs_examples.py`
- [ ] `python scripts/dev/check_docs_links.py`
- [ ] `python scripts/dev/check_example_integrity.py`
- [ ] `python scripts/dev/check_public_safety.py`
- [ ] `python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output`
- [ ] `python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`
- [ ] `python scripts/dev/run_tests.py`
- [ ] `python scripts/dev/install_matrix_audit.py`
- [ ] `python scripts/dev/build_package.py`

## Documentation

- [ ] README first-run path reviewed.
- [ ] QUICKSTART reviewed.
- [ ] CLI reference matches implementation.
- [ ] Schema reference matches implementation.
- [ ] Error-code docs match implementation.
- [ ] `docs/v1_0_readiness.md` reviewed.
- [ ] `docs/release_process.md` reviewed.
- [ ] `V1_0_RELEASE_NOTES_DRAFT.md` reviewed and updated for final release.

## Public Safety

- [ ] Public safety audit passes.
- [ ] No machine-specific paths are present in user-facing docs.
- [ ] No credentials, raw data, generated output trees, or nonpublic research content are present.
- [ ] Historical reports are intentionally retained and listed in `docs/release_reports.md`.

## CI And Tagging

- [ ] GitHub Actions are green on supported operating systems and Python versions.
- [ ] Version is bumped to `1.0.0`.
- [ ] Changelog includes v1.0.0.
- [ ] Release notes are final.
- [ ] Tag commands have been reviewed before execution.
- [ ] No PyPI publishing is performed unless a separate release decision authorizes it.

## v1.0.0 Tag Commands

```bash
git checkout main
git pull --ff-only
git tag -a v1.0.0 -m "Paper Scaffold v1.0.0"
git push origin main
git push origin v1.0.0
```
