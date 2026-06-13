"""Discover likely manuscript artifacts from Python output folders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shutil
from typing import Iterable

from .artifact_manifest import load_artifact_manifest
from .config import dumps_yaml, write_yaml

DISCOVER_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".csv", ".tex", ".bib"}
IGNORED_EXTENSIONS = {".npz", ".pt", ".pth", ".pkl", ".pickle", ".nc", ".zarr", ".zip", ".parquet"}
IGNORED_PATH_PARTS = {"raw_api_cache", "prediction_cache", "full_eval"}
IGNORED_PATH_FRAGMENTS = {"data/external"}


@dataclass(frozen=True)
class ArtifactCandidate:
    source_path: Path
    artifact_id: str
    artifact_type: str
    manuscript_path: str


def snake_case(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return normalized or "artifact"


def should_ignore_path(path: Path) -> bool:
    lowered_parts = {part.lower() for part in path.parts}
    if lowered_parts & IGNORED_PATH_PARTS:
        return True
    as_posix = path.as_posix().lower()
    if any(fragment in as_posix for fragment in IGNORED_PATH_FRAGMENTS):
        return True
    return path.suffix.lower() in IGNORED_EXTENSIONS


def classify_artifact(path: Path, supplement: bool = False) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix in {".pdf", ".png", ".jpg", ".jpeg"}:
        artifact_type = "supplement_figure" if supplement else "figure"
        destination_root = "supplement/figures" if supplement else "figures"
    elif suffix == ".tex":
        artifact_type = "supplement_table" if supplement else "table"
        destination_root = "supplement/tables" if supplement else "tables"
    elif suffix == ".csv":
        artifact_type = "data_summary"
        destination_root = "tables"
    else:
        artifact_type = "data_summary"
        destination_root = "metadata"
    return artifact_type, destination_root


def discover_artifacts(source: str | Path, supplement: bool = False) -> list[ArtifactCandidate]:
    source = Path(source)
    candidates: list[ArtifactCandidate] = []
    seen_ids: dict[str, int] = {}
    if not source.exists():
        return candidates
    for path in source.rglob("*"):
        if path.is_dir() or should_ignore_path(path):
            continue
        if path.suffix.lower() not in DISCOVER_EXTENSIONS:
            continue
        base_id = snake_case(path.stem)
        count = seen_ids.get(base_id, 0) + 1
        seen_ids[base_id] = count
        artifact_id = base_id if count == 1 else f"{base_id}_{count}"
        artifact_type, destination_root = classify_artifact(path, supplement=supplement)
        candidates.append(
            ArtifactCandidate(
                source_path=path,
                artifact_id=artifact_id,
                artifact_type=artifact_type,
                manuscript_path=f"{destination_root}/{path.name}",
            )
        )
    return sorted(candidates, key=lambda candidate: str(candidate.source_path).lower())


def append_candidates_to_manifest(manifest_path: str | Path, candidates: Iterable[ArtifactCandidate]) -> None:
    manifest_path = Path(manifest_path)
    manifest = load_artifact_manifest(manifest_path)
    artifacts = manifest.setdefault("artifacts", [])
    existing_ids = {str(item.get("id")) for item in artifacts if isinstance(item, dict)}
    for candidate in candidates:
        artifact_id = candidate.artifact_id
        counter = 2
        while artifact_id in existing_ids:
            artifact_id = f"{candidate.artifact_id}_{counter}"
            counter += 1
        existing_ids.add(artifact_id)
        artifacts.append(
            {
                "id": artifact_id,
                "type": candidate.artifact_type,
                "manuscript_path": candidate.manuscript_path,
                "source_repo": "",
                "source_path": candidate.source_path.as_posix(),
                "generated_by": "",
                "input_data": "",
                "last_updated": "",
                "caption_hint": "",
                "status": "candidate",
            }
        )
    write_yaml(manifest_path, manifest)


def candidate_manifest_entries(candidates: Iterable[ArtifactCandidate]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for candidate in candidates:
        entries.append(
            {
                "id": candidate.artifact_id,
                "type": candidate.artifact_type,
                "manuscript_path": candidate.manuscript_path,
                "source_repo": "",
                "source_path": candidate.source_path.as_posix(),
                "generated_by": "",
                "input_data": "",
                "last_updated": "",
                "caption_hint": "",
                "status": "candidate",
            }
        )
    return entries


def copy_candidates(manuscript_repo: str | Path, candidates: Iterable[ArtifactCandidate]) -> list[tuple[ArtifactCandidate, Path]]:
    manuscript_repo = Path(manuscript_repo)
    copied: list[tuple[ArtifactCandidate, Path]] = []
    for candidate in candidates:
        destination = manuscript_repo / candidate.manuscript_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(candidate.source_path, destination)
        copied.append((candidate, destination))
    return copied


def format_candidates(candidates: list[ArtifactCandidate]) -> str:
    if not candidates:
        return "No candidate manuscript artifacts found. Raw data/model/cache outputs are skipped."
    lines = ["Candidate manuscript artifacts:", "Raw data/model/cache outputs are skipped."]
    for candidate in candidates:
        lines.append(f"- {candidate.artifact_id} [{candidate.artifact_type}]")
        lines.append(f"  source: {candidate.source_path.as_posix()}")
        lines.append(f"  suggested destination: {candidate.manuscript_path}")
    lines.append("")
    lines.append("Manifest entry preview:")
    lines.append(dumps_yaml({"artifacts": candidate_manifest_entries(candidates)}))
    return "\n".join(lines)
