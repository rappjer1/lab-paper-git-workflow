# Troubleshooting

## `python` Is Not Found

Use whichever Python launcher is available on the machine. From a source checkout, the wrapper is:

```bash
python scripts/paper-scaffold.py --help
```

After installation, use:

```bash
paper-scaffold --help
```

## `origin` Is Missing

Check remotes:

```bash
git remote -v
```

Add the GitHub repo:

```bash
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

If you typed `orign`, remove it:

```bash
git remote remove orign
```

Then add `origin`.

If the message came from `github-check`, the manuscript repo can still be valid locally. Add `origin` before GitHub/Overleaf sync.

## Wrong Remote Name: `orign`

Check remote names:

```bash
git remote -v
```

If a typo exists, remove it and add the correct remote:

```bash
git remote remove orign
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

## Private GitHub Repo Is Invisible In Overleaf

Confirm that:

- The manuscript repo is on GitHub, not only local Git.
- The GitHub account connected to Overleaf has access to the repo.
- The repo is selected during Overleaf import.
- Browser pop-up or authorization prompts were not blocked.

If needed, disconnect and reconnect the GitHub integration in Overleaf, then retry import.

## Overleaf Uses The Wrong Main Document

Set the main document in Overleaf to the configured main TeX file, usually:

```text
main.tex
```

If the project uses a different file, update `metadata/manuscript_config.yaml`:

```yaml
project:
  main_tex: manuscript.tex
```

## Overleaf Does Not Show New Files

Push local commits to GitHub, then pull/sync in Overleaf.

```bash
git status
git push
```

In Overleaf, use the GitHub sync menu.

## Figure Path Is Broken

Run:

```bash
paper-scaffold check-figures --manuscript-repo <manuscript-repo>
paper-scaffold explain E003
```

Common fixes:

- Use paths relative to the manuscript repo, such as `figures/result.pdf`.
- Avoid absolute paths from a local machine.
- Confirm the figure is committed and pushed to GitHub.
- Keep figure filenames simple: lowercase words, numbers, underscores, and hyphens.

## Validation Finds A Forbidden File

Remove the file from the manuscript repo and keep it in the research repo.

If it was staged:

```bash
git restore --staged <path>
```

Then delete the copied file from the manuscript repo.

Large raw output folders should remain in the research repo, data archive, or storage system. Manuscript repos should contain only selected paper-ready figures, tables, source text, bibliography, and provenance metadata.

## Large File Warning

Run:

```bash
paper-scaffold explain E013
git ls-files -s
```

If the large file is raw data, a model checkpoint, a prediction cache, or a broad output archive, remove it from the manuscript repo. If it is a required publication figure, document why it belongs and consider a smaller/vector version.

## Validation Finds A Banned Term

Open `metadata/terminology_map.yaml`, check the suggested publication label, and update the manuscript text.

If the term is legitimate in a supplement provenance table, keep it in the supplement and document that context in `allowed_contexts`.

## Figures Are Stale

Update the source figure in the research repo, then copy only the selected figure into the manuscript repo.

```bash
paper-scaffold copy-artifacts --manuscript-repo <manuscript-repo>
paper-scaffold validate --manuscript-repo <manuscript-repo>
```

## Citation Or Label Errors

Run:

```bash
paper-scaffold check-citations --manuscript-repo <manuscript-repo>
paper-scaffold check-labels --manuscript-repo <manuscript-repo>
```

For `E012`, add the missing BibTeX entry or fix the citation key. For `E010`, rename duplicate labels. For `E011`, add the missing label or update the reference.

## Pandoc Is Missing

`import-word` requires Pandoc. Other Paper Scaffold workflows do not.

Install Pandoc only if you need automated Word conversion, or manually move Word content into LaTeX using the guide in [word_to_overleaf.md](word_to_overleaf.md).

## Word Equations Or Tables Look Wrong

Word conversion is a starting point. Run:

```bash
paper-scaffold audit-word-conversion --input <converted-file>
```

Then manually inspect:

- equations;
- citations;
- figures and captions;
- tables and long tables;
- section hierarchy;
- tracked changes or comments;
- cross-references.

## Git Shows LaTeX Build Files

These files should usually be ignored:

```text
*.aux
*.bbl
*.blg
*.log
*.out
*.synctex.gz
```

Check `.gitignore`, unstage build outputs, and commit only source files.
