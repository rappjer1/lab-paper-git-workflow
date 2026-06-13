# Existing LaTeX Cleanup

## Scenario

An existing LaTeX project compiles, but it contains build artifacts, stale figures, and local machine paths.

## Why It Gets Messy

Long-lived LaTeX folders accumulate `.aux`, `.log`, `.bbl`, duplicate final exports, unused figures, and machine-specific paths that fail for collaborators or Overleaf.

## How Paper Scaffold Helps

`audit-project` inventories the folder before cleanup. Focused checks then verify figures, citations, labels, privacy, and Overleaf readiness.

## Commands

```bash
paper-scaffold audit-project --path ./old_latex_project --write-report project_audit.md
paper-scaffold overleaf-check --manuscript-repo ./paper
paper-scaffold unused-artifacts --manuscript-repo ./paper
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
```

## What To Inspect Manually

- Which `main.tex` is canonical.
- Whether final-looking files are duplicates or real sources.
- Whether old figures are still referenced.
- Whether bibliography and supplement files are complete.

## Limitations

Paper Scaffold does not rewrite the LaTeX project. It reports what to clean and validates the result.

## Folder Structure

```text
old_latex_project/
  main.tex
  main.aux
  main.log
  figures/
  references.bib

paper/
  main.tex
  figures/
  metadata/
```
