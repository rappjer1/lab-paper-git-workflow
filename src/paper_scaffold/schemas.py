"""Lightweight schema definitions and validation for Paper Scaffold metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import load_yaml
from .messages import DiagnosticFinding

ARTIFACT_TYPES = {"figure", "table", "data_summary", "supplement_figure", "supplement_table"}


@dataclass(frozen=True)
class FieldSchema:
    name: str
    required: bool
    expected_type: str
    description: str


@dataclass(frozen=True)
class FileSchema:
    name: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...]
    description: str

    @property
    def allowed_fields(self) -> set[str]:
        return set(self.required_fields) | set(self.optional_fields)


ARTIFACT_ENTRY_SCHEMA = FileSchema(
    name="artifact manifest entry",
    required_fields=("id", "type", "manuscript_path", "source_path"),
    optional_fields=("source_repo", "generated_by", "input_data", "last_updated", "caption_hint", "status"),
    description="One copied or candidate manuscript artifact with provenance.",
)

ARTIFACT_MANIFEST_SCHEMA = FileSchema(
    name="artifact_manifest.yaml",
    required_fields=("artifacts",),
    optional_fields=(),
    description="List of manuscript figures/tables and their source provenance.",
)

TERMINOLOGY_ENTRY_SCHEMA = FileSchema(
    name="terminology map entry",
    required_fields=(),
    optional_fields=("publication_label", "banned_in", "allowed_contexts", "notes"),
    description="Mapping from implementation terminology to publication-facing wording.",
)

MANUSCRIPT_CONFIG_PROJECT_SCHEMA = FileSchema(
    name="manuscript_config.yaml project",
    required_fields=(),
    optional_fields=(
        "title",
        "slug",
        "research_repo",
        "manuscript_repo",
        "github_repo",
        "overleaf_url",
        "main_tex",
        "supplement_tex",
        "has_supplement",
        "preferred_branch",
        "figure_dir",
        "table_dir",
    ),
    description="Project-level manuscript repository settings.",
)

MANUSCRIPT_CONFIG_VALIDATION_SCHEMA = FileSchema(
    name="manuscript_config.yaml validation",
    required_fields=(),
    optional_fields=("max_file_size_mb", "forbidden_patterns"),
    description="Validation thresholds and forbidden raw-output patterns.",
)

VALIDATION_REPORT_SCHEMA = FileSchema(
    name="validation_report.json",
    required_fields=("tool", "version", "timestamp", "path", "summary", "diagnostics"),
    optional_fields=(),
    description="Machine-readable validation report emitted by paper-scaffold validate --write-json.",
)

VALIDATION_DIAGNOSTIC_SCHEMA = FileSchema(
    name="validation report diagnostic",
    required_fields=("code", "severity", "title", "path", "message", "suggested_fix"),
    optional_fields=("line",),
    description="One diagnostic entry in validation_report.json.",
)


def _as_posix(path: str | Path) -> str:
    return Path(path).as_posix()


def _unknown_field_findings(mapping: dict[str, Any], allowed: set[str], path: str | Path, prefix: str) -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    for field in sorted(set(mapping) - allowed):
        findings.append(DiagnosticFinding("W018", f"{prefix} unknown field: {field}", _as_posix(path)))
    return findings


def _required_field_findings(
    mapping: dict[str, Any],
    required: tuple[str, ...],
    path: str | Path,
    prefix: str,
    code: str,
) -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    for field in required:
        value = mapping.get(field)
        if field not in mapping or value is None or value == "":
            findings.append(DiagnosticFinding(code, f"{prefix} missing required field: {field}", _as_posix(path)))
    return findings


def validate_artifact_manifest_schema(data: Any, path: str | Path = "metadata/artifact_manifest.yaml") -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    if not isinstance(data, dict):
        return [DiagnosticFinding("E004", "artifact manifest must be a mapping", _as_posix(path))]
    findings.extend(_required_field_findings(data, ARTIFACT_MANIFEST_SCHEMA.required_fields, path, "top-level", "E004"))
    findings.extend(_unknown_field_findings(data, ARTIFACT_MANIFEST_SCHEMA.allowed_fields, path, "top-level"))
    artifacts = data.get("artifacts")
    if artifacts is None:
        return findings
    if not isinstance(artifacts, list):
        findings.append(DiagnosticFinding("E004", "top-level field artifacts must be a list", _as_posix(path)))
        return findings
    seen: set[str] = set()
    for index, artifact in enumerate(artifacts, start=1):
        prefix = f"artifact[{index}]"
        if not isinstance(artifact, dict):
            findings.append(DiagnosticFinding("E004", f"{prefix} must be a mapping", _as_posix(path)))
            continue
        findings.extend(_required_field_findings(artifact, ARTIFACT_ENTRY_SCHEMA.required_fields, path, prefix, "E004"))
        findings.extend(_unknown_field_findings(artifact, ARTIFACT_ENTRY_SCHEMA.allowed_fields, path, prefix))
        artifact_id = str(artifact.get("id") or "").strip()
        if artifact_id:
            if artifact_id in seen:
                findings.append(DiagnosticFinding("E004", f"{prefix} duplicate id: {artifact_id}", _as_posix(path)))
            seen.add(artifact_id)
        artifact_type = str(artifact.get("type") or "").strip()
        if artifact_type and artifact_type not in ARTIFACT_TYPES:
            findings.append(DiagnosticFinding("E004", f"{prefix} unsupported type: {artifact_type}", _as_posix(path)))
    return findings


def validate_artifact_manifest_file(path: str | Path) -> list[DiagnosticFinding]:
    return validate_artifact_manifest_schema(load_yaml(path), path)


def validate_terminology_map_schema(data: Any, path: str | Path = "metadata/terminology_map.yaml") -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    if not isinstance(data, dict):
        return [DiagnosticFinding("E016", "terminology map must be a mapping", _as_posix(path))]
    findings.extend(_unknown_field_findings(data, {"terms"}, path, "top-level"))
    terms = data.get("terms", {})
    if not isinstance(terms, dict):
        return findings + [DiagnosticFinding("E016", "top-level field terms must be a mapping", _as_posix(path))]
    for term, details in terms.items():
        prefix = f"term[{term}]"
        if isinstance(details, str):
            continue
        if not isinstance(details, dict):
            findings.append(DiagnosticFinding("E016", f"{prefix} must be a string or mapping", _as_posix(path)))
            continue
        findings.extend(_unknown_field_findings(details, TERMINOLOGY_ENTRY_SCHEMA.allowed_fields, path, prefix))
        for list_field in ("banned_in", "allowed_contexts"):
            if list_field in details and not isinstance(details[list_field], list):
                findings.append(DiagnosticFinding("E016", f"{prefix}.{list_field} must be a list", _as_posix(path)))
    return findings


def validate_terminology_map_file(path: str | Path) -> list[DiagnosticFinding]:
    return validate_terminology_map_schema(load_yaml(path), path)


def validate_manuscript_config_schema(data: Any, path: str | Path = "metadata/manuscript_config.yaml") -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    if not isinstance(data, dict):
        return [DiagnosticFinding("E016", "manuscript config must be a mapping", _as_posix(path))]
    findings.extend(_unknown_field_findings(data, {"project", "validation"}, path, "top-level"))
    project = data.get("project", {})
    validation = data.get("validation", {})
    if project and not isinstance(project, dict):
        findings.append(DiagnosticFinding("E016", "project must be a mapping", _as_posix(path)))
    elif isinstance(project, dict):
        findings.extend(_unknown_field_findings(project, MANUSCRIPT_CONFIG_PROJECT_SCHEMA.allowed_fields, path, "project"))
        if "has_supplement" in project and not isinstance(project["has_supplement"], bool):
            findings.append(DiagnosticFinding("E016", "project.has_supplement must be true or false", _as_posix(path)))
    if validation and not isinstance(validation, dict):
        findings.append(DiagnosticFinding("E016", "validation must be a mapping", _as_posix(path)))
    elif isinstance(validation, dict):
        findings.extend(_unknown_field_findings(validation, MANUSCRIPT_CONFIG_VALIDATION_SCHEMA.allowed_fields, path, "validation"))
        if "max_file_size_mb" in validation and not isinstance(validation["max_file_size_mb"], (int, float)):
            findings.append(DiagnosticFinding("E016", "validation.max_file_size_mb must be numeric", _as_posix(path)))
        if "forbidden_patterns" in validation and not isinstance(validation["forbidden_patterns"], list):
            findings.append(DiagnosticFinding("E016", "validation.forbidden_patterns must be a list", _as_posix(path)))
    return findings


def validate_manuscript_config_file(path: str | Path) -> list[DiagnosticFinding]:
    return validate_manuscript_config_schema(load_yaml(path), path)


def validate_validation_report_json_schema(data: Any, path: str | Path = "validation_report.json") -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    if not isinstance(data, dict):
        return [DiagnosticFinding("E016", "validation report must be a mapping", _as_posix(path))]
    findings.extend(_required_field_findings(data, VALIDATION_REPORT_SCHEMA.required_fields, path, "top-level", "E016"))
    findings.extend(_unknown_field_findings(data, VALIDATION_REPORT_SCHEMA.allowed_fields, path, "top-level"))
    summary = data.get("summary", {})
    if not isinstance(summary, dict):
        findings.append(DiagnosticFinding("E016", "summary must be a mapping", _as_posix(path)))
    else:
        for field in ("errors", "warnings", "info"):
            if not isinstance(summary.get(field), int):
                findings.append(DiagnosticFinding("E016", f"summary.{field} must be an integer", _as_posix(path)))
    diagnostics = data.get("diagnostics", [])
    if not isinstance(diagnostics, list):
        findings.append(DiagnosticFinding("E016", "diagnostics must be a list", _as_posix(path)))
        return findings
    for index, diagnostic in enumerate(diagnostics, start=1):
        prefix = f"diagnostics[{index}]"
        if not isinstance(diagnostic, dict):
            findings.append(DiagnosticFinding("E016", f"{prefix} must be a mapping", _as_posix(path)))
            continue
        for field in VALIDATION_DIAGNOSTIC_SCHEMA.required_fields:
            if field not in diagnostic or diagnostic.get(field) is None:
                findings.append(DiagnosticFinding("E016", f"{prefix} missing required field: {field}", _as_posix(path)))
        findings.extend(_unknown_field_findings(diagnostic, VALIDATION_DIAGNOSTIC_SCHEMA.allowed_fields, path, prefix))
    return findings
