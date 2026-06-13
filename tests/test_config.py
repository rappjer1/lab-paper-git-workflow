from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.config import ManuscriptConfig, loads_yaml, write_yaml


def test_loads_yaml_nested_mapping_and_list():
    data = loads_yaml(
        """
project:
  title: Example
  has_supplement: true
validation:
  max_file_size_mb: 10
  forbidden_patterns:
    - "*.npz"
    - "full_eval"
"""
    )
    assert data["project"]["title"] == "Example"
    assert data["project"]["has_supplement"] is True
    assert data["validation"]["forbidden_patterns"] == ["*.npz", "full_eval"]


def test_config_loading_merges_defaults(tmp_path):
    config_path = tmp_path / "metadata" / "manuscript_config.yaml"
    write_yaml(
        config_path,
        {
            "project": {"title": "Example", "manuscript_repo": str(tmp_path)},
            "validation": {"max_file_size_mb": 5, "forbidden_patterns": ["*.zip"]},
        },
    )
    config = ManuscriptConfig.load(tmp_path)
    assert config.project["title"] == "Example"
    assert config.main_tex == "main.tex"
    assert config.max_file_size_mb == 5
    assert "*.zip" in config.forbidden_patterns
    assert "*.npz" in config.forbidden_patterns
