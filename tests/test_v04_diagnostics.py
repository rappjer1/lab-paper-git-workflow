from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.cli import main
from paper_scaffold.discovery import discover_artifacts
from paper_scaffold.messages import all_messages
from paper_scaffold.scaffold import InitOptions, init_manuscript


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_message_registry_has_v04_codes():
    codes = {message.code for message in all_messages()}
    expected = {
        *(f"E{number:03d}" for number in range(1, 16)),
        *(f"W{number:03d}" for number in range(1, 18)),
        *(f"I{number:03d}" for number in range(1, 7)),
    }
    assert expected <= codes
    for message in all_messages():
        assert message.title
        assert message.explanation
        assert message.suggested_fix


def test_explain_known_and_unknown_codes(capsys):
    assert main(["explain", "E003"]) == 0
    known = capsys.readouterr().out
    assert "E003" in known
    assert "Missing figure path" in known
    assert "check-figures" in known

    assert main(["explain", "NOPE"]) == 2
    unknown = capsys.readouterr().out
    assert "Unknown diagnostic code" in unknown
    assert "E001" in unknown


def test_validate_write_report_uses_diagnostic_sections(tmp_path):
    manuscript = tmp_path / "paper"
    init_manuscript(
        InitOptions(
            research_repo="./research-project",
            manuscript_repo=str(manuscript),
            title="Diagnostics Report Test",
            slug="diagnostics_report_test",
            has_supplement=True,
            use_template=True,
        )
    )
    report_path = manuscript / "validation_report.md"
    assert main(["validate", "--manuscript-repo", str(manuscript), "--write-report", str(report_path)]) == 0
    report = report_path.read_text(encoding="utf-8")
    assert "Paper Scaffold Validation Report" in report
    assert "Git Status Summary" in report
    assert "## Warnings" in report
    assert "W015" in report


def test_demo_and_focused_checks(tmp_path):
    output = tmp_path / "demo_manuscript"
    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    assert (output / "main.tex").exists()
    assert (output / "figures" / "example_metric_plot.pdf").exists()
    assert main(["overleaf-check", "--manuscript-repo", str(output)]) == 0
    assert main(["check-figures", "--manuscript-repo", str(output)]) == 0
    assert main(["check-citations", "--manuscript-repo", str(output)]) == 0
    assert main(["check-labels", "--manuscript-repo", str(output)]) == 0


def test_privacy_check_detects_and_redacts_private_values(tmp_path, capsys):
    text_file = tmp_path / "notes.md"
    text_file.write_text(
        "Local source: C:\\Users\\Researcher\\draft.docx\napi_key=abcdefghijkl\ncontact=a@example.org\n",
        encoding="utf-8",
    )
    assert main(["privacy-check", "--path", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    assert "W017" in output
    assert "<local-path>" in output
    assert "<redacted>" in output
    assert "<email>" in output
    assert "C:\\Users" not in output
    assert "abcdefghijkl" not in output
    assert "a@example.org" not in output


def test_citation_and_label_checks_report_errors(tmp_path, capsys):
    (tmp_path / "references.bib").write_text("", encoding="utf-8")
    (tmp_path / "main.tex").write_text(
        r"""
\section{Results}
\cite{missing_key}
\label{fig:duplicate}
\label{fig:duplicate}
\ref{fig:missing}
""",
        encoding="utf-8",
    )
    assert main(["check-citations", "--manuscript-repo", str(tmp_path)]) == 1
    citation_output = capsys.readouterr().out
    assert "E012" in citation_output
    assert "missing_key" in citation_output

    assert main(["check-labels", "--manuscript-repo", str(tmp_path)]) == 1
    label_output = capsys.readouterr().out
    assert "E010" in label_output
    assert "E011" in label_output


def test_word_conversion_audit_is_warning_only(tmp_path, capsys):
    converted = tmp_path / "converted.tex"
    converted.write_text(
        r"""
\begin{longtable}{ll}
a & b
\end{longtable}
""",
        encoding="utf-8",
    )
    assert main(["audit-word-conversion", "--input", str(converted)]) == 0
    output = capsys.readouterr().out
    assert "W008" in output
    assert "Word conversion is a starting point" in output


def test_discovery_keeps_duplicate_stems_unique(tmp_path):
    source = tmp_path / "outputs"
    source.mkdir()
    (source / "plot.pdf").write_text("pdf", encoding="utf-8")
    (source / "plot.png").write_text("png", encoding="utf-8")
    candidates = discover_artifacts(source)
    assert [candidate.artifact_id for candidate in candidates] == ["plot", "plot_2"]


def test_error_code_docs_are_public_docs():
    docs = (REPO_ROOT / "docs" / "error_codes.md").read_text(encoding="utf-8")
    assert "E003" in docs
    assert "W017" in docs
    assert "I001" in docs
