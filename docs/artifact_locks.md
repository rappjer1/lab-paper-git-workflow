# Artifact Locks

Artifact locks record the hashes of manuscript artifacts at a submission or revision handoff point.

Create a lock:

```bash
paper-scaffold freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
```

Compare the current manuscript repo to a lock:

```bash
paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json
```

`--lock` may be relative to the manuscript repo, relative to the current working directory, or absolute.

## Reports

Write comparison reports:

```bash
paper-scaffold compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md --write-json ./paper/lock_comparison.json
```

The command exits with:

- `0` when locked artifacts are unchanged and not missing
- `1` when a locked artifact changed or is missing
- `2` when the lock file cannot be read

New artifacts that are absent from the lock are reported as warnings because they may be intentional additions after a submission or revision.

## Diagnostics

- `E032`: lock file missing
- `E033`: locked artifact missing from the current manuscript artifact set
- `W040`: artifact hash changed since the lock
- `W041`: current artifact is not present in the lock
- `I042`: comparison passed
- `I044`: comparison report written

## Limitations

Locks compare manuscript artifact files, not raw data, full analysis workflows, or compiled PDFs. Use them as a handoff record alongside provenance reports and release checks.
