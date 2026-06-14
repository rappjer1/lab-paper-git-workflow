"""Check synthetic example artifact integrity."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCAN_ROOTS = [REPO_ROOT / "examples", REPO_ROOT / "templates"]
CHECK_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".csv", ".tex", ".bib", ".yaml", ".yml", ".md"}
TEXT_EXTENSIONS = {".csv", ".tex", ".bib", ".yaml", ".yml", ".md"}
MAX_EXAMPLE_BYTES = 250_000
LOCAL_PATH_PATTERNS = [
    ("Windows absolute path", re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s`'\"<>]+")),
    ("Unix home path", re.compile(r"/home/[^\s`'\"<>]+")),
    ("macOS user path", re.compile(r"/Users/[^\s`'\"<>]+")),
]


def is_placeholder(path: Path) -> bool:
    return ".placeholder" in "".join(path.suffixes)


def checked_extension(path: Path) -> str | None:
    if is_placeholder(path):
        return None
    suffix = path.suffix.lower()
    return suffix if suffix in CHECK_EXTENSIONS else None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_file(path: Path) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    ext = checked_extension(path)
    if ext is None:
        return []
    problems: list[str] = []
    data = path.read_bytes()
    if len(data) > MAX_EXAMPLE_BYTES:
        problems.append(f"{rel}: file is unexpectedly large ({len(data)} bytes)")

    if ext == ".pdf" and not data.startswith(b"%PDF"):
        problems.append(f"{rel}: PDF does not start with %PDF")
    elif ext == ".png" and not data.startswith(b"\x89PNG\r\n\x1a\n"):
        problems.append(f"{rel}: PNG magic bytes missing")
    elif ext in {".jpg", ".jpeg"} and not data.startswith(b"\xff\xd8\xff"):
        problems.append(f"{rel}: JPEG magic bytes missing")
    elif ext in TEXT_EXTENSIONS:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            problems.append(f"{rel}: expected UTF-8 text")
            text = ""
        if ext == ".csv" and text and "," not in text and "\n" not in text:
            problems.append(f"{rel}: CSV has no delimiter or newline")
        for label, pattern in LOCAL_PATH_PATTERNS:
            if pattern.search(text):
                problems.append(f"{rel}: contains private/local path pattern ({label})")
    return problems


def iter_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.exists():
            for path in root.rglob("*"):
                if path.is_file() and checked_extension(path) is not None:
                    files.append(path)
    return sorted(files)


def build_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Check example and template artifact integrity.")


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    files = iter_files()
    problems: list[str] = []
    for path in files:
        problems.extend(check_file(path))
    print("Example integrity check")
    print(f"- files checked: {len(files)}")
    if problems:
        print(f"- problems: {len(problems)}")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("- problems: 0")
    print("Example integrity passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
