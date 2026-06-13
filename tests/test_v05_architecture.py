from __future__ import annotations

import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.cli import build_parser, main
from paper_scaffold.config import write_yaml
from paper_scaffold.discovery import discover_artifacts
from paper_scaffold.scaffold import InitOptions, init_manuscript
from paper_scaffold.schemas import validate_artifact_manifest_schema, validate_validation_report_json_schema
from paper_scaffold import __version__


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_schema_validation_valid_manifest():
    findings = validate_artifact_manifest_schema(
        {
            "artifacts": [
                {
                    "id": "main_result",
                    "type": "figure",
                    "manuscript_path": "figures/main_result.pdf",
                    "source_path": "outputs/main_result.pdf",
                }
            ]
        }
    )
    assert not [finding for finding in findings if finding.message.severity == "ERROR"]


def test_schema_validation_invalid_manifest_reports_index_and_unknown_field():
    findings = validate_artifact_manifest_schema(
        {
            "artifacts": [
                {
                    "id": "main_result",
                    "type": "plot",
                    "manuscript_path": "figures/main_result.pdf",
                    "extra_note": "local metadata",
                }
            ]
        },
        "metadata/artifact_manifest.yaml",
    )
    formatted = "\n".join(f"{finding.code} {finding.detail} {finding.path}" for finding in findings)
    assert "E004 artifact[1] missing required field: source_path metadata/artifact_manifest.yaml" in formatted
    assert "E004 artifact[1] unsupported type: plot metadata/artifact_manifest.yaml" in formatted
    assert "W018 artifact[1] unknown field: extra_note metadata/artifact_manifest.yaml" in formatted


def test_validate_writes_json_report(tmp_path):
    manuscript = tmp_path / "paper"
    init_manuscript(
        InitOptions(
            research_repo="./research-project",
            manuscript_repo=str(manuscript),
            title="JSON Report Test",
            slug="json_report_test",
            has_supplement=True,
            use_template=True,
        )
    )
    report_path = manuscript / "validation_report.json"
    assert main(["validate", "--manuscript-repo", str(manuscript), "--write-json", str(report_path)]) == 0
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["tool"] == "Paper Scaffold"
    assert data["version"] == __version__
    assert set(data["summary"]) == {"errors", "warnings", "info"}
    assert isinstance(data["diagnostics"], list)
    assert not validate_validation_report_json_schema(data)


def test_stale_artifacts_detects_modified_source(tmp_path, capsys):
    manuscript = tmp_path / "paper"
    source_dir = tmp_path / "source"
    (manuscript / "metadata").mkdir(parents=True)
    (manuscript / "figures").mkdir()
    source_dir.mkdir()
    source = source_dir / "figure.pdf"
    copied = manuscript / "figures" / "figure.pdf"
    source.write_text("new figure", encoding="utf-8")
    copied.write_text("old figure", encoding="utf-8")
    os.utime(copied, (1000, 1000))
    os.utime(source, (2000, 2000))
    write_yaml(
        manuscript / "metadata" / "artifact_manifest.yaml",
        {
            "artifacts": [
                {
                    "id": "figure",
                    "type": "figure",
                    "manuscript_path": "figures/figure.pdf",
                    "source_repo": str(source_dir),
                    "source_path": "figure.pdf",
                }
            ]
        },
    )
    assert main(["stale-artifacts", "--manuscript-repo", str(manuscript)]) == 0
    output = capsys.readouterr().out
    assert "W019" in output
    assert "source changed after manuscript copy" in output


def test_unused_artifacts_detects_unreferenced_figure(tmp_path, capsys):
    manuscript = tmp_path / "paper"
    (manuscript / "figures").mkdir(parents=True)
    (manuscript / "main.tex").write_text("\\section{Results}\n", encoding="utf-8")
    (manuscript / "figures" / "orphan.pdf").write_text("pdf", encoding="utf-8")
    assert main(["unused-artifacts", "--manuscript-repo", str(manuscript)]) == 0
    output = capsys.readouterr().out
    assert "W020" in output
    assert "figures/orphan.pdf" in output


def test_discover_artifacts_destination_suggestions(tmp_path):
    source = tmp_path / "outputs"
    source.mkdir()
    (source / "result.pdf").write_text("pdf", encoding="utf-8")
    (source / "summary.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (source / "table.tex").write_text("\\begin{tabular}{ll}a & b\\end{tabular}\n", encoding="utf-8")
    normal = {candidate.source_path.name: candidate.manuscript_path for candidate in discover_artifacts(source)}
    supplement = {candidate.source_path.name: candidate.manuscript_path for candidate in discover_artifacts(source, supplement=True)}
    assert normal["result.pdf"] == "figures/result.pdf"
    assert normal["summary.csv"] == "tables/summary.csv"
    assert normal["table.tex"] == "tables/table.tex"
    assert supplement["result.pdf"] == "supplement/figures/result.pdf"
    assert supplement["table.tex"] == "supplement/tables/table.tex"


def test_cli_help_mentions_v05_commands():
    help_text = build_parser().format_help()
    assert "stale-artifacts" in help_text
    assert "unused-artifacts" in help_text
    assert "validate" in help_text


def test_adr_files_and_roadmap_exist():
    for number in range(1, 7):
        matches = list((REPO_ROOT / "docs" / "adr").glob(f"{number:04d}-*.md"))
        assert matches, number
        text = matches[0].read_text(encoding="utf-8")
        assert "## Context" in text
        assert "## Decision" in text
        assert "## Consequences" in text
        assert "## Alternatives Considered" in text
        assert "## What Would Make Us Revisit This?" in text
    assert (REPO_ROOT / "ROADMAP.md").exists()


def test_public_readme_contains_core_workflow_and_roadmap():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "Keep research code and manuscript source separate" in readme
    assert "validation_report.json" in readme
    assert "stale-artifacts" in readme
    assert "ROADMAP.md" in readme
