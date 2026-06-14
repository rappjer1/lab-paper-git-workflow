# Dogfood: Python Outputs To Manuscript

Goal: practice finding small generated figures and tables before copying them into a manuscript repository.

Represents: a research project with selected publication artifacts and nearby raw outputs that should not be copied wholesale. All files are synthetic; no real research data are included.

Commands:

```bash
python scripts/paper-scaffold.py discover-artifacts --source examples/dogfood/python_outputs_to_manuscript/input/outputs --manifest scratch/dogfood_python/metadata/artifact_manifest.yaml --suggest-only
python scripts/paper-scaffold.py validate --manuscript-repo scratch/dogfood_python
```

Expected result: Paper Scaffold suggests the small valid synthetic PDF/CSV/TEX files and ignores raw/cache-like files.

Manual review still needed: confirm captions, figure quality, and whether each artifact belongs in the paper.
