# Multi-Paper Project Split

## Scenario

One research project produces outputs for more than one manuscript.

## Why It Gets Messy

Shared code and outputs can tempt teams to keep every manuscript and artifact in one repository. That creates unclear histories, accidental cross-paper artifacts, and Overleaf sync risks.

## How Paper Scaffold Helps

Each manuscript gets its own clean repo and artifact manifest. The shared research project remains the source of generated outputs, and each paper copies only what it needs.

## Commands

```bash
paper-scaffold init --manuscript-repo ./paper_a
paper-scaffold init --manuscript-repo ./paper_b
paper-scaffold discover-artifacts --source ./outputs/paper_a --manifest ./paper_a/metadata/artifact_manifest.yaml
paper-scaffold discover-artifacts --source ./outputs/paper_b --manifest ./paper_b/metadata/artifact_manifest.yaml
```

## What To Inspect Manually

- Whether each paper has distinct artifact IDs.
- Whether shared outputs are copied to the correct manuscript repo.
- Whether terminology maps differ intentionally.
- Whether each repo can be synced to Overleaf independently.

## Limitations

Paper Scaffold does not manage shared scientific dependencies. It only helps keep manuscript repositories separate and provenance explicit.

## Folder Structure

```text
research_project/
  outputs/
    paper_a/
    paper_b/

paper_a/
  metadata/artifact_manifest.yaml

paper_b/
  metadata/artifact_manifest.yaml
```
