# Quick Start

Paper Scaffold helps you create a clean manuscript repository from research outputs.

Use it from a checkout:

```bash
python scripts/paper-scaffold.py doctor
python scripts/paper-scaffold.py quickstart
```

Or after editable install:

```bash
paper-scaffold doctor
paper-scaffold quickstart
```

## Word + Python To Overleaf In 20 Minutes

1. Create or clone a manuscript repo.
2. Run doctor.
3. Convert a Word draft or start from the LaTeX template.
4. Discover Python artifacts.
5. Copy selected artifacts.
6. Validate.
7. Commit and push.
8. Import the GitHub repo into Overleaf if you use Overleaf.

```bash
paper-scaffold doctor
paper-scaffold init --manuscript-repo ./paper
paper-scaffold import-word --input draft.docx --output ./paper/converted.tex
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml
paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md
```

If Pandoc is not installed, skip `import-word` and paste/split text manually using [docs/word_to_overleaf.md](docs/word_to_overleaf.md).

## Run The Demo

```bash
paper-scaffold demo --output scratch/demo_manuscript --overwrite
paper-scaffold validate --manuscript-repo scratch/demo_manuscript
```

From a checkout:

```bash
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
```

## Manual Fallback Without The CLI

1. Create a separate manuscript repository.
2. Add `main.tex`, `references.bib`, `sections/`, `figures/`, `tables/`, `supplement/`, and `metadata/`.
3. Copy only selected publication figures and tables.
4. Create `metadata/artifact_manifest.yaml`.
5. Create `metadata/terminology_map.yaml` if implementation labels need cleanup.
6. Add a `.gitignore` for LaTeX build files and raw/model/cache outputs.
7. Run `git status` and inspect every staged file.
8. Commit and push to GitHub.
9. Import the GitHub repo into Overleaf if desired.

## Next Reading

- [docs/getting_started.md](docs/getting_started.md)
- [docs/word_to_overleaf.md](docs/word_to_overleaf.md)
- [docs/python_outputs_to_overleaf.md](docs/python_outputs_to_overleaf.md)
- [docs/existing_latex_project.md](docs/existing_latex_project.md)
- [docs/github_overleaf_sync.md](docs/github_overleaf_sync.md)
