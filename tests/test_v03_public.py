from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.cli import main
from paper_scaffold.scaffold import InitOptions, init_manuscript


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_demo_command_creates_temp_output(tmp_path):
    output = tmp_path / "demo_manuscript"
    exit_code = main(["demo", "--output", str(output), "--overwrite"])
    assert exit_code == 0
    assert (output / "main.tex").exists()
    assert (output / "figures" / "example_metric_plot.pdf").exists()
    assert (output / "tables" / "example_summary_table.csv").exists()
    assert (output / "metadata" / "artifact_manifest.yaml").exists()


def test_doctor_message_when_run_in_tool_repo(capsys):
    exit_code = main(["doctor", "--manuscript-repo", str(REPO_ROOT)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Paper Scaffold tool repo" in output
    assert "Missing main.tex is expected here" in output


def test_validate_write_report(tmp_path):
    manuscript = tmp_path / "paper"
    init_manuscript(
        InitOptions(
            research_repo="./research-project",
            manuscript_repo=str(manuscript),
            title="Report Test",
            slug="report_test",
            has_supplement=True,
            use_template=True,
        )
    )
    report_path = manuscript / "validation_report.md"
    exit_code = main(["validate", "--manuscript-repo", str(manuscript), "--write-report", str(report_path)])
    assert exit_code == 0
    report = report_path.read_text(encoding="utf-8")
    assert "Paper Scaffold Validation Report" in report
    assert "Repository path" in report
    assert "Git Status Summary" in report


def test_discover_artifacts_suggest_only(tmp_path, capsys):
    source = tmp_path / "outputs"
    source.mkdir()
    (source / "figure.pdf").write_text("pdf", encoding="utf-8")
    (source / "model.pt").write_text("model", encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    exit_code = main(["discover-artifacts", "--source", str(source), "--manifest", str(manifest), "--suggest-only"])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "figure" in output
    assert "Manifest entry preview" in output
    assert "model.pt" not in output
    assert not manifest.exists()


def test_public_docs_files_exist():
    docs = [
        "docs/getting_started.md",
        "docs/word_to_overleaf.md",
        "docs/python_outputs_to_overleaf.md",
        "docs/existing_latex_project.md",
        "docs/github_overleaf_sync.md",
        "docs/artifact_manifest.md",
        "docs/terminology_cleanup.md",
        "docs/validation.md",
        "docs/troubleshooting.md",
        "docs/faq.md",
        "docs/design_principles.md",
    ]
    for relative in docs:
        assert (REPO_ROOT / relative).exists(), relative


def test_readme_has_no_private_project_terms():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8").lower()
    banned = [
        "r:\\code",
        "sandro",
        "jer" + "emy",
        "our " + "lab",
        "lab " + "members",
    ]
    for term in banned:
        assert term not in readme
