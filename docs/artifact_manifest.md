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

## Schema

The manifest schema is intentionally small:

- top-level `artifacts` is required and must be a list;
- each artifact must be a mapping;
- each artifact requires `id`, `type`, `manuscript_path`, and `source_path`;
- unknown fields are warnings, not fatal errors;
- duplicate IDs and unsupported types are errors.

Schema validation is dependency-free and runs as part of:

```bash
paper-scaffold validate --manuscript-repo <manuscript-repo>
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

## Valid Example

```yaml
artifacts:
  - id: main_result
    type: figure
    manuscript_path: figures/main_result.pdf
    source_repo: ./research-project
    source_path: outputs/main_result.pdf
    generated_by: scripts/make_figures.py
    input_data: outputs/summary.csv
    last_updated: 2026-06-13
    caption_hint: Main result figure.
    status: final
```

## Invalid Example

```yaml
artifacts:
  - id: main_result
    type: plot
    manuscript_path: figures/main_result.pdf
```

This produces diagnostics similar to:

```text
E004 [ERROR] Manifest artifact missing (metadata/artifact_manifest.yaml): artifact[1] missing required field: source_path
E004 [ERROR] Manifest artifact missing (metadata/artifact_manifest.yaml): artifact[1] unsupported type: plot
```

## Copying Artifacts

Use:

```bash
paper-scaffold copy-artifacts --manuscript-repo <manuscript-repo>
```

The tool copies files listed in the manifest. It does not copy directories unless `--allow-directories` is used. Directory copying should be rare.

## Stale And Unused Artifacts

Check whether source outputs changed after copying:

```bash
paper-scaffold stale-artifacts --manuscript-repo <manuscript-repo>
```

Check whether copied manuscript artifacts are not referenced by TeX:

```bash
paper-scaffold unused-artifacts --manuscript-repo <manuscript-repo>
```

## What The Manifest Is Not

It is not a raw data archive.

It is not a replacement for the research repo.

It is not a place to paste full result tables unless those tables are part of the submitted manuscript or supplement.
