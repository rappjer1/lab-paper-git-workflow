# Paper Scaffold

[![Tests](https://github.com/rappjer1/lab-paper-git-workflow/actions/workflows/tests.yml/badge.svg)](https://github.com/rappjer1/lab-paper-git-workflow/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Paper Scaffold is a lightweight Python CLI and documentation set for creating clean manuscript repositories from selected research outputs.

## What It Is

Paper Scaffold helps you keep manuscript source, selected figures/tables, and provenance metadata in a separate repository from research code and generated outputs. It is designed for local-first workflows that may later connect to GitHub and Overleaf.

Core message: Keep research code and manuscript source separate. Copy only selected paper-ready artifacts into the manuscript repo, then validate the repo before syncing or sharing.

It does not write the paper, create remote repositories, compile LaTeX, upload to Overleaf, choose artifacts for you, or replace review.

## Start Here

- New user entry point: [docs/start_here.md](docs/start_here.md)
- Common workflow map: [docs/common_paths.md](docs/common_paths.md)
- Command cheat sheet: [docs/one_page_reference.md](docs/one_page_reference.md)
- Full CLI reference: [docs/cli_reference.md](docs/cli_reference.md)
- Terms used in the docs: [docs/glossary.md](docs/glossary.md)

Try the tool from a checkout:

```bash
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript --write-json scratch/demo_manuscript/validation_report.json
```

## Choose A Workflow

| Starting point | Read | Main commands |
| --- | --- | --- |
| Try the tool | [five-minute demo](docs/walkthroughs/five_minute_demo.md) | `self-test`, `demo`, `validate` |
| Python figures or tables | [Python outputs walkthrough](docs/walkthroughs/python_outputs_to_manuscript.md) | `discover-artifacts`, `copy-artifacts`, `provenance-report` |
| Existing LaTeX folder | [LaTeX cleanup walkthrough](docs/walkthroughs/existing_latex_cleanup.md) | `doctor`, `validate`, `check-figures`, `check-citations` |
| Submission package | [pre-submission walkthrough](docs/walkthroughs/pre_submission_package.md) | `release-check`, `freeze-artifacts`, `package-submission` |
| Revision round | [reviewer response walkthrough](docs/walkthroughs/reviewer_response_round.md) | `provenance-report`, `reviewer-binder`, `compare-lock` |
| Unsure | [which workflow?](docs/which_workflow.md) | `recipes list`, `recipes show <id>` |

Recipe commands:

```bash
paper-scaffold recipes list
paper-scaffold recipes show pre-submission-flight-check
paper-scaffold release-check --manuscript-repo ./paper
```

Use-case recipe docs: [docs/use_cases](docs/use_cases).

## Install Or Run Without Install

No install is required from a checkout:

```bash
git clone https://github.com/rappjer1/lab-paper-git-workflow.git
cd lab-paper-git-workflow
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py self-test
```

Editable install:

```bash
python -m pip install -e ".[dev]"
paper-scaffold --help
```

Installed fallback when the console script is not on `PATH`:

```bash
python -m paper_scaffold --help
python -m paper_scaffold self-test
```

Install details and platform notes: [docs/install.md](docs/install.md), [docs/compatibility.md](docs/compatibility.md), [docs/troubleshooting.md](docs/troubleshooting.md).

## Core Commands

- `self-test`: run a no-network smoke workflow.
- `demo`: create a synthetic manuscript repo.
- `init`: create a clean manuscript repo scaffold.
- `discover-artifacts`: find likely manuscript figures and tables.
- `copy-artifacts`: copy manifest-listed artifacts.
- `validate`: check manuscript structure, metadata, terminology, and Git state.
- `release-check`: run consolidated pre-submission checks.
- `provenance-report`: write a Markdown/JSON artifact bill of materials.
- `stale-artifacts` and `unused-artifacts`: find outdated or unreferenced manuscript artifacts.
- `freeze-artifacts` and `compare-lock`: lock artifact hashes and detect drift.
- `add-manuscript-ci`: add a dependency-free manuscript hygiene workflow.
- `package-submission`: create a clean local submission folder.
- `reviewer-binder`: create a revision-round checklist and evidence folder.

Complete list: [docs/cli_reference.md](docs/cli_reference.md). Diagnostic codes: [docs/error_codes.md](docs/error_codes.md).

## What Not To Commit

Keep manuscript repositories small and reviewable. Do not commit:

- Raw data dumps or external data exports.
- Model checkpoints, prediction caches, and generated run folders.
- Large binary arrays or archives such as `.npz`, `.pt`, `.pth`, `.pkl`, `.pickle`, `.nc`, `.zarr`, or `.zip`.
- Full output trees when only selected paper artifacts are needed.
- API credentials, machine-local paths, or personal notes.
- LaTeX build files such as `.aux`, `.log`, `.bbl`, `.out`, `.toc`, and `.synctex.gz`.

## Examples And Walkthroughs

- Walkthrough index: [docs/walkthroughs/README.md](docs/walkthroughs/README.md)
- Example index: [examples/README.md](examples/README.md)
- Dogfood examples: [examples/dogfood](examples/dogfood)
- Example integrity guide: [docs/example_integrity.md](docs/example_integrity.md)

Examples are synthetic and intentionally small.

## Provenance And Reports

Paper Scaffold records what was copied, where it came from, whether manuscript files reference it, and whether hashes changed after locking.

- Provenance guide: [docs/provenance_ledger.md](docs/provenance_ledger.md)
- Artifact locks: [docs/artifact_locks.md](docs/artifact_locks.md)
- Submission packaging: [docs/submission_packaging.md](docs/submission_packaging.md)
- Schema reference: [docs/schema_reference.md](docs/schema_reference.md)
- Exit codes: [docs/exit_codes.md](docs/exit_codes.md)

## Stability

The v0.9 series is the release-candidate hardening series for v1.0. Command names, documented flags, schemas, diagnostic codes, and exit-code conventions are being frozen.

- Public contract: [docs/contract.md](docs/contract.md)
- Versioning policy: [docs/versioning_policy.md](docs/versioning_policy.md)
- v1.0 readiness: [docs/v1_0_readiness.md](docs/v1_0_readiness.md)
- Release process: [docs/release_process.md](docs/release_process.md)
- Roadmap: [ROADMAP.md](ROADMAP.md)

## Contributing

Contributions should keep examples generic, small, and public-safe. Add tests for CLI or docs-contract changes and run the maintainer checks in [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

If Paper Scaffold helps your project, cite or acknowledge it using [CITATION.cff](CITATION.cff) or link to this repository.

## License

MIT. See [LICENSE](LICENSE).
