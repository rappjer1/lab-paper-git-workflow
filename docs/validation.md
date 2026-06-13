# Validation

`paper-scaffold validate` checks whether a manuscript repository is clean enough to sync through GitHub/Overleaf.

```bash
paper-scaffold validate --manuscript-repo ./paper
```

Write a report:

```bash
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md
```

Write Markdown and JSON reports:

```bash
paper-scaffold validate --manuscript-repo ./paper --write-report ./paper/validation_report.md --write-json ./paper/validation_report.json
```

The Markdown report includes diagnostic counts, grouped findings, Git status context, top next actions, and a reference to `docs/error_codes.md`.

The JSON report has this stable shape:

```json
{
  "tool": "Paper Scaffold",
  "version": "0.5.0",
  "timestamp": "...",
  "path": "./paper",
  "summary": {
    "errors": 0,
    "warnings": 0,
    "info": 0
  },
  "diagnostics": []
}
```

For a focused check, use:

```bash
paper-scaffold overleaf-check --manuscript-repo ./paper
paper-scaffold github-check --repo ./paper
paper-scaffold privacy-check --path ./paper
paper-scaffold check-figures --manuscript-repo ./paper
paper-scaffold check-citations --manuscript-repo ./paper
paper-scaffold check-labels --manuscript-repo ./paper
paper-scaffold stale-artifacts --manuscript-repo ./paper
paper-scaffold unused-artifacts --manuscript-repo ./paper
```

Explain any code:

```bash
paper-scaffold explain E003
```

Reference: [error_codes.md](error_codes.md)

## Manuscript Shape

Checks for:

- `main.tex`
- `references.bib`
- `figures/`
- supplement file if configured

## Forbidden Files

Flags common raw/model/cache outputs:

- `.npz`
- `.pt`
- `.pth`
- `.pkl`
- `.pickle`
- `.nc`
- `.zip`
- `data/external`
- `full_eval`
- `prediction_cache`
- `raw_api_cache`

## Large Files

Warns when files exceed the configured size threshold. The default is 25 MB.

Large publication figures may be valid, but validation asks you to inspect them before committing.

## Artifact Manifest

Checks that `metadata/artifact_manifest.yaml` parses, follows the schema, and that every listed `manuscript_path` exists.

Use `stale-artifacts` when regenerating outputs in the research repo. It compares source and manuscript copies by modification time and hash. It reports warnings only and does not copy files by default.

Use `unused-artifacts` before submission cleanup. It scans figures and tables in manuscript artifact folders and reports files not referenced from TeX source.

## Terminology Map

Searches `.tex`, `.bib`, and `.md` files for terms banned by `metadata/terminology_map.yaml`.

The terminology map schema is also checked when the file exists.

## Git Status

Reports:

- current branch;
- remote `origin`;
- number of status entries;
- staged LaTeX build files.

Missing `origin` is reported by `github-check` and `doctor`. It does not block `validate`, because many users validate a local manuscript repo before creating the GitHub repository.

## Word Conversion Audit

After converting a Word draft with Pandoc, run:

```bash
paper-scaffold audit-word-conversion --input ./paper/converted.tex --write-report ./paper/word_conversion_audit.md
```

This is a heuristic pass for common cleanup needs: equations, table environments, raw HTML, markdown image placeholders, citation syntax, and tracked-change remnants.

## Optional Tools

Optional tools are reported by `paper-scaffold doctor`, not required by validation:

- Pandoc for Word conversion.
- `latexmk` or `pdflatex` for local LaTeX builds.
- GitHub CLI for optional repository creation workflows.
