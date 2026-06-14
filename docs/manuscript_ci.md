# Manuscript CI

`paper-scaffold add-manuscript-ci` writes a small GitHub Actions workflow into a manuscript repository:

```bash
paper-scaffold add-manuscript-ci --manuscript-repo ./paper
```

The generated file is:

```text
paper/.github/workflows/manuscript-checks.yml
```

## What It Checks

The workflow uses only Python standard library code available on the GitHub runner. It does not install Paper Scaffold and does not require LaTeX, Pandoc, GitHub CLI, Overleaf, network calls beyond the normal Actions runner setup, or PyPI publishing.

It checks for:

- `main.tex`
- optional warning for missing `references.bib`
- forbidden raw/model/cache output suffixes such as `.npz`, `.pt`, `.pkl`, `.nc`, `.zarr`, `.parquet`, and `.h5`
- LaTeX build artifacts such as `.aux`, `.log`, `.bbl`, and `.synctex.gz`
- files larger than 25 MB

## Overwrite Protection

If the workflow already exists, the command exits with `E030` unless `--overwrite` is passed:

```bash
paper-scaffold add-manuscript-ci --manuscript-repo ./paper --overwrite
```

## Recommended Use

Run local checks first:

```bash
paper-scaffold validate --manuscript-repo ./paper
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
paper-scaffold add-manuscript-ci --manuscript-repo ./paper
```

Commit the workflow only when the manuscript repo should run repository hygiene checks on pushes and pull requests.

## Limitations

The generated CI is advisory. It does not compile the manuscript, contact Overleaf, create a submission package, or replace journal-specific checks.
