"""Normalize tracked text files to LF bytes in the working tree and Git index."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys


TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".cff",
    ".tex",
    ".bib",
    ".txt",
    ".ini",
    ".cfg",
}
GITATTRIBUTES_TEXT = """* text=auto
*.py text eol=lf
*.md text eol=lf
*.toml text eol=lf
*.yaml text eol=lf
*.yml text eol=lf
*.json text eol=lf
*.cff text eol=lf
*.tex text eol=lf
*.bib text eol=lf
*.txt text eol=lf
*.ini text eol=lf
*.cfg text eol=lf
"""
PROBLEM_FILES = [
    ".gitattributes",
    "src/paper_scaffold/provenance.py",
    "src/paper_scaffold/cli.py",
    "pyproject.toml",
]


@dataclass(frozen=True)
class TrackedFile:
    path: str
    mode: str
    blob: str


@dataclass(frozen=True)
class LineStats:
    lf_count: int
    cr_count: int
    bare_cr: bool
    collapsed: bool


def run_git(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def tracked_text_files() -> list[TrackedFile]:
    result = run_git(["ls-files", "-s"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    tracked: list[TrackedFile] = []
    for raw_line in result.stdout.decode("utf-8", errors="replace").splitlines():
        parts = raw_line.split(None, 3)
        if len(parts) != 4:
            continue
        mode, blob, _stage, path = parts
        if path == ".gitattributes" or Path(path).suffix.lower() in TEXT_SUFFIXES:
            tracked.append(TrackedFile(path=path, mode=mode, blob=blob))
    if ".gitattributes" not in {item.path for item in tracked}:
        tracked.append(TrackedFile(path=".gitattributes", mode="100644", blob=""))
    return tracked


def blob_bytes(blob: str) -> bytes:
    if not blob:
        return b""
    result = run_git(["cat-file", "-p", blob])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def normalize_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def has_bare_cr(data: bytes) -> bool:
    return any(byte == 13 and (index + 1 == len(data) or data[index + 1] != 10) for index, byte in enumerate(data))


def line_stats(data: bytes, path: str) -> LineStats:
    lf_count = data.count(b"\n")
    cr_count = data.count(b"\r")
    collapsed = False
    if path == ".gitattributes":
        collapsed = lf_count <= 10
    elif path == "src/paper_scaffold/provenance.py":
        collapsed = lf_count <= 50
    elif path == "src/paper_scaffold/cli.py":
        collapsed = lf_count <= 100
    elif path == "pyproject.toml":
        collapsed = lf_count <= 10
    elif len(data) > 1000 and lf_count <= 2:
        collapsed = True
    return LineStats(lf_count=lf_count, cr_count=cr_count, bare_cr=has_bare_cr(data), collapsed=collapsed)


def write_blob(data: bytes) -> str:
    result = run_git(["hash-object", "-w", "--no-filters", "--stdin"], input_bytes=data)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("ascii").strip()


def update_index(mode: str, blob: str, path: str) -> None:
    result = run_git(["update-index", "--add", "--cacheinfo", f"{mode},{blob},{path}"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))


def status_porcelain_tracked() -> list[str]:
    result = run_git(["status", "--porcelain", "--untracked-files=no"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return [line for line in result.stdout.decode("utf-8", errors="replace").splitlines() if line]


def tracked_path_from_status(line: str) -> str:
    path = line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip()


def unrelated_tracked_changes() -> list[str]:
    tracked_by_path = {item.path: item for item in tracked_text_files()}
    unrelated: list[str] = []
    for line in status_porcelain_tracked():
        path = tracked_path_from_status(line)
        item = tracked_by_path.get(path)
        if item is None:
            unrelated.append(line)
            continue
        worktree_path = Path(path)
        if not worktree_path.exists() or not worktree_path.is_file():
            unrelated.append(line)
            continue
        try:
            index_normalized = normalize_bytes(blob_bytes(item.blob))
            working_normalized = normalize_bytes(worktree_path.read_bytes())
        except OSError:
            unrelated.append(line)
            continue
        if index_normalized != working_normalized:
            unrelated.append(line)
    return unrelated


def desired_working_bytes(path: str) -> bytes:
    if path == ".gitattributes":
        return GITATTRIBUTES_TEXT.encode("utf-8")
    file_path = Path(path)
    if not file_path.exists():
        return b""
    return normalize_bytes(file_path.read_bytes())


def print_problem_file_summary(label: str, values: dict[str, LineStats]) -> None:
    print(label)
    print("path\tlf_count\tcr_count\tbare_cr\tcollapsed")
    for path in PROBLEM_FILES:
        stats = values.get(path)
        if stats is None:
            print(f"{path}\t<not tracked>\t<not tracked>\t<not tracked>\t<not tracked>")
        else:
            print(f"{path}\t{stats.lf_count}\t{stats.cr_count}\t{stats.bare_cr}\t{stats.collapsed}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Normalize tracked text files to LF bytes in the working tree and Git index.")
    parser.add_argument("--apply", action="store_true", help="Write normalized LF bytes to the working tree and index")
    parser.add_argument("--force", action="store_true", help="Operate even when tracked files have non-line-ending changes")
    args = parser.parse_args(argv)

    if not args.force:
        unrelated = unrelated_tracked_changes()
        if unrelated:
            print("Refusing to normalize because tracked files have non-line-ending changes:")
            for line in unrelated:
                print(f"- {line}")
            print("Commit/stash those changes or rerun with --force.")
            return 2

    tracked = tracked_text_files()
    before = {item.path: line_stats(blob_bytes(item.blob), item.path) for item in tracked if item.path in PROBLEM_FILES}
    print_problem_file_summary("Before index blob summary", before)

    changed = 0
    after: dict[str, LineStats] = {}
    for item in tracked:
        normalized = desired_working_bytes(item.path)
        if not normalized and item.path != ".gitattributes":
            continue
        current_blob_bytes = blob_bytes(item.blob)
        if normalize_bytes(current_blob_bytes) != normalized or current_blob_bytes != normalized:
            changed += 1
        if args.apply:
            Path(item.path).parent.mkdir(parents=True, exist_ok=True)
            Path(item.path).write_bytes(normalized)
            blob = write_blob(normalized)
            update_index(item.mode, blob, item.path)
            if item.path in PROBLEM_FILES:
                after[item.path] = line_stats(blob_bytes(blob), item.path)
        else:
            if item.path in PROBLEM_FILES:
                after[item.path] = line_stats(normalized, item.path)

    print("")
    print_problem_file_summary("After normalized blob summary" if args.apply else "Dry-run normalized summary", after)
    print("")
    print(f"Tracked text files needing normalized index blobs: {changed}")
    if not args.apply:
        print("Dry run only. Rerun with --apply to write normalized working-tree and index blobs.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
