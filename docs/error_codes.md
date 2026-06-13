# Diagnostic Error Codes

Paper Scaffold diagnostics use stable codes so command output, reports, and docs can point to the same fix.

Use:

```bash
paper-scaffold explain E003
paper-scaffold explain --list
```

## Errors

| Code | Title | Common cause | Typical fix |
| --- | --- | --- | --- |
| E001 | `main.tex` missing | The manuscript repo does not contain the configured main TeX file. | Create `main.tex` or update `project.main_tex` in `metadata/manuscript_config.yaml`. |
| E002 | `references.bib` missing | The bibliography file is absent. | Add `references.bib` or update the manuscript to use the correct file. |
| E003 | Missing figure path | `\includegraphics{...}` points to a file that is not in the manuscript repo. | Copy the figure into the repo or fix the relative path. |
| E004 | Manifest artifact missing | `metadata/artifact_manifest.yaml` has invalid entries or points to missing manuscript files. | Run `copy-artifacts` or update the manifest. |
| E005 | Forbidden raw output found | Raw data, model outputs, caches, or checkpoint-like files were copied into the manuscript repo. | Remove the file and keep only paper-ready artifacts. |
| E006 | Banned implementation label found | A term from `metadata/terminology_map.yaml` appears in manuscript text. | Replace it with the publication-facing label. |
| E007 | Git remote origin missing | The repo is not connected to a GitHub remote named `origin`. | Add the intended GitHub manuscript repository as `origin`. |
| E008 | Absolute local path found | A source file contains a machine-specific path. | Replace it with a relative path inside the manuscript repo. |
| E009 | Supplement configured but missing | Config says a supplement exists, but the supplement file is absent. | Create `supplement/supplement.tex` or set `has_supplement: false`. |
| E010 | Duplicate LaTeX label | The same `\label{...}` key appears more than once. | Rename labels so each key is unique. |
| E011 | Missing LaTeX label target | A `\ref`, `\cref`, `\autoref`, or `\eqref` points to an undefined label. | Add the missing label or fix the reference key. |
| E012 | Citation key missing from bibliography | A citation in TeX is not present in `references.bib`. | Add the BibTeX entry or fix the citation key. |
| E013 | File larger than configured maximum | A file exceeds the manuscript repo size threshold. | Remove raw outputs or explicitly review whether the file belongs in the repo. |
| E014 | Forbidden directory found | A raw/cache/output directory was copied into the manuscript repo. | Move the directory back to the research repo or archive. |
| E015 | Artifact source missing | `copy-artifacts` cannot find a manifest source path. | Regenerate the source artifact or correct `source_repo` and `source_path`. |

## Warnings

| Code | Title | Common cause | Typical fix |
| --- | --- | --- | --- |
| W001 | Pandoc missing | Word conversion tools are not installed. | Install Pandoc only if using `import-word`. |
| W002 | LaTeX compiler missing | `latexmk` or `pdflatex` is not installed locally. | Install LaTeX only if local compilation is needed. |
| W003 | GitHub CLI missing | `gh` is not installed. | Use the GitHub website or install GitHub CLI if desired. |
| W004 | Working tree has uncommitted changes | Git status is not clean or upstream is not configured. | Review `git status --short` and commit intentionally. |
| W005 | Figure present but not referenced | A figure file exists but is not used by `\includegraphics`. | Remove stale figures or reference them intentionally. |
| W006 | Raster figure concern | A raster figure may be low resolution, have spaces in the name, or lack a vector alternative. | Prefer PDF for vector plots and high-resolution PNG/JPG for raster images. |
| W007 | Table may be too wide | A generated table may not fit manuscript layout. | Inspect the compiled manuscript and adjust table formatting. |
| W008 | Word conversion needs cleanup | Converted Word/Pandoc text has patterns that often need manual review. | Audit equations, citations, tables, figures, captions, and tracked changes. |
| W009 | Overleaf sync may fail with Git LFS or submodules | The repo uses Git LFS pointers or submodules. | Avoid LFS/submodules for simple manuscript repos or confirm Overleaf support. |
| W010 | No artifact manifest found | The manuscript repo lacks `metadata/artifact_manifest.yaml`. | Add a manifest when figures/tables are copied from a research repo. |
| W011 | No terminology map found | The repo lacks `metadata/terminology_map.yaml`. | Add one if implementation labels need cleanup. |
| W012 | No supplement found | No supplement file was detected. | Ignore if the manuscript has no supplement. |
| W013 | No LICENSE found | A public repository has no license. | Add a license before public release. |
| W014 | No README found | The repository lacks a README. | Add a README explaining the manuscript repo. |
| W015 | Uncited bibliography entry | A BibTeX entry is not cited by TeX source. | Remove stale references or cite them intentionally. |
| W016 | Figure or table may be missing a label | A figure/table environment lacks `\label{...}`. | Add labels where cross-references are needed. |
| W017 | Possible private or secret text | The privacy scan found a local path, email, token-like text, or private marker. | Redact the value before publishing. |

## Info

| Code | Title | Meaning |
| --- | --- | --- |
| I001 | Running inside Paper Scaffold tool repo | The current repo is the tool repo, not a manuscript repo. |
| I002 | Optional tool missing but workflow can continue | A missing optional dependency does not block the current command. |
| I003 | Manuscript repo shape detected | Expected manuscript markers were found. |
| I004 | Git remote origin configured | A Git remote named `origin` exists. |
| I005 | Artifact manifest valid | The manifest parsed and referenced files exist. |
| I006 | No forbidden files found | No raw/model/cache output patterns were detected. |
