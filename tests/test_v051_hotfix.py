from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.checks import check_overleaf
from paper_scaffold.cli import main
from paper_scaffold.messages import severity_counts
from paper_scaffold.validation import validate_manuscript_repo


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_demo_validation_has_no_errors_or_warnings(tmp_path):
    output = tmp_path / "demo_manuscript"
    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    report = validate_manuscript_repo(output)
    assert report.errors == []
    assert report.warnings == []
    assert (output / "figures" / "example_metric_plot.pdf").exists()
    assert not (output / "figures" / "example_metric_plot.png").exists()
    main_tex = (output / "main.tex").read_text(encoding="utf-8")
    assert r"\includegraphics[width=0.75\linewidth]{figures/example_metric_plot.pdf}" in main_tex
    assert "example_reference" in main_tex


def test_demo_overleaf_check_has_no_errors_or_w005(tmp_path):
    output = tmp_path / "demo_manuscript"
    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    findings = check_overleaf(output)
    counts = severity_counts(findings)
    assert counts["ERROR"] == 0
    assert not [finding for finding in findings if finding.code == "W005"]


def test_windows_clean_clone_notes_are_documented():
    docs = (
        (REPO_ROOT / "docs" / "troubleshooting.md").read_text(encoding="utf-8")
        + "\n"
        + (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    )
    assert "paper-scaffold.exe --help" in docs
    assert 'export PATH="/path/to/env/Scripts:$PATH"' in docs
    assert "TMP=\"$PWD/scratch/tmp\" TEMP=\"$PWD/scratch/tmp\" python -m pytest tests --basetemp=scratch/pytest-tmp -p no:cacheprovider" in docs
