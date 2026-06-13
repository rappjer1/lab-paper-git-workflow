# Use-Case Recipes

These recipes show how to use Paper Scaffold in common manuscript cleanup and handoff situations. They are intentionally generic and small so they can be reused across lab projects.

Start with:

```bash
paper-scaffold recipes list
paper-scaffold recipes show paper-archaeology
```

## Recipes

- [Word draft to Overleaf](word-to-overleaf.md)
- [Python artifact handoff](python-artifact-handoff.md)
- [Existing LaTeX cleanup](existing-latex-cleanup.md)
- [Overleaf ZIP rehab](overleaf-zip-rehab.md)
- [Paper archaeology](paper-archaeology.md)
- [Reviewer response binder](reviewer-response-binder.md)
- [Undergraduate artifact harvest](undergraduate-artifact-harvest.md)
- [Pre-submission flight check](pre-submission-flight-check.md)
- [Multi-paper project split](multi-paper-project-split.md)

## General Pattern

```text
research_project/
  scripts/
  outputs/
  caches/

paper/
  main.tex
  references.bib
  figures/
  tables/
  metadata/
    artifact_manifest.yaml
```

The research project remains the place for code, raw outputs, model checkpoints, caches, and broad result directories. The manuscript repo receives only text, references, selected figures/tables, and provenance metadata.
