# Paper Scaffold

[![Tests](https://github.com/rappjer1/lab-paper-git-workflow/actions/workflows/tests.yml/badge.svg)](https://github.com/rappjer1/lab-paper-git-workflow/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Paper Scaffold is a lightweight workflow and CLI for turning research outputs into clean GitHub/Overleaf manuscript repositories.

## Start Here

Paper Scaffold does not write papers automatically. It helps you create and check a clean manuscript repository, copy only selected paper-ready artifacts, and keep provenance records for figures and tables.

Run from a checkout with `python scripts/paper-scaffold.py ...`. After install, use `paper-scaffold ...`. If the console script is not on `PATH`, use `python -m paper_scaffold ...`.

### I Just Want To Try It

```bash
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
```

### I Have Python Figures Or Tables

```bash
python scripts/paper-scaffold.py discover-artifacts --source <output-folder> --suggest-only
python scripts/paper-scaffold.py validate --manuscript-repo <repo>
```

### I Have A Manuscript Repo

```bash
python scripts/paper-scaffold.py release-check --manuscript-repo <repo>
python scripts/paper-scaffold.py provenance-report --manuscript-repo <repo>
```

Not sure which path fits? Use the workflow guide: [docs/which_workflow.md](docs/which_workflow.md).

## What This Is

Paper Scaffold helps researchers create a separate manuscript repository from a research/code repository. It gives you docs, templates, and a small Python CLI for moving Word drafts, Python-generated figures/tables, and existing LaTeX projects into a clean manuscript repo that can be pushed to GitHub and imported into Overleaf.

Core message:

> Keep research code and manuscript source separate. Copy only paper-ready artifacts into a clean manuscript repository, track provenance in a manifest, validate before syncing to Overleaf.

## Who This Is For

Use this if you are a researcher, graduate student, analyst, or research software engineer who has:

- A Word draft that needs to become an Overleaf-ready project.
- Python-generated figures or tables that need to move into a paper.
- An existing LaTeX folder that needs cleanup before GitHub/Overleaf sync.
- A research/code repository that should feed selected artifacts into a separate manuscript repository.
- A messy inherited project, Overleaf ZIP export, revision binder, or multi-paper output folder that needs triage before copying files.

You do not need Overleaf, Pandoc, LaTeX, GitHub CLI, or GitHub Actions to read the workflow docs or use the basic scaffold.

Paper Scaffold does not create GitHub repositories, upload to Overleaf, compile LaTeX, replace scientific review, or decide which artifacts belong in a paper.

## Stability Status

v0.9.x is the release-candidate hardening series. The core CLI is approaching v1.0, and command names, schemas, diagnostic codes, and exit-code conventions are being frozen. Users should expect small polish changes before v1.0, not major workflow churn.

See [contract.md](docs/contract.md), [versioning_policy.md](docs/versioning_policy.md), and [v1_0_readiness.md](docs/v1_0_readiness.md).

## The Problem It Solves

Research repositories often collect scripts, notebooks, model outputs, generated figures, result caches, manuscript drafts, and copied submission folders. That is convenient during analysis but risky for manuscript writing.

Paper Scaffold helps prevent:

- Connecting Overleaf to an entire analysis repo.
- Accidentally committing raw data, model outputs, or large result folders.
- Losing track of which figure came from which script.
- Losing track of whether a manuscript artifact matches its declared source output.
- Using implementation labels in the main manuscript text.
- Replacing Git branches/tags with repeated ZIP files.

## The 5-Minute Demo

From a source checkout:

```bash
python scripts/paper-scaffold.py doctor
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py quickstart
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
python scripts/paper-scaffold.py artifact-status --manuscript-repo scratch/demo_manuscript
python scripts/paper-scaffold.py package-submission --manuscript-repo scratch/demo_manuscript --output scratch/submission_package --overwrite
```

After installation, use `paper-scaffold` directly:

```bash
paper-scaffold doctor
paper-scaffold self-test
paper-scaffold quickstart
paper-scaffold demo --output scratch/demo_manuscript --overwrite
```

If the console script is not on `PATH`, use the module fallback:

```bash
python -m paper_scaffold self-test
python -m paper_scaffold --help
```

The first command to run is usually:

```bash
python -m paper_scaffold self-test
```

or, from a checkout:

```bash
python scripts/paper-scaffold.py self-test
```

## Three Common Workflows

### Word Draft To Overleaf-Ready Repo

```bash
paper-scaffold doctor
paper-scaffold init --manuscript-repo ./paper
paper-scaffold import-word --input draft.docx --output ./paper/converted.tex
paper-scaffold validate --manuscript-repo ./paper
```

Word conversion is a starting point. You must manually check equations, references, figures, tables, captions, and cross-references.

Guide: [docs/word_to_overleaf.md](docs/word_to_overleaf.md)

### Python Figures/Tables To Manuscript Repo

```bash
paper-scaffold doctor
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper
paper-scaffold validate --manuscript-repo ./paper
```

Guide: [docs/python_outputs_to_overleaf.md](docs/python_outputs_to_overleaf.md)

### Existing LaTeX Project To GitHub/Overleaf

```bash
paper-scaffold doctor --manuscript-repo ./paper
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md
git add .
git commit -m "Clean manuscript repository"
git push
```

Guide: [docs/existing_latex_project.md](docs/existing_latex_project.md)

## Use-Case Recipes

Paper Scaffold includes workflow recipes for common cleanup and handoff situations:

```bash
paper-scaffold recipes list
paper-scaffold recipes show paper-archaeology
```

Out-of-box recipes cover:

- Paper archaeology for messy inherited project folders.
- Overleaf ZIP rehab for turning downloaded exports into clean Git repos.
- Reviewer response binders for revision artifacts and checklists.
- Pre-submission flight checks before sync, sharing, or journal submission.
- Undergraduate-safe artifact harvesting for reviewable figure/table handoff.
- Multi-paper project splits where one research project feeds multiple manuscript repos.

Guide: [docs/use_cases](docs/use_cases)

## Install

No install is required if you run from a checkout:

```bash
git clone https://github.com/rappjer1/lab-paper-git-workflow.git
cd lab-paper-git-workflow
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py self-test
```

Editable install:

```bash
python -m pip install -e .
paper-scaffold --help
```

Module fallback after install:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

Development install:

```bash
python -m pip install -e ".[dev]"
python scripts/dev/run_tests.py
```

The test runner creates unique repo-local pytest temp directories for CMD, PowerShell, and Git Bash.

Local package and install-matrix audits:

```bash
python scripts/dev/build_package.py
python scripts/dev/install_matrix_audit.py
```

These checks build or consume local artifacts only. They do not publish to PyPI.

v0.9 install and test hardening:

- `python scripts/paper-scaffold.py ...` works from a checkout.
- `paper-scaffold ...` works when the console script is on `PATH`.
- `python -m paper_scaffold ...` works after install even when the console script path is unavailable.
- `paper-scaffold self-test` runs the core no-network smoke workflow.
- `python scripts/dev/run_tests.py` avoids shell-specific pytest temp-directory syntax.
- `python scripts/dev/install_matrix_audit.py` checks source, editable, fallback, console-script, and optional wheel/sdist install modes.

## Quick Start

```bash
python -m paper_scaffold self-test
paper-scaffold doctor
paper-scaffold init --manuscript-repo ./paper
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md --write-json ./paper/validation_report.json
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
paper-scaffold provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md
paper-scaffold add-manuscript-ci --manuscript-repo ./paper
paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package
```

Then push `./paper` to GitHub and import that GitHub repo into Overleaf if you use Overleaf.

More detail: [docs/getting_started.md](docs/getting_started.md)

## Core Commands

- `paper-scaffold doctor`: check Python, Git, optional tools, and repo shape.
- `paper-scaffold quickstart`: print the three common workflows.
- `paper-scaffold self-test`: run an installed-use no-network smoke test.
- `paper-scaffold schema`: list or show metadata schema summaries.
- `paper-scaffold recipes`: list or show workflow recipes.
- `paper-scaffold demo`: create a small demo manuscript repo.
- `paper-scaffold init`: create a clean manuscript repo scaffold.
- `paper-scaffold import-word`: convert `.docx` with Pandoc when available.
- `paper-scaffold audit-project`: read-only audit of a messy project folder.
- `paper-scaffold discover-artifacts`: find likely manuscript figures/tables.
- `paper-scaffold add-artifact`: add one manifest entry interactively or by flags.
- `paper-scaffold copy-artifacts`: copy files listed in the manifest.
- `paper-scaffold stale-artifacts`: report copied artifacts whose source changed later.
- `paper-scaffold unused-artifacts`: report figure/table files not referenced from TeX.
- `paper-scaffold release-check`: run consolidated pre-submission checks.
- `paper-scaffold provenance-report`: generate a Markdown/JSON bill of materials for manuscript artifacts.
- `paper-scaffold artifact-status`: print compact provenance status counts.
- `paper-scaffold freeze-artifacts`: write current manuscript artifact hashes to a lock file.
- `paper-scaffold compare-lock`: compare current manuscript artifact hashes to a lock file.
- `paper-scaffold add-manuscript-ci`: add a dependency-free GitHub Actions manuscript hygiene workflow.
- `paper-scaffold package-submission`: create a clean source/artifact folder for journal upload review.
- `paper-scaffold reviewer-binder`: create a lightweight response-round checklist and evidence folder.
- `paper-scaffold terminology-check`: find banned implementation labels.
- `paper-scaffold git-check`: summarize Git state.
- `paper-scaffold validate`: check manuscript repo shape, artifacts, terminology, and Git state.
- `paper-scaffold overleaf-instructions`: print GitHub/Overleaf sync guidance.
- `paper-scaffold explain`: explain a diagnostic code such as `E003`.
- `paper-scaffold overleaf-check`: check paths, figures, large files, and Overleaf sync risks.
- `paper-scaffold github-check`: check GitHub-readiness, remotes, status, repository docs, and privacy warnings.
- `paper-scaffold privacy-check`: scan text files for local paths, emails, token-like strings, and private markers.
- `paper-scaffold check-figures`: check `\includegraphics` paths and figure files.
- `paper-scaffold check-citations`: compare TeX citation keys against `references.bib`.
- `paper-scaffold check-labels`: check duplicate and missing LaTeX label targets.
- `paper-scaffold audit-word-conversion`: flag common Pandoc/Word conversion cleanup issues.

## Diagnostics And Reports

When a check finds a problem, it prints a stable diagnostic code:

```bash
paper-scaffold explain E003
paper-scaffold explain --list
```

Use focused checks before GitHub/Overleaf sync:

```bash
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md --write-json ./paper/validation_report.json
paper-scaffold overleaf-check --manuscript-repo ./paper
paper-scaffold github-check --repo ./paper
paper-scaffold privacy-check --path ./paper
paper-scaffold check-figures --manuscript-repo ./paper
paper-scaffold check-citations --manuscript-repo ./paper
paper-scaffold check-labels --manuscript-repo ./paper
paper-scaffold stale-artifacts --manuscript-repo ./paper
paper-scaffold unused-artifacts --manuscript-repo ./paper
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
paper-scaffold provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
paper-scaffold artifact-status --manuscript-repo ./paper
paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md --write-json ./paper/lock_comparison.json
paper-scaffold add-manuscript-ci --manuscript-repo ./paper
paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package
paper-scaffold reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1
```

Reference: [docs/error_codes.md](docs/error_codes.md)
Provenance guide: [docs/provenance_ledger.md](docs/provenance_ledger.md)
Artifact lock guide: [docs/artifact_locks.md](docs/artifact_locks.md)
Submission package guide: [docs/submission_packaging.md](docs/submission_packaging.md)
Workflow guide: [docs/which_workflow.md](docs/which_workflow.md)
Install guide: [docs/install.md](docs/install.md)
CLI reference: [docs/cli_reference.md](docs/cli_reference.md)
Schema reference: [docs/schema_reference.md](docs/schema_reference.md)
Example integrity: [docs/example_integrity.md](docs/example_integrity.md)
Contract: [docs/contract.md](docs/contract.md)
v1.0 readiness: [docs/v1_0_readiness.md](docs/v1_0_readiness.md)
Release process: [docs/release_process.md](docs/release_process.md)
Exit codes: [docs/exit_codes.md](docs/exit_codes.md)
Compatibility: [docs/compatibility.md](docs/compatibility.md)

## Recommended Manuscript Repo Structure

```text
paper/
  README.md
  .gitignore
  main.tex
  references.bib
  sections/
  figures/
  tables/
  supplement/
    supplement.tex
    figures/
    tables/
  metadata/
    artifact_manifest.yaml
    artifact_lock.json
    provenance_ledger.json
    terminology_map.yaml
    manuscript_config.yaml
```

## What Not To Commit

Keep these out of manuscript repositories:

- Raw data and external data dumps.
- Model checkpoints and prediction caches.
- `.npz`, `.pt`, `.pth`, `.pkl`, `.pickle`, `.nc`, `.zarr`, `.zip`, and large binary outputs.
- `full_eval/`, `prediction_cache/`, `raw_api_cache/`, and `data/external/`.
- Full generated output trees when only one figure is needed.
- LaTeX build artifacts such as `.aux`, `.log`, `.bbl`, and `.synctex.gz`.

## Overleaf/GitHub Workflow

Paper Scaffold does not require Overleaf. If you use Overleaf, the recommended pattern is:

1. Keep the manuscript source in a clean GitHub repo.
2. In Overleaf, create a new project from GitHub.
3. Treat GitHub as the source of truth.
4. If editing locally, push to GitHub and then sync in Overleaf.
5. If editing in Overleaf, push from Overleaf and then pull locally.

Guide: [docs/github_overleaf_sync.md](docs/github_overleaf_sync.md)

## Examples

- [examples/README.md](examples/README.md)
- [examples/minimal_word_workflow](examples/minimal_word_workflow)
- [examples/minimal_python_artifacts](examples/minimal_python_artifacts)
- [examples/existing_latex_cleanup](examples/existing_latex_cleanup)
- [examples/messy_project_archaeology](examples/messy_project_archaeology)
- [examples/reviewer_response_binder](examples/reviewer_response_binder)
- [examples/reviewer_response_round](examples/reviewer_response_round)
- [examples/submission_packaging](examples/submission_packaging)
- [examples/manuscript_ci](examples/manuscript_ci)
- [examples/multi_paper_split](examples/multi_paper_split)

Generate the Python example artifacts:

```bash
python examples/minimal_python_artifacts/make_example_figure.py
```

Example artifacts are synthetic and intentionally small. Run `python scripts/dev/check_example_integrity.py` to verify that example PDFs and images have valid file signatures and that text examples do not contain local/private paths.

## Roadmap And Architecture

- [ROADMAP.md](ROADMAP.md)
- [Architecture decision records](docs/adr)

## Limitations

- Paper Scaffold does not write the science for you.
- It does not automatically create GitHub repositories.
- It does not upload anything to Overleaf.
- It does not require LaTeX and does not compile LaTeX unless you install separate tools.
- Word conversion requires Pandoc and still needs manual review.
- Artifact discovery suggests candidates; humans still review provenance, captions, and filenames.
- It does not manage Git LFS.

## Contributing

Contributions are welcome. Please open an issue before large changes, keep examples generic, avoid large binary files, update docs, and add tests for CLI changes.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation / Acknowledgement

If Paper Scaffold helps your project, cite or acknowledge it using [CITATION.cff](CITATION.cff) or link to this repository.

## License

MIT. See [LICENSE](LICENSE).
