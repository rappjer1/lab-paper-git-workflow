"""Validation checks for clean manuscript repositories."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import fnmatch
from typing import Iterable

from .artifact_manifest import load_artifact_manifest, validate_artifacts
from .config import ManuscriptConfig
from .git_helpers import git_summary
from .messages import DiagnosticFinding, format_finding, severity_counts
from .terminology import find_banned_terms


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_info(self, message: str) -> None:
        self.info.append(message)

    def format(self) -> str:
        lines = ["Validation passed." if self.ok else "Validation failed."]
        if self.errors:
            lines.append("\nErrors:")
            lines.extend(f"- {message}" for message in self.errors)
        if self.warnings:
            lines.append("\nWarnings:")
            lines.extend(f"- {message}" for message in self.warnings)
        if self.info:
            lines.append("\nInfo:")
            lines.extend(f"- {message}" for message in self.info)
        return "\n".join(lines)


def _iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
            continue
        yield path


def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def forbidden_file_matches(root: str | Path, patterns: list[str]) -> list[Path]:
    root = Path(root)
    matches: list[Path] = []
    for path in _iter_files(root):
        rel = _relative_posix(path, root)
        for pattern in patterns:
            normalized = pattern.replace("\\", "/")
            if "*" in normalized or "?" in normalized:
                if fnmatch.fnmatch(path.name, normalized) or fnmatch.fnmatch(rel, normalized):
                    matches.append(path)
                    break
            elif normalized in rel or any(part == normalized for part in rel.split("/")):
                matches.append(path)
                break
    return matches


def large_files(root: str | Path, max_file_size_mb: float) -> list[tuple[Path, float]]:
    root = Path(root)
    threshold = max_file_size_mb * 1024 * 1024
    found: list[tuple[Path, float]] = []
    for path in _iter_files(root):
        size = path.stat().st_size
        if size > threshold:
            found.append((path, size / 1024 / 1024))
    return found


def _artifact_destinations_exist(root: Path, report: ValidationReport) -> None:
    try:
        manifest = load_artifact_manifest(root)
    except ValueError as exc:
        report.add_error(str(exc))
        return
    for error in validate_artifacts(manifest):
        report.add_error(error)
    for artifact in manifest.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        manuscript_path = artifact.get("manuscript_path")
        if not manuscript_path:
            continue
        destination = root / str(manuscript_path)
        if not destination.exists():
            report.add_error(f"listed artifact is missing from manuscript repo: {manuscript_path}")


def validation_markdown_report(manuscript_repo: str | Path) -> str:
    root = Path(manuscript_repo)
    from .checks import check_manuscript

    findings = check_manuscript(root)
    counts = severity_counts(findings)

    lines = [
        "# Paper Scaffold Validation Report",
        "",
        f"- Timestamp: {datetime.now(timezone.utc).isoformat()}",
        f"- Repository path: {root.as_posix()}",
        f"- Summary: {counts.get('ERROR', 0)} errors, {counts.get('WARNING', 0)} warnings, {counts.get('INFO', 0)} info",
    ]
    summary = git_summary(root) if (root / ".git").exists() else {"branch": None, "remotes": {}, "status": []}
    remotes = summary.get("remotes") or {}
    origin = ", ".join(remotes.get("origin", [])) if isinstance(remotes, dict) else ""
    lines.extend(
        [
            "",
            "## Git Status Summary",
            f"- Branch: {summary.get('branch') or '<not a git repo>'}",
            f"- Origin: {origin or '<not configured>'}",
            f"- Status entries: {len(summary.get('status') or [])}",
        ]
    )
    for severity in ["ERROR", "WARNING", "INFO"]:
        group = [finding for finding in findings if finding.message.severity == severity]
        lines.extend(["", f"## {severity.title()}s"])
        if group:
            lines.extend(f"- {format_finding(finding)}" for finding in group)
        else:
            lines.append("- None.")
    lines.extend(["", "## Next Actions"])
    if counts.get("ERROR", 0):
        lines.append("- Fix errors before syncing to Overleaf or publishing the manuscript repository.")
    else:
        lines.append("- Review warnings, commit intentionally, and sync through GitHub when ready.")
    if counts.get("WARNING", 0):
        lines.append("- Review warnings and decide whether they are acceptable for your project.")
    lines.append("- Run focused checks such as `check-figures`, `check-citations`, and `check-labels` when editing those areas.")
    return "\n".join(lines) + "\n"


def validate_manuscript_repo(manuscript_repo: str | Path) -> ValidationReport:
    root = Path(manuscript_repo)
    report = ValidationReport()
    from .checks import check_manuscript

    findings = check_manuscript(root)
    counts = severity_counts(findings)
    report.add_info(f"summary: {counts.get('ERROR', 0)} errors, {counts.get('WARNING', 0)} warnings, {counts.get('INFO', 0)} info")
    for finding in findings:
        formatted = format_finding(finding)
        if finding.message.severity == "ERROR":
            report.add_error(formatted)
        elif finding.message.severity == "WARNING":
            report.add_warning(formatted)
        else:
            report.add_info(formatted)
    return report
