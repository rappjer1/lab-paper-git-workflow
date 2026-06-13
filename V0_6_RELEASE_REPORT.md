# v0.6.0 Release Report

## Scope

v0.6.0 adds a public use-case and recipes layer on top of the existing Paper Scaffold CLI:

- `paper-scaffold recipes list`
- `paper-scaffold recipes show <recipe-id>`
- `paper-scaffold audit-project --path <path> --write-report <report.md>`
- `paper-scaffold release-check --manuscript-repo <path> --write-report <report.md>`

The release keeps examples generic and synthetic. It does not add network behavior, GitHub publishing, Overleaf upload, large binaries, or project-specific research files.

## Commands Added

- `recipes`: lists and shows reusable workflow recipes.
- `audit-project`: read-only project archaeology scanner for messy folders.
- `release-check`: consolidated pre-submission check runner for manuscript repos.

## Documentation Added

- `docs/use_cases/README.md`
- `docs/use_cases/word-to-overleaf.md`
- `docs/use_cases/python-artifact-handoff.md`
- `docs/use_cases/existing-latex-cleanup.md`
- `docs/use_cases/overleaf-zip-rehab.md`
- `docs/use_cases/paper-archaeology.md`
- `docs/use_cases/reviewer-response-binder.md`
- `docs/use_cases/undergraduate-artifact-harvest.md`
- `docs/use_cases/pre-submission-flight-check.md`
- `docs/use_cases/multi-paper-project-split.md`

The README now links the use-case gallery and lists the new commands.

## Examples Added

- `examples/messy_project_archaeology/`
- `examples/reviewer_response_binder/`
- `examples/multi_paper_split/`

The messy-project example uses tiny text placeholders, including files with `.png` and `.npz` extensions, so the audit command can demonstrate filename and category behavior without committing large or real binary data.

## Diagnostics Added

- `W022`: suspicious final/final2/final_FINAL filename.
- `W023`: LaTeX build artifact found during project audit.
- `W024`: raw or generated output found during project audit.
- `I020`: likely manuscript file or Overleaf export folder found.
- `I021`: likely figure or table candidate found.

Existing `W020` and `W021` meanings were preserved.

## Validation Results

Passed:

```powershell
<python> scripts\paper-scaffold.py --help
<python> scripts\paper-scaffold.py recipes list
<python> scripts\paper-scaffold.py recipes show paper-archaeology
<python> scripts\paper-scaffold.py demo --output scratch\demo_manuscript --overwrite
<python> scripts\paper-scaffold.py release-check --manuscript-repo scratch\demo_manuscript --write-report scratch\demo_manuscript\release_check.md
<python> scripts\paper-scaffold.py audit-project --path examples\messy_project_archaeology --write-report scratch\messy_project_audit.md
```

Release check result on the demo manuscript:

- 0 errors
- 0 warnings
- 2 info

Messy project audit result:

- 0 errors
- 5 warnings
- 8 info

The exact requested pytest command reproduced the known Windows temp-directory issue:

```powershell
<python> -m pytest tests
```

Failure mode:

- `PermissionError: [WinError 5] Access is denied: 'C:\Users\<user>\AppData\Local\Temp\pytest-of-<user>'`

The documented Windows workaround passed:

```powershell
New-Item -ItemType Directory -Force -Path scratch\tmp,scratch\pytest-tmp | Out-Null
$env:TMP=(Resolve-Path scratch\tmp).Path
$env:TEMP=(Resolve-Path scratch\tmp).Path
<python> -m pytest tests --basetemp=scratch\pytest-tmp -p no:cacheprovider
```

Result:

- 47 passed

## Tests Added

- Recipes list command works.
- Recipes show command works for a known recipe.
- Unknown recipe fails gracefully with available IDs.
- `audit-project` writes a Markdown report for the synthetic messy-project example.
- `release-check` runs on the demo manuscript and writes a report.
- Use-case docs exist and are linked.
- README links use cases and release-check.
- New synthetic examples do not contain local private paths or emails.

## Limitations

- `audit-project` is heuristic and read-only; it does not decide which file is scientifically canonical.
- `release-check` does not compile LaTeX or upload to Overleaf.
- The use-case gallery is documentation-first and intentionally lightweight.
- Example `.png` and `.npz` files are text placeholders, not real binary artifacts.

## v0.7 Candidates

- Optional LaTeX compile wrapper when local tools are available.
- Recipe-specific report templates.
- More structured JSON output for `audit-project` and `release-check`.
- A guided cleanup workflow that converts audit findings into a reviewed copy plan.
- More examples for journals with supplements, response letters, or data availability statements.
