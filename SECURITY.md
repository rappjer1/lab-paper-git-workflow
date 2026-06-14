# Security

Paper Scaffold does not require API keys, credentials, access tokens, or cloud secrets for core checks. Core validation, demo, provenance, packaging, public-safety, and test-runner workflows make no network calls.

Do not submit private documents, credentials, unpublished data, confidential manuscript text, sensitive research data, raw data, model outputs, or large generated artifacts in public GitHub issues or pull requests.

Examples in this repository are synthetic and intentionally small.

`paper-scaffold privacy-check` and `scripts/dev/check_public_safety.py` are heuristic checks. They can catch common local paths, secret-like strings, and unsafe public-repo patterns, but they are not a substitute for manual review before making a repository public.

If you find a security concern, report it privately to the repository maintainer if possible. If private reporting is not available, open a minimal public issue that describes the type of concern without including secrets, private files, confidential text, or sensitive data.
