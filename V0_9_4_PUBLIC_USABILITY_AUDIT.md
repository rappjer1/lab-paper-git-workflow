# v0.9.4 Public Usability Audit

Perspective: a public user landing on the repository for the first time.

## README First 60 Seconds

Finding: the README explained the project well, but the first actionable command was buried after several sections.

Action: added a top-level `Start Here` section with three minimal paths: try the tool, inspect Python outputs, and validate an existing manuscript repo.

## First Command

Finding: users needed a clearer first command from a checkout.

Action: documented `python scripts/paper-scaffold.py self-test` as the safest first checkout command and kept `paper-scaffold` and `python -m paper_scaffold` as installed alternatives.

## Workflow Choice

Finding: workflow selection was spread across README, Quick Start, and use-case docs.

Action: added `docs/which_workflow.md` with a decision table and linked it from README, Quick Start, and Getting Started.

## Install Instruction Scattering

Finding: install and invocation modes were repeated, but this is useful for a CLI with checkout, console-script, and module-fallback modes.

Action: kept the three invocation modes but moved detailed decision-making into docs.

## Duplicate Or Contradictory Docs

Finding: no direct contradictions were found, but Quick Start used installed commands before checkout commands.

Action: rewrote Quick Start to use checkout commands first and mention installed alternatives.

## Copy-Paste Examples

Finding: existing examples were useful but lacked a single index and realistic end-to-end dogfood commands.

Action: added `examples/README.md`, `examples/dogfood/`, and `scripts/dev/run_dogfood.py`.

## Contract Docs Discoverability

Finding: v0.9.3 contract docs were present but not visible enough from the README.

Action: linked `docs/contract.md`, `docs/versioning_policy.md`, and `docs/v1_0_readiness.md` from README and added docs drift checks.

## Concept Clarity

Finding: the difference between research repo, manuscript repo, artifact manifest, provenance ledger, and submission package was present across docs but not in one decision point.

Action: added workflow guide descriptions and Getting Started inspection points that name these files and folders.

## Automation Expectations

Finding: some users could infer that Paper Scaffold automates manuscript preparation end to end.

Action: added explicit language that Paper Scaffold does not write papers, choose artifacts, create GitHub repos, upload to Overleaf, or replace scientific review.

## Public Language

Finding: a few public docs included machine-specific interpreter examples from prior Windows validation notes.

Action: replaced those with generic environment guidance.

## Private Or Project-Specific Strings

Finding: README and docs were searched for local paths and project-specific research terms. Machine-specific examples in public docs were removed. Search/checklist language was kept generic.

Action: added `scripts/dev/check_docs_examples.py` and kept text-blob and contract checks in the validation path.

## Known Limitations

- The README is still comprehensive; some users may prefer Quick Start first.
- The dogfood runner validates workflow shape but does not compile LaTeX or test Overleaf/GitHub integration.
- The docs/examples checker is intentionally lightweight, not a full Markdown link checker.
- Clean-install audit still needs to be run from a committed or pushed release branch for exact public-source validation.
