# Examples

All examples are synthetic and intentionally small. They are meant to show workflow shape, not scientific claims.

Files with artifact extensions are real tiny synthetic files, not mislabeled text placeholders. Run:

```bash
python scripts/dev/check_example_integrity.py
```

| Example | Demonstrates | Command to try | Modifies files |
| --- | --- | --- | --- |
| `minimal_python_artifacts` | Small Python-generated figure/table outputs and an artifact manifest. | `python examples/minimal_python_artifacts/make_example_figure.py` | yes, regenerates example outputs |
| `minimal_word_workflow` | Word-to-LaTeX cleanup concepts using Markdown placeholders. | `python scripts/paper-scaffold.py audit-word-conversion --input examples/minimal_word_workflow/sample_converted.md` | no |
| `existing_latex_cleanup` | Before/after structure for cleaning an existing LaTeX project. | `python scripts/paper-scaffold.py audit-project --path examples/existing_latex_cleanup` | no |
| `messy_project_archaeology` | Triage of old notes, exports, generated outputs, and stale files. | `python scripts/paper-scaffold.py audit-project --path examples/messy_project_archaeology` | no |
| `reviewer_response_binder` | Response-round checklist and artifact manifest concepts. | `python scripts/paper-scaffold.py recipes show reviewer-response-binder` | no |
| `multi_paper_split` | Splitting one project output folder into multiple paper manifests. | `python scripts/paper-scaffold.py recipes show multi-paper-project-split` | no |
| `manuscript_ci` | Dependency-free manuscript CI workflow shape. | `python scripts/paper-scaffold.py add-manuscript-ci --manuscript-repo scratch/demo_manuscript --overwrite` | yes |
| `submission_packaging` | Clean source/artifact package structure. | `python scripts/paper-scaffold.py package-submission --manuscript-repo scratch/demo_manuscript --output scratch/submission_package --overwrite` | yes |
| `reviewer_response_round` | Reviewer response round template. | `python scripts/paper-scaffold.py reviewer-binder --manuscript-repo scratch/demo_manuscript --round 1 --output scratch/reviewer_response_round_1 --overwrite` | yes |
| `dogfood/python_outputs_to_manuscript` | Discovering selected Python artifacts without copying first. | `python scripts/paper-scaffold.py discover-artifacts --source examples/dogfood/python_outputs_to_manuscript/input/outputs --manifest scratch/dogfood_python/metadata/artifact_manifest.yaml --suggest-only` | no |
| `dogfood/existing_latex_cleanup` | Validating a tiny existing LaTeX project. | `python scripts/paper-scaffold.py validate --manuscript-repo examples/dogfood/existing_latex_cleanup/project` | no |
| `dogfood/reviewer_response_round` | Creating a response binder from a demo manuscript. | `python scripts/paper-scaffold.py reviewer-binder --manuscript-repo scratch/demo_manuscript --round 1 --output scratch/reviewer_response_round_1 --overwrite` | yes |
| `dogfood/submission_package` | Packaging a demo manuscript for manual upload review. | `python scripts/paper-scaffold.py package-submission --manuscript-repo scratch/demo_manuscript --output scratch/submission_package --overwrite` | yes |
| `dogfood/messy_project_audit` | Auditing an old project folder before copying files. | `python scripts/paper-scaffold.py audit-project --path examples/dogfood/messy_project_audit/project --write-report scratch/messy_project_audit.md` | optional report |

For a maintained end-to-end check, run:

```bash
python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output
```
