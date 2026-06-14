from pathlib import Path
import importlib.util
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK_EXAMPLE_INTEGRITY = REPO_ROOT / "scripts" / "dev" / "check_example_integrity.py"
GENERATE_EXAMPLE_ARTIFACTS = REPO_ROOT / "scripts" / "dev" / "generate_example_artifacts.py"
CLEAN_CLONE_DOGFOOD_AUDIT = REPO_ROOT / "scripts" / "dev" / "clean_clone_dogfood_audit.py"
CHECK_DOCS_EXAMPLES = REPO_ROOT / "scripts" / "dev" / "check_docs_examples.py"
CHECK_CONTRACTS = REPO_ROOT / "scripts" / "dev" / "check_contracts.py"
TEXT_BLOB_GUARD = REPO_ROOT / "scripts" / "dev" / "check_text_blobs.py"
RUN_DOGFOOD = REPO_ROOT / "scripts" / "dev" / "run_dogfood.py"
RUN_TESTS = REPO_ROOT / "scripts" / "dev" / "run_tests.py"


DOGFOOD_PDFS = [
    REPO_ROOT / "examples" / "dogfood" / "python_outputs_to_manuscript" / "input" / "outputs" / "summary_plot.pdf",
    REPO_ROOT / "examples" / "dogfood" / "existing_latex_cleanup" / "project" / "figures" / "summary_plot.pdf",
    REPO_ROOT / "examples" / "dogfood" / "messy_project_audit" / "project" / "outputs" / "figure_final.pdf",
    REPO_ROOT / "examples" / "dogfood" / "messy_project_audit" / "project" / "outputs" / "figure_final2.pdf",
]


def load_clean_clone_audit_module():
    spec = importlib.util.spec_from_file_location("clean_clone_dogfood_audit_dev_script", CLEAN_CLONE_DOGFOOD_AUDIT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_script(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_example_integrity_checker_passes():
    result = run_script(CHECK_EXAMPLE_INTEGRITY)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Example integrity passed." in result.stdout


def test_dogfood_pdfs_are_valid_synthetic_pdfs():
    for path in DOGFOOD_PDFS:
        assert path.read_bytes().startswith(b"%PDF"), path


def test_generate_example_artifacts_check_lists_targets():
    result = run_script(GENERATE_EXAMPLE_ARTIFACTS, "--check")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "examples/minimal_python_artifacts/outputs/example_metric_plot.pdf" in result.stdout
    assert "examples/messy_project_archaeology/outputs/fig1_final.png" in result.stdout


def test_clean_clone_dogfood_audit_help_works():
    result = run_script(CLEAN_CLONE_DOGFOOD_AUDIT, "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--clone-path" in result.stdout
    assert "--overwrite" in result.stdout


def test_clean_clone_dogfood_audit_builds_expected_steps(tmp_path):
    audit = load_clean_clone_audit_module()
    steps = audit.build_steps(tmp_path, "python")
    commands = [" ".join(step.command) for step in steps]
    assert any("scripts/dev/check_example_integrity.py" in command for command in commands)
    assert any("scripts/dev/run_dogfood.py" in command for command in commands)
    assert any("scripts/dev/run_tests.py" in command for command in commands)


def test_example_integrity_docs_and_reports_exist():
    assert (REPO_ROOT / "docs" / "example_integrity.md").exists()
    assert (REPO_ROOT / "V0_9_5_PUBLIC_POLISH_AUDIT.md").exists()
    assert (REPO_ROOT / "V0_9_5_EXAMPLE_INTEGRITY_AND_DOGFOOD_REPORT.md").exists()


def test_examples_index_lists_dogfood_examples_and_integrity_check():
    doc = (REPO_ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    for scenario in [
        "dogfood/python_outputs_to_manuscript",
        "dogfood/existing_latex_cleanup",
        "dogfood/reviewer_response_round",
        "dogfood/submission_package",
        "dogfood/messy_project_audit",
    ]:
        assert scenario in doc
    assert "check_example_integrity.py" in doc


def test_check_docs_examples_still_passes():
    result = run_script(CHECK_DOCS_EXAMPLES)
    assert result.returncode == 0, result.stdout + result.stderr


def test_check_contracts_still_passes():
    result = run_script(CHECK_CONTRACTS)
    assert result.returncode == 0, result.stdout + result.stderr


def test_text_blob_guard_still_passes():
    result = run_script(TEXT_BLOB_GUARD)
    assert result.returncode == 0, result.stdout + result.stderr


def test_run_dogfood_still_passes(tmp_path):
    result = run_script(RUN_DOGFOOD, "--output", str(tmp_path / "dogfood"), "--keep-output")
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / "dogfood" / "demo_manuscript").exists()
    assert "Dogfood summary:" in result.stdout


def test_run_tests_help_still_passes():
    result = run_script(RUN_TESTS, "--help")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--pytest-args" in result.stdout
