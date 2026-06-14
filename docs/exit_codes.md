# Exit Codes

Paper Scaffold v0.9 documents the intended pre-1.0 exit-code convention.

| Exit code | Meaning |
| --- | --- |
| `0` | Success or no blocking issues. |
| `1` | Unexpected runtime failure, user-input failure, or pre-1.0 blocking finding from legacy checks. |
| `2` | Validation/check errors, invalid command input, missing required paths, or overwrite protection. |

Warnings usually do not block unless a command explicitly treats them as blocking. Most warning-only checks return `0`.

## Current Notes

Some older check commands still return `1` when blocking findings are present. v1.0 should freeze the command-by-command behavior and avoid further exit-code drift.

## Practical Use In Scripts

For CI or local smoke tests:

```bash
paper-scaffold self-test
paper-scaffold validate --manuscript-repo ./paper
paper-scaffold release-check --manuscript-repo ./paper
```

Treat nonzero exits as requiring review. Use diagnostic codes and generated reports for details.
