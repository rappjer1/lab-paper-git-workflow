"""Lightweight docs and examples drift checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from paper_scaffold.cli import build_parser  # noqa: E402


DOGFOOD_SCENARIOS = [
    "python_outputs_to_manuscript",
    "existing_latex_cleanup",
    "reviewer_response_round",
    "submission_package",
    "messy_project_audit",
]


REQUIRED_DOCS = [
    "README.md",
    "QUICKSTART.md",
    "docs/start_here.md",
    "docs/common_paths.md",
    "docs/one_page_reference.md",
    "docs/glossary.md",
    "docs/privacy_and_data_safety.md",
    "docs/github_repo_settings.md",
    "docs/release_reports.md",
    "docs/getting_started.md",
    "docs/which_workflow.md",
    "docs/cli_reference.md",
    "docs/schema_reference.md",
    "docs/contract.md",
    "docs/v1_0_readiness.md",
    "docs/example_integrity.md",
    "PUBLIC_RELEASE_CHECKLIST.md",
    "V1_0_RELEASE_NOTES_DRAFT.md",
    "V1_0_FINAL_CHECKLIST.md",
    "V0_9_9_RELEASE_CANDIDATE_REPORT.md",
    "docs/walkthroughs/README.md",
    "docs/walkthroughs/five_minute_demo.md",
    "docs/walkthroughs/python_outputs_to_manuscript.md",
    "docs/walkthroughs/existing_latex_cleanup.md",
    "docs/walkthroughs/pre_submission_package.md",
    "docs/walkthroughs/reviewer_response_round.md",
    "examples/README.md",
]


README_LINKS = [
    "docs/start_here.md",
    "docs/common_paths.md",
    "docs/one_page_reference.md",
    "docs/walkthroughs/README.md",
    "docs/which_workflow.md",
    "docs/cli_reference.md",
    "docs/schema_reference.md",
    "docs/contract.md",
    "docs/glossary.md",
    "docs/privacy_and_data_safety.md",
    "docs/github_repo_settings.md",
    "docs/release_reports.md",
    "docs/v1_0_readiness.md",
    "docs/example_integrity.md",
]

QUICKSTART_LINKS = [
    "docs/start_here.md",
    "docs/common_paths.md",
    "docs/one_page_reference.md",
    "docs/walkthroughs/README.md",
    "docs/cli_reference.md",
    "docs/privacy_and_data_safety.md",
]


def cli_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        choices = getattr(action, "choices", None)
        if choices:
            return set(choices)
    raise RuntimeError("argparse subcommands not found")


def main() -> int:
    problems: list[str] = []
    for rel in REQUIRED_DOCS:
        if not (REPO_ROOT / rel).exists():
            problems.append(f"missing required doc: {rel}")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for link in README_LINKS:
        if link not in readme:
            problems.append(f"README missing link: {link}")

    quickstart = (REPO_ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    for link in QUICKSTART_LINKS:
        if link not in quickstart:
            problems.append(f"QUICKSTART missing link: {link}")

    examples_readme = (REPO_ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    for scenario in DOGFOOD_SCENARIOS:
        link = f"dogfood/{scenario}"
        if link not in examples_readme:
            problems.append(f"examples README missing dogfood link: {link}")

    for scenario in DOGFOOD_SCENARIOS:
        folder = REPO_ROOT / "examples" / "dogfood" / scenario
        readme_path = folder / "README.md"
        if not folder.exists():
            problems.append(f"missing dogfood folder: {folder.relative_to(REPO_ROOT).as_posix()}")
            continue
        if not readme_path.exists():
            problems.append(f"missing dogfood README: {readme_path.relative_to(REPO_ROOT).as_posix()}")
            continue
        text = readme_path.read_text(encoding="utf-8")
        if "```" not in text or "paper-scaffold.py" not in text:
            problems.append(f"dogfood README lacks command snippet: {readme_path.relative_to(REPO_ROOT).as_posix()}")
        if not ((folder / "input").exists() or (folder / "project").exists()):
            problems.append(f"dogfood scenario lacks input/ or project/: {folder.relative_to(REPO_ROOT).as_posix()}")
        for required in ["expected_commands.md", "expected_outputs.md"]:
            if not (folder / required).exists():
                problems.append(f"missing dogfood file: {(folder / required).relative_to(REPO_ROOT).as_posix()}")

    cli_doc = (REPO_ROOT / "docs" / "cli_reference.md").read_text(encoding="utf-8")
    headings = set(re.findall(r"^### `([^`]+)`", cli_doc, flags=re.MULTILINE))
    commands = cli_commands()
    missing = sorted(commands - headings)
    extra = sorted(headings - commands)
    if missing:
        problems.append("CLI reference missing commands: " + ", ".join(missing))
    if extra:
        problems.append("CLI reference has unknown commands: " + ", ".join(extra))

    print("Docs/examples check")
    if problems:
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("- required docs: ok")
    print("- README links: ok")
    print("- QUICKSTART links: ok")
    print("- examples README dogfood links: ok")
    print("- dogfood examples: ok")
    print("- CLI reference command headings: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
