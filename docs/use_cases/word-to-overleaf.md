# Word Draft To Overleaf

## Scenario

A team drafted in Word and now wants a clean GitHub/Overleaf manuscript repository.

## Why It Gets Messy

Word conversion can produce imperfect LaTeX, missing figure paths, converted comments, table layout issues, and citation placeholders. The converted file is a starting point, not a finished source.

## How Paper Scaffold Helps

It creates a separate manuscript repo, runs the Word conversion command when Pandoc is available, and gives focused checks for conversion artifacts, figures, citations, and local paths.

## Commands

```bash
paper-scaffold doctor
paper-scaffold init --manuscript-repo ./paper
paper-scaffold import-word --input draft.docx --output ./paper/converted.tex
paper-scaffold audit-word-conversion --input ./paper/converted.tex
paper-scaffold validate --manuscript-repo ./paper
```

## What To Inspect Manually

- Equations and special symbols.
- Converted tables and captions.
- Citation keys and bibliography entries.
- Figure placeholders and relative paths.
- Tracked changes, comments, and author notes.

## Limitations

Paper Scaffold does not guarantee a clean Word conversion. It points to common problems so a human can review them.

## Folder Structure

```text
paper/
  converted.tex
  main.tex
  references.bib
  figures/
  tables/
  metadata/
```
