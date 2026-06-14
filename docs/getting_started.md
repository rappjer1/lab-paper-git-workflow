# Getting Started

This guide walks through the shortest useful path: check your tools, create a sample manuscript repo, add one figure, validate, push to GitHub, and import to Overleaf if desired.

## Install Or No Install

Run from a source checkout:

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
paper-scaffold self-test
```

Module fallback after install:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

These three invocation modes are equivalent for normal commands:

```bash
python scripts/paper-scaffold.py doctor
paper-scaffold doctor
python -m paper_scaffold doctor
```

## Run Doctor

```bash
paper-scaffold doctor
```

From a checkout:

```bash
python scripts/paper-scaffold.py doctor
```

`doctor` reports required and optional tools. Missing Pandoc, LaTeX, GitHub CLI, or Overleaf access does not block the basic workflow.

## Create A Sample Manuscript Repo

```bash
paper-scaffold init --manuscript-repo ./paper --title "Example Paper" --slug example_paper --non-interactive
```

This creates a small manuscript repository with LaTeX source, figures/tables folders, supplement folders, and metadata files.

## Add One Figure

If your research repo has a final figure:

```bash
paper-scaffold add-artifact \
  --manuscript-repo ./paper \
  --id example_metric_plot \
  --type figure \
  --source-repo ./research-project \
  --source-path outputs/final/example_metric_plot.pdf \
  --destination figures/example_metric_plot.pdf \
  --generated-by scripts/make_figures.py \
  --input-data outputs/final/example_summary_table.csv \
  --caption-hint "Example metric plot." \
  --status final \
  --no-copy-now
```

To discover candidates automatically:

```bash
paper-scaffold discover-artifacts --source ./research-project/outputs/final --manifest ./paper/metadata/artifact_manifest.yaml
```

Add `--write --copy --manuscript-repo ./paper` only after reviewing the suggestions.

## Validate

```bash
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md
```

Fix errors before syncing with collaborators or Overleaf.

## Push To GitHub

Create a GitHub repository manually, then:

```bash
cd paper
git init
git add .
git commit -m "Initialize manuscript repository"
git branch -M main
git remote add origin https://github.com/<owner>/<paper-repo>.git
git push -u origin main
```

GitHub CLI is optional. Paper Scaffold does not create GitHub repositories automatically.

## Import To Overleaf

In Overleaf:

1. New Project -> Import from GitHub.
2. Select the manuscript repository.
3. Set `main.tex` as the main document.
4. Compile.
5. Sync through GitHub when editing locally or in Overleaf.

Overleaf is optional. You can use the manuscript repo with local LaTeX tools or another editor.
