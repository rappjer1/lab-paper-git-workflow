# Quick Start

Paper Scaffold helps you create and check a clean manuscript repository from selected research outputs. It does not write the paper, create remote repositories, upload to Overleaf, or decide which artifacts belong in the manuscript.

From a checkout, use:

```bash
python scripts/paper-scaffold.py <command>
```

After install, use either:

```bash
paper-scaffold <command>
python -m paper_scaffold <command>
```

## 1. Smoke Test The Checkout

```bash
python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
```

Expected result: a local smoke-test folder under `scratch/self_test`.

## 2. Create A Demo Manuscript

```bash
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/validation_report.md --write-json scratch/demo_manuscript/validation_report.json
python scripts/paper-scaffold.py overleaf-check --manuscript-repo scratch/demo_manuscript
```

Expected result: a synthetic manuscript repo with zero validation errors.

## 3. Start A Real Manuscript Repo

```bash
python scripts/paper-scaffold.py init --manuscript-repo ./paper --non-interactive
python scripts/paper-scaffold.py validate --manuscript-repo ./paper
```

Expected result: a clean scaffold with `main.tex`, `references.bib`, `figures/`, `tables/`, `supplement/`, and `metadata/`.

## 4. Discover Python Artifacts

```bash
python scripts/paper-scaffold.py discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml --suggest-only
python scripts/paper-scaffold.py discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper
python scripts/paper-scaffold.py provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
```

Expected result: reviewed figures and tables copied into the manuscript repo and recorded in metadata.

## 5. Prepare A Submission Package

```bash
python scripts/paper-scaffold.py release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
python scripts/paper-scaffold.py freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
python scripts/paper-scaffold.py package-submission --manuscript-repo ./paper --output ./submission_package
```

Expected result: a clean local folder for manual journal upload review.

## 6. Create A Reviewer Binder

```bash
python scripts/paper-scaffold.py reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1
python scripts/paper-scaffold.py compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json
```

Expected result: a response-round checklist and evidence folder.

## 7. Run Maintainer Checks

```bash
python scripts/dev/check_text_blobs.py
python scripts/dev/check_contracts.py
python scripts/dev/check_docs_examples.py
python scripts/dev/check_docs_links.py
python scripts/dev/check_example_integrity.py
python scripts/dev/run_tests.py
```

Expected result: docs, examples, contracts, and tests pass in a source checkout.

## Next Reading

- [docs/start_here.md](docs/start_here.md)
- [docs/common_paths.md](docs/common_paths.md)
- [docs/one_page_reference.md](docs/one_page_reference.md)
- [docs/walkthroughs/README.md](docs/walkthroughs/README.md)
- [docs/which_workflow.md](docs/which_workflow.md)
- [docs/getting_started.md](docs/getting_started.md)
- [docs/install.md](docs/install.md)
- [docs/cli_reference.md](docs/cli_reference.md)
- [docs/schema_reference.md](docs/schema_reference.md)
- [docs/privacy_and_data_safety.md](docs/privacy_and_data_safety.md)
- [docs/troubleshooting.md](docs/troubleshooting.md)
