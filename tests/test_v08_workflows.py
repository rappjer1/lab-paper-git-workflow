from pathlib import Path
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold.cli import main
from paper_scaffold.config import write_yaml
from paper_scaffold.messages import all_messages
from paper_scaffold import __version__


REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_workflow_repo(repo: Path) -> None:
    (repo / "figures").mkdir(parents=True, exist_ok=True)
    (repo / "tables").mkdir(parents=True, exist_ok=True)
    (repo / "metadata").mkdir(parents=True, exist_ok=True)
    (repo / "main.tex").write_text(
        r"""\documentclass{article}
\usepackage{graphicx}
\begin{document}
\includegraphics{figures/referenced.pdf}
\input{tables/table.tex}
\end{document}
""",
        encoding="utf-8",
    )
    (repo / "references.bib").write_text("", encoding="utf-8")
    (repo / "figures" / "referenced.pdf").write_text("referenced figure bytes", encoding="utf-8")
    (repo / "figures" / "unreferenced.pdf").write_text("unreferenced figure bytes", encoding="utf-8")
    (repo / "tables" / "table.tex").write_text(r"\begin{tabular}{lr}A & 1\\\end{tabular}", encoding="utf-8")
    write_yaml(
        repo / "metadata" / "manuscript_config.yaml",
        {"project": {"main_tex": "main.tex", "has_supplement": False}},
    )
    write_yaml(
        repo / "metadata" / "artifact_manifest.yaml",
        {
            "artifacts": [
                {"id": "referenced", "type": "figure", "manuscript_path": "figures/referenced.pdf"},
                {"id": "unreferenced", "type": "figure", "manuscript_path": "figures/unreferenced.pdf"},
                {"id": "table", "type": "table", "manuscript_path": "tables/table.tex"},
            ]
        },
    )


def test_manuscript_ci_workflow_generation_and_overwrite_protection(tmp_path):
    repo = tmp_path / "paper"
    _write_workflow_repo(repo)
    workflow = repo / ".github" / "workflows" / "manuscript-checks.yml"

    assert main(["add-manuscript-ci", "--manuscript-repo", str(repo)]) == 0
    text = workflow.read_text(encoding="utf-8")
    assert "name: manuscript-checks" in text
    assert "forbidden raw/generated output" in text

    assert main(["add-manuscript-ci", "--manuscript-repo", str(repo)]) == 2
    assert main(["add-manuscript-ci", "--manuscript-repo", str(repo), "--overwrite"]) == 0


def test_submission_package_creation_and_overwrite_protection(tmp_path):
    repo = tmp_path / "paper"
    output = tmp_path / "submission"
    _write_workflow_repo(repo)

    assert main(["package-submission", "--manuscript-repo", str(repo), "--output", str(output)]) == 0
    assert (output / "main.tex").exists()
    assert (output / "references.bib").exists()
    assert (output / "figures" / "referenced.pdf").exists()
    assert (output / "tables" / "table.tex").exists()
    assert (output / "README_SUBMISSION.md").exists()
    assert (output / "submission_package_manifest.json").exists()
    assert main(["package-submission", "--manuscript-repo", str(repo), "--output", str(output)]) == 2


def test_submission_package_excludes_scratch_build_and_latex_artifacts(tmp_path):
    repo = tmp_path / "paper"
    output = tmp_path / "submission"
    _write_workflow_repo(repo)
    (repo / "scratch").mkdir()
    (repo / "build").mkdir()
    (repo / "scratch" / "scratch_notes.tex").write_text("scratch", encoding="utf-8")
    (repo / "build" / "generated_table.tex").write_text("build", encoding="utf-8")
    (repo / "main.aux").write_text("latex build", encoding="utf-8")

    assert main(["package-submission", "--manuscript-repo", str(repo), "--output", str(output)]) == 0
    assert not (output / "scratch" / "scratch_notes.tex").exists()
    assert not (output / "build" / "generated_table.tex").exists()
    assert not (output / "main.aux").exists()


def test_submission_package_excludes_unreferenced_figures_by_default(tmp_path):
    repo = tmp_path / "paper"
    output = tmp_path / "submission"
    _write_workflow_repo(repo)

    assert main(["package-submission", "--manuscript-repo", str(repo), "--output", str(output)]) == 0
    assert not (output / "figures" / "unreferenced.pdf").exists()
    manifest = json.loads((output / "submission_package_manifest.json").read_text(encoding="utf-8"))
    assert "figures/unreferenced.pdf" in manifest["excluded_unreferenced_artifacts"]


def test_submission_package_includes_unreferenced_figures_when_requested(tmp_path):
    repo = tmp_path / "paper"
    output = tmp_path / "submission"
    _write_workflow_repo(repo)

    assert main(["package-submission", "--manuscript-repo", str(repo), "--output", str(output), "--include-unreferenced"]) == 0
    assert (output / "figures" / "unreferenced.pdf").exists()


def test_compare_lock_unchanged_changed_and_missing_cases(tmp_path):
    repo = tmp_path / "paper"
    _write_workflow_repo(repo)
    lock = repo / "metadata" / "artifact_lock.json"

    assert main(["freeze-artifacts", "--manuscript-repo", str(repo), "--write-lock", str(lock)]) == 0
    assert main(["compare-lock", "--manuscript-repo", str(repo), "--lock", str(lock)]) == 0

    (repo / "figures" / "referenced.pdf").write_text("changed bytes", encoding="utf-8")
    assert main(["compare-lock", "--manuscript-repo", str(repo), "--lock", str(lock)]) == 1

    (repo / "figures" / "referenced.pdf").unlink()
    assert main(["compare-lock", "--manuscript-repo", str(repo), "--lock", str(lock)]) == 1
    assert main(["compare-lock", "--manuscript-repo", str(repo), "--lock", str(repo / "metadata" / "missing_lock.json")]) == 2


def test_compare_lock_accepts_cwd_relative_lock_path(tmp_path, monkeypatch):
    repo = tmp_path / "paper"
    _write_workflow_repo(repo)
    lock = repo / "metadata" / "artifact_lock.json"
    assert main(["freeze-artifacts", "--manuscript-repo", str(repo), "--write-lock", str(lock)]) == 0

    monkeypatch.chdir(tmp_path)
    assert main(["compare-lock", "--manuscript-repo", str(repo), "--lock", str(lock.relative_to(tmp_path))]) == 0


def test_reviewer_binder_output_files_and_overwrite_protection(tmp_path):
    repo = tmp_path / "paper"
    output = tmp_path / "reviewer_response_round_1"
    _write_workflow_repo(repo)

    assert main(["reviewer-binder", "--manuscript-repo", str(repo), "--round", "1", "--output", str(output)]) == 0
    expected = {
        "README.md",
        "response_checklist.md",
        "response_artifact_manifest.yaml",
        "provenance_snapshot.md",
        "release_check.md",
        "artifact_status.txt",
        "artifact_lock_snapshot.json",
    }
    assert expected <= {path.name for path in output.iterdir()}
    assert "Round 1" in (output / "README.md").read_text(encoding="utf-8")
    assert main(["reviewer-binder", "--manuscript-repo", str(repo), "--round", "1", "--output", str(output)]) == 2


def test_v08_diagnostic_codes_and_docs_are_registered():
    codes = {message.code for message in all_messages()}
    assert {*(f"E{number:03d}" for number in range(30, 36))} <= codes
    assert {*(f"W{number:03d}" for number in range(40, 46))} <= codes
    assert {*(f"I{number:03d}" for number in range(40, 45))} <= codes
    docs = "\n".join(
        [
            (REPO_ROOT / "README.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "manuscript_ci.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "submission_packaging.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "artifact_locks.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "reviewer_response_binder.md").read_text(encoding="utf-8"),
        ]
    )
    assert "add-manuscript-ci" in docs
    assert "package-submission" in docs
    assert "compare-lock" in docs
    assert "reviewer-binder" in docs


def test_text_blob_guard_script_still_passes():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "dev" / "check_text_blobs.py")],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_release_check_and_provenance_commands_still_pass_on_demo(tmp_path):
    output = tmp_path / "demo_manuscript"
    release_report = output / "release_check.md"
    provenance_report = output / "provenance_report.md"
    provenance_json = output / "metadata" / "provenance_ledger.json"

    assert main(["demo", "--output", str(output), "--overwrite"]) == 0
    assert main(["release-check", "--manuscript-repo", str(output), "--write-report", str(release_report)]) == 0
    assert main(
        [
            "provenance-report",
            "--manuscript-repo",
            str(output),
            "--write-md",
            str(provenance_report),
            "--write-json",
            str(provenance_json),
        ]
    ) == 0
    assert "# Paper Scaffold Release Check" in release_report.read_text(encoding="utf-8")
    assert "# Paper Scaffold Provenance Report" in provenance_report.read_text(encoding="utf-8")
    assert json.loads(provenance_json.read_text(encoding="utf-8"))["version"] == __version__
