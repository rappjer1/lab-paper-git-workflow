from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_DOGFOOD = REPO_ROOT / "scripts" / "dev" / "run_dogfood.py"
CHECK_DOCS_EXAMPLES = REPO_ROOT / "scripts" / "dev" / "check_docs_examples.py"
CHECK_CONTRACTS = REPO_ROOT / "scripts" / "dev" / "check_contracts.py"
TEXT_BLOB_GUARD = REPO_ROOT / "scripts" / "dev" / "check_text_blobs.py"
RUN_TESTS = REPO_ROOT / "scripts" / "dev" / "run_tests.py"


DOGFOOD_SCENARIOS = [
    "python_outputs_to_manuscript",
    "existing_latex_cleanup",
    "reviewer_response_round",
    "submission_package",
    "messy_project_audit",
]


def test_run_dogfood_succeeds_in_temp_output(tmp_path):
    output = tmp_path / "dogfood"
    result = subprocess.run(
        [sys.executable, str(RUN_DOGFOOD), "--output", str(output), "--keep-output"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / "dogfood_report.md").exists()
    assert (output / "demo_manuscript").exists()
    assert (output / "submission_package").exists()
    assert "Dogfood summary:" in result.stdout


def test_check_docs_examples_passes():
    result = subprocess.run(
        [sys.executable, str(CHECK_DOCS_EXAMPLES)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Docs/examples check" in result.stdout


def test_which_workflow_exists_and_includes_core_workflows():
    doc = (REPO_ROOT / "docs" / "which_workflow.md").read_text(encoding="utf-8")
    for phrase in [
        "Word draft",
        "Python outputs",
        "LaTeX",
        "submission package",
        "reviewers",
        "messy project",
        "Overleaf sync",
    ]:
        assert phrase in doc


def test_examples_index_lists_dogfood_examples():
    doc = (REPO_ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    for scenario in DOGFOOD_SCENARIOS:
        assert f"dogfood/{scenario}" in doc


def test_dogfood_scenario_folders_exist():
    for scenario in DOGFOOD_SCENARIOS:
        folder = REPO_ROOT / "examples" / "dogfood" / scenario
        assert (folder / "README.md").exists()
        assert (folder / "expected_commands.md").exists()
        assert (folder / "expected_outputs.md").exists()
        assert (folder / "input").exists() or (folder / "project").exists()


def test_readme_links_to_which_workflow():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/which_workflow.md" in readme


def test_quickstart_includes_core_checkout_commands():
    quickstart = (REPO_ROOT / "QUICKSTART.md").read_text(encoding="utf-8")
    for command in ["self-test", "demo", "discover-artifacts", "release-check"]:
        assert command in quickstart
    assert "python scripts/paper-scaffold.py" in quickstart
    assert "python -m paper_scaffold" in quickstart


def test_v1_0_prep_notes_exist():
    assert (REPO_ROOT / "V1_0_PREP_NOTES.md").exists()


def test_check_contracts_still_passes():
    result = subprocess.run(
        [sys.executable, str(CHECK_CONTRACTS)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_text_blob_guard_still_passes():
    result = subprocess.run(
        [sys.executable, str(TEXT_BLOB_GUARD)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_run_tests_help_still_passes():
    result = subprocess.run(
        [sys.executable, str(RUN_TESTS), "--help"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--pytest-args" in result.stdout
