"""Generated provenance ledger helpers for manuscript artifacts."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from . import __version__
from .artifact_manifest import load_artifact_manifest, resolve_source_path
from .checks import FIGURE_EXTENSIONS, TABLE_EXTENSIONS, iter_files, read_text, relative
from .config import ManuscriptConfig
from .git_helpers import current_branch, run_git

ARTIFACT_REFERENCE_TYPES = {"figure", "table", "supplement_figure", "supplement_table"}
ARTIFACT_FILE_EXTENSIONS = FIGURE_EXTENSIONS | TABLE_EXTENSIONS
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
INPUT_RE = re.compile(r"\\(?:input|include|subfile)\{([^}]+)\}")


@dataclass(frozen=True)
class TexReference:
    source_file: Path
    line: int
    raw_path: str
    kind: str
    resolved_path: Path
    exists: bool
    usage_area: str

    def to_dict(self, root: Path) -> dict[str, object]:
        return {
            "source_file": relative(self.source_file, root),
            "line": self.line,
            "raw_path": self.raw_path,
            "kind": self.kind,
            "resolved_path": relative(self.resolved_path, root),
            "exists": self.exists,
            "usage_area": self.usage_area,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_mtime(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


def git_commit(path: Path) -> str:
    if not path.exists() or not path.is_dir():
        return ""
    result = run_git(["rev-parse", "HEAD"], path)
    if result.ok:
        return result.stdout.strip()
    return ""


def _usage_area(root: Path, path: Path) -> str:
    rel = relative(path, root)
    return "supplement" if rel == "supplement/supplement.tex" or rel.startswith("supplement/") else "main"


def _reference_candidates(root: Path, source_file: Path, raw_path: str, kind: str) -> list[Path]:
    raw = Path(raw_path)
    if raw.is_absolute():
        candidates = [raw]
    else:
        candidates = [root / raw, source_file.parent / raw]
    expanded = list(candidates)
    if raw.suffix == "":
        if kind == "figure":
            for candidate in candidates:
                expanded.extend(candidate.with_suffix(suffix) for suffix in sorted(FIGURE_EXTENSIONS))
        else:
            expanded.extend(candidate.with_suffix(".tex") for candidate in candidates)
    return expanded


def _select_reference_path(root: Path, source_file: Path, raw_path: str, kind: str) -> tuple[Path, bool]:
    candidates = _reference_candidates(root, source_file, raw_path, kind)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve(), True
    return candidates[0].resolve(), False


def scan_tex_references(root: Path) -> list[TexReference]:
    refs: list[TexReference] = []
    if not root.exists():
        return refs
    for path in sorted(root.rglob("*.tex"), key=lambda item: item.as_posix().lower()):
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            for match in INCLUDEGRAPHICS_RE.finditer(line):
                raw_path = match.group(1).strip()
                resolved, exists = _select_reference_path(root, path, raw_path, "figure")
                refs.append(TexReference(path, line_number, raw_path, "includegraphics", resolved, exists, _usage_area(root, path)))
            for match in INPUT_RE.finditer(line):
                raw_path = match.group(1).strip()
                resolved, exists = _select_reference_path(root, path, raw_path, "input")
                refs.append(TexReference(path, line_number, raw_path, "input", resolved, exists, _usage_area(root, path)))
    return refs


def _is_artifact_like_reference(ref: TexReference) -> bool:
    raw = ref.raw_path.replace("\\", "/").lower()
    suffix = ref.resolved_path.suffix.lower()
    if ref.kind == "includegraphics":
        return True
    return (
        suffix in ARTIFACT_FILE_EXTENSIONS
        or raw.startswith(("figures/", "tables/", "supplement/figures/", "supplement/tables/"))
        or "/figures/" in raw
        or "/tables/" in raw
    )


def _artifact_files(root: Path) -> list[Path]:
    folders = [root / "figures", root / "tables", root / "supplement" / "figures", root / "supplement" / "tables"]
    found: list[Path] = []
    for folder in folders:
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*"), key=lambda item: item.as_posix().lower()):
            if path.is_file() and path.suffix.lower() in ARTIFACT_FILE_EXTENSIONS:
                found.append(path.resolve())
    return found


def _source_declared(artifact: dict[str, Any]) -> bool:
    return bool(str(artifact.get("source_path") or "").strip() or str(artifact.get("source_repo") or "").strip())


def _artifact_status(source_declared: bool, source_exists: bool, manuscript_exists: bool, source_hash: str | None, manuscript_hash: str | None) -> str:
    if not manuscript_exists:
        return "missing_manuscript"
    if source_declared and not source_exists:
        return "missing_source"
    if source_exists and source_hash and manuscript_hash and source_hash != manuscript_hash:
        return "stale"
    if not source_declared:
        return "unknown"
    return "current"


def _used_in_main_or_supplement(usage_areas: set[str]) -> str:
    if {"main", "supplement"}.issubset(usage_areas):
        return "both"
    if "main" in usage_areas:
        return "main"
    if "supplement" in usage_areas:
        return "supplement"
    return "none"


def _ledger_entry(root: Path, artifact: dict[str, Any], refs_by_path: dict[Path, list[TexReference]]) -> dict[str, object]:
    artifact_id = str(artifact.get("id") or "<missing-id>")
    artifact_type = str(artifact.get("type") or "unknown")
    manuscript_path = str(artifact.get("manuscript_path") or "")
    manuscript = (root / manuscript_path).resolve() if manuscript_path else root.resolve()
    source_declared = _source_declared(artifact)
    source = resolve_source_path(artifact).resolve() if source_declared else Path()
    source_repo = str(artifact.get("source_repo") or "")
    source_repo_path = Path(source_repo) if source_repo else None
    source_exists = bool(source_declared and source.exists())
    manuscript_exists = bool(manuscript_path and manuscript.exists())
    source_hash = file_sha256(source) if source_exists else None
    manuscript_hash = file_sha256(manuscript) if manuscript_exists else None
    references = refs_by_path.get(manuscript, [])
    used_in_tex_files = sorted({relative(ref.source_file, root) for ref in references})
    usage_areas = {ref.usage_area for ref in references}
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "manuscript_path": manuscript_path,
        "source_path": str(artifact.get("source_path") or ""),
        "source_repo": source_repo,
        "source_git_commit": git_commit(source_repo_path) if source_repo_path else "",
        "source_exists": source_exists,
        "manuscript_exists": manuscript_exists,
        "source_sha256": source_hash or "",
        "manuscript_sha256": manuscript_hash or "",
        "source_mtime": file_mtime(source) if source_exists else "",
        "manuscript_mtime": file_mtime(manuscript) if manuscript_exists else "",
        "copied_at": str(artifact.get("copied_at") or ""),
        "generated_by": str(artifact.get("generated_by") or ""),
        "used_in_tex_files": used_in_tex_files,
        "used_in_main_or_supplement": _used_in_main_or_supplement(usage_areas),
        "status": _artifact_status(source_declared, source_exists, manuscript_exists, source_hash, manuscript_hash),
        "notes": str(artifact.get("notes") or artifact.get("caption_hint") or ""),
    }


def build_provenance_ledger(manuscript_repo: str | Path) -> dict[str, object]:
    root = Path(manuscript_repo)
    config = ManuscriptConfig.load(root)
    manifest = load_artifact_manifest(root)
    refs = scan_tex_references(root)
    refs_by_path: dict[Path, list[TexReference]] = defaultdict(list)
    for ref in refs:
        if ref.exists:
            refs_by_path[ref.resolved_path].append(ref)

    artifacts = [_ledger_entry(root, artifact, refs_by_path) for artifact in manifest.get("artifacts", []) if isinstance(artifact, dict)]
    manifest_paths = {
        (root / str(artifact.get("manuscript_path") or "")).resolve()
        for artifact in manifest.get("artifacts", [])
        if isinstance(artifact, dict) and artifact.get("manuscript_path")
    }
    untracked = []
    for path in _artifact_files(root):
        if path not in manifest_paths:
            untracked.append(
                {
                    "artifact_id": f"untracked:{relative(path, root)}",
                    "artifact_type": "untracked",
                    "manuscript_path": relative(path, root),
                    "source_path": "",
                    "source_repo": "",
                    "source_git_commit": "",
                    "source_exists": False,
                    "manuscript_exists": True,
                    "source_sha256": "",
                    "manuscript_sha256": file_sha256(path) or "",
                    "source_mtime": "",
                    "manuscript_mtime": file_mtime(path) or "",
                    "copied_at": "",
                    "generated_by": "",
                    "used_in_tex_files": sorted({relative(ref.source_file, root) for ref in refs_by_path.get(path, [])}),
                    "used_in_main_or_supplement": _used_in_main_or_supplement({ref.usage_area for ref in refs_by_path.get(path, [])}),
                    "status": "untracked",
                    "notes": "present in manuscript artifact folders but not listed in metadata/artifact_manifest.yaml",
                }
            )
    referenced_missing = [
        ref.to_dict(root)
        for ref in refs
        if not ref.exists and _is_artifact_like_reference(ref)
    ]

    all_statuses = Counter(str(entry["status"]) for entry in artifacts + untracked)
    unreferenced = [
        entry
        for entry in artifacts
        if entry["artifact_type"] in ARTIFACT_REFERENCE_TYPES
        and entry["manuscript_exists"]
        and not entry["used_in_tex_files"]
    ]
    branch = current_branch(root)
    commit_result = run_git(["rev-parse", "HEAD"], root)
    git_commit_value = commit_result.stdout.strip() if commit_result.ok else ""
    summary = {
        "total_manifest_artifacts": len(artifacts),
        "current": all_statuses.get("current", 0),
        "stale": all_statuses.get("stale", 0),
        "missing_source": all_statuses.get("missing_source", 0),
        "missing_manuscript_artifact": all_statuses.get("missing_manuscript", 0),
        "untracked_manuscript_artifacts": all_statuses.get("untracked", 0),
        "unreferenced_artifacts": len(unreferenced),
        "referenced_missing_artifacts": len(referenced_missing),
        "unknown": all_statuses.get("unknown", 0),
    }
    return {
        "tool": "Paper Scaffold",
        "version": __version__,
        "generated_at": utc_now(),
        "manuscript_repo": root.as_posix(),
        "git": {
            "branch": branch or "",
            "commit": git_commit_value,
        },
        "config": {
            "main_tex": config.main_tex,
            "supplement_tex": config.supplement_tex,
            "has_supplement": config.has_supplement,
        },
        "summary": summary,
        "artifacts": artifacts,
        "untracked_artifacts": untracked,
        "referenced_missing_artifacts": referenced_missing,
    }


def write_json(path: str | Path, data: dict[str, object]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _entries_by_status(ledger: dict[str, object], status: str) -> list[dict[str, object]]:
    return [entry for entry in ledger.get("artifacts", []) if isinstance(entry, dict) and entry.get("status") == status]


def _unreferenced_entries(ledger: dict[str, object]) -> list[dict[str, object]]:
    entries = []
    for entry in ledger.get("artifacts", []):
        if not isinstance(entry, dict):
            continue
        if entry.get("artifact_type") not in ARTIFACT_REFERENCE_TYPES:
            continue
        if entry.get("manuscript_exists") and not entry.get("used_in_tex_files"):
            entries.append(entry)
    return entries


def _format_artifact_list(entries: list[dict[str, object]], empty: str) -> list[str]:
    if not entries:
        return [f"- {empty}"]
    lines = []
    for entry in entries:
        usage = ", ".join(str(item) for item in entry.get("used_in_tex_files", []) or [])
        suffix = f"; used in {usage}" if usage else ""
        lines.append(f"- `{entry.get('artifact_id')}` -> `{entry.get('manuscript_path')}` ({entry.get('status')}){suffix}")
    return lines


def provenance_markdown_report(ledger: dict[str, object]) -> str:
    summary = ledger.get("summary", {}) if isinstance(ledger.get("summary"), dict) else {}
    git = ledger.get("git", {}) if isinstance(ledger.get("git"), dict) else {}
    artifacts = [entry for entry in ledger.get("artifacts", []) if isinstance(entry, dict)]
    untracked = [entry for entry in ledger.get("untracked_artifacts", []) if isinstance(entry, dict)]
    missing_refs = [entry for entry in ledger.get("referenced_missing_artifacts", []) if isinstance(entry, dict)]
    lines = [
        "# Paper Scaffold Provenance Report",
        "",
        f"- Generated: {ledger.get('generated_at')}",
        f"- Manuscript repo path: {ledger.get('manuscript_repo')}",
        f"- Git branch: {git.get('branch') or '<not detected>'}",
        f"- Git commit: {git.get('commit') or '<not detected>'}",
        "- Summary counts:",
        f"  - Total manifest artifacts: {summary.get('total_manifest_artifacts', 0)}",
        f"  - Current: {summary.get('current', 0)}",
        f"  - Stale: {summary.get('stale', 0)}",
        f"  - Missing source: {summary.get('missing_source', 0)}",
        f"  - Missing manuscript artifact: {summary.get('missing_manuscript_artifact', 0)}",
        f"  - Untracked manuscript artifacts: {summary.get('untracked_manuscript_artifacts', 0)}",
        f"  - Unreferenced artifacts: {summary.get('unreferenced_artifacts', 0)}",
        f"  - Referenced missing artifacts: {summary.get('referenced_missing_artifacts', 0)}",
        "",
        "## 1. Current Artifacts",
        *_format_artifact_list(_entries_by_status(ledger, "current"), "None."),
        "",
        "## 2. Stale Artifacts",
        *_format_artifact_list(_entries_by_status(ledger, "stale"), "None."),
        "",
        "## 3. Missing Sources",
        *_format_artifact_list(_entries_by_status(ledger, "missing_source"), "None."),
        "",
        "## 4. Missing Manuscript Files",
        *_format_artifact_list(_entries_by_status(ledger, "missing_manuscript"), "None."),
        "",
        "## 5. Untracked Artifacts",
        *_format_artifact_list(untracked, "None."),
        "",
        "## 6. Referenced Files Not Found",
    ]
    if missing_refs:
        for ref in missing_refs:
            lines.append(f"- `{ref.get('raw_path')}` from `{ref.get('source_file')}` line {ref.get('line')} resolves to `{ref.get('resolved_path')}`")
    else:
        lines.append("- None.")
    lines.extend(["", "## 7. Artifact Usage Map"])
    if artifacts:
        for entry in artifacts:
            usage = entry.get("used_in_tex_files") or []
            usage_text = ", ".join(str(item) for item in usage) if usage else "not referenced"
            lines.append(f"- `{entry.get('artifact_id')}`: {usage_text}; area: {entry.get('used_in_main_or_supplement')}")
    else:
        lines.append("- No manifest artifacts.")
    lines.extend(["", "## 8. Recommended Next Actions"])
    if summary.get("missing_manuscript_artifact", 0) or summary.get("referenced_missing_artifacts", 0):
        lines.append("- Restore missing manuscript artifacts or fix TeX references before submission.")
    if summary.get("missing_source", 0):
        lines.append("- Review missing sources; the manuscript copy may be usable, but provenance is incomplete.")
    if summary.get("stale", 0):
        lines.append("- Review stale artifacts and rerun the generating workflow or copy step if the updated source should appear in the manuscript.")
    if summary.get("untracked_manuscript_artifacts", 0):
        lines.append("- Add intentional untracked artifacts to `metadata/artifact_manifest.yaml` or remove stale files.")
    if summary.get("unreferenced_artifacts", 0):
        lines.append("- Reference intentional artifacts from TeX or remove them from the manuscript repo.")
    if not lines[-1].startswith("-"):
        lines.append("- No provenance issues found. Freeze artifact hashes before a submission or revision handoff.")
    return "\n".join(lines) + "\n"


def artifact_status_text(ledger: dict[str, object]) -> str:
    summary = ledger.get("summary", {}) if isinstance(ledger.get("summary"), dict) else {}
    lines = [
        "Artifact status",
        f"- total manifest artifacts: {summary.get('total_manifest_artifacts', 0)}",
        f"- current: {summary.get('current', 0)}",
        f"- stale: {summary.get('stale', 0)}",
        f"- missing source: {summary.get('missing_source', 0)}",
        f"- missing manuscript artifact: {summary.get('missing_manuscript_artifact', 0)}",
        f"- untracked manuscript artifacts: {summary.get('untracked_manuscript_artifacts', 0)}",
        f"- unreferenced artifacts: {summary.get('unreferenced_artifacts', 0)}",
        f"- referenced missing artifacts: {summary.get('referenced_missing_artifacts', 0)}",
    ]
    return "\n".join(lines)


def build_artifact_lock(ledger: dict[str, object]) -> dict[str, object]:
    locked = []
    for entry in ledger.get("artifacts", []):
        if not isinstance(entry, dict):
            continue
        if not entry.get("manuscript_exists") or not entry.get("manuscript_sha256"):
            continue
        locked.append(
            {
                "artifact_id": entry.get("artifact_id"),
                "artifact_type": entry.get("artifact_type"),
                "manuscript_path": entry.get("manuscript_path"),
                "manuscript_sha256": entry.get("manuscript_sha256"),
                "manuscript_mtime": entry.get("manuscript_mtime"),
                "status": entry.get("status"),
            }
        )
    return {
        "tool": "Paper Scaffold",
        "version": __version__,
        "generated_at": utc_now(),
        "manuscript_repo": ledger.get("manuscript_repo"),
        "artifacts": locked,
    }
