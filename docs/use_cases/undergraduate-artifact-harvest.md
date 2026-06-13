# Undergraduate Artifact Harvest

## Scenario

A junior contributor has generated candidate figures and tables, and a maintainer needs a safe review workflow.

## Why It Gets Messy

Student output folders can contain plots, notebooks, raw data extracts, logs, and caches. A clear review step prevents accidental bulk-copying into the manuscript repo.

## How Paper Scaffold Helps

`discover-artifacts` lists candidates without copying by default. `audit-project` flags raw outputs and final-looking duplicates. The maintainer decides what to copy through the manifest.

## Commands

```bash
paper-scaffold discover-artifacts --source ./student_outputs --manifest ./paper/metadata/artifact_manifest.yaml
paper-scaffold audit-project --path ./student_outputs --write-report student_outputs_audit.md
paper-scaffold validate --manuscript-repo ./paper
```

## What To Inspect Manually

- Whether candidate artifacts are final enough for a manuscript.
- Whether axes, labels, units, and captions are publication-ready.
- Whether any raw data or caches are present.
- Whether contributor filenames should be normalized before copying.

## Limitations

Paper Scaffold does not replace mentoring or scientific review. It gives a safer first pass for artifact triage.

## Folder Structure

```text
student_outputs/
  candidate_figures/
  tables/
  scratch/

paper/
  figures/
  tables/
  metadata/artifact_manifest.yaml
```
