"""Read-only audit helpers for messy project folders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .checks import check_privacy, format_findings, iter_files, read_text, relative
from .messages import DiagnosticFinding, severity_counts

MANUSCRIPT_EXTENSIONS = {".tex", ".docx", ".md", ".bib"}
FIGURE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".svg"}
TABLE_EXTENSIONS = {".csv", ".xlsx", ".tex"}
RAW_OUTPUT_EXTENSIONS = {".npz", ".pt", ".pth", ".pkl", ".pickle", ".nc", ".parquet", ".h5", ".hdf5", ".tif", ".tiff", ".zip"}
LATEX_BUILD_SUFFIXES = (".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".run.xml", ".synctex.gz", ".toc")
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache"}
SUSPICIOUS_FINAL_RE = re.compile(r"(?i)(?:final[_-]?final|final[_-]?v?\d+|final2|v\d+[_-]?final)")
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")


@dataclass(frozen=True)
class ProjectAuditResult:
    root: Path
    total_files: int
    overleaf_export_dirs: list[str]
    findings: list[DiagnosticFinding]


def _is_latex_build_file(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(suffix) for suffix in LATEX_BUILD_SUFFIXES)


def _looks_like_table(path: Path) -> bool:
    suffix = path.suffix.lower()
    parts = {part.lower() for part in path.parts}
    return suffix in {".csv", ".xlsx"} or (suffix == ".tex" and ("table" in path.stem.lower() or "tables" in parts))


def _looks_like_overleaf_export(directory: Path) -> bool:
    if any(part in SKIP_DIRS for part in directory.parts):
        return False
    name_hit = "overleaf" in directory.name.lower() or "export" in directory.name.lower()
    source_hit = (directory / "main.tex").exists()
    build_hit = any(child.is_file() and _is_latex_build_file(child) for child in directory.iterdir()) if directory.exists() else False
    return source_hit and (build_hit or name_hit)


def _referenced_graphics(path: Path) -> set[str]:
    if path.suffix.lower() != ".tex":
        return set()
    try:
        text = read_text(path)
    except OSError:
        return set()
    return {match.group(1).strip() for match in INCLUDEGRAPHICS_RE.finditer(text)}


def audit_project(path: str | Path, *, large_file_mb: float = 25.0) -> ProjectAuditResult:
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(root)

    files = sorted(iter_files(root), key=lambda item: item.as_posix().lower())
    findings: list[DiagnosticFinding] = []
    overleaf_dirs = [
        relative(directory, root)
        for directory in sorted((candidate for candidate in root.rglob("*") if candidate.is_dir()), key=lambda item: item.as_posix().lower())
        if _looks_like_overleaf_export(directory)
    ]
    for directory in overleaf_dirs:
        findings.append(DiagnosticFinding("I020", "candidate Overleaf export folder", directory))

    threshold = large_file_mb * 1024 * 1024
    graphics_references: set[str] = set()
    for file_path in files:
        graphics_references.update(_referenced_graphics(file_path))

    for file_path in files:
        rel = relative(file_path, root)
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()

        if suffix in MANUSCRIPT_EXTENSIONS:
            findings.append(DiagnosticFinding("I020", "likely manuscript/source file", rel))
        if suffix in FIGURE_EXTENSIONS:
            detail = "figure candidate"
            if file_path.name in graphics_references or rel in graphics_references:
                detail = "figure candidate referenced by TeX"
            findings.append(DiagnosticFinding("I021", detail, rel))
        if _looks_like_table(file_path):
            findings.append(DiagnosticFinding("I021", "table candidate", rel))
        if suffix in RAW_OUTPUT_EXTENSIONS:
            findings.append(DiagnosticFinding("W024", "raw/generated output candidate; keep out of manuscript repos unless intentionally archived", rel))
        if _is_latex_build_file(file_path):
            findings.append(DiagnosticFinding("W023", "LaTeX build artifact should be regenerated, not committed", rel))
        if SUSPICIOUS_FINAL_RE.search(name):
            findings.append(DiagnosticFinding("W022", "filename looks like repeated final/export versioning", rel))
        if file_path.stat().st_size > threshold:
            size_mb = file_path.stat().st_size / 1024 / 1024
            findings.append(DiagnosticFinding("E013", f"{size_mb:.1f} MB", rel))

    findings.extend(check_privacy(root))
    return ProjectAuditResult(root=root, total_files=len(files), overleaf_export_dirs=overleaf_dirs, findings=findings)


def format_project_audit(result: ProjectAuditResult) -> str:
    counts = severity_counts(result.findings)
    lines = [
        "# Paper Scaffold Project Audit",
        "",
        f"- Path: {result.root.as_posix()}",
        f"- Files scanned: {result.total_files}",
        f"- Summary: {counts.get('ERROR', 0)} errors, {counts.get('WARNING', 0)} warnings, {counts.get('INFO', 0)} info",
        "",
        "## Candidate Overleaf Exports",
    ]
    if result.overleaf_export_dirs:
        lines.extend(f"- {directory}" for directory in result.overleaf_export_dirs)
    else:
        lines.append("- None detected.")
    lines.extend(["", "## Diagnostics"])
    if result.findings:
        lines.append("```text")
        lines.append(format_findings(result.findings))
        lines.append("```")
    else:
        lines.append("No likely manuscript files, artifacts, raw outputs, build artifacts, large files, or privacy concerns detected.")
    lines.extend(
        [
            "",
            "## Notes",
            "- This audit is read-only. It does not move, delete, copy, or rename files.",
            "- Use findings as a triage list before creating a clean manuscript repository.",
            "- Keep raw/generated outputs in the research project or archive, not in the manuscript repo.",
        ]
    )
    return "\n".join(lines) + "\n"
