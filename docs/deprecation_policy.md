# Deprecation Policy

Paper Scaffold is still pre-1.0. v0.9.x is the compatibility-hardening series that prepares the public interface for v1.0.

## After v1.0

Avoid removing public commands after v1.0 without a deprecation period.

Deprecations should warn for at least one minor release before removal. Where cheap, keep aliases longer than the minimum window, especially for command names and commonly used flags.

Schema fields should be accepted for at least one compatibility window after replacement. Generated reports may add fields, but consumers should not be forced to migrate on a patch release.

Breaking changes require a major version after v1.0.

## What Should Warn

- Command renames.
- Flag renames.
- Schema field replacements.
- Diagnostic code retirement.
- Exit-code behavior changes.

## What Usually Does Not Need Deprecation

- Adding optional flags.
- Adding diagnostic codes.
- Adding generated JSON fields.
- Improving prose in reports or docs.
- Fixing behavior that was clearly a bug and not documented as public contract.
