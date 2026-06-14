# Dogfood: Existing LaTeX Cleanup

Goal: validate a small existing manuscript folder before GitHub/Overleaf sync.

Represents: a minimal LaTeX project with source text, bibliography, and one figure reference. All files are synthetic; no real research data are included.

Commands:

```bash
python scripts/paper-scaffold.py validate --manuscript-repo examples/dogfood/existing_latex_cleanup/project
python scripts/paper-scaffold.py check-figures --manuscript-repo examples/dogfood/existing_latex_cleanup/project
```

Expected result: checks run without needing LaTeX or Overleaf. The referenced PDF is a valid tiny synthetic file.

Manual review still needed: inspect final figure quality and journal-specific formatting.
