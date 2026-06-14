from pathlib import Path
import re
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(*parts: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *parts],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_v097_public_docs_exist():
    docs = [
        "docs/start_here.md",
        "docs/common_paths.md",
        "docs/one_page_reference.md",
        "docs/glossary.md",
        "docs/walkthroughs/README.md",
        "docs/walkthroughs/five_minute_demo.md",
        "docs/walkthroughs/python_outputs_to_manuscript.md",
        "docs/walkthroughs/existing_latex_cleanup.md",
        "docs/walkthroughs/pre_submission_package.md",
        "docs/walkthroughs/reviewer_response_round.md",
    ]
    for rel in docs:
        assert (REPO_ROOT / rel).exists(), rel


def test_v097_docs_links_checker_passes():
    result = run_script("scripts/dev/check_docs_links.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "local Markdown links: ok" in result.stdout


def test_v097_docs_examples_checker_passes():
    result = run_script("scripts/dev/check_docs_examples.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "required docs: ok" in result.stdout
    assert "CLI reference command headings: ok" in result.stdout


def test_v097_readme_links_new_entry_points():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for link in [
        "docs/start_here.md",
        "docs/common_paths.md",
        "docs/one_page_reference.md",
        "docs/walkthroughs/README.md",
        "docs/cli_reference.md",
        "docs/glossary.md",
    ]:
        assert link in readme


def test_v097_quickstart_mentions_core_paths_and_commands():
    quickstart = (REPO_ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    for needle in [
        "docs/start_here.md",
        "docs/common_paths.md",
        "self-test",
        "demo",
        "validate",
        "discover-artifacts",
        "provenance-report",
        "package-submission",
        "reviewer-binder",
    ]:
        assert needle in quickstart


def test_v097_cli_reference_covers_all_parser_commands():
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from paper_scaffold.cli import build_parser  # noqa: PLC0415

    parser = build_parser()
    commands: set[str] | None = None
    for action in parser._actions:
        choices = getattr(action, "choices", None)
        if choices:
            commands = set(choices)
            break
    assert commands

    cli_doc = (REPO_ROOT / "docs" / "cli_reference.md").read_text(encoding="utf-8")
    headings = set(re.findall(r"^### `([^`]+)`", cli_doc, flags=re.MULTILINE))
    assert commands - headings == set()


def test_v097_contract_and_text_guards_still_pass():
    for script in ["check_contracts.py", "check_text_blobs.py"]:
        result = run_script(f"scripts/dev/{script}")
        assert result.returncode == 0, result.stdout + result.stderr


def test_v097_run_tests_help_works():
    result = run_script("scripts/dev/run_tests.py", "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--pytest-args" in result.stdout
