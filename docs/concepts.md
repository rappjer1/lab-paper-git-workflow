# Concepts

This workflow exists to keep computation, manuscript editing, provenance, and Overleaf sync in separate places.

```text
Research repo
  scripts, models, data, generated outputs
        |
        | selected artifacts + manifest
        v
Manuscript repo
  LaTeX, figures, tables, references, supplement
        |
        v
GitHub private repo <-> Overleaf project
```

## Research Repo Vs Manuscript Repo

The research repo is where computations happen. It contains scripts, notebooks, model code, data access logic, generated results, and diagnostics.

The manuscript repo is where paper source lives. It contains LaTeX, references, selected publication figures and tables, supplement files, and metadata that explains where those artifacts came from.

Do not connect Overleaf to the research repo.

## Analysis Artifacts Vs Manuscript Artifacts

Analysis artifacts are all outputs produced while doing the work: raw metrics, large CSVs, caches, model predictions, diagnostic grids, temporary figures, and evaluation directories.

Manuscript artifacts are the small selected subset that belongs in the paper: final figures, final tables, and small supplement files.

The manuscript repo should contain manuscript artifacts, not the whole analysis output tree.

## Source Outputs Vs Copied Publication Figures

The source output stays in the research repo, often under a path like `outputs/final_figures/figure_1.pdf`.

The copied publication figure lives in the manuscript repo, often under `figures/figure_1.pdf`.

The manifest links the two paths. That link is enough for provenance. You do not need to copy the surrounding output directory.

## Provenance Vs Raw Data

Provenance answers: where did this figure or table come from?

Raw data answers: what underlying records were used?

The manuscript repo needs provenance, not raw data. Keep raw data in the research repo, a data archive, or the approved storage location for the project.

## Overleaf Project Vs GitHub Repo

GitHub should be the canonical source for the manuscript repo. Overleaf is a frontend for editing and compilation.

The clean pattern is:

1. Push the manuscript repo to GitHub.
2. Create a new Overleaf project from GitHub.
3. Sync Overleaf after local commits.
4. Push from Overleaf only when edits were made there.

## Main Manuscript Vs Supplement

The main manuscript should contain the primary narrative, figures, and tables.

The supplement can contain additional methods, diagnostics, provenance tables, and supporting figures. It is still manuscript source, not a dump of all results.

## Code Names Vs Publication Names

Code names are implementation labels. They are useful in scripts, configs, logs, and provenance tables.

Publication names are scientific labels. They belong in the title, abstract, methods, results, and discussion.

Use `metadata/terminology_map.yaml` to make this explicit. For example, a run label like `internal_model_v1` might map to `probabilistic runoff model`.

## Why Repeated ZIP Files Are A Bad Long-Term Workflow

ZIP files are fine for one-off transfers. They are bad as the main workflow because:

- They hide what changed.
- They encourage names like `paper_final_revised_2.zip`.
- They make it easy to use stale files.
- They are hard to review.
- They do not preserve branch history.

Use Git branches for active work and tags for important states such as `submission-v1`, `revision-1`, and `accepted-version`.
