# v0.9.2 Clean Install Audit Report

Branch: `v0.9.2-clean-install-audit`

Version: `0.9.2`

## Problem Fixed

v0.9.2 adds a maintainer-facing clean-install audit so release candidates can verify the public-user path from a fresh clone through no-install usage, editable install, module fallback, text-blob checks, and the shell-independent test runner.

## Files Changed

- `scripts/dev/clean_install_audit.py`
- `docs/clean_install_audit.md`
- `docs/install.md`
- `docs/compatibility.md`
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `pyproject.toml`
- `src/paper_scaffold/__init__.py`
- `src/paper_scaffold/schema_reference.py`
- `docs/schema_reference.md`
- `tests/test_v09_release_candidate.py`
- `tests/test_v092_clean_install_audit.py`
- `V0_9_2_CLEAN_INSTALL_AUDIT_REPORT.md`

## Audit Coverage

The audit script checks:

- fresh clone into `scratch/clean-install/` or `--clone-path`;
- no-install wrapper help and self-test;
- editable install with `python -m pip install -e ".[dev]"`;
- installed `paper-scaffold --help` when available on `PATH`;
- `python -m paper_scaffold --help`;
- installed-use self-test through the module fallback;
- text blob guard;
- full tests through `scripts/dev/run_tests.py`;
- optional package build when `build` is installed.

## Validation Results

Passed:

- `<python> scripts/dev/check_text_blobs.py`
- `<python> scripts/dev/run_tests.py`
- `<python> scripts/paper-scaffold.py --version`
- `<python> -m paper_scaffold --help`
- `<python> scripts/paper-scaffold.py self-test --output scratch/self_test --keep-output`
- `<python> scripts/dev/clean_install_audit.py --help`
- `<python> -m ruff check .`

Observed results:

- Version output: `paper-scaffold 0.9.2`
- Full test suite: `91 passed in 26.54s`
- Self-test: 10 steps passed, 0 failed
- Text blob guard: all tracked text blobs passed
- Ruff: passed

The full clean-install audit script was not run against this uncommitted working tree because Git clones do not include uncommitted changes. Run it after committing or from a pushed release branch to audit the exact public-user source.

## Known Limitations

- The clean-install audit may require network access if `--source` points to a remote repository.
- Editable install with `.[dev]` may require package-index access if pytest or other dev dependencies are not already installed.
- Git clones do not include uncommitted working-tree edits; run the audit from a committed source or a pushed branch when validating release candidates.
- The installed console-script and package-build checks are optional because PATH and local build tooling vary by machine.
- v0.9.2 does not add product workflows, publish to PyPI, rename the project, or change repository visibility.

## Ready Status

v0.9.2 is ready for review.

## Exact Git Commands

```bash
git status --short
git add CHANGELOG.md CONTRIBUTING.md V0_9_2_CLEAN_INSTALL_AUDIT_REPORT.md docs/clean_install_audit.md docs/compatibility.md docs/install.md docs/schema_reference.md pyproject.toml scripts/dev/clean_install_audit.py src/paper_scaffold/__init__.py src/paper_scaffold/schema_reference.py tests/test_v09_release_candidate.py tests/test_v092_clean_install_audit.py
git commit -m "Add clean install audit"
git push -u origin v0.9.2-clean-install-audit
git checkout main
git pull --ff-only
git merge --no-ff v0.9.2-clean-install-audit
git tag -a v0.9.2 -m "Paper Scaffold v0.9.2"
git push origin main
git push origin v0.9.2
```
