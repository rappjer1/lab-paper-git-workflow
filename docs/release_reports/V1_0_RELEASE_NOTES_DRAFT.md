# Paper Scaffold v1.0.0 Release Notes Draft

Paper Scaffold is a local-first CLI and documentation set for creating clean manuscript repositories from selected research outputs.

## Who It Is For

Paper Scaffold is for researchers and maintainers who want to separate manuscript source from research code, generated output trees, and exploratory artifacts. It is useful when a manuscript repository needs selected figures, tables, metadata, provenance notes, and sharing checks before GitHub or Overleaf handoff.

## What v1.0 Stabilizes

v1.0 stabilizes the current command names, documented flags, schema names, diagnostic codes, and exit-code conventions used by normal manuscript workflows.

Stable workflow areas:

- No-install CLI usage from a source checkout.
- Editable install usage.
- `python -m paper_scaffold` fallback invocation.
- Manuscript scaffold creation and synthetic demo generation.
- Artifact discovery, copy, provenance, status, freeze, and lock comparison.
- Manuscript validation, release checks, and focused checks for figures, citations, labels, GitHub readiness, Overleaf readiness, and privacy review.
- Manuscript CI workflow generation.
- Submission package creation.
- Reviewer-response binder creation.
- Public contract, schema, diagnostic, and release-process documentation.

## What It Does Not Do

Paper Scaffold does not write the manuscript, choose scientific claims, compile LaTeX, upload to Overleaf, create remote repositories, publish packages, or require network access for core local checks.

## Upgrade Notes

From v0.9.x, no migration is expected for normal generated demo repositories, artifact manifests, provenance reports, or validation reports. Before tagging v1.0, maintainers should run the release-candidate audit and review any skipped optional checks.

Recommended maintainer checks:

```bash
python scripts/dev/release_candidate_audit.py --output scratch/release-candidate
python scripts/dev/run_tests.py
python scripts/dev/check_public_safety.py
```

## First Commands

Run from a checkout:

```bash
python scripts/paper-scaffold.py --help
python scripts/paper-scaffold.py self-test
python scripts/paper-scaffold.py demo --output scratch/demo_manuscript --overwrite
python scripts/paper-scaffold.py validate --manuscript-repo scratch/demo_manuscript
```

Editable install:

```bash
python -m pip install -e ".[dev]"
paper-scaffold --help
python -m paper_scaffold --help
```

## Known Limitations

- Package publishing is not part of this release note draft.
- LaTeX/Pandoc compilation remains outside the core tool.
- GitHub and Overleaf setup steps remain user-controlled.
- The tool validates and packages selected artifacts; it does not judge scientific correctness.
