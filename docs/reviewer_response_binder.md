# Reviewer Response Binder

`paper-scaffold reviewer-binder` creates a lightweight folder for revision-round evidence:

```bash
paper-scaffold reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1
```

The command does not write responses for you. It creates structure and snapshots that help keep response artifacts separate from manuscript source and raw analysis outputs.

## Generated Files

The binder contains:

- `README.md`
- `response_checklist.md`
- `response_artifact_manifest.yaml`
- `provenance_snapshot.md`
- `release_check.md`
- `artifact_status.txt`
- `artifact_lock_snapshot.json`

## Suggested Revision Workflow

```bash
paper-scaffold reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1
paper-scaffold release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md
```

Use the binder to map reviewer points to manuscript changes or supporting artifacts. Keep confidential review text out of public repositories unless the journal and authors explicitly allow it.

## Overwrite Protection

Existing binder folders are not replaced unless `--overwrite` is passed:

```bash
paper-scaffold reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1 --overwrite
```

## Limitations

The binder does not format a journal response letter, verify scientific claims, or rerun analyses. It is a small, auditable handoff folder.
