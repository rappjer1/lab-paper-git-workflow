"""Environment checks for manuscript workflow setup."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import sys

from .git_helpers import git_summary


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    status: str
    detail: str
    next_action: str = ""
    code: str = ""


def _tool_check(name: str, executable: str, optional: bool = True, missing_code: str = "") -> DoctorCheck:
    found = shutil.which(executable)
    if found:
        return DoctorCheck(name, "OK", found)
    status = "optional" if optional else "missing"
    return DoctorCheck(name, status, f"{executable} not found on PATH", f"Install {executable} if you need this feature.", missing_code)


def _path_check(path: Path, label: str) -> DoctorCheck:
    if path.exists():
        return DoctorCheck(label, "OK", str(path))
    return DoctorCheck(label, "missing", str(path), f"Create {path.name} or initialize a manuscript repo.")


def looks_like_manuscript_repo(path: Path) -> bool:
    markers = [
        path / "main.tex",
        path / "references.bib",
        path / "figures",
        path / "metadata" / "manuscript_config.yaml",
    ]
    return sum(1 for marker in markers if marker.exists()) >= 2


def looks_like_tool_repo(path: Path) -> bool:
    markers = [
        path / "src" / "paper_scaffold" / "cli.py",
        path / "templates" / "manuscript_repo",
        path / "pyproject.toml",
        path / "docs",
    ]
    return sum(1 for marker in markers if marker.exists()) >= 3


def run_doctor(cwd: str | Path = ".") -> list[DoctorCheck]:
    root = Path(cwd).resolve()
    is_tool_repo = looks_like_tool_repo(root)
    is_manuscript_repo = looks_like_manuscript_repo(root)
    checks: list[DoctorCheck] = [
        DoctorCheck("Python", "OK", sys.version.replace("\n", " ")),
        DoctorCheck("Current directory", "OK", str(root)),
        _tool_check("Git", "git", optional=False),
        _tool_check("Pandoc", "pandoc", optional=True, missing_code="W001"),
        _tool_check("latexmk", "latexmk", optional=True, missing_code="W002"),
        _tool_check("pdflatex", "pdflatex", optional=True, missing_code="W002"),
        _tool_check("GitHub CLI", "gh", optional=True, missing_code="W003"),
    ]

    summary = git_summary(root)
    branch = summary.get("branch")
    if branch:
        checks.append(DoctorCheck("Git repository", "OK", f"branch: {branch}"))
        remotes = summary.get("remotes") or {}
        if isinstance(remotes, dict) and remotes.get("origin"):
            checks.append(DoctorCheck("Git remote origin", "OK", ", ".join(remotes["origin"]), code="I004"))
        else:
            checks.append(DoctorCheck("Git remote origin", "missing", "origin not configured", "Add a GitHub manuscript repo as origin when you are ready to sync.", "E007"))
    else:
        checks.append(DoctorCheck("Git repository", "missing", "not inside a Git repo", "Run this inside the manuscript repo or initialize Git."))

    if is_tool_repo:
        checks.append(
            DoctorCheck(
                "Repository context",
                "OK",
                "This is the Paper Scaffold tool repo, not a manuscript repo. Missing main.tex is expected here.",
                code="I001",
            )
        )
    elif is_manuscript_repo:
        checks.append(DoctorCheck("Repository context", "OK", "This looks like a manuscript repo.", code="I003"))
    else:
        checks.append(DoctorCheck("Repository context", "missing", "not enough manuscript markers found", "Run paper-scaffold init or move into a manuscript repo."))

    if not is_tool_repo:
        checks.extend(
            [
                _path_check(root / "main.tex", "main.tex"),
                _path_check(root / "references.bib", "references.bib"),
                _path_check(root / "figures", "figures/"),
            ]
        )
    return checks


def format_doctor_checks(checks: list[DoctorCheck]) -> str:
    lines = ["paper-scaffold doctor"]
    for check in checks:
        label = check.status.upper()
        code = f"{check.code} " if check.code else ""
        lines.append(f"[{label}] {code}{check.name}: {check.detail}")
        if check.next_action:
            lines.append(f"  next: {check.next_action}")
    lines.append("")
    lines.append("Next actions:")
    lines.append("- If you have a Word draft, read docs/word_to_overleaf.md and use import-word if Pandoc is available.")
    lines.append("- If you have Python figures/tables, read docs/python_outputs_to_overleaf.md and use discover-artifacts.")
    lines.append("- Before Overleaf sync, run paper-scaffold validate.")
    return "\n".join(lines)
