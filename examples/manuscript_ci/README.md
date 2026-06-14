# Manuscript CI Example

Use the generated workflow when a manuscript repository should run lightweight hygiene checks on pushes and pull requests.

```bash
paper-scaffold demo --output scratch/demo_manuscript --overwrite
paper-scaffold add-manuscript-ci --manuscript-repo scratch/demo_manuscript --overwrite
```

The workflow is written to:

```text
scratch/demo_manuscript/.github/workflows/manuscript-checks.yml
```

It checks for manuscript shape, forbidden raw outputs, LaTeX build artifacts, and large files without requiring LaTeX or Pandoc.
