"""Artifact manifest parsing and copying."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import shutil

from .config import load_yaml, write_yaml
from .schemas import ARTIFACT_TYPES, validate_artifact_manifest_schema

SUPPORTED_ARTIFACT_TYPES = ARTIFACT_TYPES


@dataclass(frozen=True)
class ArtifactCopyResult:
    artifact_id: str
    source: Path
    destination: Path
    status: str
    message: str


def manifest_path(manuscript_repo_or_path: str | Path) -> Path:
    path = Path(manuscript_repo_or_path)
    if path.is_dir():
        return path / "metadata" / "artifact_manifest.yaml"
    return path


def load_artifact_manifest(manuscript_repo_or_path: str | Path) -> dict[str, Any]:
    path = manifest_path(manuscript_repo_or_path)
    data = load_yaml(path)
    if not isinstance(data, dict):
        return {"artifacts": []}
    artifacts = data.get("artifacts")
    if artifacts is None:
        data["artifacts"] = []
    elif not isinstance(artifacts, list):
        raise ValueError(f"artifacts must be a list in {path}")
    return data


def validate_artifacts(manifest: dict[str, Any]) -> list[str]:
    return [finding.detail for finding in validate_artifact_manifest_schema(manifest) if finding.message.severity == "ERROR"]


def resolve_source_path(artifact: dict[str, Any]) -> Path:
    source_path = Path(str(artifact.get("source_path") or ""))
    if source_path.is_absolute():
        return source_path
    source_repo = str(artifact.get("source_repo") or "").strip()
    if source_repo:
        return Path(source_repo) / source_path
    return source_path


def append_artifact(manuscript_repo: str | Path, artifact: dict[str, Any]) -> None:
    path = manifest_path(manuscript_repo)
    manifest = load_artifact_manifest(path)
    manifest.setdefault("artifacts", [])
    manifest["artifacts"].append(artifact)
    errors = validate_artifacts(manifest)
    if errors:
        raise ValueError("Invalid artifact manifest after append:\n" + "\n".join(errors))
    write_yaml(path, manifest)


def copy_artifacts(
    manuscript_repo: str | Path,
    allow_directories: bool = False,
    max_file_size_mb: float = 25,
) -> list[ArtifactCopyResult]:
    repo = Path(manuscript_repo)
    manifest = load_artifact_manifest(repo)
    results: list[ArtifactCopyResult] = []
    max_bytes = int(max_file_size_mb * 1024 * 1024)
    for artifact in manifest.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        artifact_id = str(artifact.get("id") or "<missing-id>")
        source = resolve_source_path(artifact)
        destination = repo / str(artifact.get("manuscript_path") or "")
        if not source.exists():
            results.append(ArtifactCopyResult(artifact_id, source, destination, "missing", "source file is missing"))
            continue
        if source.is_dir() and not allow_directories:
            results.append(ArtifactCopyResult(artifact_id, source, destination, "skipped", "source is a directory"))
            continue
        if source.is_file() and source.stat().st_size > max_bytes:
            results.append(
                ArtifactCopyResult(artifact_id, source, destination, "warning", "source file exceeds size threshold")
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)
        results.append(ArtifactCopyResult(artifact_id, source, destination, "copied", "copied"))
    return results
