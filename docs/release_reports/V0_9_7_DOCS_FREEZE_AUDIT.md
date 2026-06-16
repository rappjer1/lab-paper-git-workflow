# v0.9.7 Docs Freeze Audit

Branch: `v0.9.7-docs-freeze-public-walkthroughs`

Purpose: audit the public documentation information architecture, first-run path, walkthrough coverage, and public-language readiness before the v1.0 stabilization window.

## Scope

Audited:

- `README.md`
- `QUICKSTART.md`
- `docs/start_here.md`
- `docs/common_paths.md`
- `docs/one_page_reference.md`
- `docs/walkthroughs/`
- `docs/glossary.md`
- Existing install, compatibility, troubleshooting, release, schema, contract, and CLI reference docs
- Public examples index and dogfood links

Not audited as a product feature change:

- CLI behavior
- Metadata schema behavior
- Workflow command behavior
- Packaging or publishing behavior

## Information Architecture Findings

### Entry Point

Status: addressed.

`README.md` now starts with a short description, a clear "What It Is" section, direct links to `docs/start_here.md`, `docs/common_paths.md`, `docs/one_page_reference.md`, `docs/cli_reference.md`, and `docs/glossary.md`, plus checkout-first demo commands.

### New User Path

Status: addressed.

`docs/start_here.md` gives a first command, demo path, workflow selection table, invocation modes, what belongs in a manuscript repo, and links to fast references.

### Workflow Selection

Status: addressed.

`docs/common_paths.md` maps common user situations to commands and docs. `docs/which_workflow.md` remains the more detailed decision guide.

### Command Density

Status: addressed.

`docs/one_page_reference.md` provides a compact command reference. The full `docs/cli_reference.md` remains the command contract source.

### Walkthrough Coverage

Status: addressed.

Added public walkthroughs for:

- five-minute demo
- Python outputs to manuscript
- existing LaTeX cleanup
- pre-submission package
- reviewer response round

### Terminology

Status: addressed.

Added `docs/glossary.md` and linked it from README, Start Here, Common Paths, One-Page Reference, and walkthroughs.

## Public-Language Scan

Scan scope:

The scan covered personal names, workstation names, local drive paths, project-specific research terms, chat-platform wording, credential wording, and privacy terms across `README.md`, `QUICKSTART.md`, `docs`, `examples`, `scripts`, and `tests`.

Result summary:

- No hits for personal names, workstation names, local machine paths, or project-specific research terms.
- No hits for the requested project-specific research terms.
- Remaining privacy-language hits are generic privacy/security documentation, diagnostics, and tests.
- Remaining credential-language hit is in an ADR explaining why manual credential-based publishing is not used.
- Remaining chat-platform hits are the existing contract-preserved launch-summary command reference and a legacy launch-copy pointer. No new v0.9.7 walkthrough depends on that channel.

Follow-up needed before v1.0:

- Decide whether the legacy launch-copy docs should be renamed or folded into a generic announcement guide.
- Decide whether the legacy launch-summary command should remain under its current exact name for v1.0 or enter a deprecation path after the contract freeze.

## Link And Drift Checks

Status: addressed.

Added `scripts/dev/check_docs_links.py` for local Markdown link checks across README, QUICKSTART, and `docs/**/*.md`.

Updated `scripts/dev/check_docs_examples.py` to require:

- new public docs
- walkthrough docs
- README links
- QUICKSTART links
- examples README dogfood links
- CLI reference coverage for all argparse commands

Updated GitHub Actions to run `check_docs_links.py`.

## Validation Results

Passed:

- `<python> scripts/dev/check_text_blobs.py`
- `<python> scripts/dev/check_contracts.py`
- `<python> scripts/dev/check_docs_examples.py`
- `<python> scripts/dev/check_docs_links.py`
- `<python> scripts/dev/check_example_integrity.py`
- `<python> scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output`
- `<python> scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`
- `<python> scripts/dev/run_tests.py`

Full test result:

- `139 passed`

Optional package build:

- `<python> -m build` was skipped because the selected environment did not have the `build` module installed.

## Known Limitations

- Some historical docs still use generic privacy language because privacy checks are part of the product.
- The legacy launch-summary command name remains documented because command names are under the public contract.
- The optional local package build requires installing the `build` extra first.

## Audit Conclusion

v0.9.7 is ready as a documentation-freeze and public-walkthrough release candidate. It does not add product workflows, change command behavior, publish packages, or require external tools for normal use.
