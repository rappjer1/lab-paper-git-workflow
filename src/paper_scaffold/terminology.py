"""Terminology map loading and banned-term scanning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Iterable

from .config import load_yaml

TEXT_EXTENSIONS = {".tex", ".bib", ".md"}


@dataclass(frozen=True)
class TerminologyHit:
    path: Path
    line_number: int
    term: str
    publication_label: str
    line: str


def terminology_path(manuscript_repo_or_path: str | Path) -> Path:
    path = Path(manuscript_repo_or_path)
    if path.is_dir():
        return path / "metadata" / "terminology_map.yaml"
    return path


def load_terminology_map(manuscript_repo_or_path: str | Path) -> dict[str, Any]:
    path = terminology_path(manuscript_repo_or_path)
    data = load_yaml(path)
    if not isinstance(data, dict):
        return {"terms": {}}
    data.setdefault("terms", {})
    return data


def iter_text_files(root: str | Path) -> Iterable[Path]:
    root = Path(root)
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def banned_terms(terminology_map: dict[str, Any]) -> dict[str, dict[str, Any]]:
    terms = terminology_map.get("terms", {}) if isinstance(terminology_map, dict) else {}
    banned: dict[str, dict[str, Any]] = {}
    if not isinstance(terms, dict):
        return banned
    for term, details in terms.items():
        if not isinstance(details, dict):
            details = {"publication_label": str(details)}
        if details.get("banned_in"):
            banned[str(term)] = details
    return banned


def find_banned_terms(root: str | Path, terminology_map: dict[str, Any] | None = None) -> list[TerminologyHit]:
    root = Path(root)
    term_map = terminology_map or load_terminology_map(root)
    banned = banned_terms(term_map)
    hits: list[TerminologyHit] = []
    if not banned:
        return hits
    for path in iter_text_files(root):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, start=1):
            for term, details in banned.items():
                if re.search(re.escape(term), line):
                    hits.append(
                        TerminologyHit(
                            path=path,
                            line_number=line_number,
                            term=term,
                            publication_label=str(details.get("publication_label") or ""),
                            line=line.strip(),
                        )
                    )
    return hits


def format_terminology_hits(hits: list[TerminologyHit], root: str | Path) -> str:
    root = Path(root)
    if not hits:
        return "No banned terminology found."
    lines = ["Banned terminology found:"]
    for hit in hits:
        try:
            rel = hit.path.relative_to(root)
        except ValueError:
            rel = hit.path
        suggestion = f" -> use '{hit.publication_label}'" if hit.publication_label else ""
        lines.append(f"- {rel}:{hit.line_number}: {hit.term}{suggestion}")
        lines.append(f"  {hit.line}")
    return "\n".join(lines)
