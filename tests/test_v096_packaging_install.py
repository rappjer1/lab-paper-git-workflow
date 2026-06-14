from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_PACKAGE = REPO_ROOT / "scripts" / "dev" / "build_package.py"
INSTALL_MATRIX_AUDIT = REPO_ROOT / "scripts" / "dev" / "install_matrix_audit.py"
CHECK_CONTRACTS = REPO_ROOT / "scripts" / "dev" / "check_contracts.py"


def run_script(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_build_package_help_works():
    result = run_script(BUILD_PACKAGE, "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--dist-dir" in result.stdout
    assert "--clean" in result.stdout
    assert "--isolated" in result.stdout


def test_install_matrix_audit_help_works():
    result = run_script(INSTALL_MATRIX_AUDIT, "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--work-dir" in result.stdout
    assert "--dist-dir" in result.stdout
    assert "--allow-deps" in result.stdout


def test_install_matrix_existing_work_dir_is_not_removed(tmp_path):
    work_dir = tmp_path / "existing-work-dir"
    work_dir.mkdir()
    marker = work_dir / "keep.txt"
    marker.write_text("do not remove\n", encoding="utf-8")

    result = run_script(INSTALL_MATRIX_AUDIT, "--work-dir", str(work_dir))

    assert result.returncode == 2
    assert marker.exists()
    assert "already exists" in result.stderr


def test_pyproject_includes_build_optional_extra_not_runtime_dependency():
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'build = ["build>=1.2"]' in text
    dependencies_block = text.split("[project.optional-dependencies]", maxsplit=1)[0]
    assert '"build' not in dependencies_block


def test_install_docs_mention_module_fallback_and_no_pypi_publishing():
    docs = "\n".join(
        [
            (REPO_ROOT / "README.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "install.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "release_process.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"),
        ]
    )
    assert "python -m paper_scaffold" in docs
    assert "scripts/dev/build_package.py" in docs
    assert "scripts/dev/install_matrix_audit.py" in docs
    assert "Do not publish to PyPI" in docs


def test_existing_contract_audit_still_passes():
    result = run_script(CHECK_CONTRACTS)
    assert result.returncode == 0, result.stdout + result.stderr
