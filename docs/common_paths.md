# Common Paths

This page maps common manuscript cleanup situations to the shortest Paper Scaffold path. Commands use a source checkout so they work before installation.

## 1. I Want To Try The Tool

Read first: [start_here.md](start_here.md), [walkthroughs/five_minute_demo.md](walkthroughs/five_minute_demo.md)

```bash
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
```

Expected result: a small synthetic manuscript with no validation errors.

## 2. I Need A Clean Manuscript Repo

Read first: [getting_started.md](getting_started.md), [folder_structure.md](folder_structure.md)

```bash
python scripts/paper-scaffold.py init --manuscript-repo ./paper --non-interactive
python scripts/paper-scaffold.py validate --manuscript-repo ./paper
```

Expected result: `main.tex`, `references.bib`, `figures/`, `tables/`, `supplement/`, and `metadata/`.

## 3. I Have Python Outputs

Read first: [walkthroughs/python_outputs_to_manuscript.md](walkthroughs/python_outputs_to_manuscript.md), [python_outputs_to_overleaf.md](python_outputs_to_overleaf.md)

```bash
python scripts/paper-scaffold.py discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml --suggest-only
python scripts/paper-scaffold.py discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper
python scripts/paper-scaffold.py validate --manuscript-repo ./paper
```

Expected result: reviewed artifacts copied into the manuscript repo and recorded in the manifest.

## 4. I Have An Existing LaTeX Project

Read first: [walkthroughs/existing_latex_cleanup.md](walkthroughs/existing_latex_cleanup.md), [existing_latex_project.md](existing_latex_project.md)

```bash
python scripts/paper-scaffold.py doctor --manuscript-repo ./paper
python scripts/paper-scaffold.py validate --manuscript-repo ./paper --write-report ./paper/validation_report.md
python scripts/paper-scaffold.py check-figures --manuscript-repo ./paper
python scripts/paper-scaffold.py check-citations --manuscript-repo ./paper
python scripts/paper-scaffold.py check-labels --manuscript-repo ./paper
```

Expected result: focused diagnostics before the project is pushed or synced.

## 5. I Need A Submission Folder

Read first: [walkthroughs/pre_submission_package.md](walkthroughs/pre_submission_package.md), [submission_packaging.md](submission_packaging.md)

```bash
python scripts/paper-scaffold.py release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
python scripts/paper-scaffold.py freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
python scripts/paper-scaffold.py package-submission --manuscript-repo ./paper --output ./submission_package
```

Expected result: a clean local folder for manual journal upload review.

## 6. I Need A Reviewer Response Binder

Read first: [walkthroughs/reviewer_response_round.md](walkthroughs/reviewer_response_round.md), [reviewer_response_binder.md](reviewer_response_binder.md)

```bash
python scripts/paper-scaffold.py provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md
python scripts/paper-scaffold.py reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1
```

Expected result: a response checklist and evidence folder that can be reviewed before sharing.

## 7. I Need Provenance Or Artifact Drift Checks

Read first: [provenance_ledger.md](provenance_ledger.md), [artifact_locks.md](artifact_locks.md)

```bash
python scripts/paper-scaffold.py provenance-report --manuscript-repo ./paper --write-json ./paper/metadata/provenance_ledger.json
python scripts/paper-scaffold.py artifact-status --manuscript-repo ./paper
python scripts/paper-scaffold.py compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json
```

Expected result: current, stale, missing, changed, and untracked artifact summaries.

## 8. I Need Help With Terms

Read first: [terminology_cleanup.md](terminology_cleanup.md), [glossary.md](glossary.md)

```bash
python scripts/paper-scaffold.py terminology-check --manuscript-repo ./paper
python scripts/paper-scaffold.py explain E006
```

Expected result: publication text can be checked against a small terminology map before sharing.

## 9. I Need To Install Or Audit Installation

Read first: [install.md](install.md), [clean_install_audit.md](clean_install_audit.md), [compatibility.md](compatibility.md)

```bash
python -m pip install -e ".[dev]"
python -m paper_scaffold --help
python scripts/dev/run_tests.py
python scripts/dev/clean_install_audit.py --help
```

Expected result: source, editable, module fallback, and test-runner paths are documented and testable.

## 10. I Am Maintaining A Release

Read first: [release_process.md](release_process.md), [contract.md](contract.md), [v1_0_readiness.md](v1_0_readiness.md), [privacy_and_data_safety.md](privacy_and_data_safety.md)

```bash
python scripts/dev/check_text_blobs.py
python scripts/dev/check_contracts.py
python scripts/dev/check_docs_examples.py
python scripts/dev/check_docs_links.py
python scripts/dev/check_example_integrity.py
python scripts/dev/check_public_safety.py
python scripts/dev/run_tests.py
```

Expected result: docs, examples, contracts, and tests pass before a release tag is proposed.

## 11. I Need To Review Public Repository Settings

Read first: [github_repo_settings.md](github_repo_settings.md), [release_reports.md](release_reports.md)

Expected result: maintainers can review repository description, topics, branch protection, Actions, issue settings, security policy, and release/tagging approach without Paper Scaffold changing remote settings automatically.
