# Word To Overleaf Example

Input draft:

```text
draft.docx
```

Convert to LaTeX with Pandoc:

```bash
pandoc draft.docx -o converted.tex
```

Or through the CLI:

```bash
paper-scaffold import-word --input draft.docx --output converted.tex
```

The result is:

```text
converted.tex
```

Manual split:

```text
converted.tex
  -> sections/01_introduction.tex
  -> sections/02_methods.tex
  -> sections/03_results.tex
  -> sections/04_discussion.tex
```

After splitting, compare the compiled PDF against the original Word draft. Check equations, citations, figures, tables, captions, and cross-references manually.
