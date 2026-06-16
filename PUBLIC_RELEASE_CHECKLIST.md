# Public Release Checklist

Use this before tagging v1.0 or announcing a public release. It is a maintainer checklist, not an automated publishing workflow.

## Required Local Checks

- [ ] Clean clone audit passes with `python scripts/dev/clean_install_audit.py`.
- [ ] Install matrix passes with `python scripts/dev/install_matrix_audit.py`.
- [ ] Dogfood scenarios pass with `python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output`.
- [ ] Public safety audit passes with `python scripts/dev/check_public_safety.py`.
- [ ] Contract audit passes with `python scripts/dev/check_contracts.py`.
- [ ] Text blob guard passes with `python scripts/dev/check_text_blobs.py`.
- [ ] Root layout check passes with `python scripts/dev/check_root_layout.py`.
- [ ] Docs/examples check passes with `python scripts/dev/check_docs_examples.py`.
- [ ] Docs link check passes with `python scripts/dev/check_docs_links.py`.
- [ ] Example integrity check passes with `python scripts/dev/check_example_integrity.py`.
- [ ] Test runner passes with `python scripts/dev/run_tests.py`.

## Required Manual Review

- [ ] GitHub Actions is green on supported operating systems and Python versions.
- [ ] README first-run path is clear.
- [ ] `docs/start_here.md`, `docs/common_paths.md`, and walkthroughs are current.
- [ ] No private paths are present.
- [ ] No secrets or credential values are present.
- [ ] No invalid fake PDFs, PNGs, or other mislabeled artifact files are present.
- [ ] No generated `scratch/` outputs are tracked.
- [ ] No raw data, model checkpoints, prediction caches, or broad output folders are tracked.
- [ ] No unpublished manuscript text or sensitive research material is present.
- [ ] No claims imply that Paper Scaffold writes the science, guarantees compilation, creates remote repositories, uploads to Overleaf, or publishes packages.
- [ ] Historical release reports are listed in `docs/release_reports.md`.
- [ ] Historical release reports live under `docs/release_reports/`, not the repository root.
- [ ] Security policy, code of conduct, citation file, license, and contributing docs are present.
- [ ] Release notes are drafted.

## Tag Instructions

After review, merge to `main`, confirm CI passes, and tag intentionally:

```bash
git checkout main
git pull --ff-only origin main
git tag -a v<version> -m "Paper Scaffold v<version>"
git push origin main
git push origin v<version>
```

## Public Visibility Reminder

Do not change repository visibility, create remote repositories, upload to Overleaf, publish to PyPI, or push tags as part of a local audit. Those actions require explicit maintainer approval.
