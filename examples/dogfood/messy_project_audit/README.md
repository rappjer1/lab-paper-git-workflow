# Dogfood: Messy Project Audit

Goal: audit an old project folder before deciding what belongs in a clean manuscript repo.

Represents: a folder with manuscript notes, exported LaTeX files, selected figures, duplicate finals, and raw/cache outputs. All files are synthetic; no real research data are included.

Commands:

```bash
python scripts/paper-scaffold.py audit-project --path examples/dogfood/messy_project_audit/project --write-report scratch/messy_project_audit.md
```

Expected result: a triage report identifying likely manuscript files, candidate figures/tables with valid tiny synthetic PDFs, and files that should not move into the manuscript repo.

Manual review still needed: choose canonical files and decide which artifacts are actually publication-ready.
