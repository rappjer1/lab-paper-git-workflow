# v0.7.3 Text Blob Fix Report

## Problem Summary

GitHub raw view can display a tracked text file as a handful of very long lines when the committed Git blob contains CR-only or otherwise collapsed line endings. Local working-tree files can still look normal after checkout, so local `wc -l`, imports, and pytest may pass while public raw readability is broken.

This hotfix adds a permanent guard that inspects Git blobs, not just working-tree files.

## Files Normalized

The normalization utility was run against tracked text files:

```powershell
<python> scripts\dev\normalize_text_blobs.py --apply
```

Problem-file before/after index blob summary:

| Path | Before LF | Before CR | After LF | After CR |
| --- | ---: | ---: | ---: | ---: |
| `.gitattributes` | 13 | 0 | 13 | 0 |
| `src/paper_scaffold/provenance.py` | 445 | 0 | 445 | 0 |
| `src/paper_scaffold/cli.py` | 835 | 0 | 835 | 0 |
| `pyproject.toml` | 41 | 0 | 41 | 0 |

The current branch already had LF-normalized blobs for those key files, but the utility now provides the missing repair path and guard for future commits.

## Git Blob Verification

Passed:

```powershell
<python> scripts\dev\check_text_blobs.py
```

Result:

- All tracked text blobs use LF line endings.
- No tracked text blob contained CR bytes.
- Key files passed collapsed-file line-count checks.

Key blob counts:

- `.gitattributes`: 13 LF, 0 CR.
- `src/paper_scaffold/provenance.py`: 445 LF, 0 CR.
- `src/paper_scaffold/cli.py`: 835 LF, 0 CR.
- `pyproject.toml`: 41 LF, 0 CR.

## Permanent Guard

Added:

- `scripts/dev/check_text_blobs.py`
- `scripts/dev/normalize_text_blobs.py`
- `tests/test_text_blob_line_endings.py`

Updated:

- `.github/workflows/tests.yml` now runs `python scripts/dev/check_text_blobs.py` before pytest.
- `CONTRIBUTING.md` documents the local blob guard and normalization utility.
- `docs/troubleshooting.md` documents why local line counts can pass while GitHub raw is broken.

## Validation Commands

Passed:

```powershell
<python> scripts\paper-scaffold.py --help
<python> scripts\paper-scaffold.py demo --output scratch\demo_manuscript --overwrite
<python> scripts\paper-scaffold.py provenance-report --manuscript-repo scratch\demo_manuscript --write-md scratch\demo_manuscript\provenance_report.md --write-json scratch\demo_manuscript\provenance_ledger.json
<python> scripts\paper-scaffold.py release-check --manuscript-repo scratch\demo_manuscript --write-report scratch\demo_manuscript\release_check.md
```

Full pytest passed with the documented Windows temp workaround:

```powershell
New-Item -ItemType Directory -Force -Path scratch\tmp,scratch\pytest-tmp | Out-Null
$env:TMP=(Resolve-Path scratch\tmp).Path
$env:TEMP=(Resolve-Path scratch\tmp).Path
<python> -m pytest tests --basetemp=scratch\pytest-tmp -p no:cacheprovider
```

Result:

- 57 passed

## Status

v0.7.3 is a narrow line-ending/blob normalization hotfix. It adds no product features and changes no public API behavior.

## Git Commands

```powershell
git status --short
git add .
git commit -m "Add text blob normalization guard"
git push -u origin v0.7.3-text-blob-normalization-guard

git switch main
git merge --no-ff v0.7.3-text-blob-normalization-guard
git tag v0.7.3
git push origin main v0.7.3
```
