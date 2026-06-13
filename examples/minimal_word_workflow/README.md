# Minimal Word Workflow

This example shows the expected steps for moving a Word draft into a manuscript repository.

No Word document is included. Use your own `draft.docx`.

## Steps

```bash
paper-scaffold doctor
paper-scaffold import-word --input draft.docx --output converted.tex
```

If Pandoc is unavailable, export or paste the text manually and split it into `sections/*.tex`.

See:

- `sample_converted.md`
- `expected_steps.md`
