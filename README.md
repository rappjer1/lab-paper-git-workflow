# lab-paper-git-workflow

Internal lab guide and lightweight tooling for creating clean manuscript Git repositories from research/code repositories, then connecting those manuscript repositories to GitHub and Overleaf.

This repo is not a manuscript repo. It is not a research/modeling repo. It is a reusable workflow guide plus a small Python CLI that helps lab members keep those two jobs separate.

## What This Repo Is

`lab-paper-git-workflow` gives the lab a standard way to move from "the analysis is done in a research repo" to "the paper source is clean, reviewable, and synced with Overleaf."

It includes:

- A manual workflow that works even if you never install the Python package.
- A template manuscript repository with LaTeX, figures, tables, supplement, and metadata folders.
- A CLI named `paper-scaffold` for initializing, validating, and updating manuscript repos.
- Provenance manifests for copied figures and tables.
- Terminology maps that separate code labels from publication-facing labels.

## What Problem It Solves

Research repos tend to collect everything: scripts, model outputs, generated figures, result caches, copied manuscript folders, Overleaf ZIPs, and temporary drafts. That is normal during analysis, but it is a bad place to edit the final paper.

The failure modes are predictable:

- Overleaf gets connected to a full analysis repo.
- Large generated files get staged by accident.
- Implementation labels leak into the manuscript.
- Figures are copied without a record of where they came from.
- Repeated ZIP files replace branches, tags, and commits.
- Nobody can tell which folder is the current manuscript.

This repo prevents that by making the manuscript repo small, explicit, and boring.

## Use This When...

- You have a research repo that produced figures, tables, or diagnostics for a paper.
- You want a separate private GitHub repo for the manuscript.
- You want Overleaf to compile and edit the paper, but GitHub to remain the canonical source.
- You need to track where publication figures and tables came from.
- You need to clean implementation-specific model or cache names out of manuscript text.

## Do Not Use This When...

- You are trying to version raw data, model checkpoints, or full evaluation outputs.
- You want Overleaf connected directly to the full analysis repo.
- You need a data archive or release package. Use the lab data archive workflow for that.
- You are trying to reproduce model training. That belongs in the research repo.

## The 5-Minute Version

1. Keep the research repo as the source of computations.
2. Create a separate manuscript repo.
3. Copy only selected publication figures, tables, references, manuscript source, and supplement files.
4. Record copied artifacts in `metadata/artifact_manifest.yaml`.
5. Keep implementation labels in metadata, not in main paper text.
6. Push the manuscript repo to private GitHub.
7. Create a new Overleaf project from that GitHub repo.
8. Use Git branches and tags instead of repeated ZIP folders.

## Recommended Workflow

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

The research repo remains the source of truth for computation. The manuscript repo becomes the source of truth for paper source files.

## The Full Clean Workflow

1. Finish or freeze the analysis outputs needed for the next manuscript update.
2. Create or update a separate manuscript repo.
3. Copy publication-ready figures and tables into `figures/`, `tables/`, `supplement/figures/`, or `supplement/tables/`.
4. Update `metadata/artifact_manifest.yaml` with source paths, scripts, inputs, dates, and status.
5. Update `metadata/terminology_map.yaml` with implementation labels that should not appear in the main text.
6. Run `paper-scaffold validate`.
7. Commit and push to GitHub.
8. Sync Overleaf from GitHub.
9. For revisions, use branches such as `revision-1` and tags such as `submission-v1`.

## Quick Start

From a checkout of this repo:

```bash
python scripts/paper-scaffold.py init
python scripts/paper-scaffold.py add-artifact
python scripts/paper-scaffold.py validate --manuscript-repo <manuscript-repo>
```

After package installation, the same commands are available as:

```bash
paper-scaffold init
paper-scaffold add-artifact
paper-scaffold validate --manuscript-repo <manuscript-repo>
```

See [QUICKSTART.md](QUICKSTART.md) for Git Bash, PowerShell, and manual fallback steps.

## Folder Structure

This repository:

```text
docs/                       workflow guides
templates/manuscript_repo/  starter manuscript repo
src/paper_scaffold/         Python CLI implementation
scripts/paper-scaffold.py   run-from-checkout wrapper
examples/                   generic example YAML files
tests/                      lightweight tests
```

A scaffolded manuscript repo:

```text
main.tex
references.bib
sections/
figures/
tables/
supplement/
metadata/
  artifact_manifest.yaml
  terminology_map.yaml
  manuscript_config.yaml
```

## What Belongs In The Research Repo Vs Manuscript Repo

Research repo:

- Code, notebooks, scripts, and model definitions.
- Raw or processed data, where permitted by the project.
- Full generated output trees.
- Model checkpoints and prediction caches.
- External API caches.
- Reproducibility instructions for computation.

Manuscript repo:

- `main.tex`, section files, and supplement source.
- `references.bib`.
- Publication figures and tables selected from the research repo.
- Small summary files only when they are part of the submitted supplement.
- Metadata that records artifact provenance.
- Terminology map for publication labels.

## What Never Belongs In The Manuscript Repo

Do not commit:

- `.npz`, `.pt`, `.pth`, `.pkl`, `.nc`, or large binary outputs.
- `full_eval/`, `prediction_cache/`, `raw_api_cache/`, `raw_results/`, or `raw_outputs/`.
- Raw external data dumps.
- Full model run directories.
- Repeated Overleaf ZIP snapshots.
- A second copy of the research repo.

## How To Connect GitHub To Overleaf

Preferred path:

1. Create a private GitHub repo for the manuscript.
2. Push the manuscript source to GitHub.
3. In Overleaf, create a new project from GitHub.
4. Set `main.tex` as the main document.
5. Pull/sync in Overleaf after local commits.
6. Push from Overleaf only when edits were made there.

Do not connect Overleaf to the full analysis repo. Existing Overleaf projects are usually best kept as archives; create a new Overleaf project from GitHub when possible.

## How To Update Figures/Tables

1. Regenerate outputs in the research repo.
2. Copy only the selected publication figure or table into the manuscript repo.
3. Update `metadata/artifact_manifest.yaml`.
4. Run `paper-scaffold copy-artifacts` if the manifest should drive copying.
5. Run `paper-scaffold validate`.
6. Commit the figure/table update with a clear message.

The manifest is the record of provenance. It is not a raw data archive.

## How To Use Codex Safely

Tell Codex:

- The repo path and current branch.
- Whether it may edit code, manuscript text, metadata, or results.
- Which repos are off limits.
- Whether expensive jobs are forbidden.
- That it should not create ZIP snapshots unless requested.
- That it should report changed files and run validation.

Use separate chats or branches for manuscript text, data/API audits, and model training.

## Common Mistakes

- Connecting Overleaf to the research repo.
- Copying whole `results/` folders because one figure is needed.
- Keeping old manuscript folders named `paper_final`, `paper_final2`, and `paper_final_really`.
- Using code labels in the abstract or results section.
- Forgetting to commit the artifact manifest after copying figures.
- Editing the same paragraph locally and in Overleaf at the same time.
- Typing `orign` instead of `origin` when adding a remote.

## Common Failure Modes

- `paper-scaffold validate` reports missing `origin`: add the GitHub remote.
- Overleaf does not show the latest figure: sync from GitHub and recompile.
- A large file warning appears: remove the file and keep it in the research repo.
- A banned term appears: update the text with the publication label or adjust the terminology map if the term is allowed in that context.
- Git shows LaTeX build files staged: unstage them and rely on `.gitignore`.

## Minimal Example

```bash
git clone <research-repo>
git clone <manuscript-repo>
cd <path-to-lab-paper-git-workflow>
python scripts/paper-scaffold.py init --manuscript-repo <manuscript-repo>
python scripts/paper-scaffold.py add-artifact --manuscript-repo <manuscript-repo>
python scripts/paper-scaffold.py validate --manuscript-repo <manuscript-repo>
cd <manuscript-repo>
git add .
git commit -m "Initialize manuscript repo"
git push
```

## Advanced Example With Supplement

```bash
python scripts/paper-scaffold.py init \
  --research-repo R:/Code/my_project \
  --manuscript-repo R:/Code/manuscripts/my_project_paper \
  --title "Example Rainfall-Runoff Manuscript" \
  --slug example_rainfall_runoff \
  --has-supplement \
  --use-template \
  --non-interactive
```

Then add main and supplement artifacts to `metadata/artifact_manifest.yaml`:

```yaml
artifacts:
  - id: hydrograph_summary
    type: figure
    manuscript_path: figures/hydrograph_summary.pdf
    source_repo: R:/Code/my_project
    source_path: outputs/final_figures/hydrograph_summary.pdf
    generated_by: scripts/make_publication_figures.py
    input_data: outputs/summary_metrics.csv
    last_updated: 2026-06-10
    caption_hint: Example hydrograph summary.
    status: final
  - id: supplement_diagnostic_grid
    type: supplement_figure
    manuscript_path: supplement/figures/diagnostic_grid.pdf
    source_repo: R:/Code/my_project
    source_path: outputs/final_figures/diagnostic_grid.pdf
    generated_by: scripts/make_diagnostics.py
    input_data: outputs/diagnostic_summary.csv
    last_updated: 2026-06-10
    caption_hint: Supplementary diagnostic grid.
    status: final
```

## FAQ

**Should I ever connect Overleaf to the research repo?**

No. Create a separate manuscript repo.

**Can the manuscript repo contain code?**

Only tiny helper scripts that are part of the manuscript build. Analysis, modeling, and data processing code belong in the research repo.

**Do I need the CLI?**

No. The docs describe the manual workflow. The CLI just makes the checks and scaffold faster.

**Where do figure captions live?**

Final captions live in LaTeX. `caption_hint` in the manifest is a reminder, not the submitted caption.

**What should I tag?**

Tag important paper states, such as `submission-v1`, `revision-1-response`, or `accepted-version`.

## Maintainer Checklist

- Keep templates small and generic.
- Keep examples generic and non-project-specific.
- Add validation checks only when they prevent real mistakes.
- Avoid hard-coding one manuscript, dataset, or modeling framework.
- Keep docs useful for a new graduate student working manually.
- Test the wrapper script from a source checkout.
