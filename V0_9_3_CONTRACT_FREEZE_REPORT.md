# v0.9.3 Contract Freeze Report

Branch: `v0.9.3-contract-freeze`

Version: `0.9.3`

## Purpose

v0.9.3 makes the pre-v1.0 public contract explicit. It documents command names, command behavior, diagnostic code stability, user-authored schemas, generated JSON reports, exit-code conventions, deprecation policy, versioning policy, and the v1.0 readiness checklist.

This release does not add major product workflows.

## Contract Docs Added

- `docs/contract.md`
- `docs/deprecation_policy.md`
- `docs/versioning_policy.md`
- `docs/v1_0_readiness.md`

## Contract Files Added

- `contracts/cli_commands.yaml`
- `contracts/diagnostic_codes.yaml`
- `contracts/schema_names.yaml`
- `contracts/exit_codes.yaml`

## Audit Script Added

- `scripts/dev/check_contracts.py`

The audit checks:

- argparse command names against `contracts/cli_commands.yaml` and `docs/cli_reference.md`;
- `messages.py` diagnostic codes against `contracts/diagnostic_codes.yaml` and `docs/error_codes.md`;
- schema registry names against `contracts/schema_names.yaml` and `docs/schema_reference.md`;
- exit-code docs against `contracts/exit_codes.yaml`.

## Tests Added

- `tests/test_v093_contract_freeze.py`

Coverage includes:

- contract audit script pass;
- every CLI command listed in contract metadata;
- every diagnostic code listed in contract metadata;
- every schema name listed in contract metadata;
- required contract policy docs present;
- CLI, diagnostic, and schema references include public contract entries;
- README links to contract docs;
- text blob guard still passes;
- `run_tests.py --help` still passes.

## Documentation Updated

- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/cli_reference.md`
- `docs/schema_reference.md`
- `docs/error_codes.md`

## Validation Results

Passed:

- `<python> scripts/dev/check_text_blobs.py`
- `<python> scripts/dev/check_contracts.py`
- `<python> scripts/paper-scaffold.py --version`
- `<python> scripts/paper-scaffold.py --help`
- `<python> -m paper_scaffold --help`
- `<python> scripts/paper-scaffold.py schema list`
- `<python> scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`
- `<python> scripts/dev/run_tests.py`
- `<python> -m ruff check .`

Observed results:

- Version output: `paper-scaffold 0.9.3`
- Contract audit: passed
- Full test suite: `102 passed in 27.98s`
- Self-test: 10 steps passed, 0 failed
- Schema list: 7 schemas listed
- Text blob guard: all tracked text blobs passed
- Ruff: passed

Optional package build:

- `<python> -m build` was attempted.
- Result: unavailable in the local environment, `No module named build`.

## Known Limitations

- `scripts/dev/check_contracts.py` parses the small contract YAML subset used in this repo; it is not a general YAML parser.
- The contract files are release metadata, not generated source of truth.
- v0.9.3 does not normalize every legacy command exit edge case before v1.0.
- Package build was not validated locally because the build frontend is not installed in the current environment.
- No network, Overleaf, GitHub CLI, Pandoc, or LaTeX workflow is required or validated by this release.

## Remaining Before v1.0

- Run `scripts/dev/clean_install_audit.py` from a committed or pushed release branch.
- Confirm GitHub Actions are green on all matrix entries.
- Decide whether any legacy exit-code behavior needs normalization before v1.0.
- Confirm the public CLI, schema, diagnostic, and exit-code contracts are acceptable as the v1.0 freeze.

## Ready Status

v0.9.3 is ready for review.

## Exact Git Commands

```bash
git status --short
git add .github/workflows/tests.yml CHANGELOG.md README.md ROADMAP.md V0_9_3_CONTRACT_FREEZE_REPORT.md contracts/cli_commands.yaml contracts/diagnostic_codes.yaml contracts/exit_codes.yaml contracts/schema_names.yaml docs/cli_reference.md docs/contract.md docs/deprecation_policy.md docs/error_codes.md docs/schema_reference.md docs/v1_0_readiness.md docs/versioning_policy.md pyproject.toml scripts/dev/check_contracts.py src/paper_scaffold/__init__.py src/paper_scaffold/schema_reference.py tests/test_v09_release_candidate.py tests/test_v093_contract_freeze.py
git commit -m "Freeze public contract metadata"
git push -u origin v0.9.3-contract-freeze
git checkout main
git pull --ff-only
git merge --no-ff v0.9.3-contract-freeze
git tag -a v0.9.3 -m "Paper Scaffold v0.9.3"
git push origin main
git push origin v0.9.3
```
