"""Readable schema summaries for Paper Scaffold metadata files."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


@dataclass(frozen=True)
class SchemaField:
    name: str
    expected_type: str
    required: bool
    description: str


@dataclass(frozen=True)
class SchemaReference:
    name: str
    title: str
    status: str
    authored_by: str
    description: str
    fields: tuple[SchemaField, ...]
    minimal_example: str


SCHEMAS: dict[str, SchemaReference] = {
    "artifact-manifest": SchemaReference(
        name="artifact-manifest",
        title="artifact_manifest.yaml",
        status="pre-1.0 stable",
        authored_by="user-authored",
        description="Tracks selected manuscript figures, tables, and data summaries copied from research outputs.",
        fields=(
            SchemaField("artifacts", "list[artifact]", True, "Artifact entries for files copied or proposed for the manuscript."),
            SchemaField("artifacts[].id", "string", True, "Stable artifact identifier."),
            SchemaField("artifacts[].type", "string", True, "One of figure, table, data_summary, supplement_figure, supplement_table."),
            SchemaField("artifacts[].manuscript_path", "string", True, "Path inside the manuscript repository."),
            SchemaField("artifacts[].source_path", "string", True, "Path to the source output, absolute or relative to source_repo."),
            SchemaField("artifacts[].source_repo", "string", False, "Research repository or source folder."),
            SchemaField("artifacts[].generated_by", "string", False, "Script or workflow that generated the source output."),
            SchemaField("artifacts[].input_data", "string", False, "Small human-readable input summary."),
            SchemaField("artifacts[].last_updated", "string", False, "Date or timestamp maintained by the user."),
            SchemaField("artifacts[].status", "string", False, "Draft/final/example/local status label."),
        ),
        minimal_example=(
            "artifacts:\n"
            "  - id: example_metric_plot\n"
            "    type: figure\n"
            "    manuscript_path: figures/example_metric_plot.pdf\n"
            "    source_repo: ../research_project\n"
            "    source_path: outputs/example_metric_plot.pdf\n"
        ),
    ),
    "manuscript-config": SchemaReference(
        name="manuscript-config",
        title="manuscript_config.yaml",
        status="pre-1.0 stable",
        authored_by="user-authored",
        description="Stores manuscript repo settings and validation thresholds.",
        fields=(
            SchemaField("project", "mapping", False, "Project-level metadata."),
            SchemaField("project.title", "string", False, "Human-readable manuscript title."),
            SchemaField("project.slug", "string", False, "Short identifier for generated labels and folders."),
            SchemaField("project.main_tex", "string", False, "Main TeX source file; default is main.tex."),
            SchemaField("project.supplement_tex", "string", False, "Supplement TeX file; default is supplement/supplement.tex."),
            SchemaField("project.has_supplement", "boolean", False, "Whether supplement_tex is expected."),
            SchemaField("validation.max_file_size_mb", "number", False, "Large-file threshold."),
            SchemaField("validation.forbidden_patterns", "list[string]", False, "Raw/cache/model-output patterns to block."),
        ),
        minimal_example=(
            "project:\n"
            "  title: Example Paper\n"
            "  slug: example_paper\n"
            "  main_tex: main.tex\n"
            "  has_supplement: true\n"
            "validation:\n"
            "  max_file_size_mb: 25\n"
        ),
    ),
    "terminology-map": SchemaReference(
        name="terminology-map",
        title="terminology_map.yaml",
        status="pre-1.0 stable",
        authored_by="user-authored",
        description="Maps implementation labels to publication-facing language and flags banned manuscript terms.",
        fields=(
            SchemaField("terms", "mapping", True, "Implementation term keys."),
            SchemaField("terms.<term>.publication_label", "string", False, "Preferred manuscript wording."),
            SchemaField("terms.<term>.banned_in", "list[string]", False, "Contexts where the term should not appear."),
            SchemaField("terms.<term>.allowed_contexts", "list[string]", False, "Contexts where the term is acceptable."),
            SchemaField("terms.<term>.notes", "string", False, "Reviewer or maintainer notes."),
        ),
        minimal_example=(
            "terms:\n"
            "  internal_metric_name:\n"
            "    publication_label: descriptive metric name\n"
            "    banned_in:\n"
            "      - main_text\n"
        ),
    ),
    "provenance-ledger": SchemaReference(
        name="provenance-ledger",
        title="provenance_ledger.json",
        status="generated pre-1.0 stable",
        authored_by="generated",
        description="Generated bill of materials for manuscript artifacts, source hashes, and TeX usage.",
        fields=(
            SchemaField("tool", "string", True, "Tool name."),
            SchemaField("version", "string", True, "Paper Scaffold version."),
            SchemaField("generated_at", "string", True, "UTC timestamp."),
            SchemaField("manuscript_repo", "string", True, "Repository path used for the report."),
            SchemaField("summary", "mapping", True, "Current/stale/missing/untracked counts."),
            SchemaField("artifacts", "list[artifact]", True, "Generated provenance entries."),
            SchemaField("untracked_artifacts", "list[artifact]", False, "Artifact-like files not in the manifest."),
        ),
        minimal_example='{"tool": "Paper Scaffold", "version": "0.9.4", "summary": {"current": 1}, "artifacts": []}',
    ),
    "artifact-lock": SchemaReference(
        name="artifact-lock",
        title="artifact_lock.json",
        status="generated pre-1.0 stable",
        authored_by="generated",
        description="Frozen manuscript artifact hashes for a submission or revision handoff.",
        fields=(
            SchemaField("tool", "string", True, "Tool name."),
            SchemaField("version", "string", True, "Paper Scaffold version."),
            SchemaField("generated_at", "string", True, "UTC timestamp."),
            SchemaField("manuscript_repo", "string", True, "Repository path used for the lock."),
            SchemaField("artifacts", "list[locked artifact]", True, "Artifact ids, paths, hashes, mtimes, and statuses."),
        ),
        minimal_example='{"tool": "Paper Scaffold", "version": "0.9.4", "artifacts": [{"artifact_id": "fig1", "manuscript_path": "figures/fig1.pdf", "manuscript_sha256": "..."}]}',
    ),
    "validation-report": SchemaReference(
        name="validation-report",
        title="validation_report.json",
        status="generated pre-1.0 stable",
        authored_by="generated",
        description="Machine-readable validation diagnostics from `validate --write-json`.",
        fields=(
            SchemaField("tool", "string", True, "Tool name."),
            SchemaField("version", "string", True, "Paper Scaffold version."),
            SchemaField("timestamp", "string", True, "UTC timestamp."),
            SchemaField("path", "string", True, "Validated manuscript path."),
            SchemaField("summary", "mapping", True, "Error/warning/info counts."),
            SchemaField("diagnostics", "list[diagnostic]", True, "Structured diagnostic entries."),
        ),
        minimal_example='{"tool": "Paper Scaffold", "version": "0.9.4", "summary": {"errors": 0, "warnings": 0, "info": 1}, "diagnostics": []}',
    ),
    "lock-comparison": SchemaReference(
        name="lock-comparison",
        title="lock_comparison.json",
        status="generated pre-1.0 stable",
        authored_by="generated",
        description="Machine-readable comparison between current manuscript artifacts and an artifact lock.",
        fields=(
            SchemaField("tool", "string", True, "Tool name."),
            SchemaField("created_at", "string", True, "UTC timestamp."),
            SchemaField("manuscript_repo", "string", True, "Manuscript path."),
            SchemaField("lock_path", "string", True, "Compared lock file path."),
            SchemaField("summary", "mapping", True, "Unchanged, changed, missing, and new artifact counts."),
            SchemaField("changed", "list[artifact]", True, "Locked artifacts with changed hashes."),
            SchemaField("missing", "list[artifact]", True, "Locked artifacts missing from current state."),
            SchemaField("new", "list[artifact]", True, "Current artifacts absent from the lock."),
        ),
        minimal_example='{"tool": "Paper Scaffold", "summary": {"unchanged": 1, "changed": 0, "missing": 0, "new": 0}, "changed": [], "missing": [], "new": []}',
    ),
}


def schema_names() -> list[str]:
    return sorted(SCHEMAS)


def get_schema(name: str) -> SchemaReference:
    normalized = name.strip().lower()
    if normalized not in SCHEMAS:
        raise KeyError(normalized)
    return SCHEMAS[normalized]


def schema_to_dict(schema: SchemaReference) -> dict[str, Any]:
    return {
        "name": schema.name,
        "title": schema.title,
        "status": schema.status,
        "authored_by": schema.authored_by,
        "description": schema.description,
        "fields": [
            {
                "name": field.name,
                "type": field.expected_type,
                "required": field.required,
                "description": field.description,
            }
            for field in schema.fields
        ],
        "minimal_example": schema.minimal_example,
    }


def format_schema(schema: SchemaReference) -> str:
    lines = [
        f"# {schema.title}",
        "",
        f"- Schema name: `{schema.name}`",
        f"- Status: {schema.status}",
        f"- Source: {schema.authored_by}",
        "",
        schema.description,
        "",
        "## Fields",
        "",
        "| Field | Type | Required | Description |",
        "| --- | --- | --- | --- |",
    ]
    for field in schema.fields:
        required = "yes" if field.required else "no"
        lines.append(f"| `{field.name}` | `{field.expected_type}` | {required} | {field.description} |")
    lines.extend(["", "## Minimal Example", "", "```text", schema.minimal_example, "```"])
    return "\n".join(lines)


def format_schema_json(schema: SchemaReference) -> str:
    return json.dumps(schema_to_dict(schema), indent=2) + "\n"
