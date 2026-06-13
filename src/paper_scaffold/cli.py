"""Command line interface for paper_scaffold."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Any

from .artifact_manifest import SUPPORTED_ARTIFACT_TYPES, append_artifact, copy_artifacts
from .config import ManuscriptConfig
from .git_helpers import git_summary
from .scaffold import InitOptions, init_manuscript
from .terminology import find_banned_terms, format_terminology_hits
from .validation import forbidden_file_matches, large_files, validate_manuscript_repo


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
        research_repo=args.research_repo or "R:/Code/my_project",
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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
