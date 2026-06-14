from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(*parts: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *parts],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_public_safety_check_passes():
    result = run_script("scripts/dev/check_public_safety.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Public safety check passed." in result.stdout


def test_public_safety_allowlist_exists():
    path = REPO_ROOT / "contracts" / "public_safety_allowlist.yaml"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "allowlist:" in text
    assert "allowed_paths:" in text
    assert "reason:" in text


def test_public_trust_docs_exist():
    for rel in [
        "docs/privacy_and_data_safety.md",
        "docs/github_repo_settings.md",
        "docs/release_reports.md",
    ]:
        assert (REPO_ROOT / rel).exists(), rel


def test_public_release_checklist_mentions_v1_public_safety_items():
    text = (REPO_ROOT / "PUBLIC_RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
    for needle in [
        "clean_install_audit.py",
        "install_matrix_audit.py",
        "check_public_safety.py",
        "check_contracts.py",
        "check_text_blobs.py",
        "check_docs_links.py",
        "check_example_integrity.py",
        "No private paths",
        "No secrets",
        "No invalid fake PDFs",
        "No generated `scratch/` outputs",
        "Release notes",
    ]:
        assert needle in text


def test_security_doc_warns_against_public_sensitive_content():
    text = (REPO_ROOT / "SECURITY.md").read_text(encoding="utf-8")
    assert "Do not submit private documents" in text
    assert "credentials" in text
    assert "public GitHub issues or pull requests" in text
    assert "heuristic checks" in text
    assert "make no network calls" in text


def test_readme_still_links_core_entry_points():
    text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for link in [
        "docs/start_here.md",
        "docs/common_paths.md",
        "docs/cli_reference.md",
        "docs/privacy_and_data_safety.md",
    ]:
        assert link in text


def test_public_trust_existing_checks_still_pass():
    for script in [
        "check_docs_links.py",
        "check_docs_examples.py",
        "check_example_integrity.py",
        "check_contracts.py",
        "check_text_blobs.py",
    ]:
        result = run_script(f"scripts/dev/{script}")
        assert result.returncode == 0, result.stdout + result.stderr


def test_run_tests_help_still_passes():
    result = run_script("scripts/dev/run_tests.py", "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--pytest-args" in result.stdout
