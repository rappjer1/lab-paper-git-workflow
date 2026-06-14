# Pre-Submission Package

Goal: create a clean local folder for manual journal upload review without including scratch files, build artifacts, or unreferenced figures by default.

## Commands

```bash
python scripts/paper-scaffold.py release-check --manuscript-repo ./paper --write-report ./paper/release_check.md
python scripts/paper-scaffold.py freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
python scripts/paper-scaffold.py package-submission --manuscript-repo ./paper --output ./submission_package
python scripts/paper-scaffold.py compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json --write-report ./paper/lock_comparison.md --write-json ./paper/lock_comparison.json
```

## Include Unreferenced Artifacts Deliberately

By default, `package-submission` excludes unreferenced figure-like files. If a journal asks for extra source figures or supplemental material, pass the explicit flag:

```bash
python scripts/paper-scaffold.py package-submission --manuscript-repo ./paper --output ./submission_package --include-unreferenced
```

## What To Inspect

- `release_check.md`
- `metadata/artifact_lock.json`
- `lock_comparison.md`
- The final package folder before upload

## More Detail

- [submission_packaging.md](../submission_packaging.md)
- [artifact_locks.md](../artifact_locks.md)
- [error_codes.md](../error_codes.md)
