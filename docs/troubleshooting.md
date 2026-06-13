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

## Overleaf Does Not Show New Files

Push local commits to GitHub, then pull/sync in Overleaf.

```bash
git status
git push
```

In Overleaf, use the GitHub sync menu.

## Validation Finds A Forbidden File

Remove the file from the manuscript repo and keep it in the research repo.

If it was staged:

```bash
git restore --staged <path>
```

Then delete the copied file from the manuscript repo.

## Validation Finds A Banned Term

Open `metadata/terminology_map.yaml`, check the suggested publication label, and update the manuscript text.

If the term is legitimate in a supplement provenance table, keep it in the supplement and document that context in `allowed_contexts`.

## Figures Are Stale

Update the source figure in the research repo, then copy only the selected figure into the manuscript repo.

```bash
paper-scaffold copy-artifacts --manuscript-repo <manuscript-repo>
paper-scaffold validate --manuscript-repo <manuscript-repo>
```

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
