from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.cli import main
from paper_scaffold.config import write_yaml
from paper_scaffold.provenance import build_provenance_ledger
from paper_scaffold.schemas import validate_provenance_ledger_json_schema


def _write_minimal_repo(repo: Path, main_tex: str) -> None:
    (repo / "figures").mkdir(parents=True, exist_ok=True)
    (repo / "tables").mkdir(parents=True, exist_ok=True)
    (repo / "metadata").mkdir(parents=True, exist_ok=True)
    (repo / "main.tex").write_text(main_tex, encoding="utf-8")
    (repo / "references.bib").write_text("", encoding="utf-8")


def _write_manifest(repo: Path, artifacts: list[dict[str, object]]) -> None:
    write_yaml(repo / "metadata" / "artifact_manifest.yaml", {"artifacts": artifacts})


def test_provenance_report_on_demo_writes_markdown_and_json(tmp_path):
    output = tmp_path / "demo_manuscript"
    md = output / "provenance_report.md"
    ledger_json = output / "provenance_ledger.json"
    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    assert main(["provenance-report", "--manuscript-repo", str(output), "--write-md", str(md), "--write-json", str(ledger_json)]) == 0
    assert "# Paper Scaffold Provenance Report" in md.read_text(encoding="utf-8")
    ledger = json.loads(ledger_json.read_text(encoding="utf-8"))
    assert validate_provenance_ledger_json_schema(ledger) == []
    assert ledger["summary"]["total_manifest_artifacts"] == 3
    assert ledger["summary"]["current"] == 3
    assert ledger["summary"]["unreferenced_artifacts"] == 0
    assert {artifact["artifact_id"] for artifact in ledger["artifacts"]} == {
        "example_metric_plot",
        "example_summary_table",
        "example_table",
    }


def test_artifact_status_reports_current_artifacts(tmp_path, capsys):
    output = tmp_path / "demo_manuscript"
    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    assert main(["artifact-status", "--manuscript-repo", str(output)]) == 0
    text = capsys.readouterr().out
    assert "Artifact status" in text
    assert "- current: 3" in text
    assert "- stale: 0" in text


def test_freeze_artifacts_writes_lock_file(tmp_path):
    output = tmp_path / "demo_manuscript"
    lock = output / "metadata" / "artifact_lock.json"
    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    assert main(["freeze-artifacts", "--manuscript-repo", str(output), "--write-lock", str(lock)]) == 0
    data = json.loads(lock.read_text(encoding="utf-8"))
    assert data["tool"] == "Paper Scaffold"
    assert len(data["artifacts"]) == 3
    assert all(entry["manuscript_sha256"] for entry in data["artifacts"])


def test_stale_artifact_detected_when_source_hash_changes(tmp_path):
    source = tmp_path / "source" / "main_result.pdf"
    source.parent.mkdir(parents=True)
    source.write_text("new source bytes", encoding="utf-8")
    repo = tmp_path / "paper"
    _write_minimal_repo(repo, r"\documentclass{article}\usepackage{graphicx}\begin{document}\includegraphics{figures/main_result.pdf}\end{document}")
    (repo / "figures" / "main_result.pdf").write_text("old manuscript bytes", encoding="utf-8")
    _write_manifest(
        repo,
        [
            {
                "id": "main_result",
                "type": "figure",
                "manuscript_path": "figures/main_result.pdf",
                "source_path": source.as_posix(),
                "generated_by": "scripts/make_figures.py",
            }
        ],
    )
    ledger = build_provenance_ledger(repo)
    assert ledger["summary"]["stale"] == 1
    assert ledger["artifacts"][0]["status"] == "stale"


def test_missing_source_is_warning_not_crash(tmp_path):
    repo = tmp_path / "paper"
    _write_minimal_repo(repo, r"\documentclass{article}\usepackage{graphicx}\begin{document}\includegraphics{figures/main_result.pdf}\end{document}")
    (repo / "figures" / "main_result.pdf").write_text("manuscript bytes", encoding="utf-8")
    _write_manifest(
        repo,
        [
            {
                "id": "main_result",
                "type": "figure",
                "manuscript_path": "figures/main_result.pdf",
                "source_path": (tmp_path / "missing" / "main_result.pdf").as_posix(),
            }
        ],
    )
    assert main(["provenance-report", "--manuscript-repo", str(repo)]) == 0
    ledger = build_provenance_ledger(repo)
    assert ledger["summary"]["missing_source"] == 1
    assert ledger["artifacts"][0]["status"] == "missing_source"


def test_untracked_artifact_detection_works(tmp_path):
    repo = tmp_path / "paper"
    _write_minimal_repo(repo, r"\documentclass{article}\usepackage{graphicx}\begin{document}\includegraphics{figures/untracked.pdf}\end{document}")
    (repo / "figures" / "untracked.pdf").write_text("untracked bytes", encoding="utf-8")
    _write_manifest(repo, [])
    ledger = build_provenance_ledger(repo)
    assert ledger["summary"]["untracked_manuscript_artifacts"] == 1
    assert ledger["untracked_artifacts"][0]["manuscript_path"] == "figures/untracked.pdf"


def test_usage_detection_finds_includegraphics(tmp_path):
    source = tmp_path / "source.pdf"
    source.write_text("same bytes", encoding="utf-8")
    repo = tmp_path / "paper"
    _write_minimal_repo(repo, r"\documentclass{article}\usepackage{graphicx}\begin{document}\includegraphics{figures/main_result.pdf}\end{document}")
    (repo / "figures" / "main_result.pdf").write_text("same bytes", encoding="utf-8")
    _write_manifest(
        repo,
        [
            {
                "id": "main_result",
                "type": "figure",
                "manuscript_path": "figures/main_result.pdf",
                "source_path": source.as_posix(),
            }
        ],
    )
    artifact = build_provenance_ledger(repo)["artifacts"][0]
    assert artifact["used_in_tex_files"] == ["main.tex"]
    assert artifact["used_in_main_or_supplement"] == "main"


def test_supplement_usage_detection_works(tmp_path):
    source = tmp_path / "supp_result.pdf"
    source.write_text("same bytes", encoding="utf-8")
    repo = tmp_path / "paper"
    _write_minimal_repo(repo, r"\documentclass{article}\begin{document}Main text.\end{document}")
    (repo / "supplement" / "figures").mkdir(parents=True)
    (repo / "supplement" / "supplement.tex").write_text(
        r"\documentclass{article}\usepackage{graphicx}\begin{document}\includegraphics{figures/supp_result.pdf}\end{document}",
        encoding="utf-8",
    )
    (repo / "supplement" / "figures" / "supp_result.pdf").write_text("same bytes", encoding="utf-8")
    _write_manifest(
        repo,
        [
            {
                "id": "supp_result",
                "type": "supplement_figure",
                "manuscript_path": "supplement/figures/supp_result.pdf",
                "source_path": source.as_posix(),
            }
        ],
    )
    artifact = build_provenance_ledger(repo)["artifacts"][0]
    assert artifact["used_in_tex_files"] == ["supplement/supplement.tex"]
    assert artifact["used_in_main_or_supplement"] == "supplement"
