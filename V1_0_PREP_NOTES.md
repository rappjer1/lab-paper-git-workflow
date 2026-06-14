# v1.0 Prep Notes

## Already Stable

- `paper-scaffold` console-script name.
- `python -m paper_scaffold` fallback.
- Core manuscript validation commands.
- Artifact manifest, provenance ledger, artifact lock, and lock comparison concepts.
- Diagnostic code registry and `paper-scaffold explain`.
- Cross-platform test runner.
- Clean-install audit script.
- Contract audit script and metadata files.
- Synthetic demo and dogfood examples.

## Still Needs Manual Review

- Confirm GitHub Actions are green on all supported operating systems and Python versions.
- Run the clean-install audit from a committed or pushed release branch.
- Review CLI reference against `paper-scaffold --help`.
- Review schema reference against `paper-scaffold schema list`.
- Review diagnostic docs against `paper-scaffold explain --list`.
- Confirm public docs have no private paths, credentials, or project-specific research content.
- Confirm examples remain small and synthetic.
- Decide whether any legacy exit-code edge cases need normalization before v1.0.

## Recommended v1.0 Scope

- Freeze documented command names and high-use flags.
- Freeze user-authored schema required fields.
- Freeze diagnostic code meanings.
- Freeze generated JSON field names that downstream users may parse.
- Keep all normal workflows dependency-free except optional Word conversion.
- Keep release scope focused on stability, docs, and compatibility.

## Avoid Before v1.0

- Adding major new product workflows.
- Renaming the project or CLI.
- Publishing to PyPI without an explicit release-process decision.
- Adding real research data, private manuscript text, or large binaries.
- Requiring Pandoc, LaTeX, GitHub CLI, Overleaf, or network access for normal use.
- Changing diagnostic meanings without updating contract metadata and docs.

## Proposed v1.0 Release Checklist

```bash
python scripts/dev/check_text_blobs.py
python scripts/dev/check_contracts.py
python scripts/dev/check_docs_examples.py
python scripts/dev/run_dogfood.py --output scratch/dogfood --keep-output
python scripts/dev/run_tests.py
python scripts/dev/clean_install_audit.py
python scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output
```

Then confirm:

- README first-run path is clear.
- Quick Start and Getting Started match current commands.
- Contract docs are discoverable.
- GitHub Actions are green.
- Tag commands have been reviewed and are intentional.
