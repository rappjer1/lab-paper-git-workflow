"""Audit dogfood checks from a fresh clone or local release-candidate copy."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
IGNORE_NAMES = {".git", ".pytest_cache", ".ruff_cache", "__pycache__", "scratch", "build", "dist"}


@dataclass(frozen=True)
class AuditStep:
    name: str
    command: list[str]


@dataclass(frozen=True)
class AuditResult:
    name: str
    exit_code: int


def make_run_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"


def default_clone_path(repo_root: Path = REPO_ROOT, run_id: str | None = None) -> Path:
    return repo_root / "scratch" / "clean-clone-dogfood" / f"paper-scaffold-{run_id or make_run_id()}"


def is_local_source(source: str) -> bool:
    return Path(source).exists()


def handle_remove_readonly(func, path, exc_info) -> None:
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        raise exc_info[1]


def remove_tree(path: Path) -> None:
    shutil.rmtree(path, onerror=handle_remove_readonly)


def overlay_working_tree(source: Path, clone_path: Path) -> None:
    for item in source.iterdir():
        if item.name in IGNORE_NAMES:
            continue
        target = clone_path / item.name
        if item.is_dir():
            if target.exists():
                remove_tree(target)
            shutil.copytree(item, target, ignore=shutil.ignore_patterns(*IGNORE_NAMES))
        else:
            shutil.copy2(item, target)


def prepare_clone(source: str, clone_path: Path, overwrite: bool) -> None:
    if clone_path.exists():
        if not overwrite:
            raise FileExistsError(f"clone path already exists: {clone_path}")
        remove_tree(clone_path)
    clone_path.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(["git", "clone", source, str(clone_path)], cwd=REPO_ROOT, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"git clone failed with exit code {completed.returncode}")
    if is_local_source(source):
        overlay_working_tree(Path(source).resolve(), clone_path)


def build_steps(clone_path: Path, python_executable: str) -> list[AuditStep]:
    return [
        AuditStep("text blob guard", [python_executable, "scripts/dev/check_text_blobs.py"]),
        AuditStep("contract audit", [python_executable, "scripts/dev/check_contracts.py"]),
        AuditStep("docs/examples check", [python_executable, "scripts/dev/check_docs_examples.py"]),
        AuditStep("example integrity", [python_executable, "scripts/dev/check_example_integrity.py"]),
        AuditStep("dogfood", [python_executable, "scripts/dev/run_dogfood.py", "--output", "scratch/dogfood"]),
        AuditStep("tests", [python_executable, "scripts/dev/run_tests.py"]),
        AuditStep("self-test", [python_executable, "scripts/paper-scaffold.py", "self-test", "--output", "scratch/self_test", "--keep-output"]),
    ]


def run_step(step: AuditStep, clone_path: Path) -> AuditResult:
    print(f"[run] {step.name}", flush=True)
    completed = subprocess.run(step.command, cwd=clone_path, check=False)
    print(f"[exit {completed.returncode}] {step.name}", flush=True)
    return AuditResult(step.name, completed.returncode)


def summarize(results: list[AuditResult]) -> int:
    failures = [result for result in results if result.exit_code != 0]
    print("")
    print("Clean clone dogfood audit summary")
    for result in results:
        state = "passed" if result.exit_code == 0 else "failed"
        print(f"- {result.name}: {state} (exit {result.exit_code})")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit dogfood checks from a fresh clone or local source copy.")
    parser.add_argument("--source", default=str(REPO_ROOT), help="Git clone source. Local paths are cloned then overlaid with the working tree.")
    parser.add_argument("--clone-path", type=Path, default=None, help="Fresh clone destination. Defaults under scratch/clean-clone-dogfood/.")
    parser.add_argument("--python", default=sys.executable, help="Python executable to use inside the clone.")
    parser.add_argument("--overwrite", action="store_true", help="Delete an existing clone path before cloning.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    clone_path = args.clone_path or default_clone_path()
    try:
        prepare_clone(args.source, clone_path, args.overwrite)
    except (FileExistsError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Clone path: {clone_path}")
    results = [run_step(step, clone_path) for step in build_steps(clone_path, args.python)]
    return summarize(results)


if __name__ == "__main__":
    raise SystemExit(main())
