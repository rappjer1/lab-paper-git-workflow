# v0.8 Release Report

Branch: `v0.8-manuscript-ci-and-submission-packaging`

Version: `0.8.0`

## Files Changed

Modified:

- `CHANGELOG.md`
- `QUICKSTART.md`
- `README.md`
- `ROADMAP.md`
- `docs/error_codes.md`
- `docs/provenance_ledger.md`
- `docs/troubleshooting.md`
- `docs/use_cases/README.md`
- `docs/use_cases/pre-submission-flight-check.md`
- `docs/use_cases/reviewer-response-binder.md`
- `pyproject.toml`
- `src/paper_scaffold/__init__.py`
- `src/paper_scaffold/cli.py`
- `src/paper_scaffold/messages.py`
- `src/paper_scaffold/recipes.py`

Added:

- `docs/artifact_locks.md`
- `docs/manuscript_ci.md`
- `docs/reviewer_response_binder.md`
- `docs/submission_packaging.md`
- `examples/manuscript_ci/README.md`
- `examples/manuscript_ci/workflow_summary.txt`
- `examples/reviewer_response_round/README.md`
- `examples/reviewer_response_round/response_round_template.md`
- `examples/submission_packaging/README.md`
- `examples/submission_packaging/expected_structure.txt`
- `src/paper_scaffold/workflows.py`
- `tests/test_v08_workflows.py`
- `V0_8_RELEASE_REPORT.md`

## Commands Added

- `paper-scaffold add-manuscript-ci --manuscript-repo <path>`
- `paper-scaffold package-submission --manuscript-repo <path> --output <submission_dir>`
- `paper-scaffold compare-lock --manuscript-repo <path> --lock metadata/artifact_lock.json`
- `paper-scaffold reviewer-binder --manuscript-repo <path> --round <id> --output <folder>`

## Docs Added

- `docs/manuscript_ci.md`
- `docs/submission_packaging.md`
- `docs/reviewer_response_binder.md`
- `docs/artifact_locks.md`

## Diagnostics Added

Errors:

- `E030`: manuscript CI workflow could not be written.
- `E031`: submission package output exists.
- `E032`: artifact lock missing.
- `E033`: locked artifact missing.
- `E034`: manuscript repository missing.
- `E035`: reviewer binder output exists.

Warnings:

- `W040`: artifact hash changed since lock.
- `W041`: new artifact not present in lock.
- `W042`: untracked artifact excluded from package.
- `W043`: unreferenced artifact excluded from package.
- `W044`: manuscript CI is advisory.
- `W045`: reviewer binder needs manual review.

Info:

- `I040`: manuscript CI workflow written.
- `I041`: submission package written.
- `I042`: artifact lock comparison passed.
- `I043`: reviewer binder written.
- `I044`: artifact lock comparison report written.

## Validation And Test Results

Requested validation commands passed on Windows with the project Python interpreter.

- `scripts/dev/check_text_blobs.py`: passed; tracked text blobs use LF line endings.
- `scripts/paper-scaffold.py --help`: passed and lists the four new commands.
- `demo --output scratch/demo_manuscript --overwrite`: passed; demo validation summary was 0 errors and 0 warnings.
- `freeze-artifacts`: passed and wrote `scratch/demo_manuscript/metadata/artifact_lock.json`.
- `compare-lock`: passed; 3 locked artifacts, 3 unchanged, 0 changed, 0 missing, 0 new; wrote Markdown and JSON reports.
- `add-manuscript-ci`: passed and wrote `.github/workflows/manuscript-checks.yml` in the demo manuscript.
- `package-submission`: passed and wrote `scratch/submission_package`.
- `reviewer-binder`: passed and wrote `scratch/reviewer_response_round_1`.
- `release-check`: passed; summary was 0 errors, 0 warnings, 2 info.
- `pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider`: passed, 68 tests.

Additional checks:

- `ruff check .`: passed.
- Focused v0.8 test module: 11 passed.

The final validation run used elevated repo filesystem access because sandboxed PowerShell could not create or clean repo-local pytest scratch directories on this Windows checkout.

## Known Limitations

- Generated manuscript CI is advisory and does not compile LaTeX.
- Submission packaging uses source-file and TeX-reference heuristics; journal-specific requirements still need manual review.
- Artifact locks compare manuscript artifact hashes only; they do not verify raw-data reproducibility or scientific correctness.
- Reviewer binders create checklist/evidence structure but do not write journal response letters or handle confidential review text.
- The text-blob guard checks tracked Git blobs. Run it again after staging if you want the index to include newly added files in the same guard.

## Readiness

v0.8 is ready for commit and review on the current branch. Do not publish, merge, or tag until the branch is reviewed.

## Exact Git Commands

```bash
git status --short
git add CHANGELOG.md QUICKSTART.md README.md ROADMAP.md docs/error_codes.md docs/provenance_ledger.md docs/troubleshooting.md docs/use_cases/README.md docs/use_cases/pre-submission-flight-check.md docs/use_cases/reviewer-response-binder.md docs/artifact_locks.md docs/manuscript_ci.md docs/reviewer_response_binder.md docs/submission_packaging.md examples/manuscript_ci examples/reviewer_response_round examples/submission_packaging pyproject.toml src/paper_scaffold/__init__.py src/paper_scaffold/cli.py src/paper_scaffold/messages.py src/paper_scaffold/recipes.py src/paper_scaffold/workflows.py tests/test_v08_workflows.py V0_8_RELEASE_REPORT.md
python scripts/dev/check_text_blobs.py
git commit -m "Add manuscript CI and submission packaging workflows"
git push -u origin v0.8-manuscript-ci-and-submission-packaging
git checkout main
git pull --ff-only
git merge --no-ff v0.8-manuscript-ci-and-submission-packaging
git tag -a v0.8.0 -m "Paper Scaffold v0.8.0"
git push origin main
git push origin v0.8.0
```
