"""Check Paper Scaffold public contract metadata against implementation and docs."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from paper_scaffold.cli import build_parser  # noqa: E402
from paper_scaffold.messages import all_messages  # noqa: E402
from paper_scaffold.schema_reference import schema_names  # noqa: E402


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_contract_list(path: Path, root_key: str) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    items: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_root = False
    for raw_line in lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith(" ") and raw_line.strip() == f"{root_key}:":
            in_root = True
            continue
        if not in_root:
            continue
        stripped = raw_line.strip()
        if stripped.startswith("- "):
            if current is not None:
                items.append(current)
            current = {}
            remainder = stripped[2:].strip()
            if remainder:
                key, value = split_key_value(remainder, path)
                current[key] = parse_scalar(value)
        elif current is not None:
            key, value = split_key_value(stripped, path)
            current[key] = parse_scalar(value)
    if current is not None:
        items.append(current)
    return items


def split_key_value(text: str, path: Path) -> tuple[str, str]:
    if ":" not in text:
        raise ValueError(f"expected key/value in {path}: {text}")
    key, value = text.split(":", 1)
    return key.strip(), value.strip()


def get_argparse_commands() -> list[str]:
    parser = build_parser()
    for action in parser._actions:
        choices = getattr(action, "choices", None)
        if choices:
            return sorted(choices)
    raise RuntimeError("could not find argparse subcommands")


def read_doc(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def check_set(label: str, expected: set[str], actual: set[str]) -> list[str]:
    problems: list[str] = []
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        problems.append(f"{label} missing: {', '.join(missing)}")
    if extra:
        problems.append(f"{label} extra: {', '.join(extra)}")
    return problems


def check_cli_contract() -> list[str]:
    problems: list[str] = []
    commands = set(get_argparse_commands())
    contract_items = parse_contract_list(REPO_ROOT / "contracts" / "cli_commands.yaml", "commands")
    contract_commands = {str(item.get("command", "")) for item in contract_items}
    problems.extend(check_set("contracts/cli_commands.yaml commands", commands, contract_commands))
    for item in contract_items:
        for key in ["command", "purpose", "modifies_files", "stable_for_1_0", "notes"]:
            if key not in item:
                problems.append(f"cli command entry missing {key}: {item}")

    doc = read_doc("docs/cli_reference.md")
    doc_commands = set(re.findall(r"^### `([^`]+)`", doc, flags=re.MULTILINE))
    problems.extend(check_set("docs/cli_reference.md command headings", commands, doc_commands))
    return problems


def check_diagnostic_contract() -> list[str]:
    problems: list[str] = []
    messages = {message.code: message for message in all_messages()}
    contract_items = parse_contract_list(REPO_ROOT / "contracts" / "diagnostic_codes.yaml", "diagnostics")
    contract_codes = {str(item.get("code", "")) for item in contract_items}
    problems.extend(check_set("contracts/diagnostic_codes.yaml codes", set(messages), contract_codes))
    for item in contract_items:
        code = str(item.get("code", ""))
        for key in ["code", "severity", "title", "stable_for_1_0", "notes"]:
            if key not in item:
                problems.append(f"diagnostic entry missing {key}: {item}")
        if code in messages and item.get("severity") != messages[code].severity:
            problems.append(f"diagnostic severity mismatch for {code}: contract={item.get('severity')} implementation={messages[code].severity}")

    doc = read_doc("docs/error_codes.md")
    for code in sorted(messages):
        if not re.search(rf"\b{re.escape(code)}\b", doc):
            problems.append(f"docs/error_codes.md missing {code}")
    return problems


def check_schema_contract() -> list[str]:
    problems: list[str] = []
    schemas = set(schema_names())
    contract_items = parse_contract_list(REPO_ROOT / "contracts" / "schema_names.yaml", "schemas")
    contract_schemas = {str(item.get("schema", "")) for item in contract_items}
    problems.extend(check_set("contracts/schema_names.yaml schemas", schemas, contract_schemas))
    for item in contract_items:
        for key in ["schema", "user_authored", "generated", "stable_for_1_0", "docs_path"]:
            if key not in item:
                problems.append(f"schema entry missing {key}: {item}")
    doc = read_doc("docs/schema_reference.md")
    for schema in sorted(schemas):
        if schema not in doc:
            problems.append(f"docs/schema_reference.md missing {schema}")
    return problems


def check_exit_code_contract() -> list[str]:
    problems: list[str] = []
    expected_codes = {"0", "1", "2"}
    contract_items = parse_contract_list(REPO_ROOT / "contracts" / "exit_codes.yaml", "exit_codes")
    contract_codes = {str(item.get("code", "")) for item in contract_items}
    problems.extend(check_set("contracts/exit_codes.yaml codes", expected_codes, contract_codes))
    for item in contract_items:
        for key in ["code", "meaning", "stable_for_1_0"]:
            if key not in item:
                problems.append(f"exit code entry missing {key}: {item}")
    doc = read_doc("docs/exit_codes.md")
    for code in sorted(expected_codes):
        if f"`{code}`" not in doc:
            problems.append(f"docs/exit_codes.md missing exit code {code}")
    return problems


def main() -> int:
    checks = [
        ("CLI commands", check_cli_contract),
        ("Diagnostic codes", check_diagnostic_contract),
        ("Schemas", check_schema_contract),
        ("Exit codes", check_exit_code_contract),
    ]
    problems: list[str] = []
    print("Paper Scaffold contract audit")
    for label, check in checks:
        found = check()
        if found:
            print(f"- {label}: {len(found)} problem(s)")
            problems.extend(found)
        else:
            print(f"- {label}: ok")
    if problems:
        print("\nContract audit failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("\nContract audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
