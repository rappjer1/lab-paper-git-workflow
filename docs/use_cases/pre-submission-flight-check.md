# Pre-Submission Flight Check

## Scenario

The manuscript is nearly ready to sync, share, submit, or archive.

## Why It Gets Messy

Final edits often introduce missing figure paths, stale artifacts, unused files, citation drift, duplicate labels, and local paths. These can pass unnoticed until a collaborator or Overleaf tries to build the project.

## How Paper Scaffold Helps

`release-check` runs the focused manuscript checks together and writes one report that can be reviewed before a release-like commit. v0.8 adds optional artifact lock comparison, dependency-free manuscript CI, and clean submission package generation.

## Commands

```bash
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
paper-scaffold validate --manuscript-repo ./paper --write-json ./paper/validation_report.json
paper-scaffold overleaf-check --manuscript-repo ./paper
paper-scaffold provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
paper-scaffold artifact-status --manuscript-repo ./paper
paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md
paper-scaffold add-manuscript-ci --manuscript-repo ./paper
paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package
```

## What To Inspect Manually

- Any warnings that remain after automated checks.
- Figure rendering and final layout in Overleaf or local LaTeX.
- Journal-specific requirements.
- Whether the Git working tree contains only intentional changes.
- Whether each figure/table is listed in the manifest and referenced from TeX.
- Whether any source/manuscript artifact hashes differ.
- Whether `compare-lock` reports changed or missing locked artifacts.
- Whether the submission package excludes scratch, build, and stale unreferenced files.

## Limitations

Release checks and generated CI are heuristics. They do not compile LaTeX, submit to a journal, or replace final human review.

Provenance reports are also heuristic. They are a manuscript artifact bill of materials, not a full reproducibility proof.

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
