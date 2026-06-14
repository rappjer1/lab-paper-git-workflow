# Getting Started

This guide walks through two practical paths:

- a five-minute local demo using synthetic files;
- a fifteen-minute dry run on your own project folder.

No LaTeX installation or Overleaf account is required for the demo. Paper Scaffold checks repository shape, metadata, artifact provenance, and common sync risks; it does not compile the paper or upload anything.

The bundled examples are synthetic and intentionally small. Example file integrity is documented in [example_integrity.md](example_integrity.md).

## Install Or No Install

Run from a source checkout:

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

Module fallback after install:

```bash
python -m paper_scaffold --help
```

These invocation modes are equivalent for normal commands:

```bash
python scripts/paper-scaffold.py doctor
paper-scaffold doctor
python -m paper_scaffold doctor
```

For choosing a workflow, see [which_workflow.md](which_workflow.md).

## Five-Minute Local Demo

Run:

```bash
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
python scripts/paper-scaffold.py release-check --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/release_check.md
python scripts/paper-scaffold.py provenance-report --manuscript-repo scratch/demo_manuscript --write-md scratch/demo_manuscript/provenance_report.md
```

Inspect after the commands run:

- `scratch/demo_manuscript/main.tex`
- `scratch/demo_manuscript/figures/`
- `scratch/demo_manuscript/tables/`
- `scratch/demo_manuscript/metadata/artifact_manifest.yaml`
- `scratch/demo_manuscript/release_check.md`
- `scratch/demo_manuscript/provenance_report.md`

Expected result: the demo validates with no errors. The figure and table are synthetic, small, and safe to inspect.

## Fifteen-Minute Real Project Dry Run

Use this when you have a project folder but are not ready to copy files.

1. Audit the project folder:

```bash
python scripts/paper-scaffold.py audit-project --path <project-folder> --write-report scratch/project_audit.md
```

Inspect:

- likely manuscript files;
- generated output folders;
- suspicious final-version filenames;
- raw/cache/model outputs that should not move into a manuscript repo.

2. Create or point at a manuscript repo:

```bash
python scripts/paper-scaffold.py init --manuscript-repo <repo> --non-interactive
```

Inspect:

- `main.tex`
- `references.bib`
- `metadata/manuscript_config.yaml`
- `metadata/artifact_manifest.yaml`
- `metadata/terminology_map.yaml`

3. Discover candidate figures and tables without writing:

```bash
python scripts/paper-scaffold.py discover-artifacts --source <output-folder> --manifest <repo>/metadata/artifact_manifest.yaml --suggest-only
```

Inspect:

- candidate figure/table filenames;
- suggested destinations;
- skipped raw/cache/model files.

4. Validate the manuscript repo:

```bash
python scripts/paper-scaffold.py validate --manuscript-repo <repo> --write-report <repo>/validation_report.md
python scripts/paper-scaffold.py release-check --manuscript-repo <repo> --write-report <repo>/release_check.md
```

Inspect:

- blocking errors first;
- warnings about unreferenced figures, missing citations, private paths, or large files;
- whether the report recommends manual review before sync or submission.

## What To Do Next

- For Python output handoff, read [python_outputs_to_overleaf.md](python_outputs_to_overleaf.md).
- For existing LaTeX cleanup, read [existing_latex_project.md](existing_latex_project.md).
- For submission packaging, read [submission_packaging.md](submission_packaging.md).
- For reviewer response organization, read [reviewer_response_binder.md](reviewer_response_binder.md).
- For GitHub/Overleaf sync, read [github_overleaf_sync.md](github_overleaf_sync.md).

Paper Scaffold prepares clean files and reports. Humans still review scientific content, journal requirements, captions, figure quality, and collaborator-facing text.
