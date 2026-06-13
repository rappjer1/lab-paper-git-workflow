"""Config loading and small YAML helpers for paper_scaffold.

The project intentionally avoids a hard dependency on PyYAML. If PyYAML is
installed it is used. Otherwise, a small parser supports the simple mappings and
lists used by this repository's generated YAML files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_FORBIDDEN_PATTERNS = [
    "*.npz",
    "*.pt",
    "*.pth",
    "*.pkl",
    "*.nc",
    "*.zip",
    "data/external",
    "full_eval",
    "prediction_cache",
    "raw_api_cache",
    "raw_results",
    "raw_outputs",
]

DEFAULT_CONFIG: dict[str, Any] = {
    "project": {
        "title": "",
        "slug": "",
        "research_repo": "",
        "manuscript_repo": "",
        "github_repo": "",
        "overleaf_url": "",
        "main_tex": "main.tex",
        "supplement_tex": "supplement/supplement.tex",
        "has_supplement": True,
    },
    "validation": {
        "max_file_size_mb": 25,
        "forbidden_patterns": DEFAULT_FORBIDDEN_PATTERNS.copy(),
    },
}


def _strip_inline_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            if index == 0 or line[index - 1].isspace():
                return line[:index].rstrip()
    return line.rstrip()


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"[]", "[ ]"}:
        return []
    if value in {"{}", "{ }"}:
        return {}
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "none", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    try:
        if "." not in value:
            return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def _prepare_yaml_lines(text: str) -> list[tuple[int, str]]:
    prepared: list[tuple[int, str]] = []
    for raw in text.splitlines():
        raw = raw.rstrip()
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        line = _strip_inline_comment(raw)
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        prepared.append((indent, line.strip()))
    return prepared


def _split_key_value(content: str) -> tuple[str, str]:
    if ":" not in content:
        raise ValueError(f"Expected key/value YAML content, got: {content!r}")
    key, value = content.split(":", 1)
    return key.strip(), value.strip()


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    if lines[index][0] < indent:
        return {}, index

    is_list = lines[index][0] == indent and lines[index][1].startswith("- ")
    if is_list:
        items: list[Any] = []
        while index < len(lines):
            current_indent, content = lines[index]
            if current_indent < indent or current_indent != indent or not content.startswith("- "):
                break
            rest = content[2:].strip()
            if not rest:
                value, index = _parse_block(lines, index + 1, indent + 2)
                items.append(value)
                continue
            if ":" in rest:
                item: dict[str, Any] = {}
                key, value = _split_key_value(rest)
                index += 1
                if value:
                    item[key] = _parse_scalar(value)
                else:
                    nested, index = _parse_block(lines, index, indent + 2)
                    item[key] = nested
                while index < len(lines):
                    child_indent, child_content = lines[index]
                    if child_indent <= indent:
                        break
                    if child_indent != indent + 2 or child_content.startswith("- "):
                        break
                    child_key, child_value = _split_key_value(child_content)
                    index += 1
                    if child_value:
                        item[child_key] = _parse_scalar(child_value)
                    else:
                        nested, index = _parse_block(lines, index, indent + 4)
                        item[child_key] = nested
                items.append(item)
            else:
                items.append(_parse_scalar(rest))
                index += 1
        return items, index

    mapping: dict[str, Any] = {}
    while index < len(lines):
        current_indent, content = lines[index]
        if current_indent < indent or current_indent != indent or content.startswith("- "):
            break
        key, value = _split_key_value(content)
        index += 1
        if value:
            mapping[key] = _parse_scalar(value)
        elif index < len(lines) and lines[index][0] > current_indent:
            nested, index = _parse_block(lines, index, lines[index][0])
            mapping[key] = nested
        else:
            mapping[key] = {}
    return mapping, index


def loads_yaml(text: str) -> Any:
    try:
        import yaml  # type: ignore
    except Exception:
        lines = _prepare_yaml_lines(text)
        if not lines:
            return {}
        data, index = _parse_block(lines, 0, lines[0][0])
        if index != len(lines):
            raise ValueError("Could not parse the full YAML document")
        return data
    return yaml.safe_load(text) or {}


def load_yaml(path: str | Path) -> Any:
    path = Path(path)
    if not path.exists():
        return {}
    return loads_yaml(path.read_text(encoding="utf-8"))


def _format_scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    yaml_special_prefixes = (" ", "#", "{", "[", "*", "&", "!", "%", "@", "`", "-", "?", ":")
    if text == "" or text.startswith(yaml_special_prefixes) or ": " in text:
        return '"' + text.replace('"', '\\"') + '"'
    return text


def dumps_yaml(data: Any, indent: int = 0) -> str:
    lines: list[str] = []
    pad = " " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                if value == []:
                    lines.append(f"{pad}{key}: []")
                elif value == {}:
                    lines.append(f"{pad}{key}: {{}}")
                else:
                    lines.append(f"{pad}{key}:")
                    lines.append(dumps_yaml(value, indent + 2))
            else:
                lines.append(f"{pad}{key}: {_format_scalar(value)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if not item:
                    lines.append(f"{pad}- {{}}")
                    continue
                first = True
                for key, value in item.items():
                    prefix = "- " if first else "  "
                    if isinstance(value, (dict, list)):
                        if value == []:
                            lines.append(f"{pad}{prefix}{key}: []")
                        elif value == {}:
                            lines.append(f"{pad}{prefix}{key}: {{}}")
                        else:
                            lines.append(f"{pad}{prefix}{key}:")
                            lines.append(dumps_yaml(value, indent + 4))
                    else:
                        lines.append(f"{pad}{prefix}{key}: {_format_scalar(value)}")
                    first = False
            elif isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(dumps_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}- {_format_scalar(item)}")
    else:
        lines.append(f"{pad}{_format_scalar(data)}")
    return "\n".join(lines)


def write_yaml(path: str | Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dumps_yaml(data).rstrip() + "\n", encoding="utf-8")


def merge_config(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = {key: value.copy() if isinstance(value, dict) else value for key, value in base.items()}
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_config(merged[key], value)
        else:
            merged[key] = value
    return merged


@dataclass(frozen=True)
class ManuscriptConfig:
    """Loaded manuscript configuration."""

    data: dict[str, Any]
    path: Path | None = None

    @classmethod
    def load(cls, manuscript_repo: str | Path) -> "ManuscriptConfig":
        repo = Path(manuscript_repo)
        config_path = repo / "metadata" / "manuscript_config.yaml"
        raw = load_yaml(config_path)
        data = merge_config(DEFAULT_CONFIG, raw if isinstance(raw, dict) else {})
        if not data["project"].get("manuscript_repo"):
            data["project"]["manuscript_repo"] = str(repo)
        return cls(data=data, path=config_path if config_path.exists() else None)

    @classmethod
    def from_file(cls, path: str | Path) -> "ManuscriptConfig":
        path = Path(path)
        raw = load_yaml(path)
        data = merge_config(DEFAULT_CONFIG, raw if isinstance(raw, dict) else {})
        return cls(data=data, path=path)

    @property
    def project(self) -> dict[str, Any]:
        return self.data.get("project", {})

    @property
    def validation(self) -> dict[str, Any]:
        return self.data.get("validation", {})

    @property
    def manuscript_repo(self) -> Path:
        return Path(str(self.project.get("manuscript_repo") or "."))

    @property
    def main_tex(self) -> str:
        return str(self.project.get("main_tex") or "main.tex")

    @property
    def supplement_tex(self) -> str:
        return str(self.project.get("supplement_tex") or "supplement/supplement.tex")

    @property
    def has_supplement(self) -> bool:
        return bool(self.project.get("has_supplement", True))

    @property
    def max_file_size_mb(self) -> float:
        return float(self.validation.get("max_file_size_mb") or 25)

    @property
    def forbidden_patterns(self) -> list[str]:
        configured = self.validation.get("forbidden_patterns") or []
        patterns = list(dict.fromkeys(list(configured) + DEFAULT_FORBIDDEN_PATTERNS))
        return [str(pattern) for pattern in patterns]
