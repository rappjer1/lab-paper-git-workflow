# Overleaf From GitHub

The goal is a clean manuscript GitHub repo that Overleaf can import.

## Exact Workflow

1. Create a private GitHub manuscript repo.
2. Push manuscript source.
3. In Overleaf: New Project -> Import from GitHub.
4. Select the manuscript repo.
5. Set `main.tex` as the main document.
6. Compile.
7. If there is a supplement, either compile `supplement/supplement.tex` separately or set it as main temporarily.

## Local Edit Sync Rule

If editing locally:

```bash
git status
git add .
git commit -m "Update manuscript"
git push
```

Then pull/sync in Overleaf.

## Overleaf Edit Sync Rule

If editing in Overleaf:

1. Push Overleaf changes back to GitHub.
2. Pull locally before editing.

```bash
git pull
```

Avoid editing the same lines locally and in Overleaf at the same time.

## Common Errors

Repo not found:

- Confirm the GitHub repo exists.
- Confirm it is the manuscript repo, not the research repo.

`origin` misspelled as `orign`:

```bash
git remote -v
git remote remove orign
git remote add origin https://github.com/<owner>/<repo>.git
```

Private repo permission:

- Make sure Overleaf has access to the GitHub account or organization.

File too large:

- Remove raw data/model/cache outputs from the manuscript repo.
- Keep large outputs in the research repo or archive.

Missing figure path:

- Check the path in LaTeX.
- Check the figure exists in the manuscript repo.
- Check filename case.

Wrong main document:

- Set `main.tex` as the main document.
- For supplement-only compile checks, temporarily set `supplement/supplement.tex`.
