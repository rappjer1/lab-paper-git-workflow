# Quick Start

Paper Scaffold helps you create and check a clean manuscript repository from selected research outputs. It does not write the paper, create GitHub repositories, upload to Overleaf, or decide which artifacts belong in the manuscript.

From a checkout, examples use:

```bash
python scripts/paper-scaffold.py <command>
```

After install, use:

```bash
paper-scaffold <command>
python -m paper_scaffold <command>
```

## Choose Your Starting Point

### Try The Tool

```bash
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
```

Expected result: a synthetic manuscript repo in `scratch/demo_manuscript` and validation output with no errors.

### Start A Manuscript Repo

```bash
python scripts/paper-scaffold.py init --manuscript-repo ./paper --non-interactive
python scripts/paper-scaffold.py validate --manuscript-repo ./paper
```

Expected result: a clean manuscript scaffold with `main.tex`, `references.bib`, `sections/`, `figures/`, `tables/`, and `metadata/`.

### Validate An Existing Manuscript Repo

```bash
python scripts/paper-scaffold.py release-check --manuscript-repo <repo> --write-report <repo>/release_check.md
python scripts/paper-scaffold.py overleaf-check --manuscript-repo <repo>
```

Expected result: focused diagnostics before GitHub/Overleaf sync or submission.

### Discover Python Artifacts

```bash
python scripts/paper-scaffold.py discover-artifacts --source <output-folder> --manifest <repo>/metadata/artifact_manifest.yaml --suggest-only
python scripts/paper-scaffold.py validate --manuscript-repo <repo>
```

Expected result: a candidate list of paper-ready figures and tables. Add `--write --copy --manuscript-repo <repo>` only after reviewing the suggestions.

### Package For Submission

```bash
python scripts/paper-scaffold.py release-check --manuscript-repo <repo>
python scripts/paper-scaffold.py freeze-artifacts --manuscript-repo <repo> --write-lock <repo>/metadata/artifact_lock.json
python scripts/paper-scaffold.py package-submission --manuscript-repo <repo> --output <submission-folder>
```

Expected result: a clean source/artifact folder for manual journal upload review.

### Create A Reviewer Binder

```bash
python scripts/paper-scaffold.py provenance-report --manuscript-repo <repo> --write-md <repo>/provenance_report.md
python scripts/paper-scaffold.py reviewer-binder --manuscript-repo <repo> --round 1 --output <response-folder>
```

Expected result: a response-round checklist and evidence folder. Keep confidential reviewer text out of public repositories.

## Manual Fallback Without The CLI

1. Create a separate manuscript repository.
2. Add `main.tex`, `references.bib`, `sections/`, `figures/`, `tables/`, `supplement/`, and `metadata/`.
3. Copy only selected publication figures and tables.
4. Create `metadata/artifact_manifest.yaml`.
5. Create `metadata/terminology_map.yaml` if implementation labels need cleanup.
6. Add a `.gitignore` for LaTeX build files and raw/model/cache outputs.
7. Run `git status` and inspect every staged file.
8. Commit and push to GitHub if you use GitHub.
9. Import the GitHub repo into Overleaf if desired.

## Next Reading

- [docs/which_workflow.md](docs/which_workflow.md)
- [docs/getting_started.md](docs/getting_started.md)
- [docs/install.md](docs/install.md)
- [docs/cli_reference.md](docs/cli_reference.md)
- [docs/schema_reference.md](docs/schema_reference.md)
- [docs/example_integrity.md](docs/example_integrity.md)
- [docs/word_to_overleaf.md](docs/word_to_overleaf.md)
- [docs/python_outputs_to_overleaf.md](docs/python_outputs_to_overleaf.md)
- [docs/existing_latex_project.md](docs/existing_latex_project.md)
- [docs/submission_packaging.md](docs/submission_packaging.md)
- [docs/reviewer_response_binder.md](docs/reviewer_response_binder.md)
