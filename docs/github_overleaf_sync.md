# GitHub And Overleaf Sync

Use GitHub as the canonical manuscript source. Use Overleaf as the editor and compiler connected to that GitHub repo.

## Preferred Workflow

1. Create a private GitHub manuscript repo.
2. Push manuscript source.
3. In Overleaf, create a new project from GitHub.
4. Use GitHub as canonical source.
5. Pull/sync in Overleaf after local commits.
6. Push from Overleaf only when edits were made there.
7. Avoid editing the same lines simultaneously in Overleaf and locally.

## Create The GitHub Repo

GitHub CLI is optional. If `gh` is installed:

```bash
gh repo create my-project-paper --private --source . --remote origin --push
```

If `gh` is not installed, create the private repo in the browser, then add the remote:

```bash
git remote add origin https://github.com/<owner>/<repo>.git
git branch -M main
git push -u origin main
```

Common typo:

```bash
git remote add orign ...
```

The remote should be `origin`, not `orign`.

## Git Bash Paths

Git Bash uses forward slashes:

```bash
cd /r/Code/manuscripts/my_project_paper
git status
```

## PowerShell Paths

PowerShell can use backslashes:

```powershell
Set-Location R:\Code\manuscripts\my_project_paper
git status
```

Quote paths with spaces:

```powershell
Set-Location "R:\Code\manuscripts\my project paper"
```

## Create Overleaf From GitHub

In Overleaf:

1. Create a new project.
2. Choose the GitHub import option.
3. Select the private manuscript repo.
4. Set the main document, usually `main.tex`.
5. Compile once.
6. Sync from GitHub after local commits.

Existing Overleaf projects usually should not be attached to existing GitHub repos. Create a new Overleaf project from GitHub when possible and keep old Overleaf projects as archives.

## Avoid Sync Conflicts

Do not edit the same paragraph locally and in Overleaf at the same time.

Clean pattern:

1. Pull latest from GitHub locally.
2. Edit locally.
3. Commit and push.
4. Pull/sync in Overleaf.

Or:

1. Edit in Overleaf.
2. Push from Overleaf.
3. Pull locally before making more edits.

## What Not To Sync

Do not sync:

- Full analysis repos.
- Raw data.
- Model outputs.
- Prediction caches.
- Large evaluation directories.
- ZIP snapshots.
