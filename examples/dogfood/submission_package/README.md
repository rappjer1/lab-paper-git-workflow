# Dogfood: Submission Package

Goal: package a clean manuscript folder for manual journal upload review.

Represents: a final pre-submission check after the manuscript repo validates. All files are synthetic; no real research data are included.

Commands:

```bash
python scripts/paper-scaffold.py package-submission --manuscript-repo scratch/demo_manuscript --output scratch/submission_package --overwrite
```

Expected result: a clean package folder with manuscript source and referenced synthetic artifacts.

Manual review still needed: journal-specific file names, cover letter, and submission portal requirements.
