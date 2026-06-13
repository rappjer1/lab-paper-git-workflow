# Multi-Paper Split Example

This synthetic example shows how one research project can feed separate manuscript repositories. Each paper gets its own manifest and should copy only the artifacts it needs.

Use:

```bash
paper-scaffold init --manuscript-repo ./paper_a
paper-scaffold init --manuscript-repo ./paper_b
paper-scaffold discover-artifacts --source ./project_outputs/paper_a --manifest ./paper_a/metadata/artifact_manifest.yaml
paper-scaffold discover-artifacts --source ./project_outputs/paper_b --manifest ./paper_b/metadata/artifact_manifest.yaml
```
