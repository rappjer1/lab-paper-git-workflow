# Public Launch Copy

Paper Scaffold is a small open-source workflow/tool for moving research projects into clean GitHub/Overleaf manuscript repositories.

It is aimed at researchers who have:

- a Word draft,
- Python-generated figures/tables,
- or an existing LaTeX folder that needs cleanup.

The main idea is to keep the research/code repo separate from the manuscript repo, copy only paper-ready artifacts, track provenance in a manifest, and validate the manuscript repo before syncing to Overleaf.

Repository:

```text
https://github.com/rappjer1/lab-paper-git-workflow
```

Useful commands:

```bash
paper-scaffold doctor
paper-scaffold quickstart
paper-scaffold demo
paper-scaffold discover-artifacts
paper-scaffold validate
```

What it does:

- Scaffolds clean manuscript repositories.
- Helps convert Word drafts with Pandoc when available.
- Discovers likely publication artifacts from output folders.
- Tracks figure/table provenance in `metadata/artifact_manifest.yaml`.
- Validates before GitHub/Overleaf sync.

What it does not do:

- It does not write the science.
- It does not create GitHub or Overleaf projects automatically.
- It does not upload anything to Overleaf.
- It does not require Overleaf, Pandoc, LaTeX, or GitHub CLI.

Feedback welcome, especially from anyone who has fought with Word-to-Overleaf conversion, missing figure paths, or accidental commits of large result folders.
