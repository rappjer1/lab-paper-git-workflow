# Python Outputs To Overleaf

Python should generate publication artifacts in the research repo. The manuscript repo should receive only selected final figures and tables, with provenance recorded in `metadata/artifact_manifest.yaml`.

## Save Figures With Stable Filenames

Use stable names:

```text
figures/model_comparison.pdf
figures/site_map.png
tables/model_comparison.tex
```

Avoid timestamps and random hashes in final manuscript filenames.

## Prefer The Right File Type

- Use vector PDF for plots.
- Use PNG for rasters, photos, and image-based diagnostics.
- Use CSV for provenance or review tables.
- Use generated LaTeX tables for manuscript inclusion.

## Keep Generation Scripts In The Research Repo

Figure and table scripts belong in the research repo. The manuscript repo should not become a second analysis repo.

## Copy Only Selected Publication Artifacts

Do not copy whole output folders. Copy the selected figure/table files that appear in the manuscript or supplement.

## Use The Artifact Manifest

Each copied file should have an entry in:

```text
metadata/artifact_manifest.yaml
```

## Example Manifest Entries

```yaml
artifacts:
  - id: model_comparison
    type: figure
    manuscript_path: figures/model_comparison.pdf
    source_repo: R:/Code/my_project
    source_path: outputs/final_figures/model_comparison.pdf
    generated_by: scripts/make_figures.py
    input_data: outputs/summary_metrics.csv
    last_updated: 2026-06-13
    caption_hint: Model comparison across evaluation groups.
    status: final
  - id: map_overview
    type: figure
    manuscript_path: figures/map_overview.png
    source_repo: R:/Code/my_project
    source_path: outputs/final_figures/map_overview.png
    generated_by: scripts/make_maps.py
    input_data: data/processed/site_summary.csv
    last_updated: 2026-06-13
    caption_hint: Overview map for study sites.
    status: final
  - id: summary_metrics_csv
    type: data_summary
    manuscript_path: tables/summary_metrics.csv
    source_repo: R:/Code/my_project
    source_path: outputs/final_tables/summary_metrics.csv
    generated_by: scripts/make_tables.py
    input_data: outputs/summary_metrics_raw.csv
    last_updated: 2026-06-13
    caption_hint: CSV summary used to generate manuscript table.
    status: final
  - id: summary_metrics_table
    type: table
    manuscript_path: tables/summary_metrics.tex
    source_repo: R:/Code/my_project
    source_path: outputs/final_tables/summary_metrics.tex
    generated_by: scripts/make_tables.py
    input_data: outputs/final_tables/summary_metrics.csv
    last_updated: 2026-06-13
    caption_hint: Rounded publication table.
    status: final
```

## Recommended Python Figure Export

```python
fig.savefig("figures/my_figure.pdf", bbox_inches="tight")
fig.savefig("figures/my_figure.png", dpi=300, bbox_inches="tight")
```

Use explicit filenames and commit only the publication copy in the manuscript repo.

## Table Export

Use CSV for provenance:

```python
summary.to_csv("tables/model_summary.csv", index=False)
```

Use LaTeX for manuscript inclusion:

```python
rounded = summary.round(2)
rounded.to_latex("tables/model_summary.tex", index=False)
```

Round values for publication. Keep high-precision raw outputs in the research repo.

## Discover Candidates

```bash
paper-scaffold discover-artifacts --source R:/Code/my_project/outputs/final --manifest metadata/artifact_manifest.yaml
```

This is dry-run by default. Use `--write` to append suggestions and `--copy` to copy files.

## Warnings

- Do not screenshot plots.
- Do not commit raw model outputs.
- Do not commit `.npz`, `.pt`, `.pkl`, `.nc`, `full_eval`, `prediction_cache`, or external API caches.
- Do not manually rename figures without updating the manifest.
- Do not copy whole output directories because one figure is needed.
