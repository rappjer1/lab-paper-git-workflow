# ADR 0005: Packaging And Release Strategy

- Status: accepted

## Context

Paper Scaffold is public and installable from GitHub source. It is not yet published to PyPI.

## Decision

Remain GitHub-source-installable for v0.5. Prepare the project for PyPI later by keeping package metadata clean, versions explicit, and tests/CI reliable.

Do not add a PyPI publishing workflow in v0.5. PyPI Trusted Publishing is the preferred future release route when the package is ready.

## Consequences

Release risk stays low. Users can install with `python -m pip install -e .` or from a GitHub checkout. Publishing credentials are not introduced.

## Alternatives Considered

- Publish immediately to PyPI: premature before schema and CLI stability.
- Add manual token-based publishing: not needed and less secure than Trusted Publishing.
- uv: useful for fast development workflows, but not needed for normal users or v0.5 CI.
- Hatch: strong packaging/build workflow, but setuptools is sufficient for the current source-installable package.
- Stay source-installable: appropriate for current maturity.

## What Would Make Us Revisit This?

Revisit for v0.8 or later when the CLI, schema, and docs are stable enough for broader package distribution.
