# Quickstart

This is the short path for a lab member who already has:

- A research repo.
- A folder of final figures.
- A folder of LaTeX manuscript files, or a plan to start from the template.
- A private GitHub repo for the manuscript.
- Optional Overleaf access.

## Git Bash

```bash
git clone <research-repo>
git clone <manuscript-repo>
cd /r/Code/lab_tools/lab-paper-git-workflow
python scripts/paper-scaffold.py init
python scripts/paper-scaffold.py add-artifact
python scripts/paper-scaffold.py validate --manuscript-repo <manuscript-repo>
cd <manuscript-repo>
git add .
git commit -m "Initialize manuscript repo"
git push
```

Git Bash uses forward slashes:

```bash
cd /r/Code/manuscripts/my_project_paper
```

## PowerShell

```powershell
git clone <research-repo>
git clone <manuscript-repo>
Set-Location R:\Code\lab_tools\lab-paper-git-workflow
python scripts\paper-scaffold.py init
python scripts\paper-scaffold.py add-artifact
python scripts\paper-scaffold.py validate --manuscript-repo <manuscript-repo>
Set-Location <manuscript-repo>
git add .
git commit -m "Initialize manuscript repo"
git push
```

PowerShell can use backslashes, but quote paths that contain spaces:

```powershell
Set-Location "R:\Code\manuscripts\my project paper"
```

## Starting From Template

```bash
python scripts/paper-scaffold.py init \
  --research-repo R:/Code/my_project \
  --manuscript-repo R:/Code/manuscripts/my_project_paper \
  --title "My Project Paper" \
  --slug my_project_paper \
  --has-supplement \
  --use-template \
  --non-interactive
```

## Starting From Existing LaTeX

```bash
python scripts/paper-scaffold.py init \
  --research-repo R:/Code/my_project \
  --manuscript-repo R:/Code/manuscripts/my_project_paper \
  --title "My Project Paper" \
  --slug my_project_paper \
  --no-template \
  --non-interactive
```

Then copy your existing `main.tex`, `sections/`, `references.bib`, figures, and supplement files into the manuscript repo by hand.

## Add One Artifact

```bash
python scripts/paper-scaffold.py add-artifact \
  --manuscript-repo R:/Code/manuscripts/my_project_paper \
  --id workflow_schematic \
  --type figure \
  --source-repo R:/Code/my_project \
  --source-path outputs/final_figures/workflow_schematic.pdf \
  --destination figures/workflow_schematic.pdf \
  --generated-by scripts/make_publication_figures.py \
  --input-data outputs/summary_metrics.csv \
  --caption-hint "Workflow schematic." \
  --status final \
  --copy-now \
  --non-interactive
```

## Manual Fallback Without The Tool

1. Create a new private GitHub repo for the manuscript.
2. Clone it locally.
3. Create `main.tex`, `references.bib`, `sections/`, `figures/`, `tables/`, `supplement/`, and `metadata/`.
4. Copy only selected publication figures and tables.
5. Create `metadata/artifact_manifest.yaml`.
6. Create `metadata/terminology_map.yaml`.
7. Add a `.gitignore` that excludes LaTeX build files and raw/model/cache outputs.
8. Run `git status` and inspect every staged file.
9. Commit and push.
10. Create a new Overleaf project from GitHub.

## Validate Before Overleaf Sync

```bash
python scripts/paper-scaffold.py validate --manuscript-repo R:/Code/manuscripts/my_project_paper
python scripts/paper-scaffold.py terminology-check --manuscript-repo R:/Code/manuscripts/my_project_paper
python scripts/paper-scaffold.py git-check --manuscript-repo R:/Code/manuscripts/my_project_paper
```
