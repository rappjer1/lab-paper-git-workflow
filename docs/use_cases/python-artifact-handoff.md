# Python Artifact Handoff

## Scenario

An analysis folder contains many figures, tables, logs, caches, and raw outputs. Only a few files belong in the manuscript.

## Why It Gets Messy

Output folders often mix final-looking figures with intermediate plots, metrics dumps, model checkpoints, and compressed result files. Copying the whole folder into a manuscript repo creates provenance and publication risks.

## How Paper Scaffold Helps

`discover-artifacts` suggests figure and table candidates, `copy-artifacts` copies selected manifest entries, and `stale-artifacts` catches source files that changed after copying.

## Commands

```bash
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper
paper-scaffold stale-artifacts --manuscript-repo ./paper
paper-scaffold validate --manuscript-repo ./paper
```

## What To Inspect Manually

- Whether each candidate is a final publication artifact.
- Whether captions, units, and panel labels match the manuscript.
- Whether the manifest source path and generator script are meaningful.
- Whether a PDF/vector version should be preferred over a PNG.

## Limitations

Discovery is heuristic. It suggests candidates but does not decide what belongs in the paper.

## Folder Structure

```text
research_project/
  outputs/final/
    figure_1.pdf
    table_1.csv
    run_cache.npz

paper/
  figures/
  tables/
  metadata/artifact_manifest.yaml
```
