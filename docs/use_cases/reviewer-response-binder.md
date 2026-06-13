# Reviewer Response Binder

## Scenario

A revision round requires new analyses, figures, tables, and notes to support reviewer responses.

## Why It Gets Messy

Response-only outputs can drift from the manuscript or get copied into the wrong folder. Teams also need a simple way to see which artifact supports which reviewer point.

## How Paper Scaffold Helps

The manuscript repo remains clean while a small response manifest and checklist document response artifacts. Release checks then catch stale, unused, or private files before resubmission.

## Commands

```bash
paper-scaffold validate --manuscript-repo ./paper
paper-scaffold stale-artifacts --manuscript-repo ./paper
paper-scaffold provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md
paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
```

## What To Inspect Manually

- Whether reviewer-only artifacts should be in the manuscript repo.
- Whether response figures match final submitted figures.
- Whether confidential review text is excluded from public repositories.
- Whether each response item has a clear evidence artifact.
- Whether response figures and tables are current relative to declared source outputs.
- Whether the artifact lock captures the exact submitted response version.

## Limitations

Paper Scaffold does not manage journal response formatting. It only helps keep supporting artifacts organized and checked.

Provenance reports do not prove the response analysis is correct. They show whether the manuscript artifacts are present, traceable to declared sources, and referenced from TeX.

## Folder Structure

```text
paper/
  main.tex
  figures/
  metadata/artifact_manifest.yaml
  reviewer_response/
    response_checklist.md
    response_artifact_manifest.yaml
```
