"""Audit public repository files for privacy, safety, and trust issues."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import fnmatch
import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST_PATH = REPO_ROOT / "contracts" / "public_safety_allowlist.yaml"
TEXT_EXTENSIONS = {".cff", ".cfg", ".ini", ".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}
ARTIFACT_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
MAX_TRACKED_BYTES = 1_000_000
SCAN_ROOTS = [
    REPO_ROOT / ".github",
    REPO_ROOT / "contracts",
    REPO_ROOT / "docs",
    REPO_ROOT / "examples",
    REPO_ROOT / "templates",
]
SCAN_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "QUICKSTART.md",
    REPO_ROOT / "CHANGELOG.md",
    REPO_ROOT / "CONTRIBUTING.md",
    REPO_ROOT / "SECURITY.md",
    REPO_ROOT / "CODE_OF_CONDUCT.md",
    REPO_ROOT / "CITATION.cff",
    REPO_ROOT / "LICENSE",
    REPO_ROOT / "PUBLIC_RELEASE_CHECKLIST.md",
    REPO_ROOT / "pyproject.toml",
]


@dataclass(frozen=True)
class AllowEntry:
    term: str
    allowed_paths: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class Finding:
    category: str
    term: str
    path: str
    line: int | None
    detail: str
    high_risk: bool = True


LOCAL_PATH_PATTERNS = [
    ("Windows local path", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s`'\"<>]+")),
    ("Unix home path", re.compile(r"/home/[^\s`'\"<>]+")),
    ("macOS user path", re.compile(r"/Users/[^\s`'\"<>]+")),
    ("UNC machine path", re.compile(r"(?<![\"'`\\])\\\\[A-Za-z0-9._-]+\\[A-Za-z0-9$._-]+")),
    ("known workstation/user term", re.compile(r"\b(?:SANDROCK|Jeremy)\b", re.IGNORECASE)),
]
SECRET_ASSIGNMENT_RE = re.compile(r"(?i)\b(api[_-]?key|secret|token|password|credential)\b\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{8,})")
AWS_KEY_RE = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
PROJECT_SPECIFIC_TERMS = [
    "hydrology",
    "CAMELS",
    "dHBV",
    "quantum",
    "rating-curve",
    "NeuralHydrology",
    "unpublished",
    "lab-internal",
    "internal lab",
    "our lab",
    "Slack",
]
SAFETY_KEYWORDS = [
    "token",
    "api_key",
    "API_KEY",
    "password",
    "secret",
    "credential",
    ".env",
    "OAuth",
    "PAT",
    "GitHub token",
    "AWS",
    "private",
]
MISLEADING_CLAIMS = [
    "writes your paper",
    "automatically uploads to Overleaf",
    "guarantees compilation",
    "guarantees reproducibility",
    "creates GitHub repos",
    "publishes to PyPI",
    "AI writes claims",
]


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def parse_allowlist(path: Path = ALLOWLIST_PATH) -> list[AllowEntry]:
    if not path.exists():
        return []
    entries: list[AllowEntry] = []
    current: dict[str, object] | None = None
    in_allowed_paths = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#") or stripped == "allowlist:":
            continue
        if stripped.startswith("- term:"):
            if current is not None:
                entries.append(entry_from_dict(current))
            current = {"term": stripped.split(":", 1)[1].strip(), "allowed_paths": [], "reason": ""}
            in_allowed_paths = False
            continue
        if current is None:
            continue
        if stripped == "allowed_paths:":
            in_allowed_paths = True
            continue
        if in_allowed_paths and stripped.startswith("- "):
            current_paths = current.setdefault("allowed_paths", [])
            assert isinstance(current_paths, list)
            current_paths.append(stripped[2:].strip())
            continue
        in_allowed_paths = False
        if stripped.startswith("reason:"):
            current["reason"] = stripped.split(":", 1)[1].strip()
    if current is not None:
        entries.append(entry_from_dict(current))
    return entries


def entry_from_dict(data: dict[str, object]) -> AllowEntry:
    paths = data.get("allowed_paths", [])
    if not isinstance(paths, list):
        paths = []
    return AllowEntry(str(data.get("term", "")), tuple(str(path) for path in paths), str(data.get("reason", "")))


def is_allowed(finding: Finding, allowlist: list[AllowEntry]) -> bool:
    for entry in allowlist:
        if finding.term.lower() != entry.term.lower():
            continue
        if any(fnmatch.fnmatch(finding.path, pattern) for pattern in entry.allowed_paths):
            return True
    return False


def iter_scan_files() -> list[Path]:
    files: set[Path] = {path for path in SCAN_FILES if path.exists() and path.is_file()}
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                files.add(path)
    for path in REPO_ROOT.glob("V*.md"):
        if path.is_file():
            files.add(path)
    for path in REPO_ROOT.glob("PUBLIC_*.md"):
        if path.is_file():
            files.add(path)
    return sorted(files, key=lambda item: item.relative_to(REPO_ROOT).as_posix().lower())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def keyword_pattern(term: str) -> re.Pattern[str]:
    if term == "api_key":
        return re.compile(r"\bapi[_-]?key\b", re.IGNORECASE)
    if term == "API_KEY":
        return re.compile(r"\bAPI_KEY\b")
    if term == ".env":
        return re.compile(r"(?<!\w)\.env(?!\w)", re.IGNORECASE)
    if term == "PAT":
        return re.compile(r"\bPAT\b")
    return re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)


def misleading_pattern(claim: str) -> re.Pattern[str]:
    return re.compile(rf"\b{re.escape(claim)}\b", re.IGNORECASE)


def line_has_negation(line: str) -> bool:
    lowered = line.lower()
    return "does not" in lowered or "do not" in lowered or "not " in lowered or "no " in lowered


def scan_text_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    relative_path = rel(path)
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        for label, pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(line):
                findings.append(Finding("local-path", label, relative_path, line_number, "local path or machine-specific name"))
        if SECRET_ASSIGNMENT_RE.search(line):
            findings.append(Finding("secret-assignment", "secret", relative_path, line_number, "secret-like assignment"))
        if AWS_KEY_RE.search(line):
            findings.append(Finding("secret-assignment", "AWS", relative_path, line_number, "AWS key-like string"))
        for term in PROJECT_SPECIFIC_TERMS:
            if keyword_pattern(term).search(line):
                findings.append(Finding("project-specific", term, relative_path, line_number, "project-specific or channel-specific term"))
        for term in SAFETY_KEYWORDS:
            if keyword_pattern(term).search(line):
                findings.append(Finding("safety-keyword", term, relative_path, line_number, "privacy/security keyword", high_risk=False))
        for claim in MISLEADING_CLAIMS:
            if misleading_pattern(claim).search(line) and not line_has_negation(line):
                findings.append(Finding("misleading-claim", claim, relative_path, line_number, "possibly misleading automation claim"))
    return findings


def check_artifact_file(path: Path) -> list[Finding]:
    relative_path = rel(path)
    suffix = path.suffix.lower()
    if suffix not in ARTIFACT_EXTENSIONS:
        return []
    if "examples" not in path.parts and "templates" not in path.parts:
        return []
    data = path.read_bytes()
    if suffix == ".pdf" and not data.startswith(b"%PDF"):
        return [Finding("invalid-artifact", "PDF", relative_path, None, "PDF does not start with %PDF")]
    if suffix == ".png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return [Finding("invalid-artifact", "PNG", relative_path, None, "PNG magic bytes missing")]
    if suffix in {".jpg", ".jpeg"} and not data.startswith(b"\xff\xd8\xff"):
        return [Finding("invalid-artifact", "JPEG", relative_path, None, "JPEG magic bytes missing")]
    return []


def tracked_files() -> list[Path]:
    result = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return []
    return [REPO_ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]


def scan_tracked_files() -> list[Finding]:
    findings: list[Finding] = []
    for path in tracked_files():
        relative_path = rel(path)
        if relative_path.startswith("scratch/"):
            findings.append(Finding("tracked-scratch", "scratch", relative_path, None, "generated scratch output is tracked"))
        if path.exists() and path.is_file() and path.stat().st_size > MAX_TRACKED_BYTES:
            findings.append(Finding("large-file", "large tracked file", relative_path, None, f"{path.stat().st_size} bytes"))
    return findings


def scan_repository() -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_scan_files():
        if path.suffix.lower() in TEXT_EXTENSIONS or path.name in {"LICENSE"}:
            findings.extend(scan_text_file(path))
        findings.extend(check_artifact_file(path))
    findings.extend(scan_tracked_files())
    return findings


def format_finding(finding: Finding, allowed: bool) -> str:
    location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
    status = "allowed" if allowed else "blocked"
    risk = "high" if finding.high_risk else "review"
    return f"[{status}] [{risk}] {finding.category}: {finding.term} at {location} ({finding.detail})"


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Check public repository files for privacy, safety, and trust issues.")


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    allowlist = parse_allowlist()
    findings = scan_repository()
    blocked = [finding for finding in findings if finding.high_risk and not is_allowed(finding, allowlist)]
    allowed = [finding for finding in findings if is_allowed(finding, allowlist)]
    review = [finding for finding in findings if not finding.high_risk and not is_allowed(finding, allowlist)]

    print("Public safety check")
    print(f"- files scanned: {len(iter_scan_files())}")
    print(f"- findings: {len(findings)}")
    print(f"- allowed findings: {len(allowed)}")
    print(f"- review-only findings: {len(review)}")
    print(f"- blocked high-risk findings: {len(blocked)}")
    for finding in sorted(blocked, key=lambda item: (item.path, item.line or 0, item.category, item.term)):
        print(f"- {format_finding(finding, allowed=False)}")
    if blocked:
        return 1
    print("Public safety check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
