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


def pyproject_text() -> str:
    return (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")


def test_package_version_consistency():
    match = re.search(r'^version = "([^"]+)"', pyproject_text(), re.MULTILINE)
    assert match is not None
    assert match.group(1) == __version__


def test_cli_version_includes_current_package_version():
    result = run_script("scripts/paper-scaffold.py", "--version")
    assert result.returncode == 0, result.stdout + result.stderr
    assert __version__ in result.stdout


def test_ruff_target_version_is_python_target():
    match = re.search(r'^target-version = "([^"]+)"', pyproject_text(), re.MULTILINE)
    assert match is not None
    assert re.fullmatch(r"py3\d{2}", match.group(1))


def test_tests_do_not_hard_code_previous_release_candidate_version():
    stale_version = "0" + ".9.9"
    offenders = []
    for path in (REPO_ROOT / "tests").glob("*.py"):
        if stale_version in path.read_text(encoding="utf-8"):
            offenders.append(path.name)
    assert offenders == []


def test_root_contains_no_historical_report_files():
    assert list(REPO_ROOT.glob("V0_*.md")) == []
    assert list(REPO_ROOT.glob("V1_0_*.md")) == []
    assert not (REPO_ROOT / "IMPLEMENTATION_REPORT.md").exists()
    assert not (REPO_ROOT / "PUBLIC_READINESS_AUDIT.md").exists()


def test_release_report_index_and_moved_reports_exist():
    assert (REPO_ROOT / "docs" / "release_reports.md").exists()
    release_reports = REPO_ROOT / "docs" / "release_reports"
    for name in [
        "IMPLEMENTATION_REPORT.md",
        "PUBLIC_READINESS_AUDIT.md",
        "V0_9_9_RELEASE_CANDIDATE_REPORT.md",
        "V1_0_FINAL_CHECKLIST.md",
        "V1_0_1_PATCH_REPORT.md",
    ]:
        assert (release_reports / name).exists(), name


def test_root_layout_check_passes():
    result = run_script("scripts/dev/check_root_layout.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Root layout check passed." in result.stdout


def test_release_patch_guard_scripts_pass():
    for script in [
        "check_docs_links.py",
        "check_contracts.py",
        "check_public_safety.py",
        "check_text_blobs.py",
    ]:
        result = run_script(f"scripts/dev/{script}")
        assert result.returncode == 0, result.stdout + result.stderr
