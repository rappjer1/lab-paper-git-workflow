# Folder Structure

The manuscript repo should be small enough that `git status` is easy to inspect.

## Recommended Manuscript Repo

```text
manuscript-repo/
  README.md
  .gitignore
  main.tex
  references.bib
  sections/
  figures/
  tables/
  supplement/
    supplement.tex
    sections/
    tables/
    figures/
  metadata/
    artifact_manifest.yaml
    terminology_map.yaml
    manuscript_config.yaml
```

## Folder Roles

`sections/` contains main manuscript section files.

`figures/` contains publication-ready main manuscript figures.

`tables/` contains publication-ready main manuscript tables.

`supplement/` contains supplement LaTeX and supplement-only figures/tables.

`metadata/` contains workflow files. These are not raw data. They record where manuscript artifacts came from and which terminology should be cleaned up.

## Before Submission Checklist

- [ ] Main manuscript compiles.
- [ ] Supplement compiles.
- [ ] References resolve.
- [ ] All figures are committed.
- [ ] All tables are committed.
- [ ] No raw data committed.
- [ ] No model outputs, caches, or full evaluation folders committed.
- [ ] No stale code labels in main text.
- [ ] Artifact manifest updated.
- [ ] Terminology map updated.
- [ ] GitHub and Overleaf are synced.
- [ ] PDF exported from Overleaf or local compile.
- [ ] Release tag created.

## Suggested Release Tags

```bash
git tag submission-v1
git push origin submission-v1
```

For revisions:

```bash
git switch -c revision-1
git tag revision-1-submitted
git push origin revision-1 revision-1-submitted
```
