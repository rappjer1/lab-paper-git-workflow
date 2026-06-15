from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold import __version__


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(*parts: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *parts],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_release_candidate_audit_help_works():
    result = run_script("scripts/dev/release_candidate_audit.py", "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--allow-dirty" in result.stdout
    assert "--skip-clean-clone" in result.stdout
    assert "--plan" in result.stdout


def test_release_candidate_audit_plan_builds_without_expensive_checks(tmp_path):
    output = tmp_path / "rc-plan"
    result = run_script("scripts/dev/release_candidate_audit.py", "--plan", "--allow-dirty", "--output", str(output))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Release candidate audit plan" in result.stdout
    assert "text blob guard" in result.stdout
    assert "version consistency" in result.stdout
    assert (output / "release_candidate_audit_report.md").exists()


def test_v1_release_notes_and_checklist_exist():
    for rel in [
        "V1_0_RELEASE_NOTES_DRAFT.md",
        "V1_0_FINAL_CHECKLIST.md",
        "V0_9_9_RELEASE_CANDIDATE_REPORT.md",
    ]:
        assert (REPO_ROOT / rel).exists(), rel


def test_release_docs_mention_release_candidate_audit():
    release_process = (REPO_ROOT / "docs" / "release_process.md").read_text(encoding="utf-8")
    readiness = (REPO_ROOT / "docs" / "v1_0_readiness.md").read_text(encoding="utf-8")
    assert "release_candidate_audit.py" in release_process
    assert "release-candidate audit" in readiness


def test_readme_mentions_approaching_v1():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "Approaching v1.0" in text
    assert "v0.9.9" in text


def test_version_is_099():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE)
    assert match is not None
    assert match.group(1) == __version__ == "0.9.9"


def test_release_candidate_guard_scripts_still_pass():
    for script in [
        "check_contracts.py",
        "check_public_safety.py",
        "check_text_blobs.py",
    ]:
        result = run_script(f"scripts/dev/{script}")
        assert result.returncode == 0, result.stdout + result.stderr


def test_run_tests_help_still_passes():
    result = run_script("scripts/dev/run_tests.py", "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--pytest-args" in result.stdout
