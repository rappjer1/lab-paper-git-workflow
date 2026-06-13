"""Command line interface for paper_scaffold."""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from datetime import date
from pathlib import Path
from typing import Any

from .artifact_manifest import SUPPORTED_ARTIFACT_TYPES, append_artifact, copy_artifacts
from .checks import (
    check_citations,
    check_figures,
    check_github_repo,
    check_labels,
    check_overleaf,
    check_privacy,
    check_stale_artifacts,
    check_unused_artifacts,
    check_word_conversion,
    format_findings,
)
from .config import ManuscriptConfig, write_yaml
from .discovery import (
    ArtifactCandidate,
    append_candidates_to_manifest,
    copy_candidates,
    discover_artifacts,
    forbidden_skipped_paths,
    format_candidates,
)
from .doctor import format_doctor_checks, run_doctor
from .git_helpers import git_summary
from .messages import DiagnosticFinding, all_messages, format_message, get_message, severity_counts
from .scaffold import InitOptions, init_manuscript, project_config_from_options
from .terminology import find_banned_terms, format_terminology_hits
from .validation import (
    forbidden_file_matches,
    large_files,
    validate_manuscript_repo,
    validation_json_report,
    validation_markdown_report,
)
from .word import WORD_REVIEW_MESSAGE, import_word


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def prompt_bool(label: str, default: bool = True) -> bool:
    default_text = "Y/n" if default else "y/N"
    value = input(f"{label} [{default_text}]: ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes", "true", "1"}


def _default_dry_run_options(args: argparse.Namespace) -> InitOptions:
    manuscript_repo = args.manuscript_repo or str(Path.cwd() / "example_manuscript_repo")
    return InitOptions(
        research_repo=args.research_repo or "./research-project",
        manuscript_repo=manuscript_repo,
        title=args.title or "Example Manuscript",
        slug=args.slug or "example_project",
        has_supplement=args.has_supplement if args.has_supplement is not None else True,
        use_template=args.use_template if args.use_template is not None else True,
        github_repo=args.github_repo or "",
        overleaf_url=args.overleaf_url or "",
        branch_name=args.branch or "main",
        figure_dir=args.figure_dir or "figures",
        table_dir=args.table_dir or "tables",
        references_file=args.references_file or "",
    )


def _collect_init_options(args: argparse.Namespace) -> InitOptions:
    if args.dry_run or args.non_interactive:
        return _default_dry_run_options(args)
    return InitOptions(
        research_repo=args.research_repo or prompt_text("Research repo path"),
        manuscript_repo=args.manuscript_repo or prompt_text("Manuscript repo path", str(Path.cwd())),
        title=args.title or prompt_text("Manuscript title"),
        slug=args.slug or prompt_text("Short project slug"),
        has_supplement=args.has_supplement if args.has_supplement is not None else prompt_bool("Need supplement?", True),
        use_template=args.use_template if args.use_template is not None else prompt_bool("Start from template?", True),
        github_repo=args.github_repo or prompt_text("GitHub repo URL if known"),
        overleaf_url=args.overleaf_url or prompt_text("Overleaf project URL if known"),
        branch_name=args.branch or prompt_text("Preferred branch name", "main"),
        figure_dir=args.figure_dir or prompt_text("Default figure directory", "figures"),
        table_dir=args.table_dir or prompt_text("Default table directory", "tables"),
        references_file=args.references_file or prompt_text("References file path if copying now"),
    )


def command_init(args: argparse.Namespace) -> int:
    options = _collect_init_options(args)
    actions = init_manuscript(options, dry_run=args.dry_run, overwrite=args.overwrite)
    if args.dry_run:
        print("Dry-run init plan:")
    else:
        print("Initialized manuscript repo:", options.manuscript_repo)
    for action in actions:
        print("-", action)
    return 0


def _collect_artifact(args: argparse.Namespace) -> dict[str, Any]:
    artifact_type = args.type or prompt_text("Artifact type", "figure")
    if artifact_type not in SUPPORTED_ARTIFACT_TYPES:
        raise SystemExit(f"Unsupported artifact type: {artifact_type}")
    artifact = {
        "id": args.id or prompt_text("Artifact ID"),
        "type": artifact_type,
        "manuscript_path": args.destination or prompt_text("Destination path in manuscript repo"),
        "source_repo": args.source_repo or prompt_text("Source research repo path"),
        "source_path": args.source_path or prompt_text("Source path relative to source repo or absolute"),
        "generated_by": args.generated_by or prompt_text("Source script", ""),
        "input_data": args.input_data or prompt_text("Input data summary", ""),
        "last_updated": args.last_updated or date.today().isoformat(),
        "caption_hint": args.caption_hint or prompt_text("Caption hint", ""),
        "status": args.status or prompt_text("Status", "draft"),
    }
    return artifact


def command_add_artifact(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    artifact = _collect_artifact(args)
    append_artifact(repo, artifact)
    print(f"Added artifact to {repo / 'metadata' / 'artifact_manifest.yaml'}: {artifact['id']}")
    copy_now = args.copy_now
    if copy_now is None and not args.non_interactive:
        copy_now = prompt_bool("Copy artifact now?", False)
    if copy_now:
        results = copy_artifacts(repo)
        for result in results:
            if result.artifact_id == artifact["id"]:
                print(f"{result.status}: {result.artifact_id}: {result.message}")
    return 0


def command_copy_artifacts(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    config = ManuscriptConfig.load(repo)
    results = copy_artifacts(repo, allow_directories=args.allow_directories, max_file_size_mb=config.max_file_size_mb)
    if not results:
        print("No artifacts listed in manifest.")
        return 0
    exit_code = 0
    for result in results:
        print(f"{result.status}: {result.artifact_id}")
        print(f"  source: {result.source}")
        print(f"  dest:   {result.destination}")
        if result.status == "missing":
            exit_code = 1
    return exit_code


def command_validate(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    report = validate_manuscript_repo(repo)
    print(report.format())
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(validation_markdown_report(repo), encoding="utf-8")
        print(f"Wrote validation report: {report_path}")
    if args.write_json:
        json_path = Path(args.write_json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(validation_json_report(repo), indent=2) + "\n", encoding="utf-8")
        print(f"Wrote validation JSON report: {json_path}")
    return 0 if report.ok else 1


def command_terminology_check(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    hits = find_banned_terms(repo)
    print(format_terminology_hits(hits, repo))
    return 1 if hits else 0


def command_git_check(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    config = ManuscriptConfig.load(repo)
    summary = git_summary(repo)
    print("Git check")
    print("- branch:", summary.get("branch") or "<not a git repo>")
    remotes = summary.get("remotes") or {}
    if remotes:
        for name, urls in remotes.items():
            print(f"- remote {name}: {', '.join(urls)}")
    else:
        print("- remote origin: missing")
    status = summary.get("status") or []
    print(f"- status entries: {len(status)}")
    for line in status[:30]:
        print("  ", line)
    if len(status) > 30:
        print(f"  ... {len(status) - 30} more")
    forbidden = forbidden_file_matches(repo, config.forbidden_patterns)
    for path in forbidden:
        print("WARNING forbidden artifact type/path:", path)
    for path, size_mb in large_files(repo, config.max_file_size_mb):
        print(f"WARNING large file: {path} ({size_mb:.1f} MB)")
    return 0


def command_overleaf_instructions(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    config = ManuscriptConfig.load(repo)
    project = config.project
    github_repo = project.get("github_repo") or "<private GitHub manuscript repo URL>"
    main_tex = project.get("main_tex") or "main.tex"
    print("Overleaf/GitHub workflow")
    print("1. Create a private GitHub repository for the manuscript if it does not already exist.")
    print(f"2. From the manuscript repo, push the branch to GitHub: {github_repo}")
    print("3. In Overleaf, create a new project from GitHub and select this manuscript repo.")
    print(f"4. Set the main document to {main_tex}.")
    print("5. Treat GitHub as canonical. Pull/sync in Overleaf after local commits.")
    print("6. Push from Overleaf only when edits were made there.")
    print("7. Avoid editing the same lines locally and in Overleaf at the same time.")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    print(format_doctor_checks(run_doctor(repo)))
    return 0


def command_import_word(args: argparse.Namespace) -> int:
    result = import_word(
        input_path=args.input,
        output_path=args.output,
        output_format=args.to,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )
    print("Pandoc command:")
    print("  " + " ".join(result.command))
    print(result.message)
    if args.split_sections:
        print("Section splitting is intentionally minimal in v0.2. Split the converted file at section headings into sections/*.tex and compare against the Word original.")
    print(WORD_REVIEW_MESSAGE)
    return 0 if result.ok else 2


def command_discover_artifacts(args: argparse.Namespace) -> int:
    candidates = discover_artifacts(args.source, supplement=args.supplement)
    print(format_candidates(candidates))
    skipped = forbidden_skipped_paths(args.source)
    if skipped:
        print(
            format_findings(
                [
                    DiagnosticFinding(
                        "W021",
                        f"{len(skipped)} raw/cache/output paths skipped",
                        Path(args.source).as_posix(),
                    )
                ]
            )
        )
    if not candidates:
        return 0

    if args.write:
        append_candidates_to_manifest(args.manifest, candidates)
        print(f"Appended {len(candidates)} candidate entries to {args.manifest}.")
    else:
        print("Suggest-only dry run. Pass --write to append these suggestions to the manifest.")

    if args.copy:
        manifest_path = Path(args.manifest)
        manuscript_repo = Path(args.manuscript_repo) if args.manuscript_repo else manifest_path.parent.parent
        copied = copy_candidates(manuscript_repo, candidates)
        print(f"Copied {len(copied)} artifacts into {manuscript_repo}.")
    else:
        print("No files copied. Pass --copy to copy candidates into the manuscript repo.")
    return 0


def command_make_slack_summary(args: argparse.Namespace) -> int:
    repo = Path(args.manuscript_repo or Path.cwd())
    config = ManuscriptConfig.load(repo)
    repo_url = config.project.get("github_repo") or "<GITHUB_REPO_URL>"
    docs_path = Path(__file__).resolve().parents[2] / "docs" / "public_launch.md"
    if docs_path.exists():
        message = docs_path.read_text(encoding="utf-8").replace("<GITHUB_REPO_URL>", str(repo_url))
    else:
        message = (
            "Paper Scaffold: <GITHUB_REPO_URL>\n\n"
            "Use it to create clean manuscript GitHub repos from Word drafts, Python outputs, and LaTeX projects.\n"
            "Start with `paper-scaffold doctor`, then `paper-scaffold validate`. Do not commit raw data or model outputs."
        ).replace("<GITHUB_REPO_URL>", str(repo_url))
    print(message)
    return 0


def command_quickstart(args: argparse.Namespace) -> int:
    print(
        """Paper Scaffold quickstart

Workflow 1: Word draft to Overleaf-ready repo
  paper-scaffold doctor
  paper-scaffold init --manuscript-repo ./paper
  paper-scaffold import-word --input draft.docx --output ./paper/converted.tex
  paper-scaffold validate --manuscript-repo ./paper
  Read: docs/word_to_overleaf.md

Workflow 2: Python outputs to paper
  paper-scaffold doctor
  paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml
  paper-scaffold discover-artifacts --source ./outputs/final --manifest ./paper/metadata/artifact_manifest.yaml --write --copy --manuscript-repo ./paper
  paper-scaffold validate --manuscript-repo ./paper
  Read: docs/python_outputs_to_overleaf.md

Workflow 3: Existing LaTeX to GitHub/Overleaf
  paper-scaffold doctor --manuscript-repo ./paper
  paper-scaffold validate --manuscript-repo ./paper
  git add .
  git commit -m "Clean manuscript repository"
  git push
  Read: docs/existing_latex_project.md and docs/github_overleaf_sync.md
"""
    )
    return 0


def command_demo(args: argparse.Namespace) -> int:
    output = Path(args.output)
    repo_root = Path(__file__).resolve().parents[2]
    example_outputs = repo_root / "examples" / "minimal_python_artifacts" / "outputs"
    if output.exists() and not args.overwrite:
        print(f"Output exists: {output}")
        print("Pass --overwrite to replace/update the demo manuscript.")
        return 2
    options = InitOptions(
        research_repo="examples/minimal_python_artifacts",
        manuscript_repo=str(output),
        title="Paper Scaffold Demo Manuscript",
        slug="paper_scaffold_demo",
        has_supplement=True,
        use_template=True,
    )
    actions = init_manuscript(options, dry_run=args.dry_run, overwrite=args.overwrite)
    if args.dry_run:
        print("Demo dry-run plan:")
        for action in actions:
            print("-", action)
        print(f"- copy example artifacts from {example_outputs}")
        print("- write artifact manifest entries")
        print("- run validation")
        return 0

    public_config_options = replace(options, manuscript_repo=output.name if output.is_absolute() else output.as_posix())
    write_yaml(output / "metadata" / "manuscript_config.yaml", project_config_from_options(public_config_options))

    manifest = output / "metadata" / "artifact_manifest.yaml"
    candidates = discover_artifacts(example_outputs)
    copy_candidates(output, candidates)
    entries = []
    display_candidates = []
    for candidate in candidates:
        source_rel = candidate.source_path.relative_to(repo_root / "examples" / "minimal_python_artifacts")
        display_source = Path("examples") / "minimal_python_artifacts" / source_rel
        display_candidates.append(
            ArtifactCandidate(
                source_path=display_source,
                artifact_id=candidate.artifact_id,
                artifact_type=candidate.artifact_type,
                manuscript_path=candidate.manuscript_path,
            )
        )
        entries.append(
            {
                "id": candidate.artifact_id,
                "type": candidate.artifact_type,
                "manuscript_path": candidate.manuscript_path,
                "source_repo": "examples/minimal_python_artifacts",
                "source_path": source_rel.as_posix(),
                "generated_by": "make_example_figure.py",
                "input_data": "synthetic data generated by example script",
                "last_updated": date.today().isoformat(),
                "caption_hint": "Synthetic demo artifact.",
                "status": "example",
            }
        )
    write_yaml(manifest, {"artifacts": entries})
    report = validate_manuscript_repo(output)
    print(f"Created demo manuscript: {output}")
    print(format_candidates(display_candidates))
    print(report.format())
    print("Next steps:")
    print(f"- Inspect {output}")
    print("- Run: paper-scaffold validate --manuscript-repo <demo-path>")
    print("- Try importing the manuscript repo into Overleaf after pushing it to GitHub.")
    return 0 if report.ok else 1


def _print_findings(findings: list) -> int:
    print(format_findings(findings))
    counts = severity_counts(findings)
    return 1 if counts.get("ERROR", 0) else 0


def command_explain(args: argparse.Namespace) -> int:
    if args.list:
        for message in all_messages():
            print(f"{message.code} [{message.severity}] {message.title}")
        return 0
    if not args.code:
        print("Provide a diagnostic code or pass --list.")
        return 2
    try:
        message = get_message(args.code)
    except KeyError:
        print(f"Unknown diagnostic code: {args.code}")
        print("Available codes:")
        for message in all_messages():
            print(f"- {message.code}: {message.title}")
        return 2
    print(format_message(message))
    return 0


def command_overleaf_check(args: argparse.Namespace) -> int:
    return _print_findings(check_overleaf(Path(args.manuscript_repo or Path.cwd())))


def command_github_check(args: argparse.Namespace) -> int:
    return _print_findings(check_github_repo(Path(args.repo or Path.cwd())))


def command_privacy_check(args: argparse.Namespace) -> int:
    findings = check_privacy(Path(args.path or Path.cwd()))
    if findings:
        print(format_findings(findings))
    else:
        print("No obvious private paths, credentials, or secret-like strings found.")
    return 0


def command_check_figures(args: argparse.Namespace) -> int:
    return _print_findings(check_figures(Path(args.manuscript_repo or Path.cwd())))


def command_check_citations(args: argparse.Namespace) -> int:
    return _print_findings(check_citations(Path(args.manuscript_repo or Path.cwd())))


def command_check_labels(args: argparse.Namespace) -> int:
    return _print_findings(check_labels(Path(args.manuscript_repo or Path.cwd())))


def command_audit_word_conversion(args: argparse.Namespace) -> int:
    findings = check_word_conversion(Path(args.input))
    output = format_findings(findings) if findings else "No common Word/Pandoc conversion issues found by heuristic checks."
    print(output)
    print(WORD_REVIEW_MESSAGE)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            "# Word Conversion Audit Report\n\n"
            f"- Input: {args.input}\n"
            f"- Findings: {len(findings)}\n\n"
            "```text\n"
            f"{output}\n"
            "```\n\n"
            f"{WORD_REVIEW_MESSAGE}\n",
            encoding="utf-8",
        )
        print(f"Wrote word conversion report: {report_path}")
    counts = severity_counts(findings)
    return 1 if counts.get("ERROR", 0) else 0


def command_stale_artifacts(args: argparse.Namespace) -> int:
    findings = check_stale_artifacts(Path(args.manuscript_repo or Path.cwd()))
    output = format_findings(findings) if findings else "No stale artifacts detected."
    print(output)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("# Stale Artifact Report\n\n```text\n" + output + "\n```\n", encoding="utf-8")
        print(f"Wrote stale artifact report: {report_path}")
    counts = severity_counts(findings)
    return 1 if counts.get("ERROR", 0) else 0


def command_unused_artifacts(args: argparse.Namespace) -> int:
    findings = check_unused_artifacts(Path(args.manuscript_repo or Path.cwd()))
    output = format_findings(findings) if findings else "No unused manuscript artifacts detected."
    print(output)
    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("# Unused Artifact Report\n\n```text\n" + output + "\n```\n", encoding="utf-8")
        print(f"Wrote unused artifact report: {report_path}")
    counts = severity_counts(findings)
    return 1 if counts.get("ERROR", 0) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="paper-scaffold", description="Create and validate clean manuscript Git repositories.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create a manuscript repository scaffold")
    init.add_argument("--dry-run", action="store_true", help="Print the planned scaffold without writing files")
    init.add_argument("--non-interactive", action="store_true", help="Use defaults and provided flags without prompting")
    init.add_argument("--overwrite", action="store_true", help="Overwrite existing template files")
    init.add_argument("--research-repo")
    init.add_argument("--manuscript-repo")
    init.add_argument("--title")
    init.add_argument("--slug")
    init.add_argument("--has-supplement", dest="has_supplement", action="store_true", default=None)
    init.add_argument("--no-supplement", dest="has_supplement", action="store_false")
    init.add_argument("--use-template", dest="use_template", action="store_true", default=None)
    init.add_argument("--no-template", dest="use_template", action="store_false")
    init.add_argument("--github-repo")
    init.add_argument("--overleaf-url")
    init.add_argument("--branch")
    init.add_argument("--figure-dir")
    init.add_argument("--table-dir")
    init.add_argument("--references-file")
    init.set_defaults(func=command_init)

    add = subparsers.add_parser("add-artifact", help="Add one figure/table entry to the artifact manifest")
    add.add_argument("--manuscript-repo")
    add.add_argument("--non-interactive", action="store_true")
    add.add_argument("--id")
    add.add_argument("--type", choices=sorted(SUPPORTED_ARTIFACT_TYPES))
    add.add_argument("--source-repo")
    add.add_argument("--source-path")
    add.add_argument("--destination")
    add.add_argument("--caption-hint")
    add.add_argument("--generated-by")
    add.add_argument("--input-data")
    add.add_argument("--last-updated")
    add.add_argument("--status")
    add.add_argument("--copy-now", dest="copy_now", action="store_true", default=None)
    add.add_argument("--no-copy-now", dest="copy_now", action="store_false")
    add.set_defaults(func=command_add_artifact)

    validate = subparsers.add_parser("validate", help="Validate a manuscript repository")
    validate.add_argument("--manuscript-repo")
    validate.add_argument("--write-report", help="Write a Markdown validation report")
    validate.add_argument("--write-json", help="Write a JSON validation report")
    validate.set_defaults(func=command_validate)

    copy = subparsers.add_parser("copy-artifacts", help="Copy files listed in the artifact manifest")
    copy.add_argument("--manuscript-repo")
    copy.add_argument("--allow-directories", action="store_true")
    copy.set_defaults(func=command_copy_artifacts)

    terms = subparsers.add_parser("terminology-check", help="Search manuscript text for banned implementation labels")
    terms.add_argument("--manuscript-repo")
    terms.set_defaults(func=command_terminology_check)

    git = subparsers.add_parser("git-check", help="Show branch, remotes, status, and artifact warnings")
    git.add_argument("--manuscript-repo")
    git.set_defaults(func=command_git_check)

    overleaf = subparsers.add_parser("overleaf-instructions", help="Print project-specific Overleaf sync instructions")
    overleaf.add_argument("--manuscript-repo")
    overleaf.set_defaults(func=command_overleaf_instructions)

    doctor = subparsers.add_parser("doctor", help="Check local tools and manuscript repo shape")
    doctor.add_argument("--manuscript-repo")
    doctor.set_defaults(func=command_doctor)

    import_word_parser = subparsers.add_parser("import-word", help="Convert a Word docx draft with Pandoc when available")
    import_word_parser.add_argument("--input", required=True, help="Input .docx file")
    import_word_parser.add_argument("--output", required=True, help="Output .tex or .md file")
    import_word_parser.add_argument("--to", choices=["latex", "markdown"], default="latex")
    import_word_parser.add_argument("--split-sections", action="store_true", help="Print section splitting guidance after conversion")
    import_word_parser.add_argument("--dry-run", action="store_true")
    import_word_parser.add_argument("--overwrite", action="store_true")
    import_word_parser.set_defaults(func=command_import_word)

    discover = subparsers.add_parser("discover-artifacts", help="Find likely manuscript artifacts in an output folder")
    discover.add_argument("--source", required=True)
    discover.add_argument("--manifest", required=True)
    discover.add_argument("--manuscript-repo", help="Manuscript repo root used with --copy")
    discover.add_argument("--write", action="store_true", help="Append candidates to the manifest")
    discover.add_argument("--copy", action="store_true", help="Copy candidates into figures/tables folders")
    discover.add_argument("--suggest-only", action="store_true", help="Alias for the default dry-run behavior")
    discover.add_argument("--supplement", action="store_true", help="Suggest supplement figure/table destinations")
    discover.set_defaults(func=command_discover_artifacts)

    slack = subparsers.add_parser("make-slack-summary", help="Print a Slack-ready launch message")
    slack.add_argument("--manuscript-repo")
    slack.set_defaults(func=command_make_slack_summary)

    quickstart = subparsers.add_parser("quickstart", help="Print the three common Paper Scaffold workflows")
    quickstart.set_defaults(func=command_quickstart)

    demo = subparsers.add_parser("demo", help="Create a small demo manuscript repository")
    demo.add_argument("--output", default="scratch/demo_manuscript")
    demo.add_argument("--overwrite", action="store_true")
    demo.add_argument("--dry-run", action="store_true")
    demo.set_defaults(func=command_demo)

    explain = subparsers.add_parser("explain", help="Explain a diagnostic code")
    explain.add_argument("code", nargs="?", help="Diagnostic code such as E003")
    explain.add_argument("--list", action="store_true", help="List all diagnostic codes")
    explain.set_defaults(func=command_explain)

    overleaf_check = subparsers.add_parser("overleaf-check", help="Check whether a manuscript repo is likely Overleaf-ready")
    overleaf_check.add_argument("--manuscript-repo")
    overleaf_check.set_defaults(func=command_overleaf_check)

    github_check = subparsers.add_parser("github-check", help="Check GitHub-readiness for a repository")
    github_check.add_argument("--repo")
    github_check.set_defaults(func=command_github_check)

    privacy_check = subparsers.add_parser("privacy-check", help="Search for private paths, credentials, and secret-like text")
    privacy_check.add_argument("--path")
    privacy_check.set_defaults(func=command_privacy_check)

    figure_check = subparsers.add_parser("check-figures", help="Check figure references and figure files")
    figure_check.add_argument("--manuscript-repo")
    figure_check.set_defaults(func=command_check_figures)

    citation_check = subparsers.add_parser("check-citations", help="Check citation keys against references.bib")
    citation_check.add_argument("--manuscript-repo")
    citation_check.set_defaults(func=command_check_citations)

    label_check = subparsers.add_parser("check-labels", help="Check LaTeX labels and references")
    label_check.add_argument("--manuscript-repo")
    label_check.set_defaults(func=command_check_labels)

    word_audit = subparsers.add_parser("audit-word-conversion", help="Audit converted Word/Pandoc TeX or Markdown")
    word_audit.add_argument("--input", required=True)
    word_audit.add_argument("--write-report")
    word_audit.set_defaults(func=command_audit_word_conversion)

    stale = subparsers.add_parser("stale-artifacts", help="Report manifest artifacts whose source changed after copying")
    stale.add_argument("--manuscript-repo")
    stale.add_argument("--write-report")
    stale.set_defaults(func=command_stale_artifacts)

    unused = subparsers.add_parser("unused-artifacts", help="Report figure/table files that are not referenced by TeX source")
    unused.add_argument("--manuscript-repo")
    unused.add_argument("--write-report")
    unused.set_defaults(func=command_unused_artifacts)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
