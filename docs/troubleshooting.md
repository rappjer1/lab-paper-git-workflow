# Troubleshooting

## `python` Is Not Found

Use whichever Python launcher is available on the machine. From a source checkout, the wrapper is:

```bash
python scripts/paper-scaffold.py --help
```

After installation, use:

```bash
paper-scaffold --help
```

After editable install, this fallback does not require the environment Scripts directory on `PATH`:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

## `paper-scaffold` Is Not Found In Git Bash After Editable Install

If editable install succeeds but Git Bash cannot find `paper-scaffold`, the environment's `Scripts` directory is probably not on `PATH`.

Call the installed executable directly:

```bash
<env-root>/Scripts/paper-scaffold.exe --help
```

Or add the environment Scripts directory to `PATH`:

```bash
export PATH="/path/to/env/Scripts:$PATH"
paper-scaffold --help
```

The module fallback also works after editable install:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

## Pytest Cannot Access The Windows Temp Directory

On some Windows machines, pytest may fail with a `PermissionError` for the default user temp folder or for a reused repo-local folder such as `scratch\pytest-tmp`. A reused basetemp can remain locked after an interrupted run, antivirus scan, editor indexing pass, or stale pytest process.

Use the shell-independent test runner:

```bash
python scripts/dev/run_tests.py
```

Use the Python executable for the environment you want to test.

The runner creates unique `scratch/test-runs/pytest-*` and `scratch/test-runs/tmp-*` folders every time, sets `TMP` and `TEMP` for the pytest subprocess, and does not require Bash, CMD, or PowerShell environment-variable syntax.

The older Git Bash style is still fine in Git Bash for one-off debugging:

```bash
mkdir -p scratch/tmp scratch/pytest-tmp
TMP="$PWD/scratch/tmp" TEMP="$PWD/scratch/tmp" python -m pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider
```

## GitHub Raw Shows A Python Or TOML File As One Long Line

GitHub raw view displays the committed Git blob. If a blob was stored with CR-only or collapsed line endings, GitHub can show a file as one very long line even when the local working tree appears normal and local tests pass.

Check tracked text blobs, not just files on disk:

```bash
python scripts/dev/check_text_blobs.py
```

If CR bytes or collapsed blobs are reported, normalize tracked text files and the Git index:

```bash
python scripts/dev/normalize_text_blobs.py --apply
```

The repository has `.gitattributes` rules so common text files are stored with LF endings:

```text
* text=auto
*.py text eol=lf
*.md text eol=lf
*.toml text eol=lf
```

Changing `.gitattributes` alone does not rewrite existing blobs. The normalization utility rewrites LF-normalized blobs into the index so the next normal commit fixes GitHub raw view going forward without rewriting history.

## `origin` Is Missing

Check remotes:

```bash
git remote -v
```

Add the GitHub repo:

```bash
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

If you typed `orign`, remove it:

```bash
git remote remove orign
```

Then add `origin`.

If the message came from `github-check`, the manuscript repo can still be valid locally. Add `origin` before GitHub/Overleaf sync.

## Wrong Remote Name: `orign`

Check remote names:

```bash
git remote -v
```

If a typo exists, remove it and add the correct remote:

```bash
git remote remove orign
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main
```

## Private GitHub Repo Is Invisible In Overleaf

Confirm that:

- The manuscript repo is on GitHub, not only local Git.
- The GitHub account connected to Overleaf has access to the repo.
- The repo is selected during Overleaf import.
- Browser pop-up or authorization prompts were not blocked.

If needed, disconnect and reconnect the GitHub integration in Overleaf, then retry import.

## Overleaf Uses The Wrong Main Document

Set the main document in Overleaf to the configured main TeX file, usually:

```text
main.tex
```

If the project uses a different file, update `metadata/manuscript_config.yaml`:

```yaml
project:
  main_tex: manuscript.tex
```

## Overleaf Does Not Show New Files

Push local commits to GitHub, then pull/sync in Overleaf.

```bash
git status
git push
```

In Overleaf, use the GitHub sync menu.

## Figure Path Is Broken

Run:

```bash
paper-scaffold check-figures --manuscript-repo <manuscript-repo>
paper-scaffold explain E003
```

Common fixes:

- Use paths relative to the manuscript repo, such as `figures/result.pdf`.
- Avoid absolute paths from a local machine.
- Confirm the figure is committed and pushed to GitHub.
- Keep figure filenames simple: lowercase words, numbers, underscores, and hyphens.

## Validation Finds A Forbidden File

Remove the file from the manuscript repo and keep it in the research repo.

If it was staged:

```bash
git restore --staged <path>
```

Then delete the copied file from the manuscript repo.

Large raw output folders should remain in the research repo, data archive, or storage system. Manuscript repos should contain only selected paper-ready figures, tables, source text, bibliography, and provenance metadata.

## Large File Warning

Run:

```bash
paper-scaffold explain E013
git ls-files -s
```

If the large file is raw data, a model checkpoint, a prediction cache, or a broad output archive, remove it from the manuscript repo. If it is a required publication figure, document why it belongs and consider a smaller/vector version.

## Validation Finds A Banned Term

Open `metadata/terminology_map.yaml`, check the suggested publication label, and update the manuscript text.

If the term is legitimate in a supplement provenance table, keep it in the supplement and document that context in `allowed_contexts`.

## Figures Are Stale

Update the source figure in the research repo, then copy only the selected figure into the manuscript repo.

```bash
paper-scaffold copy-artifacts --manuscript-repo <manuscript-repo>
paper-scaffold validate --manuscript-repo <manuscript-repo>
```

## Artifact Lock Comparison Reports Changes

Run:

```bash
paper-scaffold compare-lock --manuscript-repo <manuscript-repo> --lock metadata/artifact_lock.json --write-report <manuscript-repo>/lock_comparison.md
```

For `W040`, review the changed figure or table before creating a new lock. For `E033`, restore the missing locked artifact or document why the new submission intentionally removed it.

If `E032` appears, create a lock first or pass the correct lock path:

```bash
paper-scaffold freeze-artifacts --manuscript-repo <manuscript-repo> --write-lock <manuscript-repo>/metadata/artifact_lock.json
```

## Submission Package Output Already Exists

`package-submission` will not replace an existing folder by default:

```bash
paper-scaffold package-submission --manuscript-repo <manuscript-repo> --output <submission-folder> --overwrite
```

Review the old package before overwriting. If unreferenced files are intentionally required by the journal, use `--include-unreferenced` after checking them.

## Reviewer Binder Output Already Exists

`reviewer-binder` will not replace an existing folder by default:

```bash
paper-scaffold reviewer-binder --manuscript-repo <manuscript-repo> --round 1 --output <response-folder> --overwrite
```

Use a new output folder for each response round unless you are intentionally regenerating the same binder.

## Citation Or Label Errors

Run:

```bash
paper-scaffold check-citations --manuscript-repo <manuscript-repo>
paper-scaffold check-labels --manuscript-repo <manuscript-repo>
```

For `E012`, add the missing BibTeX entry or fix the citation key. For `E010`, rename duplicate labels. For `E011`, add the missing label or update the reference.

## Pandoc Is Missing

`import-word` requires Pandoc. Other Paper Scaffold workflows do not.

Install Pandoc only if you need automated Word conversion, or manually move Word content into LaTeX using the guide in [word_to_overleaf.md](word_to_overleaf.md).

## Word Equations Or Tables Look Wrong

Word conversion is a starting point. Run:

```bash
paper-scaffold audit-word-conversion --input <converted-file>
```

Then manually inspect:

- equations;
- citations;
- figures and captions;
- tables and long tables;
- section hierarchy;
- tracked changes or comments;
- cross-references.

## Git Shows LaTeX Build Files

These files should usually be ignored:

```text
*.aux
*.bbl
*.blg
*.log
*.out
*.synctex.gz
```

Check `.gitignore`, unstage build outputs, and commit only source files.

## Example Artifact Looks Fake

Example artifacts are synthetic, but files with publication-artifact extensions should still have valid file signatures. Run:

```bash
python scripts/dev/check_example_integrity.py
```

If you add a placeholder that is not a real artifact, use a `.placeholder` suffix and document it in the example README. See [example_integrity.md](example_integrity.md).
