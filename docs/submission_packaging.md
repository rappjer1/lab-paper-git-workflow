# Submission Packaging

`paper-scaffold package-submission` creates a clean folder containing manuscript source files and selected manuscript artifacts:

```bash
paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package
```

The command is filesystem-only. It does not compile LaTeX, upload to a journal, call Overleaf, require GitHub CLI, or publish anything.

## What Gets Included

By default, the package includes:

- manuscript source files with `.tex`, `.bib`, `.bst`, `.cls`, and `.sty` suffixes
- manifest artifacts that exist in the manuscript repo and are referenced from TeX
- untracked manuscript artifacts only when they are referenced from TeX
- `README_SUBMISSION.md`
- `submission_package_manifest.json` with copied files, excluded artifacts, and W042/W043 warning metadata

The package skips:

- `.git`, `.github`, cache folders, `scratch`, `build`, and `dist`
- LaTeX build artifacts such as `.aux`, `.log`, `.bbl`, `.fls`, and `.synctex.gz`
- unreferenced manifest artifacts unless `--include-unreferenced` is passed

## Include Unreferenced Artifacts

Some journals ask for files that are not directly included from TeX. Review those cases manually, then opt in:

```bash
paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package --include-unreferenced
```

## Overwrite Protection

Existing package folders are not replaced unless requested:

```bash
paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package --overwrite
```

## Recommended Preflight

```bash
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
paper-scaffold provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package
```

Review the output folder against journal requirements before upload.
