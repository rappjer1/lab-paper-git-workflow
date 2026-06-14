# v0.9.7 Docs Freeze Report

Branch: `v0.9.7-docs-freeze-public-walkthroughs`

Version: `0.9.7`

## Purpose

v0.9.7 is a narrow docs-freeze and public walkthrough release. It makes the project easier to evaluate from a clean checkout before the v1.0 stabilization window.

## Files Changed

Primary docs:

- `README.md`
- `QUICKSTART.md`
- `docs/start_here.md`
- `docs/common_paths.md`
- `docs/one_page_reference.md`
- `docs/glossary.md`
- `docs/walkthroughs/README.md`
- `docs/walkthroughs/five_minute_demo.md`
- `docs/walkthroughs/python_outputs_to_manuscript.md`
- `docs/walkthroughs/existing_latex_cleanup.md`
- `docs/walkthroughs/pre_submission_package.md`
- `docs/walkthroughs/reviewer_response_round.md`

Updated reference docs:

- `docs/cli_reference.md`
- `docs/compatibility.md`
- `docs/contract.md`
- `docs/getting_started.md`
- `docs/install.md`
- `docs/release_process.md`
- `docs/schema_reference.md`
- `docs/troubleshooting.md`
- `docs/v1_0_readiness.md`
- `docs/which_workflow.md`

Release/version files:

- `pyproject.toml`
- `src/paper_scaffold/__init__.py`
- `src/paper_scaffold/schema_reference.py`
- `CHANGELOG.md`
- `ROADMAP.md`

Tooling and tests:

- `.github/workflows/tests.yml`
- `scripts/dev/check_docs_examples.py`
- `scripts/dev/check_docs_links.py`
- `tests/test_v09_release_candidate.py`
- `tests/test_v097_docs_freeze.py`

Reports:

- `V0_9_7_DOCS_FREEZE_AUDIT.md`
- `V0_9_7_DOCS_FREEZE_REPORT.md`

## Docs Added

- Start page
- Common paths guide
- One-page command reference
- Glossary
- Walkthrough index
- Five-minute demo walkthrough
- Python output handoff walkthrough
- Existing LaTeX cleanup walkthrough
- Pre-submission package walkthrough
- Reviewer response round walkthrough

## Scripts Added

- `scripts/dev/check_docs_links.py`

## Tests Added

- New v0.9.7 docs freeze tests covering:
  - required public docs
  - local Markdown link checker
  - docs/examples checker
  - README entry-point links
  - QUICKSTART workflow commands
  - CLI reference coverage for all parser commands
  - contract/text guards
  - `run_tests.py --help`

## CI Update

GitHub Actions now runs:

```bash
python scripts/dev/check_docs_links.py
```

## Validation Results

Passed:

```bash
<python> scripts/dev/check_text_blobs.py
<python> scripts/dev/check_contracts.py
<python> scripts/dev/check_docs_examples.py
<python> scripts/dev/check_docs_links.py
<python> scripts/dev/check_example_integrity.py
<python> scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output
<python> scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
<python> scripts/dev/run_tests.py
```

Additional checks:

```bash
<python> scripts/paper-scaffold.py --help
<python> scripts/paper-scaffold.py --version
```

Observed results:

- Docs/examples check passed.
- Docs link check passed.
- Example integrity checked 75 files with 0 problems.
- Dogfood summary: 9 passed, 0 failed.
- Self-test summary: 10 passed, 0 failed.
- Full tests: 139 passed.
- Version output: `paper-scaffold 0.9.7`.

Optional package build:

```bash
<python> -m build
```

Result: skipped/unavailable in this environment with `No module named build`. Install the `build` extra before running this optional check.

## Public-Language Result

The public scan found no personal names, workstation names, local machine paths, or project-specific research terms. Remaining hits are generic privacy/security docs and the existing contract-preserved launch-summary command reference.

Details: `V0_9_7_DOCS_FREEZE_AUDIT.md`.

## Known Limitations

- v0.9.7 does not add new product workflows.
- The optional package build requires the `build` extra.
- The legacy launch-summary command name remains because command names are under contract freeze review.
- Paper Scaffold still does not create remote repositories, upload to Overleaf, compile LaTeX, or publish to PyPI.

## Readiness

v0.9.7 is ready for commit and review as a docs-freeze/public-walkthrough release.

## Exact Git Commands

```bash
git status --short --branch
git add .github/workflows/tests.yml CHANGELOG.md QUICKSTART.md README.md ROADMAP.md pyproject.toml
git add docs scripts/dev/check_docs_examples.py scripts/dev/check_docs_links.py
git add src/paper_scaffold/__init__.py src/paper_scaffold/schema_reference.py
git add tests/test_v09_release_candidate.py tests/test_v097_docs_freeze.py
git add V0_9_7_DOCS_FREEZE_AUDIT.md V0_9_7_DOCS_FREEZE_REPORT.md
git commit -m "Prepare v0.9.7 docs freeze"
git push -u origin v0.9.7-docs-freeze-public-walkthroughs
git checkout main
git pull --ff-only origin main
git merge --ff-only v0.9.7-docs-freeze-public-walkthroughs
git tag -a v0.9.7 -m "Paper Scaffold v0.9.7"
git push origin main
git push origin v0.9.7
```
