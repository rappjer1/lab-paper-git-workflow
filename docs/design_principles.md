# Design Principles

## Separate Computation From Publication

Research code, raw data, model outputs, and caches belong in the research repo or data archive. Manuscript source belongs in a separate manuscript repo.

## Keep Manuscript Repos Small

A manuscript repo should be easy to inspect with `git status`. It should contain source text, references, selected figures/tables, supplement files, and metadata.

## Track Provenance Without Copying Raw Outputs

Use `metadata/artifact_manifest.yaml` to record where each copied figure/table came from. Do not copy entire result directories for one figure.

## Prefer Stable Filenames

Use names like `model_comparison.pdf`, not timestamps or random hashes.

## Make Overleaf A Frontend

Overleaf is useful for editing and compilation. GitHub should remain the source of truth for the manuscript repository.

## Keep Implementation Labels Out Of Main Text

Use scientific labels in the paper. Keep code labels in manifests, reproducibility notes, or supplement provenance tables unless the implementation label is scientifically meaningful.

## Validate Before Syncing

Run validation before pushing or syncing to Overleaf. Fix forbidden files, missing artifacts, terminology issues, and Git confusion early.
