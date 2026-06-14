# Existing LaTeX Cleanup

Goal: take an existing LaTeX folder and check whether it is clean enough for GitHub sync, Overleaf import, or submission packaging.

## Commands

```bash
python scripts/paper-scaffold.py doctor --manuscript-repo ./paper
python scripts/paper-scaffold.py validate --manuscript-repo ./paper --write-report ./paper/validation_report.md --write-json ./paper/validation_report.json
python scripts/paper-scaffold.py check-figures --manuscript-repo ./paper
python scripts/paper-scaffold.py check-citations --manuscript-repo ./paper
python scripts/paper-scaffold.py check-labels --manuscript-repo ./paper
python scripts/paper-scaffold.py unused-artifacts --manuscript-repo ./paper
```

## Cleanup Checklist

- Keep `main.tex`, `references.bib`, sections, selected figures, tables, supplements, and metadata.
- Remove LaTeX build files such as `.aux`, `.log`, `.out`, `.toc`, `.fls`, and `.synctex.gz`.
- Remove scratch folders and full generated output folders.
- Verify that each `\includegraphics` target exists and is case-correct.
- Verify citation keys and labels before syncing.

## Expected Result

You should have a clean folder that can be committed as a manuscript repo, with reports that explain any remaining issues.

## More Detail

- [existing_latex_project.md](../existing_latex_project.md)
- [overleaf_from_github.md](../overleaf_from_github.md)
- [troubleshooting.md](../troubleshooting.md)
