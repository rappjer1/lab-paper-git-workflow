from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.cli import main
from paper_scaffold.discovery import discover_artifacts, should_ignore_path
from paper_scaffold.config import write_yaml
from paper_scaffold.word import import_word


def test_doctor_command_does_not_crash(tmp_path, capsys):
    exit_code = main(["doctor", "--manuscript-repo", str(tmp_path)])
    output = capsys.readouterr().out
    assert exit_code == 0
    assert "paper-scaffold doctor" in output
    assert "Python" in output


def test_forbidden_artifact_filtering():
    assert should_ignore_path(Path("outputs/full_eval/predictions.csv"))
    assert should_ignore_path(Path("outputs/prediction_cache/cache.pkl"))
    assert should_ignore_path(Path("outputs/raw_api_cache/response.json"))
    assert should_ignore_path(Path("outputs/final/model.pt"))
    assert not should_ignore_path(Path("outputs/final/figure.pdf"))


def test_artifact_discovery_dry_run_filters_outputs(tmp_path):
    source = tmp_path / "outputs"
    (source / "final").mkdir(parents=True)
    (source / "prediction_cache").mkdir()
    (source / "final" / "Figure 1.pdf").write_text("pdf placeholder", encoding="utf-8")
    (source / "final" / "summary.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (source / "prediction_cache" / "cache.pkl").write_text("cache", encoding="utf-8")
    (source / "final" / "weights.pt").write_text("weights", encoding="utf-8")

    candidates = discover_artifacts(source)
    ids = {candidate.artifact_id for candidate in candidates}
    assert ids == {"figure_1", "summary"}
    assert all(candidate.source_path.suffix in {".pdf", ".csv"} for candidate in candidates)


def test_import_word_reports_missing_pandoc(monkeypatch, tmp_path):
    monkeypatch.setattr("paper_scaffold.word.shutil.which", lambda executable: None)
    result = import_word(tmp_path / "draft.docx", tmp_path / "converted.tex")
    assert result.ok is False
    assert "Pandoc is not installed" in result.message
    assert "Word conversion is a starting point" in result.message


def test_terminology_check_command_still_works(tmp_path, capsys):
    (tmp_path / "metadata").mkdir()
    write_yaml(
        tmp_path / "metadata" / "terminology_map.yaml",
        {
            "terms": {
                "internal_label": {
                    "publication_label": "publication label",
                    "banned_in": ["main results"],
                }
            }
        },
    )
    (tmp_path / "main.tex").write_text("The internal_label result is shown.", encoding="utf-8")
    exit_code = main(["terminology-check", "--manuscript-repo", str(tmp_path)])
    output = capsys.readouterr().out
    assert exit_code == 1
    assert "internal_label" in output
    assert "publication label" in output
