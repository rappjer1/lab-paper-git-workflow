# Versioning Policy

Paper Scaffold v0.9.x is pre-1.0 release-candidate hardening. The project is documenting command, schema, diagnostic, and exit-code contracts before freezing v1.0.

## Pre-1.0 Policy

Patch releases in v0.9.x should be narrow hardening releases. They may add maintainer tooling, documentation, tests, and small compatibility fixes. They should not add major product workflows.

## Intended v1.0+ Policy

After v1.0, Paper Scaffold should follow semantic versioning:

- Patch: bug fixes, docs fixes, compatibility hardening, new tests, and non-breaking diagnostic or report additions.
- Minor: new commands, optional flags, new generated report fields, and backward-compatible schema additions.
- Major: removed commands, removed flags, breaking schema changes, incompatible generated JSON changes, or changed diagnostic code meaning.

## Docs-Only Changes

Docs-only corrections can be patch releases. Docs that announce new public behavior should ship with tests or contract metadata updates.

## Diagnostic Changes

Adding a new diagnostic code is usually minor or patch, depending on scope. Changing the meaning or severity of an existing documented code is breaking after v1.0 unless the code was explicitly marked provisional.

## Schema Changes

Adding optional accepted fields is backward-compatible. Adding required fields to user-authored schemas is breaking after v1.0 unless defaults preserve old files. Generated JSON files may add fields, but patch and minor releases should not remove fields.
