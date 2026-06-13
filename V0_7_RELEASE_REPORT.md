# v0.7.0 Release Report

## Scope

v0.7.0 is the provenance-ledger release for Paper Scaffold. It adds a generated artifact bill of materials for manuscript figures and tables while keeping `metadata/artifact_manifest.yaml` as the user-authored source of truth.

The release is read/report/freeze only. It does not copy, move, delete, publish, upload, or require network access, Pandoc, LaTeX, GitHub CLI, or Overleaf.

## Commands Added

- `paper-scaffold provenance-report --manuscript-repo <path>`
- `paper-scaffold provenance-report --manuscript-repo <path> --write-md provenance_report.md --write-json provenance_ledger.json`
- `paper-scaffold artifact-status --manuscript-repo <path>`
- `paper-scaffold freeze-artifacts --manuscript-repo <path> --write-lock metadata/artifact_lock.json`

## Ledger Schema

Generated provenance ledger entries include:

- `artifact_id`
- `artifact_type`
- `manuscript_path`
- `source_path`
- `source_repo`
- `source_git_commit`
- `source_exists`
- `manuscript_exists`
- `source_sha256`
- `manuscript_sha256`
- `source_mtime`
- `manuscript_mtime`
- `copied_at`
- `generated_by`
- `used_in_tex_files`
- `used_in_main_or_supplement`
- `status`
- `notes`

Supported statuses:

- `current`
- `stale`
- `missing_source`
- `missing_manuscript`
- `untracked`
- `unknown`

The generated JSON ledger has a lightweight schema validator in `src/paper_scaffold/schemas.py`.

## Docs Added Or Updated

- Added `docs/provenance_ledger.md`.
- Updated `README.md`.
- Updated `docs/artifact_manifest.md`.
- Updated `docs/error_codes.md`.
- Updated use-case docs for paper archaeology, reviewer response binders, and pre-submission flight checks.
- Updated `ROADMAP.md`.
- Updated `CHANGELOG.md`.

## Diagnostics Added

- `E020`: manifest artifact missing manuscript file.
- `E021`: referenced artifact missing from disk.
- `W030`: manifest artifact source missing.
- `W031`: manuscript artifact stale relative to source.
- `W032`: manuscript artifact present but not in manifest.
- `W033`: artifact in manifest but not referenced.
- `I030`: provenance ledger generated.
- `I031`: artifact lock written.

## Validation Results

Passed:

```powershell
<python> scripts\paper-scaffold.py demo --output scratch\demo_manuscript --overwrite
<python> scripts\paper-scaffold.py provenance-report --manuscript-repo scratch\demo_manuscript --write-md scratch\demo_manuscript\provenance_report.md --write-json scratch\demo_manuscript\provenance_ledger.json
<python> scripts\paper-scaffold.py artifact-status --manuscript-repo scratch\demo_manuscript
<python> scripts\paper-scaffold.py freeze-artifacts --manuscript-repo scratch\demo_manuscript --write-lock scratch\demo_manuscript\metadata\artifact_lock.json
<python> scripts\paper-scaffold.py release-check --manuscript-repo scratch\demo_manuscript --write-report scratch\demo_manuscript\release_check.md
```

Demo provenance result:

- 3 total manifest artifacts
- 3 current
- 0 stale
- 0 missing source
- 0 missing manuscript artifact
- 0 untracked manuscript artifacts
- 0 unreferenced artifacts
- 0 referenced missing artifacts

Release check result:

- 0 errors
- 0 warnings
- 2 info

Full test suite with the documented Windows temp workaround:

```powershell
New-Item -ItemType Directory -Force -Path scratch\tmp,scratch\pytest-tmp | Out-Null
$env:TMP=(Resolve-Path scratch\tmp).Path
$env:TEMP=(Resolve-Path scratch\tmp).Path
<python> -m pytest tests --basetemp=scratch\pytest-tmp -p no:cacheprovider
```

Result:

- 55 passed

## Tests Added

- Provenance report on demo writes Markdown and JSON.
- Generated provenance JSON validates against the lightweight schema.
- Artifact status reports current demo artifacts.
- Freeze-artifacts writes a lock file with manuscript hashes.
- Stale artifact detection works when source and manuscript hashes differ.
- Missing source is warning-level behavior and does not crash.
- Untracked manuscript artifact detection works.
- `\includegraphics` usage detection works.
- Supplement usage detection works.

## Known Limitations

- The ledger is not a full reproducibility proof.
- The TeX usage scanner is heuristic and does not build a full LaTeX dependency graph.
- Source Git commits are detected only when `source_repo` is a local Git worktree or subdirectory.
- Hash comparison detects file drift, not scientific correctness.
- `freeze-artifacts` records current manuscript hashes but does not enforce them.

## Next Recommended Release

v0.8 should focus on Word/Pandoc conversion quality and revision ergonomics:

- Better converted-section splitting guidance.
- More conversion cleanup diagnostics for equations, citations, and tables.
- Optional provenance-aware reviewer response templates.
- Optional comparison of `artifact_lock.json` against current manuscript artifact hashes.
