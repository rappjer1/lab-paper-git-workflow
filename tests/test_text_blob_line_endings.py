from pathlib import Path
import shutil
import subprocess

import pytest


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
    "src/paper_scaffold/provenance.py": 50,
    "src/paper_scaffold/cli.py": 100,
    "pyproject.toml": 10,
}


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], text=False, capture_output=True, check=False)


def tracked_text_blobs() -> list[tuple[str, str]]:
    if shutil.which("git") is None:
        pytest.skip("git is not available")
    result = run_git(["ls-files", "-s"])
    if result.returncode != 0:
        pytest.skip("not running inside a Git worktree")
    blobs: list[tuple[str, str]] = []
    for raw_line in result.stdout.decode("utf-8", errors="replace").splitlines():
        parts = raw_line.split(None, 3)
        if len(parts) != 4:
            continue
        blob = parts[1]
        path = parts[3]
        if path == ".gitattributes" or Path(path).suffix.lower() in TEXT_SUFFIXES:
            blobs.append((path, blob))
    return blobs


def blob_bytes(blob: str) -> bytes:
    result = run_git(["cat-file", "-p", blob])
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return result.stdout


def test_tracked_text_blobs_use_lf_line_endings():
    failures = []
    for path, blob in tracked_text_blobs():
        data = blob_bytes(blob)
        cr_count = data.count(b"\r")
        if cr_count:
            failures.append(f"{path}: CR bytes found in Git blob: {cr_count}")
    assert failures == []


def test_key_text_blobs_are_not_collapsed():
    blobs = dict(tracked_text_blobs())
    failures = []
    for path, minimum_lf_count in KEY_MIN_LF_COUNTS.items():
        blob = blobs.get(path)
        assert blob is not None, f"tracked key file is missing: {path}"
        lf_count = blob_bytes(blob).count(b"\n")
        if lf_count <= minimum_lf_count:
            failures.append(f"{path}: suspiciously low LF count in Git blob: {lf_count} <= {minimum_lf_count}")
    assert failures == []
