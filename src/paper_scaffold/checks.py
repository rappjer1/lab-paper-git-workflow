"""Heuristic manuscript checks used by diagnostics commands."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import Iterable

from .artifact_manifest import load_artifact_manifest, validate_artifacts
from .config import ManuscriptConfig
from .git_helpers import git_summary, run_git, staged_latex_build_files, status_porcelain
from .messages import DiagnosticFinding
from .terminology import find_banned_terms
from .validation import forbidden_file_matches, large_files

TEXT_EXTENSIONS = {".tex", ".bib", ".md", ".yaml", ".yml", ".txt"}
FIGURE_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
LATEX_BUILD_EXTENSIONS = {".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".run.xml", ".synctex.gz", ".toc"}

LOCAL_PATH_RE = re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|/[Uu]sers/|/home/|\\\\[^\\/\s]+\\[^\\/\s]+)")
LOCAL_PATH_VALUE_RE = re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/][^\s{}<>\"']+|/[Uu]sers/[^\s{}<>\"']+|/home/[^\s{}<>\"']+|\\\\[^\\/\s]+\\[^\\/\s{}<>\"']+)")
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
SECRET_RE = re.compile(r"(?i)(api[_-]?key|secret|token|password|credential)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{8,})")
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|autoref|cref|Cref|eqref)\{([^}]+)\}")
CITE_RE = re.compile(r"\\(?:cite|citep|citet|citealp|parencite|textcite)(?:\[[^\]]*\]){0,2}\{([^}]+)\}")
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)")


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in {".git", ".venv", "__pycache__", ".pytest_cache"} for part in path.parts):
            continue
        yield path


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in iter_files(root):
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def redacted_preview(line: str) -> str:
    line = SECRET_RE.sub(lambda match: f"{match.group(1)}=<redacted>", line)
    line = EMAIL_RE.sub("<email>", line)
    line = LOCAL_PATH_VALUE_RE.sub("<local-path>", line)
    return line.strip()[:160]


def extract_graphics(root: Path) -> list[tuple[Path, int, str]]:
    refs: list[tuple[Path, int, str]] = []
    for path in root.rglob("*.tex") if root.exists() else []:
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            for match in INCLUDEGRAPHICS_RE.finditer(line):
                refs.append((path, line_number, match.group(1).strip()))
    return refs


def resolve_graphic_path(root: Path, source_file: Path, graphic_path: str) -> Path:
    raw = Path(graphic_path)
    candidates = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.extend([root / raw, source_file.parent / raw])
    if raw.suffix == "":
        expanded = []
        for candidate in candidates:
            for suffix in FIGURE_EXTENSIONS:
                expanded.append(candidate.with_suffix(suffix))
        candidates.extend(expanded)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def check_manifest(root: Path) -> list[DiagnosticFinding]:
    manifest_path = root / "metadata" / "artifact_manifest.yaml"
    if not manifest_path.exists():
        return [DiagnosticFinding("W010", "metadata/artifact_manifest.yaml is missing", relative(manifest_path, root))]
    findings: list[DiagnosticFinding] = []
    try:
        manifest = load_artifact_manifest(root)
    except ValueError as exc:
        return [DiagnosticFinding("E004", str(exc), relative(manifest_path, root))]
    for error in validate_artifacts(manifest):
        findings.append(DiagnosticFinding("E004", error, relative(manifest_path, root)))
    missing = False
    for artifact in manifest.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        manuscript_path = str(artifact.get("manuscript_path") or "")
        if manuscript_path and not (root / manuscript_path).exists():
            missing = True
            findings.append(DiagnosticFinding("E004", f"missing artifact: {manuscript_path}", manuscript_path))
    if not findings and not missing:
        findings.append(DiagnosticFinding("I005", "metadata/artifact_manifest.yaml parsed successfully", relative(manifest_path, root)))
    return findings


def check_privacy(path: Path) -> list[DiagnosticFinding]:
    root = path
    findings: list[DiagnosticFinding] = []
    files = list(iter_text_files(root)) if root.is_dir() else [root]
    for file_path in files:
        if file_path.name.lower() in {".env", "credentials", "credentials.txt"}:
            findings.append(DiagnosticFinding("W017", "credential-like file name", relative(file_path, root if root.is_dir() else file_path.parent)))
        for line_number, line in enumerate(read_text(file_path).splitlines(), start=1):
            if LOCAL_PATH_RE.search(line) or EMAIL_RE.search(line) or SECRET_RE.search(line) or "private_repo" in line.lower():
                findings.append(
                    DiagnosticFinding(
                        "W017",
                        redacted_preview(line),
                        relative(file_path, root if root.is_dir() else file_path.parent),
                        line_number,
                    )
                )
    return findings


def check_figures(root: Path) -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    referenced_paths: set[Path] = set()
    for source_file, line_number, graphic in extract_graphics(root):
        if LOCAL_PATH_RE.search(graphic) or Path(graphic).is_absolute():
            findings.append(DiagnosticFinding("E008", redacted_preview(graphic), relative(source_file, root), line_number))
            continue
        resolved = resolve_graphic_path(root, source_file, graphic)
        if not resolved.exists():
            findings.append(DiagnosticFinding("E003", graphic, relative(source_file, root), line_number))
        else:
            referenced_paths.add(resolved.resolve())

    figure_files = [path for path in iter_files(root) if path.suffix.lower() in FIGURE_EXTENSIONS and "figures" in {part.lower() for part in path.parts}]
    for path in figure_files:
        if " " in path.name:
            findings.append(DiagnosticFinding("W006", "filename contains spaces", relative(path, root)))
        if path.resolve() not in referenced_paths:
            findings.append(DiagnosticFinding("W005", "figure is present but not referenced by includegraphics", relative(path, root)))
        if path.suffix.lower() in {".png", ".jpg", ".jpeg"} and not path.with_suffix(".pdf").exists():
            findings.append(DiagnosticFinding("W006", "raster figure has no PDF alternative", relative(path, root)))
    try:
        from PIL import Image  # type: ignore
    except Exception:
        if any(path.suffix.lower() in {".png", ".jpg", ".jpeg"} for path in figure_files):
            findings.append(DiagnosticFinding("I002", "Pillow missing; raster dimension checks skipped"))
    else:
        for path in figure_files:
            if path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
                with Image.open(path) as image:
                    width, height = image.size
                if width < 900 or height < 600:
                    findings.append(DiagnosticFinding("W006", f"low raster dimensions: {width}x{height}", relative(path, root)))
    return findings


def extract_citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for match in CITE_RE.finditer(text):
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


def check_citations(root: Path) -> list[DiagnosticFinding]:
    tex_keys: set[str] = set()
    for path in root.rglob("*.tex") if root.exists() else []:
        tex_keys.update(extract_citation_keys(read_text(path)))
    bib_path = root / "references.bib"
    bib_keys: set[str] = set()
    if bib_path.exists():
        bib_keys = set(BIB_KEY_RE.findall(read_text(bib_path)))
    findings: list[DiagnosticFinding] = []
    for key in sorted(tex_keys - bib_keys):
        findings.append(DiagnosticFinding("E012", key, "references.bib"))
    for key in sorted(bib_keys - tex_keys):
        findings.append(DiagnosticFinding("W015", key, "references.bib"))
    return findings


def check_labels(root: Path) -> list[DiagnosticFinding]:
    labels: list[tuple[str, Path, int]] = []
    refs: list[tuple[str, Path, int]] = []
    findings: list[DiagnosticFinding] = []
    for path in root.rglob("*.tex") if root.exists() else []:
        text = read_text(path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            labels.extend((match.group(1), path, line_number) for match in LABEL_RE.finditer(line))
            refs.extend((match.group(1), path, line_number) for match in REF_RE.finditer(line))
        for env in re.finditer(r"\\begin\{(figure|table)\}(.+?)\\end\{\1\}", text, flags=re.S):
            if "\\label{" not in env.group(2):
                findings.append(DiagnosticFinding("W016", f"{env.group(1)} environment may lack label", relative(path, root)))
    counts = Counter(label for label, _, _ in labels)
    defined = set(counts)
    for label, path, line_number in labels:
        if counts[label] > 1:
            findings.append(DiagnosticFinding("E010", label, relative(path, root), line_number))
    for key, path, line_number in refs:
        if key not in defined:
            findings.append(DiagnosticFinding("E011", key, relative(path, root), line_number))
    return findings


def check_word_conversion(input_path: Path) -> list[DiagnosticFinding]:
    text = read_text(input_path)
    findings: list[DiagnosticFinding] = []
    patterns = [
        (r"<\/?\w+[^>]*>", "raw HTML found"),
        (r"\[@[^]]+\]", "Pandoc markdown citation found"),
        ("\ufffd", "Unicode replacement character found"),
        (r"(?i)commented \[|deleted:|inserted:", "possible tracked-change artifact"),
        (r"!\[[^]]*\]\([^)]*\)", "markdown image placeholder found"),
        (r"\\begin\{longtable\}|\\begin\{tabular\}", "converted table needs review"),
        (r"(?i)equation editor|omml|mathml", "equation conversion marker found"),
    ]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern, detail in patterns:
            if re.search(pattern, line):
                findings.append(DiagnosticFinding("W008", detail, str(input_path), line_number))
    heading_levels = []
    for line in text.splitlines():
        if line.startswith("#"):
            heading_levels.append(len(line) - len(line.lstrip("#")))
    for previous, current in zip(heading_levels, heading_levels[1:]):
        if current > previous + 1:
            findings.append(DiagnosticFinding("W008", "section hierarchy jumps"))
            break
    return findings


def check_overleaf(root: Path) -> list[DiagnosticFinding]:
    config = ManuscriptConfig.load(root)
    findings: list[DiagnosticFinding] = []
    if not (root / config.main_tex).exists():
        findings.append(DiagnosticFinding("E001", config.main_tex))
    if config.has_supplement and not (root / config.supplement_tex).exists():
        findings.append(DiagnosticFinding("E009", config.supplement_tex))
    if not (root / "references.bib").exists():
        findings.append(DiagnosticFinding("E002", "references.bib"))
    findings.extend(check_figures(root))
    findings.extend(DiagnosticFinding("E005", relative(path, root), relative(path, root)) for path in forbidden_file_matches(root, config.forbidden_patterns))
    for path, size_mb in large_files(root, config.max_file_size_mb):
        findings.append(DiagnosticFinding("E013", f"{size_mb:.1f} MB", relative(path, root)))
    for path in iter_text_files(root):
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            if LOCAL_PATH_RE.search(line):
                findings.append(DiagnosticFinding("E008", redacted_preview(line), relative(path, root), line_number))
    if (root / ".gitmodules").exists():
        findings.append(DiagnosticFinding("W009", "submodule file detected", ".gitmodules"))
    for path in iter_files(root):
        if path.read_bytes().startswith(b"version https://git-lfs.github.com/spec/v1"):
            findings.append(DiagnosticFinding("W009", "Git LFS pointer file detected", relative(path, root)))
    for staged in staged_latex_build_files(root):
        findings.append(DiagnosticFinding("W004", f"LaTeX build artifact staged: {staged}", staged))
    return findings


def check_github_repo(root: Path) -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    summary = git_summary(root)
    branch = summary.get("branch")
    if branch:
        findings.append(DiagnosticFinding("I003", f"branch: {branch}"))
    else:
        findings.append(DiagnosticFinding("E007", "not a Git repository or no current branch"))
    remotes = summary.get("remotes") or {}
    if isinstance(remotes, dict) and remotes.get("origin"):
        findings.append(DiagnosticFinding("I004", ", ".join(remotes["origin"])))
    else:
        findings.append(DiagnosticFinding("E007", "origin remote missing"))
    upstream = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], root)
    if not upstream.ok:
        findings.append(DiagnosticFinding("W004", "upstream branch is not configured"))
    status = status_porcelain(root)
    if status:
        findings.append(DiagnosticFinding("W004", f"{len(status)} status entries"))
    if not (root / ".gitignore").exists():
        findings.append(DiagnosticFinding("W014", ".gitignore missing"))
    if not (root / "LICENSE").exists():
        findings.append(DiagnosticFinding("W013", "LICENSE missing"))
    if not (root / "README.md").exists():
        findings.append(DiagnosticFinding("W014", "README.md missing"))
    config = ManuscriptConfig.load(root)
    for path, size_mb in large_files(root, config.max_file_size_mb):
        findings.append(DiagnosticFinding("E013", f"{size_mb:.1f} MB", relative(path, root)))
    findings.extend(DiagnosticFinding("E005", relative(path, root), relative(path, root)) for path in forbidden_file_matches(root, config.forbidden_patterns))
    findings.extend(check_privacy(root))
    for staged in staged_latex_build_files(root):
        findings.append(DiagnosticFinding("W004", f"LaTeX build artifact staged: {staged}", staged))
    return findings


def check_manuscript(root: Path) -> list[DiagnosticFinding]:
    config = ManuscriptConfig.load(root)
    findings: list[DiagnosticFinding] = []
    if not root.exists():
        return [DiagnosticFinding("E001", f"repository path does not exist: {root}")]
    if not (root / config.main_tex).exists():
        findings.append(DiagnosticFinding("E001", config.main_tex))
    if not (root / "references.bib").exists():
        findings.append(DiagnosticFinding("E002", "references.bib"))
    if not (root / "figures").exists():
        findings.append(DiagnosticFinding("E003", "figures/ directory missing"))
    if config.has_supplement and not (root / config.supplement_tex).exists():
        findings.append(DiagnosticFinding("E009", config.supplement_tex))
    findings.extend(check_manifest(root))
    forbidden = forbidden_file_matches(root, config.forbidden_patterns)
    if forbidden:
        for path in forbidden:
            code = "E014" if path.is_dir() else "E005"
            findings.append(DiagnosticFinding(code, relative(path, root), relative(path, root)))
    else:
        findings.append(DiagnosticFinding("I006", "no forbidden raw/model/cache outputs found"))
    for path, size_mb in large_files(root, config.max_file_size_mb):
        findings.append(DiagnosticFinding("E013", f"{size_mb:.1f} MB", relative(path, root)))
    for hit in find_banned_terms(root):
        findings.append(DiagnosticFinding("E006", f"{hit.term} -> {hit.publication_label}", relative(hit.path, root), hit.line_number))
    findings.extend(check_privacy(root))
    findings.extend(check_figures(root))
    findings.extend(check_labels(root))
    findings.extend(check_citations(root))
    if (root / ".git").exists():
        summary = git_summary(root)
        remotes = summary.get("remotes") or {}
        if isinstance(remotes, dict) and remotes.get("origin"):
            findings.append(DiagnosticFinding("I004", ", ".join(remotes["origin"])))
        status = summary.get("status") or []
        if status:
            findings.append(DiagnosticFinding("W004", f"{len(status)} status entries"))
    return findings


def format_findings(findings: list[DiagnosticFinding]) -> str:
    from .messages import format_finding, severity_counts

    counts = severity_counts(findings)
    lines = [f"Summary: {counts.get('ERROR', 0)} errors, {counts.get('WARNING', 0)} warnings, {counts.get('INFO', 0)} info"]
    for severity in ["ERROR", "WARNING", "INFO"]:
        group = [finding for finding in findings if finding.message.severity == severity]
        if not group:
            continue
        lines.append("")
        lines.append(f"{severity}:")
        lines.extend(f"- {format_finding(finding)}" for finding in group)
    return "\n".join(lines)
