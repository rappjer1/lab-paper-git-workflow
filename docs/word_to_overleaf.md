# Word To Overleaf

Word conversion is useful, but it is not magic. Treat the converted LaTeX as a starting point that needs review.

## When This Works Well

- The Word draft uses heading styles.
- Text is mostly paragraphs, headings, and simple lists.
- Tables are simple.
- Figures can be copied separately from final Python or design outputs.
- References already exist in Zotero, BibTeX, or another citation manager.

## When This Will Need Manual Cleanup

- The document uses tracked changes, comments, text boxes, floating objects, or manually positioned content.
- Equations are complex.
- Captions and cross-references were typed manually.
- Citations are embedded in a format Pandoc is not configured to understand.
- Tables use merged cells, nested tables, or heavy formatting.

## Recommended Word Preparation

Before conversion:

- Accept or reject tracked changes.
- Remove comments or export them separately.
- Use Word heading styles for section structure.
- Use real captions if possible.
- Put references in Zotero/BibTeX if possible.
- Avoid manually positioned text boxes.
- Save a clean copy of the draft before conversion.

## Conversion Options

Preferred:

```bash
pandoc draft.docx -o converted.tex
```

Fallback:

```bash
pandoc draft.docx -t markdown -o converted.md
```

Manual:

Paste text into the section templates under `sections/`, then rebuild figures, captions, citations, and cross-references in LaTeX.

## What Pandoc Can Convert

Pandoc can usually convert:

- Headings.
- Paragraphs.
- Basic lists.
- Basic tables.
- Basic equations sometimes.
- Citations only if configured.

## What Needs Manual Review

Always review:

- Figures.
- Captions.
- Cross-references.
- Equations.
- Tables.
- Citations.
- Tracked changes.

## CLI Command

```bash
paper-scaffold import-word --input draft.docx --output converted.tex
```

Markdown output:

```bash
paper-scaffold import-word --input draft.docx --output converted.md --to markdown
```

Dry run:

```bash
paper-scaffold import-word --input draft.docx --output converted.tex --dry-run
```

If Pandoc is missing, the command prints installation/manual workflow instructions and exits cleanly.

## Split Converted Text Into Sections

After conversion:

1. Open `converted.tex`.
2. Find `\section{...}` headings.
3. Move introduction text into `sections/01_introduction.tex`.
4. Move methods text into `sections/02_methods.tex`.
5. Move results text into `sections/03_results.tex`.
6. Move discussion text into `sections/04_discussion.tex`.
7. Keep `main.tex` as the file that imports the sections.

Do not spend time preserving Word formatting that does not belong in the final paper.

## Compare Against The Original Word File

Use a practical review:

- Check section order.
- Check paragraph completeness.
- Check equations against the Word original.
- Check figure callouts and captions.
- Check table content.
- Check references and citation keys.
- Have one person read the converted PDF against the Word draft.

## Common Failure Modes

- Tracked changes appear as confusing text.
- Figures are missing or embedded in poor formats.
- Captions become plain paragraphs.
- Cross-references become static text.
- Equations need manual LaTeX cleanup.
- Citations are not converted because citation metadata was not configured.
- Tables compile but look wrong.
