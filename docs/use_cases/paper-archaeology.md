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
paper-scaffold provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md
```

## What To Inspect Manually

- Which manuscript draft is canonical.
- Whether final-looking outputs are duplicates or actual publication artifacts.
- Whether raw outputs belong in an archive instead of the manuscript repo.
- Whether Overleaf export folders contain source files worth copying.
- Whether copied manuscript figures/tables are listed in the manifest and referenced from TeX.
- Whether source files still exist after the clean manuscript repo is assembled.

## Limitations

The audit does not determine scientific correctness and does not move files. It is a triage report.

The provenance report becomes useful after selected files have been copied into the clean manuscript repo. It checks the copied artifact state; it does not clean the messy source folder.

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
