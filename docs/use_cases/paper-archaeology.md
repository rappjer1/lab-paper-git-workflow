# Paper Archaeology

## Scenario

An old or inherited project folder contains drafts, outputs, caches, exported LaTeX, and repeated final-looking files.

## Why It Gets Messy

When analysis and writing happen in the same folder, manuscript-ready artifacts sit next to raw outputs and caches. It becomes unclear what should be copied to a clean manuscript repository.

## How Paper Scaffold Helps

`audit-project` scans read-only and reports likely manuscript files, figure/table candidates, raw/generated outputs, build artifacts, candidate Overleaf exports, large files, and suspicious final filenames.

## Commands

```bash
paper-scaffold audit-project --path ./messy_project --write-report project_audit.md
paper-scaffold init --manuscript-repo ./paper
paper-scaffold discover-artifacts --source ./messy_project/outputs --manifest ./paper/metadata/artifact_manifest.yaml
paper-scaffold validate --manuscript-repo ./paper
```

## What To Inspect Manually

- Which manuscript draft is canonical.
- Whether final-looking outputs are duplicates or actual publication artifacts.
- Whether raw outputs belong in an archive instead of the manuscript repo.
- Whether Overleaf export folders contain source files worth copying.

## Limitations

The audit does not determine scientific correctness and does not move files. It is a triage report.

## Folder Structure

```text
messy_project/
  final_FINAL_notes.md
  outputs/
    fig1_final.png
    fig1_final2.png
    model_cache.npz
  overleaf_export/
    main.tex
    main.aux
    main.log

paper/
  main.tex
  figures/
  metadata/
```
