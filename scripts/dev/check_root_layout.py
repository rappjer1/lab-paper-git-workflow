"""Check that the repository root stays focused on live project files."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BLOCKED_PATTERNS = ("V0_*.md", "V1_0_*.md")
BLOCKED_NAMES = {"IMPLEMENTATION_REPORT.md", "PUBLIC_READINESS_AUDIT.md"}
ALLOWED_FILES = {
    ".gitattributes",
    ".gitignore",
    ".pre-commit-config.yaml",
    "CHANGELOG.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PUBLIC_RELEASE_CHECKLIST.md",
    "QUICKSTART.md",
    "README.md",
    "ROADMAP.md",
    "SECURITY.md",
    "pyproject.toml",
}
ALLOWED_DIRS = {
    ".git",
    ".github",
    ".pytest_cache",
    ".ruff_cache",
    "contracts",
    "docs",
    "examples",
    "scripts",
    "scratch",
    "src",
    "templates",
    "tests",
}


def relative_name(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def blocked_report_files() -> list[Path]:
    blocked: set[Path] = set()
    for pattern in BLOCKED_PATTERNS:
        blocked.update(path for path in REPO_ROOT.glob(pattern) if path.is_file())
    blocked.update(path for name in BLOCKED_NAMES if (path := REPO_ROOT / name).is_file())
    return sorted(blocked, key=relative_name)


def unknown_root_entries() -> list[Path]:
    unknown: list[Path] = []
    for path in REPO_ROOT.iterdir():
        name = path.name
        if path.is_dir() and name not in ALLOWED_DIRS:
            unknown.append(path)
        elif path.is_file() and name not in ALLOWED_FILES and path not in blocked_report_files():
            unknown.append(path)
    return sorted(unknown, key=relative_name)


def main() -> int:
    blocked = blocked_report_files()
    unknown = unknown_root_entries()

    print("Root layout check")
    print(f"- blocked historical reports in root: {len(blocked)}")
    print(f"- unknown root entries: {len(unknown)}")
    for path in blocked:
        print(f"- blocked: {relative_name(path)}")
    for path in unknown:
        print(f"- warning: unknown root entry: {relative_name(path)}")

    if blocked:
        print("Root layout check failed. Move historical reports to docs/release_reports/.")
        return 1
    print("Root layout check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
