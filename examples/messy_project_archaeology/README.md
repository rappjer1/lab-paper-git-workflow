# Messy Project Archaeology Example

This synthetic folder demonstrates `paper-scaffold audit-project`. Files use tiny text placeholders even when the extension looks binary, because the audit only needs filenames and categories.

Run:

```bash
paper-scaffold audit-project --path examples/messy_project_archaeology --write-report scratch/messy_project_audit.md
```

Expected findings include final-looking filenames, an Overleaf export folder, LaTeX build artifacts, figure/table candidates, and a raw/generated output placeholder that should not be copied into a manuscript repo.
