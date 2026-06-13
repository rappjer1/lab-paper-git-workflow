# Artifact Manifest

The artifact manifest records copied publication figures and tables. It is the link between the research repo and the manuscript repo.

It lives at:

```text
metadata/artifact_manifest.yaml
```

## Supported Types

- `figure`
- `table`
- `data_summary`
- `supplement_figure`
- `supplement_table`

## Template

```yaml
artifacts:
  - id: workflow_schematic
    type: figure
    manuscript_path: figures/workflow_schematic.pdf
    source_repo: ./research-project
    source_path: experiments/figures/workflow_schematic.pdf
    generated_by: scripts/make_workflow.py
    input_data: experiments/results/summary.csv
    last_updated: 2026-06-10
    caption_hint: Evaluation-only workflow schematic.
    status: final
```

## Field Meanings

`id` is a stable short identifier. Use lowercase words separated by underscores.

`type` is one of the supported artifact types.

`manuscript_path` is where the copied file lives inside the manuscript repo.

`source_repo` is the research repo that produced the artifact.

`source_path` is the source file path, usually relative to `source_repo`.

`generated_by` is the script or workflow that created the artifact.

`input_data` is the key input or summary file used to create the artifact.

`last_updated` is the date the manuscript copy was updated.

`caption_hint` is a reminder for the writer. Final captions live in LaTeX.

`status` is usually `draft`, `final`, or `needs_update`.

## Copying Artifacts

Use:

```bash
paper-scaffold copy-artifacts --manuscript-repo <manuscript-repo>
```

The tool copies files listed in the manifest. It does not copy directories unless `--allow-directories` is used. Directory copying should be rare.

## What The Manifest Is Not

It is not a raw data archive.

It is not a replacement for the research repo.

It is not a place to paste full result tables unless those tables are part of the submitted manuscript or supplement.
