# Python Outputs To Manuscript

Goal: review selected output files from a computation folder and copy only paper-ready artifacts into a separate manuscript repo.

## Starting Shape

```text
outputs/
  final_figure.pdf
  final_table.csv
  scratch_run_cache.tmp
paper/
  main.tex
  metadata/
```

## Commands

```bash
python scripts/paper-scaffold.py discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml --suggest-only
python scripts/paper-scaffold.py discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper
python scripts/paper-scaffold.py validate --manuscript-repo ./paper
python scripts/paper-scaffold.py provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
```

## What To Review Before Copying

- Prefer publication formats such as PDF for figures and CSV or TeX for small tables.
- Exclude caches, raw exports, checkpoints, and full output trees.
- Use stable names that describe the manuscript role, not the execution environment.
- Add captions and source notes after reviewing the generated manifest.

## Expected Result

The manuscript repo contains only reviewed files in `figures/`, `tables/`, or `supplement/`, and each copied file has a manifest entry.

## More Detail

- [python_outputs_to_overleaf.md](../python_outputs_to_overleaf.md)
- [artifact_manifest.md](../artifact_manifest.md)
- [provenance_ledger.md](../provenance_ledger.md)
- [Glossary](../glossary.md)
