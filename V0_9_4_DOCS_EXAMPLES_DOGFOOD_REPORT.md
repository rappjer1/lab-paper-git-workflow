# v0.9.4 Docs, Examples, And Dogfood Report

Branch: `v0.9.4-docs-examples-dogfood`

Version: `0.9.4`

## Purpose

v0.9.4 makes Paper Scaffold easier for a public user to understand, try, and validate before v1.0. It sharpens the README first-run path, adds a workflow decision guide, expands synthetic examples, and adds maintainable dogfood checks.

This release does not add major product workflows.

## README And Quick Start Changes

- Added a top-level README `Start Here` section.
- Clarified checkout, installed console-script, and module-fallback invocation modes.
- Added three minimal README paths:
  - try the tool;
  - inspect Python figures/tables;
  - validate an existing manuscript repo.
- Rewrote `QUICKSTART.md` around starting-point choices.
- Rewrote `docs/getting_started.md` with a five-minute demo and fifteen-minute dry run.
- Added explicit language that Paper Scaffold does not write papers, create GitHub repos, upload to Overleaf, or replace manual review.

## Docs Added

- `docs/which_workflow.md`
- `examples/README.md`
- `V1_0_PREP_NOTES.md`
- `V0_9_4_PUBLIC_USABILITY_AUDIT.md`

## Examples Added

- `examples/dogfood/python_outputs_to_manuscript/`
- `examples/dogfood/existing_latex_cleanup/`
- `examples/dogfood/reviewer_response_round/`
- `examples/dogfood/submission_package/`
- `examples/dogfood/messy_project_audit/`

Each dogfood scenario includes:

- `README.md`
- `expected_commands.md`
- `expected_outputs.md`
- tiny synthetic `input/` or `project/` files

## Scripts Added

- `scripts/dev/run_dogfood.py`
- `scripts/dev/check_docs_examples.py`

`run_dogfood.py` runs self-test, demo, release-check, provenance-report, freeze-artifacts, compare-lock, package-submission, reviewer-binder, and a messy-project audit against synthetic examples.

`check_docs_examples.py` checks required docs, README links, dogfood folder shape, dogfood command snippets, and CLI reference command headings.

## CI Update

GitHub Actions now runs:

- `scripts/dev/check_text_blobs.py`
- `scripts/dev/check_contracts.py`
- `scripts/dev/check_docs_examples.py`
- `scripts/dev/run_dogfood.py --output scratch/dogfood`
- `scripts/dev/run_tests.py`

## Tests Added

- `tests/test_v094_docs_examples_dogfood.py`

Coverage includes:

- dogfood runner success in a temp output;
- docs/examples checker pass;
- workflow guide presence and core workflow coverage;
- examples index and dogfood scenario folders;
- README workflow-guide link;
- Quick Start command coverage;
- v1.0 prep notes;
- contract audit still passing;
- text blob guard still passing;
- test runner help still passing.

## Validation Results

Passed:

- `<python> scripts/dev/check_text_blobs.py`
- `<python> scripts/dev/check_contracts.py`
- `<python> scripts/dev/check_docs_examples.py`
- `<python> scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output`
- `<python> scripts/paper-scaffold.py --version`
- `<python> scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`
- `<python> scripts/dev/run_tests.py`
- `<python> -m ruff check .`

Observed results:

- Version output: `paper-scaffold 0.9.4`
- Contract audit: passed
- Docs/examples check: passed
- Dogfood runner: 9 passed, 0 failed
- Self-test: 10 passed, 0 failed
- Full test suite: `113 passed in 36.76s`
- Text blob guard: all tracked text blobs passed
- Public-facing docs/examples search: no local/private/project-specific terms found
- Ruff: passed

Optional package build:

- `<python> -m build` was attempted.
- Result: unavailable in the local environment, `No module named build`.

## Known Limitations

- The docs/examples checker is intentionally lightweight and is not a full Markdown link checker.
- Dogfood scenarios validate workflow shape but do not compile LaTeX or test real GitHub/Overleaf integration.
- Clean-install audit should still be run from a committed or pushed branch before v1.0.
- Existing examples remain synthetic and do not represent journal-specific submission requirements.

## Remaining v1.0 Tasks

- Run clean-install audit from committed source.
- Confirm GitHub Actions are green.
- Review exit-code behavior for any legacy edge cases.
- Confirm contract metadata, CLI reference, schema reference, and diagnostic docs are acceptable as v1.0 freeze candidates.
- Do a final public-facing docs scan for local paths and private content.

## Ready Status

v0.9.4 is ready for review.

## Exact Git Commands

```bash
git status --short
git add .github/workflows/tests.yml CHANGELOG.md QUICKSTART.md README.md ROADMAP.md V0_9_4_DOCS_EXAMPLES_DOGFOOD_REPORT.md V0_9_4_PUBLIC_USABILITY_AUDIT.md V1_0_PREP_NOTES.md docs/clean_install_audit.md docs/compatibility.md docs/contract.md docs/getting_started.md docs/install.md docs/schema_reference.md docs/troubleshooting.md docs/v1_0_readiness.md docs/which_workflow.md examples/README.md examples/dogfood scripts/dev/check_docs_examples.py scripts/dev/run_dogfood.py pyproject.toml src/paper_scaffold/__init__.py src/paper_scaffold/schema_reference.py tests/test_v09_release_candidate.py tests/test_v091_test_runner.py tests/test_v094_docs_examples_dogfood.py
git commit -m "Polish docs examples and dogfood checks"
git push -u origin v0.9.4-docs-examples-dogfood
git checkout main
git pull --ff-only
git merge --no-ff v0.9.4-docs-examples-dogfood
git tag -a v0.9.4 -m "Paper Scaffold v0.9.4"
git push origin main
git push origin v0.9.4
```
