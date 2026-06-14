# Which Workflow Should I Use?

Use this guide when you know what material you have but not which Paper Scaffold path to start with.

Examples are synthetic and intentionally small. See [example_integrity.md](example_integrity.md) for how example artifacts are checked.

## Decision Table

| Situation | Start here | Commands | Output |
| --- | --- | --- | --- |
| I want to try the tool safely. | Local demo | `self-test`, `demo`, `validate` | Synthetic manuscript repo under `scratch/` |
| I have a Word draft. | Word to Overleaf guide | `init`, `import-word`, `audit-word-conversion`, `validate` | Manuscript scaffold plus converted draft text |
| I have Python outputs. | Python artifacts guide | `discover-artifacts`, `add-artifact`, `copy-artifacts`, `validate` | Artifact manifest plus selected figures/tables |
| I already have LaTeX or an Overleaf export. | Existing LaTeX cleanup guide | `validate`, `check-figures`, `check-citations`, `check-labels` | Readiness report and focused fixes |
| I am preparing submission files. | Submission packaging guide | `release-check`, `freeze-artifacts`, `package-submission` | Clean submission folder and optional lock |
| I am responding to reviewers. | Reviewer binder guide | `provenance-report`, `reviewer-binder`, `compare-lock` | Response-round checklist and evidence folder |
| I inherited a messy project folder. | Project archaeology recipe | `audit-project`, `discover-artifacts` | Triage report and candidate artifact list |
| I need to check before Overleaf sync. | GitHub/Overleaf sync guide | `overleaf-check`, `github-check`, `privacy-check` | Sync-readiness diagnostics |

## Questions

### Do You Have A Word Draft?

Relevant docs:

- [word_to_overleaf.md](word_to_overleaf.md)
- [cli_reference.md](cli_reference.md)

Commands:

```bash
python scripts/paper-scaffold.py init --manuscript-repo <repo> --non-interactive
python scripts/paper-scaffold.py import-word --input <draft.docx> --output <repo>/converted.tex
python scripts/paper-scaffold.py audit-word-conversion --input <repo>/converted.tex
```

Reads: a Word draft and the manuscript repo. Writes: converted text only when `--output` is used. Do not assume conversion is final; equations, citations, tables, figures, and tracked changes still need manual review.

### Do You Have Python Outputs?

Relevant docs:

- [python_outputs_to_overleaf.md](python_outputs_to_overleaf.md)
- [artifact_manifest.md](artifact_manifest.md)

Commands:

```bash
python scripts/paper-scaffold.py discover-artifacts --source <output-folder> --manifest <repo>/metadata/artifact_manifest.yaml --suggest-only
python scripts/paper-scaffold.py discover-artifacts --source <output-folder> --manifest <repo>/metadata/artifact_manifest.yaml --write --copy --manuscript-repo <repo>
python scripts/paper-scaffold.py validate --manuscript-repo <repo>
```

Reads: output folders and an optional manifest. Writes: manifest entries and copied artifacts only when `--write` or `--copy` is used. Do not copy whole output directories, caches, checkpoints, or raw data.

### Do You Already Have A LaTeX Or Overleaf Project?

Relevant docs:

- [existing_latex_project.md](existing_latex_project.md)
- [overleaf_from_github.md](overleaf_from_github.md)

Commands:

```bash
python scripts/paper-scaffold.py validate --manuscript-repo <repo>
python scripts/paper-scaffold.py check-figures --manuscript-repo <repo>
python scripts/paper-scaffold.py check-citations --manuscript-repo <repo>
python scripts/paper-scaffold.py check-labels --manuscript-repo <repo>
```

Reads: manuscript source files and bibliography. Writes: nothing unless you request reports. Do not commit LaTeX build files or downloaded ZIP clutter.

### Are You Preparing A Submission Package?

Use this path when you need a submission package for manual journal upload review.

Relevant docs:

- [submission_packaging.md](submission_packaging.md)
- [artifact_locks.md](artifact_locks.md)

Commands:

```bash
python scripts/paper-scaffold.py release-check --manuscript-repo <repo>
python scripts/paper-scaffold.py freeze-artifacts --manuscript-repo <repo> --write-lock <repo>/metadata/artifact_lock.json
python scripts/paper-scaffold.py package-submission --manuscript-repo <repo> --output <submission-folder>
```

Reads: manuscript repo and artifact manifest. Writes: lock files and package folders when requested. Do not upload the package without journal-specific manual review.

### Are You Responding To Reviewers?

Relevant docs:

- [reviewer_response_binder.md](reviewer_response_binder.md)
- [provenance_ledger.md](provenance_ledger.md)

Commands:

```bash
python scripts/paper-scaffold.py provenance-report --manuscript-repo <repo> --write-md <repo>/provenance_report.md
python scripts/paper-scaffold.py reviewer-binder --manuscript-repo <repo> --round 1 --output <response-folder>
python scripts/paper-scaffold.py compare-lock --manuscript-repo <repo> --lock <repo>/metadata/artifact_lock.json
```

Reads: manuscript repo, manifest, and optional lock. Writes: response folder and reports. Do not put confidential reviewer text in a public repository.

### Are You Auditing An Old Or Messy Project Folder?

Relevant docs:

- [use_cases/paper-archaeology.md](use_cases/paper-archaeology.md)
- [use_cases/overleaf-zip-rehab.md](use_cases/overleaf-zip-rehab.md)

Commands:

```bash
python scripts/paper-scaffold.py audit-project --path <project-folder> --write-report project_audit.md
python scripts/paper-scaffold.py discover-artifacts --source <project-folder> --manifest <repo>/metadata/artifact_manifest.yaml --suggest-only
```

Reads: project files. Writes: a report only when requested. Do not treat audit candidates as final publication artifacts without review.

### Are You Validating Before Overleaf Sync?

Relevant docs:

- [github_overleaf_sync.md](github_overleaf_sync.md)
- [troubleshooting.md](troubleshooting.md)

Commands:

```bash
python scripts/paper-scaffold.py overleaf-check --manuscript-repo <repo>
python scripts/paper-scaffold.py github-check --repo <repo>
python scripts/paper-scaffold.py privacy-check --path <repo>
```

Reads: manuscript repo and Git metadata. Writes: nothing. Do not connect Overleaf to a full research repository.
