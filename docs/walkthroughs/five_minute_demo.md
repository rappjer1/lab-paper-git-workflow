# Five-Minute Demo

Goal: create and validate a small synthetic manuscript repo without installing Paper Scaffold or using network access.

## Commands

```bash
python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/validation_report.md --write-json scratch/demo_manuscript/validation_report.json
python scripts/paper-scaffold.py overleaf-check --manuscript-repo scratch/demo_manuscript
```

## Expected Files

```text
scratch/demo_manuscript/
  main.tex
  references.bib
  figures/
  tables/
  metadata/
    artifact_manifest.yaml
```

## What To Inspect

- `main.tex` references the included example figure.
- `references.bib` contains the cited example entry.
- `metadata/artifact_manifest.yaml` records copied artifact provenance.
- Validation should report zero errors for the demo.

## Next Steps

- Read [Common Paths](../common_paths.md) if you are matching this to a real project.
- Read [One-Page Reference](../one_page_reference.md) for command names.
- Delete `scratch/demo_manuscript` when you are done experimenting.
