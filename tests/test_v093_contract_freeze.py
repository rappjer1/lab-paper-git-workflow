from pathlib import Path
import importlib.util
import re
import subprocess
import sys

from paper_scaffold.cli import build_parser
from paper_scaffold.messages import all_messages
from paper_scaffold.schema_reference import schema_names


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK_CONTRACTS = REPO_ROOT / "scripts" / "dev" / "check_contracts.py"
RUN_TESTS = REPO_ROOT / "scripts" / "dev" / "run_tests.py"
TEXT_BLOB_GUARD = REPO_ROOT / "scripts" / "dev" / "check_text_blobs.py"


def load_check_contracts_module():
    spec = importlib.util.spec_from_file_location("check_contracts_dev_script", CHECK_CONTRACTS)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def cli_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        choices = getattr(action, "choices", None)
        if choices:
            return set(choices)
    raise AssertionError("argparse subcommands not found")


def test_check_contracts_script_passes():
    result = subprocess.run(
        [sys.executable, str(CHECK_CONTRACTS)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Contract audit passed." in result.stdout


def test_every_cli_command_is_in_contracts():
    check_contracts = load_check_contracts_module()
    items = check_contracts.parse_contract_list(REPO_ROOT / "contracts" / "cli_commands.yaml", "commands")
    assert {item["command"] for item in items} == cli_commands()


def test_every_diagnostic_code_is_in_contracts():
    check_contracts = load_check_contracts_module()
    items = check_contracts.parse_contract_list(REPO_ROOT / "contracts" / "diagnostic_codes.yaml", "diagnostics")
    assert {item["code"] for item in items} == {message.code for message in all_messages()}


def test_every_schema_name_is_in_contracts():
    check_contracts = load_check_contracts_module()
    items = check_contracts.parse_contract_list(REPO_ROOT / "contracts" / "schema_names.yaml", "schemas")
    assert {item["schema"] for item in items} == set(schema_names())


def test_contract_policy_docs_exist():
    for rel in [
        "docs/contract.md",
        "docs/deprecation_policy.md",
        "docs/versioning_policy.md",
        "docs/v1_0_readiness.md",
    ]:
        assert (REPO_ROOT / rel).exists(), rel


def test_cli_reference_includes_all_commands_once():
    doc = (REPO_ROOT / "docs" / "cli_reference.md").read_text(encoding="utf-8")
    headings = re.findall(r"^### `([^`]+)`", doc, flags=re.MULTILINE)
    assert set(headings) == cli_commands()
    assert len(headings) == len(set(headings))


def test_error_codes_reference_includes_all_diagnostics():
    doc = (REPO_ROOT / "docs" / "error_codes.md").read_text(encoding="utf-8")
    for message in all_messages():
        assert message.code in doc


def test_schema_reference_includes_all_schema_names():
    doc = (REPO_ROOT / "docs" / "schema_reference.md").read_text(encoding="utf-8")
    for schema in schema_names():
        assert schema in doc


def test_readme_links_to_contract_docs():
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/contract.md" in readme
    assert "docs/versioning_policy.md" in readme
    assert "docs/v1_0_readiness.md" in readme


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
