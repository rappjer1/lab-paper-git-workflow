# Existing LaTeX Project Cleanup

Use this when you already have a LaTeX or Overleaf project and want to turn it into a clean GitHub/Overleaf manuscript repository.

## Cleanup Steps

1. Make a separate manuscript repository.
2. Copy LaTeX source files, references, figures, tables, and supplement files.
3. Remove build artifacts.
4. Fix relative paths.
5. Organize figures, tables, sections, and supplement files.
6. Add `.gitignore`.
7. Add `metadata/artifact_manifest.yaml`.
8. Add `metadata/terminology_map.yaml` if implementation labels need cleanup.
9. Initialize Git and push to GitHub.

## Remove Build Artifacts

Usually remove:

```text
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.run.xml
*.synctex.gz
*.toc
```

## Fix Relative Paths

Prefer simple paths:

```latex
\includegraphics{figures/example_metric_plot.pdf}
\input{sections/01_introduction}
```

Avoid paths that reach into a research repo or a local machine-specific folder.

## Add Metadata

Create:

```text
metadata/artifact_manifest.yaml
metadata/terminology_map.yaml
metadata/manuscript_config.yaml
```

The artifact manifest records where copied figures and tables came from. It is not a raw data archive.

## Validate

```bash
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md
```

Fix errors before importing into Overleaf.
