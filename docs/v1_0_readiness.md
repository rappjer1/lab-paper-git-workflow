# v1.0 Readiness Checklist

Use this as the authoritative checklist before tagging v1.0.

## Release-Candidate Audit

- `scripts/dev/release_candidate_audit.py --output scratch/release-candidate` passes from a clean working tree.
- The release-candidate audit report has no required failures.
- Any skipped optional checks are explained in the report and reviewed before tagging.
- Clean-install checks are run from a clean branch, not from an uncommitted working tree.
- Clean-clone dogfood is run without `--skip-clean-clone`.

## Core Local Checks

- Text blob guard passes with `scripts/dev/check_text_blobs.py`.
- Root layout check passes with `scripts/dev/check_root_layout.py`.
- Contract audit passes with `scripts/dev/check_contracts.py`.
- Docs/examples check passes with `scripts/dev/check_docs_examples.py`.
- Docs link check passes with `scripts/dev/check_docs_links.py`.
- Example integrity check passes with `scripts/dev/check_example_integrity.py`.
- Public safety audit passes with `scripts/dev/check_public_safety.py`.
- Dogfood scenarios pass with `scripts/dev/run_dogfood.py`.
- Self-test passes with `scripts/paper-scaffold.py self-test`.
- Full tests pass with `scripts/dev/run_tests.py`.

## Install And Invocation

- Clean install audit passes with `scripts/dev/clean_install_audit.py`.
- Install matrix audit passes with `scripts/dev/install_matrix_audit.py`.
- Editable install succeeds.
- Installed console script works when the environment script directory is on `PATH`.
- `python -m paper_scaffold` fallback passes.
- Local package build is tested with `scripts/dev/build_package.py` when the build frontend is installed.
- Local wheel and sdist artifacts are inspected locally; no PyPI publishing is performed for v1.0 unless a separate release decision changes that.

## Public Contract

- CLI reference matches argparse command names and documented flags.
- `contracts/cli_commands.yaml` matches implementation commands.
- Schema reference matches `paper-scaffold schema list`.
- `contracts/schema_names.yaml` matches schema names.
- Diagnostic codes in `messages.py` are all documented.
- Exit codes are documented.
- Command names, documented flags, schema names, diagnostic codes, and exit-code conventions are acceptable to freeze at v1.0.

## Documentation And Public Safety

- README first-run path is clear.
- `docs/start_here.md`, `docs/common_paths.md`, and walkthroughs are linked from README and QUICKSTART.
- README first-run path has been reviewed from a new-user perspective.
- Public docs contain no local paths, credentials, nonpublic research content, or project-specific research terms.
- User-facing docs contain no machine-specific local paths.
- `docs/privacy_and_data_safety.md`, `docs/github_repo_settings.md`, and `docs/release_reports.md` are current.
- [V1_0_RELEASE_NOTES_DRAFT.md](release_reports/V1_0_RELEASE_NOTES_DRAFT.md) has been reviewed.
- [V1_0_FINAL_CHECKLIST.md](release_reports/V1_0_FINAL_CHECKLIST.md) is complete.

## Repository And CI

- Repository contains no large/generated raw outputs.
- Synthetic examples validate.
- GitHub Actions are green on supported operating systems and Python versions.
- Release process is documented.
- v1.0 tag commands are reviewed before execution.
