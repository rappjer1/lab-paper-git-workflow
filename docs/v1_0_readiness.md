# v1.0 Readiness Checklist

Use this checklist before tagging v1.0.

- Clean clone audit passes with `scripts/dev/clean_install_audit.py`.
- Editable install succeeds.
- Installed console script works when the environment script directory is on `PATH`.
- `python -m paper_scaffold` fallback passes.
- Text blob guard passes.
- Contract audit passes with `scripts/dev/check_contracts.py`.
- CLI reference matches argparse command names and documented flags.
- Schema reference matches `paper-scaffold schema list`.
- Diagnostic codes in `messages.py` are all documented.
- Exit codes are documented.
- GitHub Actions are green on supported operating systems and Python versions.
- README first-run path is clear.
- Public docs contain no private paths, credentials, unpublished research content, or project-specific research terms.
- Repository contains no large/generated raw outputs.
- Synthetic examples validate.
- Release process is documented.
- v1.0 tag commands are reviewed before execution.
