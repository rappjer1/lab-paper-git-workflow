"""Validation checks for clean manuscript repositories."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import fnmatch
from typing import Iterable

from .artifact_manifest import load_artifact_manifest, validate_artifacts
from .config import ManuscriptConfig
from .git_helpers import git_summary
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


def validate_manuscript_repo(manuscript_repo: str | Path) -> ValidationReport:
    root = Path(manuscript_repo)
    report = ValidationReport()
    config = ManuscriptConfig.load(root)

    if not root.exists():
        report.add_error(f"manuscript repo does not exist: {root}")
        return report
    if not (root / config.main_tex).exists():
        report.add_error(f"missing main TeX file: {config.main_tex}")
    if not (root / "references.bib").exists():
        report.add_error("missing references.bib")
    if not (root / "figures").exists():
        report.add_error("missing figures/ directory")
    if config.has_supplement and not (root / config.supplement_tex).exists():
        report.add_error(f"missing supplement TeX file: {config.supplement_tex}")

    forbidden = forbidden_file_matches(root, config.forbidden_patterns)
    for path in forbidden:
        report.add_error(f"forbidden file or path in manuscript repo: {_relative_posix(path, root)}")

    _artifact_destinations_exist(root, report)

    for hit in find_banned_terms(root):
        report.add_error(
            f"banned term '{hit.term}' in {_relative_posix(hit.path, root)}:{hit.line_number}; "
            f"use '{hit.publication_label}'"
        )

    for path, size_mb in large_files(root, config.max_file_size_mb):
        report.add_warning(f"large file over {config.max_file_size_mb:g} MB: {_relative_posix(path, root)} ({size_mb:.1f} MB)")

    summary = git_summary(root)
    report.add_info(f"current branch: {summary.get('branch') or '<not a git repo>'}")
    remotes = summary.get("remotes") or {}
    if isinstance(remotes, dict) and remotes.get("origin"):
        report.add_info("remote origin: " + ", ".join(str(item) for item in remotes["origin"]))
    else:
        report.add_warning("remote origin is not configured")
    status = summary.get("status") or []
    if status:
        report.add_info(f"git status entries: {len(status)}")
    else:
        report.add_info("git status entries: 0")
    staged_build = summary.get("staged_latex_build_files") or []
    for path in staged_build:
        report.add_warning(f"LaTeX build artifact appears staged: {path}")

    return report
