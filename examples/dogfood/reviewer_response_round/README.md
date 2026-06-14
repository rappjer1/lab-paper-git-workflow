# Dogfood: Reviewer Response Round

Goal: create a lightweight response-round binder from a manuscript repo.

Represents: a revision handoff where artifacts and checks need to be organized before writing confidential response text elsewhere. All files are synthetic; no real reviewer text or research data are included.

Commands:

```bash
python scripts/paper-scaffold.py reviewer-binder --manuscript-repo scratch/demo_manuscript --round 1 --output scratch/reviewer_response_round_1 --overwrite
```

Expected result: a response checklist and evidence folder using synthetic demo artifacts.

Manual review still needed: write actual reviewer responses outside public example data.
