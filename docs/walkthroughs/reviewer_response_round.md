# Reviewer Response Round

Goal: create a revision-round binder with a checklist and evidence folders while keeping confidential correspondence out of public examples.

## Commands

```bash
python scripts/paper-scaffold.py provenance-report --manuscript-repo ./paper --write-md ./paper/provenance_report.md --write-json ./paper/metadata/provenance_ledger.json
python scripts/paper-scaffold.py freeze-artifacts --manuscript-repo ./paper --write-lock ./paper/metadata/artifact_lock.json
python scripts/paper-scaffold.py reviewer-binder --manuscript-repo ./paper --round 1 --output ./reviewer_response_round_1
python scripts/paper-scaffold.py compare-lock --manuscript-repo ./paper --lock metadata/artifact_lock.json
```

## Expected Files

```text
reviewer_response_round_1/
  README.md
  response_checklist.md
  evidence/
```

## Suggested Review Order

1. Record each requested change in `response_checklist.md`.
2. Link each response item to a manuscript section, figure, table, or supplement file.
3. Use `provenance_report.md` to confirm which artifacts changed.
4. Re-run `release-check` before sharing the revised manuscript repo or package.

## More Detail

- [reviewer_response_binder.md](../reviewer_response_binder.md)
- [artifact_locks.md](../artifact_locks.md)
- [provenance_ledger.md](../provenance_ledger.md)
