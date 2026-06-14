"""Check tracked text blobs for CR bytes and collapsed line endings.

This inspects Git index blobs, not just working-tree files. That matters when
the local checkout looks normal but the committed blob shown by GitHub raw is
stored with CR-only or otherwise collapsed line endings.
"""

from __future__ import annotations

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
KEY_MIN_LF_COUNTS = {
    ".gitattributes": 10,
    "src/paper_scaffold/provenance.py": 50,
    "src/paper_scaffold/cli.py": 100,
    "pyproject.toml": 10,
}


@dataclass(frozen=True)
class BlobStats:
    path: str
    lf_count: int
    cr_count: int
    bare_cr: bool
    collapsed: bool

    @property
    def ok(self) -> bool:
        return self.cr_count == 0 and not self.collapsed


def run_git(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def tracked_text_blobs() -> list[tuple[str, str]]:
    result = run_git(["ls-files", "-s"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    tracked: list[tuple[str, str]] = []
    for raw_line in result.stdout.decode("utf-8", errors="replace").splitlines():
        parts = raw_line.split(None, 3)
        if len(parts) != 4:
            continue
        blob = parts[1]
        path = parts[3]
        if path == ".gitattributes" or Path(path).suffix.lower() in TEXT_SUFFIXES:
            tracked.append((path, blob))
    return tracked


def blob_bytes(blob: str) -> bytes:
    result = run_git(["cat-file", "-p", blob])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def has_bare_cr(data: bytes) -> bool:
    return any(byte == 13 and (index + 1 == len(data) or data[index + 1] != 10) for index, byte in enumerate(data))


def blob_stats(path: str, data: bytes) -> BlobStats:
    lf_count = data.count(b"\n")
    cr_count = data.count(b"\r")
    min_lines = KEY_MIN_LF_COUNTS.get(path)
    collapsed = False
    if min_lines is not None:
        collapsed = lf_count <= min_lines
    elif len(data) > 1000 and lf_count <= 2:
        collapsed = True
    return BlobStats(
        path=path,
        lf_count=lf_count,
        cr_count=cr_count,
        bare_cr=has_bare_cr(data),
        collapsed=collapsed,
    )


def print_report(stats: list[BlobStats]) -> None:
    print("Tracked text blob line-ending report")
    print("path\tlf_count\tcr_count\tbare_cr\tcollapsed")
    for item in stats:
        marker = "FAIL" if not item.ok else "OK"
        print(f"{marker}\t{item.path}\t{item.lf_count}\t{item.cr_count}\t{item.bare_cr}\t{item.collapsed}")


def main() -> int:
    try:
        stats = [blob_stats(path, blob_bytes(blob)) for path, blob in tracked_text_blobs()]
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print_report(stats)
    failures = [item for item in stats if not item.ok]
    if failures:
        print("")
        print(f"Found {len(failures)} tracked text blob(s) with CR bytes or suspiciously collapsed line endings.")
        return 1
    print("")
    print("All tracked text blobs use LF line endings and passed collapsed-file checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
