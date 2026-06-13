# Overleaf ZIP Rehab

## Scenario

A manuscript has been shared as repeated Overleaf ZIP downloads instead of a Git-backed project.

## Why It Gets Messy

ZIP exports often include source files and generated build artifacts together. Multiple downloads can create duplicate final folders and make it hard to identify the canonical manuscript source.

## How Paper Scaffold Helps

`audit-project` identifies likely source files, build artifacts, figure/table candidates, and suspicious final filenames before a clean repo is created.

## Commands

```bash
paper-scaffold audit-project --path ./overleaf_export --write-report overleaf_export_audit.md
paper-scaffold init --manuscript-repo ./paper
paper-scaffold validate --manuscript-repo ./paper
paper-scaffold overleaf-instructions --manuscript-repo ./paper
```

## What To Inspect Manually

- The true main TeX file.
- Bibliography files and style files.
- Figures that are actually referenced by TeX.
- Build artifacts that should be ignored.

## Limitations

Paper Scaffold does not unpack ZIP files or create GitHub repositories. Unpack first, then audit.

## Folder Structure

```text
overleaf_export/
  main.tex
  main.aux
  main.log
  references.bib
  figures/

paper/
  main.tex
  references.bib
  figures/
```
