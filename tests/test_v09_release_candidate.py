from pathlib import Path
import os
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_scaffold import __version__
from paper_scaffold.cli import build_parser, main


REPO_ROOT = Path(__file__).resolve().parents[1]


def _pythonpath_env() -> dict[str, str]:
    env = os.environ.copy()
    src = str(REPO_ROOT / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src if not existing else src + os.pathsep + existing
    return env


def test_python_m_paper_scaffold_help_works():
    result = subprocess.run(
        [sys.executable, "-m", "paper_scaffold", "--help"],
        cwd=REPO_ROOT,
        env=_pythonpath_env(),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "paper-scaffold" in result.stdout
    assert "self-test" in result.stdout


def test_version_output_includes_current_version():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "paper-scaffold.py"), "--version"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert __version__ == "0.9.5"
    assert "0.9.5" in result.stdout


def test_self_test_with_temp_output_cleans_up(tmp_path):
    output = tmp_path / "self_test"
    assert main(["self-test", "--output", str(output)]) == 0
    assert not output.exists()


def test_self_test_keep_output(tmp_path):
    output = tmp_path / "self_test_keep"
    assert main(["self-test", "--output", str(output), "--keep-output"]) == 0
    assert (output / "demo_manuscript").exists()
    assert (output / "submission_package").exists()
    assert (output / "reviewer_response_round_1").exists()


def test_schema_list(capsys):
    assert main(["schema", "list"]) == 0
    output = capsys.readouterr().out
    assert "artifact-manifest" in output
    assert "lock-comparison" in output


def test_schema_show_artifact_manifest(capsys):
    assert main(["schema", "show", "artifact-manifest"]) == 0
    output = capsys.readouterr().out
    assert "# artifact_manifest.yaml" in output
    assert "manuscript_path" in output


def test_schema_show_json(capsys):
    assert main(["schema", "show", "artifact-manifest", "--json"]) == 0
    output = capsys.readouterr().out
    assert '"name": "artifact-manifest"' in output
    assert '"fields"' in output


def test_v09_docs_exist_and_readme_links_them():
    docs = [
        "docs/cli_reference.md",
        "docs/schema_reference.md",
        "docs/install.md",
        "docs/release_process.md",
        "docs/exit_codes.md",
        "docs/compatibility.md",
    ]
    for rel in docs:
        assert (REPO_ROOT / rel).exists(), rel
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/install.md" in readme
    assert "docs/cli_reference.md" in readme
    assert "docs/schema_reference.md" in readme
    assert "docs/release_process.md" in readme


def test_package_version_consistency():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', pyproject, re.MULTILINE)
    assert match is not None
    assert match.group(1) == __version__ == "0.9.5"


def test_text_blob_guard_still_passes():
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "dev" / "check_text_blobs.py")],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_all_command_parsers_still_load():
    parser = build_parser()
    help_text = parser.format_help()
    for command in [
        "doctor",
        "self-test",
        "schema",
        "demo",
        "validate",
        "release-check",
        "provenance-report",
        "package-submission",
        "reviewer-binder",
    ]:
        assert command in help_text


def test_installed_path_fallback_docs_mention_python_m():
    docs = "\n".join(
        [
            (REPO_ROOT / "README.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "QUICKSTART.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "getting_started.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "troubleshooting.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"),
            (REPO_ROOT / "docs" / "install.md").read_text(encoding="utf-8"),
        ]
    )
    assert "python -m paper_scaffold --help" in docs
    assert "python -m paper_scaffold self-test" in docs
