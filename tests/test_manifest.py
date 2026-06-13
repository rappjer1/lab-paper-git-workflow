from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.artifact_manifest import load_artifact_manifest, validate_artifacts
from paper_scaffold.config import write_yaml
from paper_scaffold.terminology import find_banned_terms


def test_artifact_manifest_parsing(tmp_path):
    manifest_path = tmp_path / "metadata" / "artifact_manifest.yaml"
    write_yaml(
        manifest_path,
        {
            "artifacts": [
                {
                    "id": "workflow_schematic",
                    "type": "figure",
                    "manuscript_path": "figures/workflow_schematic.pdf",
                    "source_repo": "./research-project",
                    "source_path": "outputs/workflow_schematic.pdf",
                    "generated_by": "scripts/make_figures.py",
                    "input_data": "outputs/summary.csv",
                    "last_updated": "2026-06-10",
                    "caption_hint": "Workflow schematic.",
                    "status": "final",
                }
            ]
        },
    )
    manifest = load_artifact_manifest(tmp_path)
    assert manifest["artifacts"][0]["id"] == "workflow_schematic"
    assert validate_artifacts(manifest) == []


def test_artifact_manifest_rejects_bad_type():
    errors = validate_artifacts(
        {
            "artifacts": [
                {
                    "id": "raw_dump",
                    "type": "raw_data",
                    "manuscript_path": "data/raw.csv",
                    "source_path": "outputs/raw.csv",
                }
            ]
        }
    )
    assert any("unsupported type" in error for error in errors)


def test_terminology_detection(tmp_path):
    (tmp_path / "metadata").mkdir()
    write_yaml(
        tmp_path / "metadata" / "terminology_map.yaml",
        {
            "terms": {
                "experiment_model_v1": {
                    "publication_label": "probabilistic model",
                    "banned_in": ["abstract", "main results"],
                }
            }
        },
    )
    tex = tmp_path / "main.tex"
    tex.write_text("The experiment_model_v1 performed well.", encoding="utf-8")
    hits = find_banned_terms(tmp_path)
    assert len(hits) == 1
    assert hits[0].publication_label == "probabilistic model"
