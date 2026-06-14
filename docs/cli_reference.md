# CLI Reference

Paper Scaffold commands are available through three invocation modes:

```bash
python scripts/paper-scaffold.py <command>
paper-scaffold <command>
python -m paper_scaffold <command>
```

Command names and documented flags are part of the public contract described in [contract.md](contract.md). Dev audit scripts such as `scripts/dev/clean_install_audit.py` remain maintainer tools, not user CLI commands.

## Global Options

```bash
paper-scaffold --help
paper-scaffold --version
python -m paper_scaffold --help
python -m paper_scaffold --version
```

## Commands

### `init`

- Purpose: create a manuscript repository scaffold.
- Modifies files: yes.
- Important flags: `--manuscript-repo`, `--title`, `--slug`, `--non-interactive`, `--overwrite`.
- Example: `paper-scaffold init --manuscript-repo ./paper --non-interactive`.
- Exit behavior: returns nonzero for invalid paths or overwrite protection.

### `add-artifact`

- Purpose: add one figure/table entry to the artifact manifest and optionally copy it.
- Modifies files: yes.
- Important flags: `--manuscript-repo`, `--id`, `--type`, `--source-path`, `--destination`, `--copy-now`, `--no-copy-now`.
- Example: `paper-scaffold add-artifact --manuscript-repo ./paper --id fig1 --type figure --source-path outputs/fig1.pdf --destination figures/fig1.pdf`.
- Exit behavior: returns nonzero for missing required paths or invalid manifest writes.

### `validate`

- Purpose: validate manuscript repository shape, metadata, forbidden files, and terminology.
- Modifies files: only with report flags.
- Important flags: `--manuscript-repo`, `--write-report`, `--write-json`.
- Example: `paper-scaffold validate --manuscript-repo ./paper --write-json ./paper/validation_report.json`.
- Exit behavior: returns nonzero when validation errors are present.

### `copy-artifacts`

- Purpose: copy files listed in `metadata/artifact_manifest.yaml`.
- Modifies files: yes.
- Important flags: `--manuscript-repo`, `--allow-directories`.
- Example: `paper-scaffold copy-artifacts --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when sources are missing or unsafe directory copies are blocked.

### `terminology-check`

- Purpose: find banned implementation labels in manuscript text.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold terminology-check --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when banned terms are found.

### `git-check`

- Purpose: print Git branch, remote, status, and manuscript artifact warnings.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold git-check --manuscript-repo ./paper`.
- Exit behavior: returns nonzero for blocking Git readiness issues.

### `overleaf-instructions`

- Purpose: print project-specific GitHub/Overleaf sync guidance.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold overleaf-instructions --manuscript-repo ./paper`.
- Exit behavior: returns nonzero for invalid manuscript paths.

### `doctor`

- Purpose: check Python, Git, optional tools, and manuscript repo shape.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold doctor --manuscript-repo ./paper`.
- Exit behavior: optional missing tools are warnings; blocking repo issues return nonzero.

### `import-word`

- Purpose: convert a `.docx` draft with Pandoc when available.
- Modifies files: yes, unless `--dry-run`.
- Important flags: `--input`, `--output`, `--to`, `--dry-run`, `--overwrite`.
- Example: `paper-scaffold import-word --input draft.docx --output ./paper/converted.tex`.
- Exit behavior: returns nonzero when Pandoc is unavailable, input is missing, or overwrite is blocked.

### `discover-artifacts`

- Purpose: find likely manuscript artifacts in output folders.
- Modifies files: only with `--write` or `--copy`.
- Important flags: `--source`, `--manifest`, `--write`, `--copy`, `--manuscript-repo`.
- Example: `paper-scaffold discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml`.
- Exit behavior: returns nonzero for missing source folders or failed writes.

### `make-slack-summary`

- Purpose: print a launch message from manuscript metadata.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold make-slack-summary --manuscript-repo ./paper`.
- Exit behavior: returns nonzero for invalid manuscript paths.

### `quickstart`

- Purpose: print common Paper Scaffold workflow commands.
- Modifies files: no.
- Important flags: none.
- Example: `paper-scaffold quickstart`.
- Exit behavior: returns zero.

### `self-test`

- Purpose: run a no-network installed-use smoke workflow.
- Modifies files: yes, under scratch or the requested output folder.
- Important flags: `--output`, `--keep-output`.
- Example: `paper-scaffold self-test --output scratch/self_test --keep-output`.
- Exit behavior: returns nonzero if any self-test step fails.

### `schema`

- Purpose: list and show metadata and generated-report schema summaries.
- Modifies files: no.
- Important flags: subcommands `list` and `show`; `show` accepts `<schema-name>` and `--json`.
- Example: `paper-scaffold schema show artifact-manifest`.
- Exit behavior: returns nonzero for unknown schema names.

### `recipes`

- Purpose: list and show use-case recipes.
- Modifies files: no.
- Important flags: subcommands `list` and `show`; `show` accepts `<recipe-id>`.
- Example: `paper-scaffold recipes show pre-submission-flight-check`.
- Exit behavior: returns nonzero for unknown recipe ids.

### `demo`

- Purpose: create a small synthetic demo manuscript repository.
- Modifies files: yes, unless `--dry-run`.
- Important flags: `--output`, `--overwrite`, `--dry-run`.
- Example: `paper-scaffold demo --output scratch/demo_manuscript --overwrite`.
- Exit behavior: returns nonzero when output exists without `--overwrite`.

### `audit-project`

- Purpose: read-only audit of a messy project folder.
- Modifies files: only with `--write-report`.
- Important flags: `--path`, `--write-report`.
- Example: `paper-scaffold audit-project --path ./messy_project --write-report project_audit.md`.
- Exit behavior: returns nonzero for invalid input paths.

### `release-check`

- Purpose: run consolidated pre-submission manuscript checks.
- Modifies files: only with `--write-report`.
- Important flags: `--manuscript-repo`, `--write-report`.
- Example: `paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md`.
- Exit behavior: returns nonzero when blocking release findings are present.

### `provenance-report`

- Purpose: generate manuscript artifact provenance reports.
- Modifies files: only with `--write-md` or `--write-json`.
- Important flags: `--manuscript-repo`, `--write-md`, `--write-json`.
- Example: `paper-scaffold provenance-report --manuscript-repo ./paper --write-json ./paper/metadata/provenance_ledger.json`.
- Exit behavior: returns nonzero when provenance errors are present.

### `artifact-status`

- Purpose: print compact artifact provenance status counts.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold artifact-status --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when provenance errors are present.

### `freeze-artifacts`

- Purpose: write current manuscript artifact hashes.
- Modifies files: yes.
- Important flags: `--manuscript-repo`, `--write-lock`.
- Example: `paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json`.
- Exit behavior: returns nonzero for missing manuscript artifacts or failed lock writes.

### `add-manuscript-ci`

- Purpose: add a dependency-free manuscript CI workflow.
- Modifies files: yes.
- Important flags: `--manuscript-repo`, `--overwrite`.
- Example: `paper-scaffold add-manuscript-ci --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when the workflow exists and `--overwrite` is not passed.

### `package-submission`

- Purpose: create a clean submission package folder.
- Modifies files: yes.
- Important flags: `--manuscript-repo`, `--output`, `--overwrite`, `--include-unreferenced`.
- Example: `paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package`.
- Exit behavior: returns nonzero when output exists without `--overwrite`.

### `compare-lock`

- Purpose: compare current manuscript artifacts to a lock file.
- Modifies files: only with report flags.
- Important flags: `--manuscript-repo`, `--lock`, `--write-report`, `--write-json`.
- Example: `paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json`.
- Exit behavior: returns nonzero for missing lock files or missing locked artifacts.

### `reviewer-binder`

- Purpose: create a response-round checklist and evidence folder.
- Modifies files: yes.
- Important flags: `--manuscript-repo`, `--round`, `--output`, `--overwrite`.
- Example: `paper-scaffold reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1`.
- Exit behavior: returns nonzero when output exists without `--overwrite`.

### `explain`

- Purpose: explain a diagnostic code.
- Modifies files: no.
- Important flags: `<code>`, `--list`.
- Example: `paper-scaffold explain E003`.
- Exit behavior: returns nonzero for unknown codes.

### `overleaf-check`

- Purpose: check whether a manuscript repo is likely Overleaf-ready.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold overleaf-check --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when blocking Overleaf-readiness errors are present.

### `github-check`

- Purpose: check GitHub-readiness for a repository.
- Modifies files: no.
- Important flags: `--repo`.
- Example: `paper-scaffold github-check --repo ./paper`.
- Exit behavior: returns nonzero when blocking GitHub-readiness errors are present.

### `privacy-check`

- Purpose: scan text files for local paths, credentials, or private markers.
- Modifies files: no.
- Important flags: `--path`.
- Example: `paper-scaffold privacy-check --path ./paper`.
- Exit behavior: returns nonzero when privacy errors are found.

### `check-figures`

- Purpose: check `\includegraphics` paths and figure files.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold check-figures --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when referenced figures are missing.

### `check-citations`

- Purpose: compare TeX citation keys to `references.bib`.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold check-citations --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when cited keys are missing from the bibliography.

### `check-labels`

- Purpose: check duplicate and missing LaTeX labels.
- Modifies files: no.
- Important flags: `--manuscript-repo`.
- Example: `paper-scaffold check-labels --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when duplicate or missing label errors are found.

### `audit-word-conversion`

- Purpose: flag common Word/Pandoc conversion issues.
- Modifies files: only with `--write-report`.
- Important flags: `--input`, `--write-report`.
- Example: `paper-scaffold audit-word-conversion --input ./paper/converted.tex`.
- Exit behavior: returns nonzero for missing input files.

### `stale-artifacts`

- Purpose: report manifest artifacts whose sources changed after copying.
- Modifies files: only with `--write-report`.
- Important flags: `--manuscript-repo`, `--write-report`.
- Example: `paper-scaffold stale-artifacts --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when stale artifact errors are present.

### `unused-artifacts`

- Purpose: report figure/table files that are not referenced by TeX source.
- Modifies files: only with `--write-report`.
- Important flags: `--manuscript-repo`, `--write-report`.
- Example: `paper-scaffold unused-artifacts --manuscript-repo ./paper`.
- Exit behavior: returns nonzero when unused artifact errors are present.
