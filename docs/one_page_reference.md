# One-Page Reference

Use this page when you already know what Paper Scaffold is and need the command names.

## Invocation

```bash
python scripts/paper-scaffold.py <command>
paper-scaffold <command>
python -m paper_scaffold <command>
```

Use the first form from a checkout, the second after install when `paper-scaffold` is on `PATH`, and the third as the installed fallback.

## Try It

```bash
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
```

## Create Or Check A Manuscript Repo

```bash
python scripts/paper-scaffold.py init --manuscript-repo ./paper --non-interactive
python scripts/paper-scaffold.py doctor --manuscript-repo ./paper
python scripts/paper-scaffold.py validate --manuscript-repo ./paper --write-report ./paper/validation_report.md --write-json ./paper/validation_report.json
python scripts/paper-scaffold.py release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
```

## Add Figures And Tables

```bash
python scripts/paper-scaffold.py discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml --suggest-only
python scripts/paper-scaffold.py add-artifact --manuscript-repo ./paper --id fig1 --type figure --source-path ./outputs/fig1.pdf --destination figures/fig1.pdf
python scripts/paper-scaffold.py copy-artifacts --manuscript-repo ./paper
```

## Provenance And Drift

```bash
python scripts/paper-scaffold.py provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
python scripts/paper-scaffold.py artifact-status --manuscript-repo ./paper
python scripts/paper-scaffold.py freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
python scripts/paper-scaffold.py compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md
```

## Focused Checks

```bash
python scripts/paper-scaffold.py overleaf-check --manuscript-repo ./paper
python scripts/paper-scaffold.py github-check --repo ./paper
python scripts/paper-scaffold.py privacy-check --path ./paper
python scripts/paper-scaffold.py check-figures --manuscript-repo ./paper
python scripts/paper-scaffold.py check-citations --manuscript-repo ./paper
python scripts/paper-scaffold.py check-labels --manuscript-repo ./paper
python scripts/paper-scaffold.py stale-artifacts --manuscript-repo ./paper
python scripts/paper-scaffold.py unused-artifacts --manuscript-repo ./paper
```

## Submission And Revision

```bash
python scripts/paper-scaffold.py add-manuscript-ci --manuscript-repo ./paper
python scripts/paper-scaffold.py package-submission --manuscript-repo ./paper --output ./submission_package
python scripts/paper-scaffold.py reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1
```

## Maintainer Checks

```bash
python scripts/dev/check_text_blobs.py
python scripts/dev/check_contracts.py
python scripts/dev/check_docs_examples.py
python scripts/dev/check_docs_links.py
python scripts/dev/check_example_integrity.py
python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output
python scripts/dev/run_tests.py
```

## More Detail

- [Start Here](start_here.md)
- [Common Paths](common_paths.md)
- [CLI Reference](cli_reference.md)
- [Error Codes](error_codes.md)
- [Glossary](glossary.md)
- [Troubleshooting](troubleshooting.md)
