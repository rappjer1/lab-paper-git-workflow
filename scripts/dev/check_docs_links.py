"""Check local Markdown links in public docs."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MARKDOWN_FILES = [REPO_ROOT / "README.md", REPO_ROOT / "QUICKSTART.md", *sorted((REPO_ROOT / "docs").rglob("*.md"))]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if not target:
        return target
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if " " in target and not target.startswith("#"):
        target = target.split()[0].strip()
    return target


def local_target_path(source: Path, target: str) -> Path | None:
    if target.startswith(EXTERNAL_PREFIXES) or target.startswith("#"):
        return None
    path_part = target.split("#", maxsplit=1)[0].split("?", maxsplit=1)[0]
    if not path_part:
        return None
    if path_part.startswith("/"):
        return REPO_ROOT / path_part.lstrip("/")
    return source.parent / path_part


def main() -> int:
    problems: list[str] = []
    for md_file in MARKDOWN_FILES:
        if not md_file.exists():
            problems.append(f"missing markdown file: {md_file.relative_to(REPO_ROOT).as_posix()}")
            continue
        text = md_file.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = normalize_target(match.group(1))
            target_path = local_target_path(md_file, target)
            if target_path is None:
                continue
            if not target_path.exists():
                rel_source = md_file.relative_to(REPO_ROOT).as_posix()
                problems.append(f"{rel_source}: broken link target {target}")

    print("Docs link check")
    if problems:
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("- local Markdown links: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
