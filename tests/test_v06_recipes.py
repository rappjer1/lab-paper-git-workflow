from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.cli import main


REPO_ROOT = Path(__file__).resolve().parents[1]
USE_CASE_IDS = [
    "word-to-overleaf",
    "python-artifact-handoff",
    "existing-latex-cleanup",
    "overleaf-zip-rehab",
    "paper-archaeology",
    "reviewer-response-binder",
    "undergraduate-artifact-harvest",
    "pre-submission-flight-check",
    "multi-paper-project-split",
]


def test_recipes_list_works(capsys):
    assert main(["recipes", "list"]) == 0
    output = capsys.readouterr().out
    assert "Available recipes:" in output
    assert "word-to-overleaf" in output
    assert "paper-archaeology" in output
    assert "pre-submission-flight-check" in output


def test_recipes_show_known_works(capsys):
    assert main(["recipes", "show", "paper-archaeology"]) == 0
    output = capsys.readouterr().out
    assert "paper-archaeology: Paper Archaeology" in output
    assert "Recommended commands:" in output
    assert "paper-scaffold audit-project --path ./messy_project" in output


def test_unknown_recipe_fails_gracefully(capsys):
    assert main(["recipes", "show", "missing-recipe"]) == 2
    output = capsys.readouterr().out
    assert "Unknown recipe: missing-recipe" in output
    assert "Available recipes:" in output


def test_audit_project_creates_markdown_report(tmp_path):
    report = tmp_path / "project_audit.md"
    example = REPO_ROOT / "examples" / "messy_project_archaeology"
    assert main(["audit-project", "--path", str(example), "--write-report", str(report)]) == 0
    text = report.read_text(encoding="utf-8")
    assert "# Paper Scaffold Project Audit" in text
    assert "Candidate Overleaf Exports" in text
    assert "W022" in text
    assert "W023" in text
    assert "W024" in text
    assert "I020" in text
    assert "I021" in text


def test_release_check_runs_on_demo_manuscript(tmp_path):
    output = tmp_path / "demo_manuscript"
    report = output / "release_check.md"
    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    assert main(["release-check", "--manuscript-repo", str(output), "--write-report", str(report)]) == 0
    text = report.read_text(encoding="utf-8")
    assert "# Paper Scaffold Release Check" in text
    assert "## validate" in text
    assert "## overleaf-check" in text
    assert "## stale-artifacts" in text
    assert "## unused-artifacts" in text


def test_use_case_docs_exist_and_readme_links_them():
    docs_root = REPO_ROOT / "docs" / "use_cases"
    assert (docs_root / "README.md").exists()
    readme = (docs_root / "README.md").read_text(encoding="utf-8")
    for use_case_id in USE_CASE_IDS:
        assert (docs_root / f"{use_case_id}.md").exists()
        assert f"{use_case_id}.md" in readme


def test_top_level_readme_links_use_cases():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "paper-scaffold recipes list" in readme
    assert "[docs/use_cases](docs/use_cases)" in readme
    assert "paper-scaffold release-check" in readme


def test_examples_do_not_contain_private_paths_or_emails():
    examples = [
        REPO_ROOT / "examples" / "messy_project_archaeology",
        REPO_ROOT / "examples" / "reviewer_response_binder",
        REPO_ROOT / "examples" / "multi_paper_split",
    ]
    text_suffixes = {".bib", ".csv", ".md", ".tex", ".txt", ".yaml", ".yml"}
    private_pattern = re.compile(r"([A-Za-z]:\\|/Users/|/home/|\\\\[^\\/\s]+\\[^\\/\s]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})")
    for example_root in examples:
        for path in example_root.rglob("*"):
            if path.is_dir() or path.suffix.lower() not in text_suffixes:
                continue
            text = path.read_text(encoding="utf-8")
            assert not private_pattern.search(text), path
