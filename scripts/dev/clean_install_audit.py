"""Audit clean clone, editable install, and installed-use workflows."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AuditCommand:
    name: str
    command: list[str]
    cwd: Path
    required: bool = True


@dataclass(frozen=True)
class AuditResult:
    name: str
    exit_code: int | None
    required: bool
    skipped: bool = False


def make_run_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"


def default_clone_path(repo_root: Path = REPO_ROOT, run_id: str | None = None) -> Path:
    run_id = run_id or make_run_id()
    return repo_root / "scratch" / "clean-install" / f"paper-scaffold-{run_id}"


def run_git_config_origin(repo_root: Path = REPO_ROOT) -> str | None:
    completed = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    origin = completed.stdout.strip()
    return origin or None


def resolve_clone_source(source: str | None, repo_root: Path = REPO_ROOT) -> str:
    if source:
        return source
    return run_git_config_origin(repo_root) or str(repo_root)


def build_clone_command(source: str, clone_path: Path) -> AuditCommand:
    return AuditCommand("fresh clone", ["git", "clone", source, str(clone_path)], clone_path.parent)


def build_required_audit_commands(python_executable: str, clone_path: Path) -> list[AuditCommand]:
    return [
        AuditCommand("no-install help", [python_executable, "scripts/paper-scaffold.py", "--help"], clone_path),
        AuditCommand("no-install self-test", [python_executable, "scripts/paper-scaffold.py", "self-test"], clone_path),
        AuditCommand("editable install", [python_executable, "-m", "pip", "install", "-e", ".[dev]"], clone_path),
        AuditCommand("module fallback help", [python_executable, "-m", "paper_scaffold", "--help"], clone_path),
        AuditCommand("installed self-test fallback", [python_executable, "-m", "paper_scaffold", "self-test"], clone_path),
        AuditCommand("text blob guard", [python_executable, "scripts/dev/check_text_blobs.py"], clone_path),
        AuditCommand("pytest runner", [python_executable, "scripts/dev/run_tests.py"], clone_path),
    ]


def build_pre_console_audit_commands(python_executable: str, clone_path: Path) -> list[AuditCommand]:
    return build_required_audit_commands(python_executable, clone_path)[:3]


def build_post_console_audit_commands(python_executable: str, clone_path: Path) -> list[AuditCommand]:
    return build_required_audit_commands(python_executable, clone_path)[3:]


def build_console_script_command(clone_path: Path) -> AuditCommand:
    return AuditCommand("installed console script help", ["paper-scaffold", "--help"], clone_path, required=False)


def build_package_build_probe(python_executable: str, clone_path: Path) -> AuditCommand:
    return AuditCommand("package build availability", [python_executable, "-m", "build", "--version"], clone_path, required=False)


def build_package_build_command(python_executable: str, clone_path: Path) -> AuditCommand:
    return AuditCommand("package build", [python_executable, "-m", "build"], clone_path, required=False)


def format_command(command: list[str]) -> str:
    return subprocess.list2cmdline(command) if sys.platform == "win32" else " ".join(command)


def run_audit_command(step: AuditCommand) -> AuditResult:
    print(f"\n[run] {step.name}", flush=True)
    print(f"cwd: {step.cwd}", flush=True)
    print(f"cmd: {format_command(step.command)}", flush=True)
    completed = subprocess.run(step.command, cwd=step.cwd, check=False)
    status = "pass" if completed.returncode == 0 else "fail"
    print(f"[{status}] {step.name}: exit code {completed.returncode}", flush=True)
    return AuditResult(step.name, completed.returncode, step.required)


def ensure_clone_target_available(clone_path: Path, overwrite: bool) -> None:
    if not clone_path.exists():
        clone_path.parent.mkdir(parents=True, exist_ok=True)
        return
    if not overwrite:
        raise FileExistsError(f"clone path already exists: {clone_path}")
    shutil.rmtree(clone_path)
    clone_path.parent.mkdir(parents=True, exist_ok=True)


def run_clean_install_audit(
    *,
    clone_source: str,
    clone_path: Path,
    python_executable: str,
    overwrite: bool = False,
) -> list[AuditResult]:
    ensure_clone_target_available(clone_path, overwrite)

    print("Paper Scaffold clean-install audit", flush=True)
    print(f"clone source: {clone_source}", flush=True)
    print(f"clone path: {clone_path}", flush=True)
    print(f"python executable: {python_executable}", flush=True)

    results: list[AuditResult] = []
    clone_step = build_clone_command(clone_source, clone_path)
    results.append(run_audit_command(clone_step))
    if results[-1].exit_code != 0:
        return results

    for step in build_pre_console_audit_commands(python_executable, clone_path):
        results.append(run_audit_command(step))

    if shutil.which("paper-scaffold"):
        results.append(run_audit_command(build_console_script_command(clone_path)))
    else:
        print("\n[skip] installed console script help: paper-scaffold is not on PATH", flush=True)
        results.append(AuditResult("installed console script help", None, required=False, skipped=True))

    for step in build_post_console_audit_commands(python_executable, clone_path):
        results.append(run_audit_command(step))

    build_probe = run_audit_command(build_package_build_probe(python_executable, clone_path))
    if build_probe.exit_code == 0:
        results.append(run_audit_command(build_package_build_command(python_executable, clone_path)))
    else:
        print("[skip] package build: build frontend is not installed", flush=True)
        results.append(AuditResult("package build", None, required=False, skipped=True))

    return results


def summarize_results(results: list[AuditResult]) -> int:
    failed_required = [result for result in results if result.required and not result.skipped and result.exit_code != 0]
    print("\nSummary", flush=True)
    for result in results:
        if result.skipped:
            state = "skipped"
        elif result.exit_code == 0:
            state = "passed"
        else:
            state = "failed"
        requirement = "required" if result.required else "optional"
        print(f"- {result.name}: {state} ({requirement})", flush=True)
    return 1 if failed_required else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit clean clone, editable install, and installed-use Paper Scaffold workflows.")
    parser.add_argument("--clone-path", type=Path, default=None, help="Fresh clone destination. Defaults to scratch/clean-install/paper-scaffold-<run-id>.")
    parser.add_argument("--source", default=None, help="Git clone source. Defaults to origin URL, then this checkout path.")
    parser.add_argument("--python", default=sys.executable, help="Python executable to use inside the clone. Defaults to this interpreter.")
    parser.add_argument("--overwrite", action="store_true", help="Delete an existing clone path before cloning.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    clone_path = args.clone_path or default_clone_path()
    clone_source = resolve_clone_source(args.source)
    try:
        results = run_clean_install_audit(
            clone_source=clone_source,
            clone_path=clone_path,
            python_executable=args.python,
            overwrite=args.overwrite,
        )
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return summarize_results(results)


if __name__ == "__main__":
    raise SystemExit(main())
