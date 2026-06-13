# Minimal Python Artifacts

This example generates small publication-style artifacts from synthetic data:

- `outputs/example_metric_plot.pdf`
- `outputs/example_metric_plot.png`
- `outputs/example_summary_table.csv`
- `outputs/example_table.tex`

Generate them with:

```bash
python make_example_figure.py
```

Discover them with:

```bash
paper-scaffold discover-artifacts --source outputs --manifest artifact_manifest.yaml
```
