from pathlib import Path
import importlib.util
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
CLEAN_INSTALL_AUDIT = REPO_ROOT / "scripts" / "dev" / "clean_install_audit.py"
RUN_TESTS = REPO_ROOT / "scripts" / "dev" / "run_tests.py"
TEXT_BLOB_GUARD = REPO_ROOT / "scripts" / "dev" / "check_text_blobs.py"


def load_clean_install_audit_module():
    spec = importlib.util.spec_from_file_location("clean_install_audit_dev_script", CLEAN_INSTALL_AUDIT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_clean_install_audit_help_works():
    result = subprocess.run(
        [sys.executable, str(CLEAN_INSTALL_AUDIT), "--help"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--clone-path" in result.stdout
    assert "--source" in result.stdout
    assert "--python" in result.stdout
    assert "--overwrite" in result.stdout


def test_clean_install_audit_command_construction_without_network(tmp_path):
    audit = load_clean_install_audit_module()
    clone_path = tmp_path / "scratch" / "clean-install" / "paper-scaffold-audit"

    clone_step = audit.build_clone_command("https://example.invalid/paper-scaffold.git", clone_path)
    required_steps = audit.build_required_audit_commands("python", clone_path)
    console_step = audit.build_console_script_command(clone_path)
    build_probe = audit.build_package_build_probe("python", clone_path)
    build_step = audit.build_package_build_command("python", clone_path)

    assert clone_step.command == ["git", "clone", "https://example.invalid/paper-scaffold.git", str(clone_path)]
    assert [step.name for step in required_steps] == [
        "no-install help",
        "no-install self-test",
        "editable install",
        "module fallback help",
        "installed self-test fallback",
        "text blob guard",
        "pytest runner",
    ]
    assert required_steps[0].command == ["python", "scripts/paper-scaffold.py", "--help"]
    assert required_steps[2].command == ["python", "-m", "pip", "install", "-e", ".[dev]"]
    assert required_steps[3].command == ["python", "-m", "paper_scaffold", "--help"]
    assert required_steps[-1].command == ["python", "scripts/dev/run_tests.py"]
    assert console_step.command == ["paper-scaffold", "--help"]
    assert console_step.required is False
    assert build_probe.command == ["python", "-m", "build", "--version"]
    assert build_step.command == ["python", "-m", "build"]
    assert build_step.required is False


def test_clean_install_audit_default_clone_path_is_unique_under_scratch(tmp_path):
    audit = load_clean_install_audit_module()
    first = audit.default_clone_path(repo_root=tmp_path)
    second = audit.default_clone_path(repo_root=tmp_path)

    assert first != second
    assert first.parent == tmp_path / "scratch" / "clean-install"
    assert first.name.startswith("paper-scaffold-")


def test_clean_install_audit_docs_exist_and_are_linked():
    doc = REPO_ROOT / "docs" / "clean_install_audit.md"
    assert doc.exists()
    docs = "\n".join(
        [
            doc.read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "install.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"),
        ]
    )
    assert "scripts/dev/clean_install_audit.py" in docs
    assert "scratch/clean-install" in docs
    assert "python -m pip install -e \".[dev]\"" in docs
    assert "python scripts/dev/run_tests.py" in docs


def test_run_tests_help_still_works():
    result = subprocess.run(
        [sys.executable, str(RUN_TESTS), "--help"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--pytest-args" in result.stdout


def test_text_blob_guard_still_passes():
    result = subprocess.run(
        [sys.executable, str(TEXT_BLOB_GUARD)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
