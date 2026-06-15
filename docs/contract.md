# Public Contract

Paper Scaffold v0.9.9 documents the public interface that is intended to become stable at v1.0.

## Command Contract

Command names are part of the public interface. The top-level `paper-scaffold` command names listed in [cli_reference.md](cli_reference.md) and `contracts/cli_commands.yaml` should not be removed or repurposed without the deprecation process after v1.0.

Command flags listed in the CLI reference are also part of the public interface. New optional flags may be added in minor releases, but existing documented flags should keep their meaning after v1.0 unless a major-version change is made.

`paper-scaffold` remains the console-script command name. `python -m paper_scaffold` remains the installed-use fallback.

## Diagnostic Contract

Diagnostic codes are stable once documented in [error_codes.md](error_codes.md) and `contracts/diagnostic_codes.yaml`.

New diagnostic codes may be added. Existing documented codes should not silently change severity or meaning after v1.0. If a code must be retired, keep `paper-scaffold explain <code>` useful for at least one compatibility window.

## Schema Contract

User-authored schemas are:

- `artifact_manifest.yaml`
- `manuscript_config.yaml`
- `terminology_map.yaml`

These should remain backward-compatible after v1.0. New optional fields may be accepted, but existing required fields should keep their meaning.

Generated JSON reports, ledgers, and locks may add fields after v1.0. They should not silently remove fields or change field meaning in patch or minor releases.

## Exit-Code Contract

Exit-code conventions are documented in [exit_codes.md](exit_codes.md) and `contracts/exit_codes.yaml`. After v1.0, command exit behavior should remain stable enough for CI scripts and local release checks.

## File-Moving Contract

Commands that create, copy, package, or overwrite files should keep explicit dry-run, output path, or overwrite safeguards where applicable. In particular, commands that replace an existing folder or generated workflow should continue to require an explicit overwrite flag.

## Dev Scripts

Maintainer scripts under `scripts/dev/`, including `run_tests.py`, `check_text_blobs.py`, `check_contracts.py`, `clean_install_audit.py`, `build_package.py`, and `install_matrix_audit.py`, are release tooling. They are documented for contributors but are not normal manuscript-user workflows.
