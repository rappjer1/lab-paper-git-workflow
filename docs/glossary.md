# Glossary

## Artifact

A selected manuscript file, usually a figure, table, or small supporting output. Paper Scaffold records artifacts in `metadata/artifact_manifest.yaml`.

## Artifact Lock

A generated JSON file that freezes artifact hashes at a submission or revision point. Use `freeze-artifacts` to write one and `compare-lock` to detect drift.

## Artifact Manifest

The user-authored YAML file that says which artifacts belong in the manuscript repo and where they came from.

## Checkout Wrapper

The script invocation used from a fresh clone:

```bash
python scripts/paper-scaffold.py <command>
```

## Console Script

The installed `paper-scaffold` command created by editable or package installation. On Windows shells, the environment Scripts directory must be on `PATH`.

## Demo Manuscript

A small synthetic manuscript produced by `demo` or `self-test`. It is used to show expected structure without needing external tools or network access.

## Dogfood Scenario

A small example under `examples/dogfood/` that exercises a real workflow shape with synthetic files.

## Manuscript Repository

The clean repository that contains manuscript source, selected artifacts, and metadata. It should not contain full research outputs or large caches.

## Module Fallback

The installed invocation that works even when the console script is not on `PATH`:

```bash
python -m paper_scaffold <command>
```

## Overleaf Check

A local check for file paths, figure references, large files, and sync risks before importing or syncing a manuscript repository.

## Provenance Ledger

A generated report that summarizes artifact sources, manuscript paths, hashes, usage, and status.

## Release Check

A consolidated pre-submission check that runs validation and related manuscript-readiness checks.

## Reviewer Binder

A local folder with a response checklist and evidence structure for a revision round.

## Submission Package

A clean local folder created for manual upload review. It excludes scratch folders, build files, and unreferenced artifacts by default.

## Terminology Map

A YAML file that maps implementation-facing terms to publication-facing language and flags terms that should not appear in manuscript text.

## More Reading

- [Start Here](start_here.md)
- [Common Paths](common_paths.md)
- [One-Page Reference](one_page_reference.md)
- [CLI Reference](cli_reference.md)
