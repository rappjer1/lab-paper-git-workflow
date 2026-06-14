from pathlib import Path
import importlib.util
import os
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_TESTS = REPO_ROOT / "scripts" / "dev" / "run_tests.py"


def load_run_tests_module():
    spec = importlib.util.spec_from_file_location("run_tests_dev_script", RUN_TESTS)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_tests_help_works():
    result = subprocess.run(
        [sys.executable, str(RUN_TESTS), "--help"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--python" in result.stdout
    assert "--keep-temp" in result.stdout
    assert "--pytest-args" in result.stdout


def test_run_tests_creates_unique_basetemp(tmp_path):
    run_tests = load_run_tests_module()
    first_basetemp, first_temp = run_tests.create_run_paths(repo_root=tmp_path)
    second_basetemp, second_temp = run_tests.create_run_paths(repo_root=tmp_path)

    assert first_basetemp != second_basetemp
    assert first_temp != second_temp
    assert first_basetemp.parent == tmp_path / "scratch" / "test-runs"
    assert first_temp.parent == tmp_path / "scratch" / "test-runs"
    assert first_basetemp.exists()
    assert first_temp.exists()


def test_run_tests_builds_shell_independent_pytest_command(tmp_path):
    run_tests = load_run_tests_module()
    basetemp = tmp_path / "scratch" / "test-runs" / "pytest-example"
    command = run_tests.build_pytest_command("python", basetemp, ["-q"])

    assert command == [
        "python",
        "-m",
        "pytest",
        "tests",
        f"--basetemp={basetemp}",
        "-p",
        "no:cacheprovider",
        "-q",
    ]
    assert all(not part.startswith("TMP=") for part in command)
    assert "$PWD" not in " ".join(command)


def test_run_tests_env_sets_temp_without_bash_syntax(tmp_path, monkeypatch):
    run_tests = load_run_tests_module()
    monkeypatch.delenv("PYTHONDONTWRITEBYTECODE", raising=False)
    temp = tmp_path / "scratch" / "test-runs" / "tmp-example"
    env = run_tests.build_subprocess_env(temp)

    assert env["TMP"] == str(temp)
    assert env["TEMP"] == str(temp)
    assert env["PYTHONDONTWRITEBYTECODE"] == "1"
    assert "TMP=" not in env["TMP"]
    assert os.pathsep not in env["TMP"]


def test_docs_and_ci_prefer_run_tests_runner():
    docs = "\n".join(
        [
            (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "troubleshooting.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "install.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "compatibility.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "V0_9_CLEAN_INSTALL_NOTES.md").read_text(encoding="utf-8"),
        ]
    )
    workflow = (REPO_ROOT / ".github" / "workflows" / "tests.yml").read_text(encoding="utf-8")

    assert "scripts/dev/run_tests.py" in docs
    assert "R:\\Code\\Envs\\nh_quantum\\python.exe scripts\\dev\\run_tests.py" in docs
    assert "scratch/test-runs" in docs
    assert "TMP=\"$PWD/scratch/tmp\" TEMP=\"$PWD/scratch/tmp\"" in docs
    assert "python scripts/dev/run_tests.py" in workflow
