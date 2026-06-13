from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.config import ManuscriptConfig
from paper_scaffold.scaffold import InitOptions, init_manuscript
from paper_scaffold.validation import forbidden_file_matches


def test_init_manuscript_creates_expected_files(tmp_path):
    manuscript_repo = tmp_path / "paper"
    options = InitOptions(
        research_repo="./research-project",
        manuscript_repo=str(manuscript_repo),
        title="Example Paper",
        slug="example_paper",
        has_supplement=True,
        use_template=True,
    )
    init_manuscript(options)

    assert (manuscript_repo / "main.tex").exists()
    assert (manuscript_repo / "references.bib").exists()
    assert (manuscript_repo / "figures").is_dir()
    assert (manuscript_repo / "supplement" / "supplement.tex").exists()
    assert (manuscript_repo / "metadata" / "manuscript_config.yaml").exists()

    config = ManuscriptConfig.load(manuscript_repo)
    assert config.project["title"] == "Example Paper"
    assert config.has_supplement is True


def test_forbidden_file_detection(tmp_path):
    (tmp_path / "figures").mkdir()
    forbidden = tmp_path / "figures" / "cache.npz"
    forbidden.write_text("not a real npz", encoding="utf-8")
    matches = forbidden_file_matches(tmp_path, ["*.npz"])
    assert forbidden in matches
