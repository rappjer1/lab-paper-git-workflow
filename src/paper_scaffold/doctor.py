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


def _tool_check(name: str, executable: str, optional: bool = True) -> DoctorCheck:
    found = shutil.which(executable)
    if found:
        return DoctorCheck(name, "OK", found)
    status = "optional" if optional else "missing"
    return DoctorCheck(name, status, f"{executable} not found on PATH", f"Install {executable} if you need this feature.")


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


def run_doctor(cwd: str | Path = ".") -> list[DoctorCheck]:
    root = Path(cwd).resolve()
    checks: list[DoctorCheck] = [
        DoctorCheck("Python", "OK", sys.version.replace("\n", " ")),
        DoctorCheck("Current directory", "OK", str(root)),
        _tool_check("Git", "git", optional=False),
        _tool_check("Pandoc", "pandoc", optional=True),
        _tool_check("latexmk", "latexmk", optional=True),
        _tool_check("pdflatex", "pdflatex", optional=True),
        _tool_check("GitHub CLI", "gh", optional=True),
    ]

    summary = git_summary(root)
    branch = summary.get("branch")
    if branch:
        checks.append(DoctorCheck("Git repository", "OK", f"branch: {branch}"))
        remotes = summary.get("remotes") or {}
        if isinstance(remotes, dict) and remotes.get("origin"):
            checks.append(DoctorCheck("Git remote origin", "OK", ", ".join(remotes["origin"])))
        else:
            checks.append(DoctorCheck("Git remote origin", "missing", "origin not configured", "Add a private GitHub manuscript repo as origin."))
    else:
        checks.append(DoctorCheck("Git repository", "missing", "not inside a Git repo", "Run this inside the manuscript repo or initialize Git."))

    if looks_like_manuscript_repo(root):
        checks.append(DoctorCheck("Manuscript repo shape", "OK", "main manuscript files/folders detected"))
    else:
        checks.append(DoctorCheck("Manuscript repo shape", "missing", "not enough manuscript markers found", "Run paper-scaffold init or move into the manuscript repo."))

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
        lines.append(f"[{label}] {check.name}: {check.detail}")
        if check.next_action:
            lines.append(f"  next: {check.next_action}")
    lines.append("")
    lines.append("Next actions:")
    lines.append("- If you have a Word draft, read docs/word_to_overleaf.md and use import-word if Pandoc is available.")
    lines.append("- If you have Python figures/tables, read docs/python_outputs_to_overleaf.md and use discover-artifacts.")
    lines.append("- Before Overleaf sync, run paper-scaffold validate.")
    return "\n".join(lines)
