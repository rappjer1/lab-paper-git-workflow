# Submission Packaging Example

This tiny example shows the intended command sequence for a clean submission package.

```bash
paper-scaffold demo --output scratch/demo_manuscript --overwrite
paper-scaffold release-check --manuscript-repo scratch/demo_manuscript --write-report scratch/demo_manuscript/release_check.md
paper-scaffold freeze-artifacts --manuscript-repo scratch/demo_manuscript --write-lock scratch/demo_manuscript/metadata/artifact_lock.json
paper-scaffold package-submission --manuscript-repo scratch/demo_manuscript --output scratch/submission_package --overwrite
```

The generated package should contain manuscript source, referenced figure/table artifacts, `README_SUBMISSION.md`, and `submission_package_manifest.json`.
