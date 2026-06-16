# v1.0.1 Patch Report

Branch: `v1.0.1-post-release-version-fix`

Version: `1.0.1`

## Purpose

v1.0.1 is a narrow post-release patch. v1.0.0 was tagged from release-candidate metadata, so this patch fixes package version metadata, restores the Ruff Python target metadata, and cleans the public repository root by moving historical release and audit reports into `docs/release_reports/`.

## Root Cleanup

Historical report, audit, preparation, and implementation files matching `V0_*.md`, `V1_0_*.md`, `IMPLEMENTATION_REPORT.md`, and `PUBLIC_READINESS_AUDIT.md` were moved from the repository root into `docs/release_reports/`.

`PUBLIC_RELEASE_CHECKLIST.md` remains in the root because it is a live checklist.

## Reports Moved

- `IMPLEMENTATION_REPORT.md`
- `PUBLIC_READINESS_AUDIT.md`
- `V0_4_RELEASE_REPORT.md`
- `V0_5_RELEASE_REPORT.md`
- `V0_5_1_CLEAN_CLONE_REPORT.md`
- `V0_6_RELEASE_REPORT.md`
- `V0_7_RELEASE_REPORT.md`
- `V0_7_3_TEXT_BLOB_FIX_REPORT.md`
- `V0_8_RELEASE_REPORT.md`
- `V0_9_RELEASE_REPORT.md`
- `V0_9_CLEAN_INSTALL_NOTES.md`
- `V0_9_STABILITY_AUDIT.md`
- `V0_9_1_TEST_RUNNER_REPORT.md`
- `V0_9_2_CLEAN_INSTALL_AUDIT_REPORT.md`
- `V0_9_3_CONTRACT_FREEZE_REPORT.md`
- `V0_9_4_PUBLIC_USABILITY_AUDIT.md`
- `V0_9_4_DOCS_EXAMPLES_DOGFOOD_REPORT.md`
- `V0_9_5_PUBLIC_POLISH_AUDIT.md`
- `V0_9_5_EXAMPLE_INTEGRITY_AND_DOGFOOD_REPORT.md`
- `V0_9_6_PACKAGING_INSTALL_REPORT.md`
- `V0_9_7_DOCS_FREEZE_AUDIT.md`
- `V0_9_7_DOCS_FREEZE_REPORT.md`
- `V0_9_8_PUBLIC_TRUST_AUDIT.md`
- `V0_9_8_PUBLIC_TRUST_AUDIT_REPORT.md`
- `V0_9_9_RELEASE_CANDIDATE_REPORT.md`
- `V1_0_PREP_NOTES.md`
- `V1_0_RELEASE_NOTES_DRAFT.md`
- `V1_0_FINAL_CHECKLIST.md`

## Validation Commands

Run for v1.0.1:

```bash
python scripts/paper-scaffold.py --version
python -m ruff check .
python scripts/dev/check_root_layout.py
python scripts/dev/check_text_blobs.py
python scripts/dev/check_contracts.py
python scripts/dev/check_docs_examples.py
python scripts/dev/check_docs_links.py
python scripts/dev/check_example_integrity.py
python scripts/dev/check_public_safety.py
python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output
python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
python scripts/dev/run_tests.py
```

Optional if the build frontend is installed:

```bash
python -m build
```

## Known Limitations

- v1.0.1 does not add user-facing workflows.
- v1.0.1 does not rewrite, move, or replace the v1.0.0 tag.
- v1.0.1 does not publish to PyPI or create GitHub releases.
- Historical report contents are retained and may mention old filenames as historical command examples.

## Exact Git Commands

```bash
git status --short
git add .
git commit -m "Fix v1.0.1 version metadata and root reports"
git push -u origin v1.0.1-post-release-version-fix
git checkout main
git pull --ff-only
git merge --ff-only v1.0.1-post-release-version-fix
git tag -a v1.0.1 -m "Paper Scaffold v1.0.1"
git push origin main
git push origin v1.0.1
```
