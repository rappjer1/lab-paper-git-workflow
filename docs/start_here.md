# Start Here

Paper Scaffold helps you keep a manuscript repository separate from the code and outputs that produced the paper. It does not write the manuscript, create remote repositories, upload to Overleaf, or decide which figures and tables are publication-ready.

It also does not guarantee LaTeX compilation, manage raw data, or replace manual review.

Use this page when you are new to the project or when you need the shortest route to the right workflow.

## First Command

From a source checkout:

```bash
python scripts/paper-scaffold.py self-test
```

After installation:

```bash
python -m paper_scaffold self-test
```

If both succeed, create a demo manuscript:

```bash
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
```

## Choose A Path

| Starting point | Use | Next page |
| --- | --- | --- |
| You want a five-minute tour | `self-test`, `demo`, `validate` | [walkthroughs/five_minute_demo.md](walkthroughs/five_minute_demo.md) |
| You have Python figures or tables | `discover-artifacts`, `copy-artifacts`, `validate` | [walkthroughs/python_outputs_to_manuscript.md](walkthroughs/python_outputs_to_manuscript.md) |
| You have an existing LaTeX folder | `doctor`, `validate`, focused checks | [walkthroughs/existing_latex_cleanup.md](walkthroughs/existing_latex_cleanup.md) |
| You are preparing a submission | `release-check`, `freeze-artifacts`, `package-submission` | [walkthroughs/pre_submission_package.md](walkthroughs/pre_submission_package.md) |
| You are answering reviewers | `provenance-report`, `reviewer-binder`, `compare-lock` | [walkthroughs/reviewer_response_round.md](walkthroughs/reviewer_response_round.md) |
| You are unsure | Read workflow map | [which_workflow.md](which_workflow.md) |

## Invocation Modes

Use whichever mode matches your setup:

```bash
python scripts/paper-scaffold.py --help
paper-scaffold --help
python -m paper_scaffold --help
```

The checkout wrapper is best for a fresh clone. The installed command is convenient when its Scripts or bin directory is on `PATH`. The module fallback works after install even when the console script is not on `PATH`.

## What Goes In The Manuscript Repo

Commit:

- `main.tex`, `references.bib`, and section files.
- Selected publication figures and tables.
- Metadata files under `metadata/`.
- Small notes needed to reproduce manuscript assembly.

Do not commit:

- Raw data dumps.
- Model checkpoints.
- Prediction caches.
- Full generated output folders.
- LaTeX build files such as `.aux`, `.log`, and `.synctex.gz`.

## Fast References

- [Quick Start](../QUICKSTART.md)
- [Common Paths](common_paths.md)
- [One-Page Reference](one_page_reference.md)
- [Walkthroughs](walkthroughs/README.md)
- [Install](install.md)
- [CLI Reference](cli_reference.md)
- [Privacy And Data Safety](privacy_and_data_safety.md)
- [Glossary](glossary.md)
- [Troubleshooting](troubleshooting.md)
- [Project README](../README.md)
