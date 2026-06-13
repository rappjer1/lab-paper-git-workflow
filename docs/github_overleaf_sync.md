# GitHub And Overleaf Sync

Use GitHub as the canonical manuscript source. Use Overleaf as an editing and compilation frontend connected to that GitHub repository.

## Preferred Workflow

1. Create a manuscript repository separate from the research/code repository.
2. Push manuscript source to GitHub.
3. In Overleaf, create a new project from GitHub.
4. Set `main.tex` as the main document.
5. Pull/sync in Overleaf after local commits.
6. Push from Overleaf only when edits were made there.
7. Avoid editing the same lines simultaneously in Overleaf and locally.

## Create The GitHub Repo

GitHub CLI is optional. If it is installed:

```bash
gh repo create paper-repo --private --source . --remote origin --push
```

If it is not installed, create the repository in the browser, then:

```bash
git remote add origin https://github.com/<owner>/<paper-repo>.git
git branch -M main
git push -u origin main
```

Common typo:

```bash
git remote add orign ...
```

The remote should be `origin`, not `orign`.

## Import Into Overleaf

1. Create a new Overleaf project.
2. Choose Import from GitHub.
3. Select the manuscript repository.
4. Set `main.tex` as the main document.
5. Compile.
6. If there is a supplement, compile `supplement/supplement.tex` separately or temporarily set it as the main document.

## Sync Rules

If editing locally:

```bash
git add .
git commit -m "Update manuscript"
git push
```

Then pull/sync in Overleaf.

If editing in Overleaf:

1. Push Overleaf changes to GitHub.
2. Pull locally before making more edits.

```bash
git pull
```

## Common Errors

Repo not found:

- Confirm the GitHub repository exists.
- Confirm Overleaf has permission to access it.

Private repository permission:

- Reconnect GitHub in Overleaf or check organization permissions.

File too large:

- Remove raw outputs from the manuscript repo.
- Keep large artifacts in the research repo, archive, or Git LFS workflow.

Missing figure path:

- Check the relative path in LaTeX.
- Check the figure exists in the manuscript repo.
- Check filename case.

Wrong main document:

- Set `main.tex` as the main document.
