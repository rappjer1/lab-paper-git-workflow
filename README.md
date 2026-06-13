# Paper Scaffold

[![Tests](https://github.com/rappjer1/lab-paper-git-workflow/actions/workflows/tests.yml/badge.svg)](https://github.com/rappjer1/lab-paper-git-workflow/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Paper Scaffold is a lightweight workflow and CLI for turning research outputs into clean GitHub/Overleaf manuscript repositories.

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

You do not need Overleaf, Pandoc, LaTeX, GitHub CLI, or GitHub Actions to read the workflow docs or use the basic scaffold.

## The Problem It Solves

Research repositories often collect scripts, notebooks, model outputs, generated figures, result caches, manuscript drafts, and copied submission folders. That is convenient during analysis but risky for manuscript writing.

Paper Scaffold helps prevent:

- Connecting Overleaf to an entire analysis repo.
- Accidentally committing raw data, model outputs, or large result folders.
- Losing track of which figure came from which script.
- Using implementation labels in the main manuscript text.
- Replacing Git branches/tags with repeated ZIP files.

## The 5-Minute Demo

From a source checkout:

```bash
python scripts/paper-scaffold.py doctor
python scripts/paper-scaffold.py quickstart
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
```

After installation, use `paper-scaffold` directly:

```bash
paper-scaffold doctor
paper-scaffold quickstart
paper-scaffold demo --output scratch/demo_manuscript --overwrite
```

The first command to run is usually:

```bash
paper-scaffold doctor
```

or, from a checkout:

```bash
python scripts/paper-scaffold.py doctor
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

## Install

No install is required if you run from a checkout:

```bash
git clone https://github.com/rappjer1/lab-paper-git-workflow.git
cd lab-paper-git-workflow
python scripts/paper-scaffold.py --help
```

Editable install:

```bash
python -m pip install -e .
paper-scaffold --help
```

Development install:

```bash
python -m pip install -e ".[dev]"
pytest tests
```

## Quick Start

```bash
paper-scaffold doctor
paper-scaffold init --manuscript-repo ./paper
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md --write-json ./paper/validation_report.json
```

Then push `./paper` to GitHub and import that GitHub repo into Overleaf if you use Overleaf.

More detail: [docs/getting_started.md](docs/getting_started.md)

## Core Commands

- `paper-scaffold doctor`: check Python, Git, optional tools, and repo shape.
- `paper-scaffold quickstart`: print the three common workflows.
- `paper-scaffold demo`: create a small demo manuscript repo.
- `paper-scaffold init`: create a clean manuscript repo scaffold.
- `paper-scaffold import-word`: convert `.docx` with Pandoc when available.
- `paper-scaffold discover-artifacts`: find likely manuscript figures/tables.
- `paper-scaffold add-artifact`: add one manifest entry interactively or by flags.
- `paper-scaffold copy-artifacts`: copy files listed in the manifest.
- `paper-scaffold stale-artifacts`: report copied artifacts whose source changed later.
- `paper-scaffold unused-artifacts`: report figure/table files not referenced from TeX.
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
```

Reference: [docs/error_codes.md](docs/error_codes.md)

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

- [examples/minimal_word_workflow](examples/minimal_word_workflow)
- [examples/minimal_python_artifacts](examples/minimal_python_artifacts)
- [examples/existing_latex_cleanup](examples/existing_latex_cleanup)

Generate the Python example artifacts:

```bash
python examples/minimal_python_artifacts/make_example_figure.py
```

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
