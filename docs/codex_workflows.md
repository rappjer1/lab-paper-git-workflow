# Codex Workflows

Codex is useful for paper repo maintenance when the task is scoped tightly. Treat it like a collaborator who needs clear boundaries.

## Safety Rules

- Start each task with the repo path and branch.
- State whether code, manuscript, data, or results can be modified.
- Explicitly forbid rerunning expensive jobs unless intended.
- Ask Codex to report changed files.
- Ask Codex to run validation.
- Ask Codex not to create ZIPs unless requested.
- Use separate chats and branches for manuscript edits, API/data audits, and model training.

## Prompt 1: Initialize A Manuscript Repo

```text
You are operating in <path-to-clean-manuscript-repo> on branch <branch>.
Initialize this as a clean manuscript repo using lab-paper-git-workflow.
The research repo is <path-to-research-repo>.
Use the template, include a supplement, and do not copy raw data, model outputs, caches, or full evaluation directories.
Run validation and report changed files.
```

## Prompt 2: Add Figures From Research Outputs

```text
You are operating in <path-to-manuscript-repo> on branch <branch>.
Add these publication figures from <path-to-research-repo>: <list paths>.
Copy only the listed files.
Update metadata/artifact_manifest.yaml with source paths, generating scripts, input summaries, dates, caption hints, and status.
Do not copy result directories, caches, raw data, or model outputs.
Run paper-scaffold validate and report changed files.
```

## Prompt 3: Make Terminology Cleanup Pass

```text
You are operating in <path-to-manuscript-repo> on branch <branch>.
Use metadata/terminology_map.yaml to find implementation labels in .tex, .bib, and .md files.
Replace banned labels in main manuscript text with publication labels.
Keep code labels only where allowed in supplement provenance or metadata.
Run paper-scaffold terminology-check and paper-scaffold validate.
Report changed files.
```

## Prompt 4: Create Supplement From Diagnostic Figures

```text
You are operating in <path-to-manuscript-repo> on branch <branch>.
Create or update the supplement using only the diagnostic figures listed below.
Copy selected figures into supplement/figures/.
Update metadata/artifact_manifest.yaml.
Do not copy the full diagnostics directory.
Do not rerun analysis.
Run validation and report changed files.
```

## Prompt 5: Validate Before Overleaf Sync

```text
You are operating in <path-to-manuscript-repo> on branch <branch>.
Do not edit files unless validation requires a small metadata or ignore-file fix.
Run paper-scaffold validate, paper-scaffold terminology-check, and paper-scaffold git-check.
Report blockers before Overleaf sync.
```

## Prompt 6: Prepare Revision Branch

```text
You are operating in <path-to-manuscript-repo>.
Create or use branch revision-<number>.
Do not create ZIP files.
Do not modify the research repo.
Prepare the manuscript repo for revision work by checking status, remotes, tags, and validation.
Report current branch and changed files.
```

## Prompt 7: Update Manuscript After New Results

```text
You are operating in <path-to-manuscript-repo> on branch <branch>.
The research repo is <path-to-research-repo>.
Only update manuscript text, selected figures/tables, and metadata needed for these new results: <summary>.
Do not rerun expensive jobs unless explicitly approved.
Do not copy raw data, caches, model outputs, or full result directories.
Run validation and report changed files.
```

## Prompt 8: Create A Release Tag

```text
You are operating in <path-to-manuscript-repo> on branch <branch>.
Validate the manuscript repo before tagging.
If validation passes, create tag <tag-name> for this submission/revision state.
Do not create ZIP files.
Report the tag, commit SHA, and validation result.
```
