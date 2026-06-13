# Pre-Submission Flight Check

## Scenario

The manuscript is nearly ready to sync, share, submit, or archive.

## Why It Gets Messy

Final edits often introduce missing figure paths, stale artifacts, unused files, citation drift, duplicate labels, and local paths. These can pass unnoticed until a collaborator or Overleaf tries to build the project.

## How Paper Scaffold Helps

`release-check` runs the focused manuscript checks together and writes one report that can be reviewed before a release-like commit.

## Commands

```bash
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
paper-scaffold validate --manuscript-repo ./paper --write-json ./paper/validation_report.json
paper-scaffold overleaf-check --manuscript-repo ./paper
```

## What To Inspect Manually

- Any warnings that remain after automated checks.
- Figure rendering and final layout in Overleaf or local LaTeX.
- Journal-specific requirements.
- Whether the Git working tree contains only intentional changes.

## Limitations

Release checks are heuristics. They do not compile LaTeX, submit to a journal, or replace final human review.

## Folder Structure

```text
paper/
  main.tex
  references.bib
  figures/
  tables/
  supplement/
  metadata/
```
