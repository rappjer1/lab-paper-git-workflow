# CLI Reference

Paper Scaffold commands are available through three equivalent invocation modes:

```bash
python scripts/paper-scaffold.py <command>
paper-scaffold <command>
python -m paper_scaffold <command>
```

## Commands

| Command | Purpose | Key arguments | Example | Modifies files |
| --- | --- | --- | --- | --- |
| `init` | Create a manuscript repo scaffold. | `--manuscript-repo`, `--title`, `--slug`, `--non-interactive`, `--overwrite` | `paper-scaffold init --manuscript-repo ./paper --non-interactive` | yes |
| `add-artifact` | Add one artifact manifest entry. | `--manuscript-repo`, `--id`, `--type`, `--source-path`, `--destination`, `--copy-now` | `paper-scaffold add-artifact --manuscript-repo ./paper --id fig1 --type figure --source-path outputs/fig1.pdf --destination figures/fig1.pdf --no-copy-now` | yes |
| `copy-artifacts` | Copy files listed in the artifact manifest. | `--manuscript-repo`, `--allow-directories` | `paper-scaffold copy-artifacts --manuscript-repo ./paper` | yes |
| `validate` | Validate manuscript repo shape and metadata. | `--manuscript-repo`, `--write-report`, `--write-json` | `paper-scaffold validate --manuscript-repo ./paper --write-json ./paper/validation_report.json` | optional report output |
| `doctor` | Check Python, Git, optional tools, and repo shape. | `--manuscript-repo` | `paper-scaffold doctor --manuscript-repo ./paper` | no |
| `quickstart` | Print common workflow commands. | none | `paper-scaffold quickstart` | no |
| `self-test` | Run an installed-use no-network smoke test. | `--output`, `--keep-output` | `paper-scaffold self-test --output scratch/self_test --keep-output` | yes, scratch only |
| `schema list` | List available schema summaries. | none | `paper-scaffold schema list` | no |
| `schema show` | Print a schema summary. | `<schema-name>`, `--json` | `paper-scaffold schema show artifact-manifest` | no |
| `recipes list` | List use-case recipes. | none | `paper-scaffold recipes list` | no |
| `recipes show` | Show one use-case recipe. | `<recipe-id>` | `paper-scaffold recipes show pre-submission-flight-check` | no |
| `demo` | Create a small synthetic demo manuscript. | `--output`, `--overwrite`, `--dry-run` | `paper-scaffold demo --output scratch/demo_manuscript --overwrite` | yes |
| `import-word` | Convert `.docx` with Pandoc when available. | `--input`, `--output`, `--to`, `--dry-run`, `--overwrite` | `paper-scaffold import-word --input draft.docx --output ./paper/converted.tex` | optional output |
| `audit-word-conversion` | Flag common Word/Pandoc conversion issues. | `--input`, `--write-report` | `paper-scaffold audit-word-conversion --input ./paper/converted.tex` | optional report output |
| `discover-artifacts` | Find likely manuscript artifacts in output folders. | `--source`, `--manifest`, `--write`, `--copy`, `--manuscript-repo` | `paper-scaffold discover-artifacts --source ./outputs --manifest ./paper/metadata/artifact_manifest.yaml` | optional manifest/copy output |
| `audit-project` | Read-only audit of a messy project folder. | `--path`, `--write-report` | `paper-scaffold audit-project --path ./messy_project --write-report project_audit.md` | optional report output |
| `release-check` | Run consolidated pre-submission checks. | `--manuscript-repo`, `--write-report` | `paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md` | optional report output |
| `provenance-report` | Generate artifact provenance reports. | `--manuscript-repo`, `--write-md`, `--write-json` | `paper-scaffold provenance-report --manuscript-repo ./paper --write-json ./paper/metadata/provenance_ledger.json` | optional report output |
| `artifact-status` | Print compact provenance counts. | `--manuscript-repo` | `paper-scaffold artifact-status --manuscript-repo ./paper` | no |
| `freeze-artifacts` | Write current manuscript artifact hashes. | `--manuscript-repo`, `--write-lock` | `paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json` | yes |
| `compare-lock` | Compare current artifacts to a lock file. | `--manuscript-repo`, `--lock`, `--write-report`, `--write-json` | `paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json` | optional report output |
| `add-manuscript-ci` | Add dependency-free manuscript CI workflow. | `--manuscript-repo`, `--overwrite` | `paper-scaffold add-manuscript-ci --manuscript-repo ./paper` | yes |
| `package-submission` | Create a clean submission package folder. | `--manuscript-repo`, `--output`, `--overwrite`, `--include-unreferenced` | `paper-scaffold package-submission --manuscript-repo ./paper --output ./submission_package` | yes |
| `reviewer-binder` | Create a response-round checklist and evidence folder. | `--manuscript-repo`, `--round`, `--output`, `--overwrite` | `paper-scaffold reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1` | yes |
| `terminology-check` | Find banned implementation labels. | `--manuscript-repo` | `paper-scaffold terminology-check --manuscript-repo ./paper` | no |
| `git-check` | Print Git status and artifact warnings. | `--manuscript-repo` | `paper-scaffold git-check --manuscript-repo ./paper` | no |
| `github-check` | Check GitHub-readiness. | `--repo` | `paper-scaffold github-check --repo ./paper` | no |
| `overleaf-instructions` | Print GitHub/Overleaf sync guidance. | `--manuscript-repo` | `paper-scaffold overleaf-instructions --manuscript-repo ./paper` | no |
| `overleaf-check` | Check Overleaf-readiness heuristics. | `--manuscript-repo` | `paper-scaffold overleaf-check --manuscript-repo ./paper` | no |
| `privacy-check` | Scan text files for local/private values. | `--path` | `paper-scaffold privacy-check --path ./paper` | no |
| `check-figures` | Check `\includegraphics` paths and figure files. | `--manuscript-repo` | `paper-scaffold check-figures --manuscript-repo ./paper` | no |
| `check-citations` | Compare TeX citation keys to `references.bib`. | `--manuscript-repo` | `paper-scaffold check-citations --manuscript-repo ./paper` | no |
| `check-labels` | Check duplicate and missing LaTeX labels. | `--manuscript-repo` | `paper-scaffold check-labels --manuscript-repo ./paper` | no |
| `stale-artifacts` | Report stale manifest artifacts. | `--manuscript-repo`, `--write-report` | `paper-scaffold stale-artifacts --manuscript-repo ./paper` | optional report output |
| `unused-artifacts` | Report unreferenced figure/table files. | `--manuscript-repo`, `--write-report` | `paper-scaffold unused-artifacts --manuscript-repo ./paper` | optional report output |
| `explain` | Explain a diagnostic code. | `<code>`, `--list` | `paper-scaffold explain E003` | no |
| `make-slack-summary` | Print a launch message from repo metadata. | `--manuscript-repo` | `paper-scaffold make-slack-summary --manuscript-repo ./paper` | no |

## Global Options

```bash
paper-scaffold --help
paper-scaffold --version
python -m paper_scaffold --help
python -m paper_scaffold --version
```
