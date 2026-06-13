"""Small wrappers around Git commands used by validation and CLI checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

LATEX_BUILD_EXTENSIONS = {
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".run.xml",
    ".synctex.gz",
    ".toc",
}


@dataclass(frozen=True)
class GitCommandResult:
    args: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run_git(args: list[str], cwd: str | Path) -> GitCommandResult:
    command = ["git", *args]
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except FileNotFoundError as exc:
        return GitCommandResult(command, 127, "", str(exc))
    except subprocess.TimeoutExpired as exc:
        return GitCommandResult(command, 124, exc.stdout or "", exc.stderr or "git command timed out")
    return GitCommandResult(command, completed.returncode, completed.stdout.strip(), completed.stderr.strip())


def current_branch(cwd: str | Path) -> str | None:
    result = run_git(["branch", "--show-current"], cwd)
    if result.ok and result.stdout:
        return result.stdout
    return None


def remotes(cwd: str | Path) -> dict[str, list[str]]:
    result = run_git(["remote", "-v"], cwd)
    parsed: dict[str, list[str]] = {}
    if not result.ok:
        return parsed
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            parsed.setdefault(parts[0], [])
            if parts[1] not in parsed[parts[0]]:
                parsed[parts[0]].append(parts[1])
    return parsed


def status_porcelain(cwd: str | Path) -> list[str]:
    result = run_git(["status", "--porcelain"], cwd)
    if not result.ok:
        return []
    return [line for line in result.stdout.splitlines() if line]


def staged_latex_build_files(cwd: str | Path) -> list[str]:
    staged: list[str] = []
    for line in status_porcelain(cwd):
        if len(line) < 4:
            continue
        index_status = line[0]
        path = line[3:].strip()
        suffixes = [Path(path).suffix]
        if path.endswith(".synctex.gz"):
            suffixes.append(".synctex.gz")
        if index_status != " " and any(suffix in LATEX_BUILD_EXTENSIONS for suffix in suffixes):
            staged.append(path)
    return staged


def git_summary(cwd: str | Path) -> dict[str, object]:
    return {
        "branch": current_branch(cwd),
        "remotes": remotes(cwd),
        "status": status_porcelain(cwd),
        "staged_latex_build_files": staged_latex_build_files(cwd),
    }
