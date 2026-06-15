"""Run the maintainer release-candidate dry-run audit."""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
REPORT_NAME = "release_candidate_audit_report.md"


@dataclass(frozen=True)
class AuditStep:
    name: str
    command: list[str] | None
    required: bool = True
    skip_reason: str | None = None


@dataclass(frozen=True)
class AuditResult:
    name: str
    status: str
    required: bool
    exit_code: int | None = None
    detail: str = ""
    command: list[str] | None = None


def make_run_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"


def default_output_path() -> Path:
    return REPO_ROOT / "scratch" / "release-candidate" / make_run_id()


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def format_command(command: list[str] | None) -> str:
    if not command:
        return ""
    return shlex.join([str(part) for part in command])


def command_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def build_steps(output: Path, python_executable: str, skip_clean_clone: bool, skip_build: bool, dirty: bool) -> list[AuditStep]:
    dogfood_output = output / "dogfood"
    self_test_output = output / "self-test"
    install_matrix_output = output / "install-matrix"
    clean_install_output = output / "clean-install"
    clean_clone_output = output / "clean-clone-dogfood"
    dist_output = output / "dist"

    steps = [
        AuditStep("text blob guard", [python_executable, "scripts/dev/check_text_blobs.py"]),
        AuditStep("contract audit", [python_executable, "scripts/dev/check_contracts.py"]),
        AuditStep("docs/examples check", [python_executable, "scripts/dev/check_docs_examples.py"]),
        AuditStep("docs link check", [python_executable, "scripts/dev/check_docs_links.py"]),
        AuditStep("example integrity check", [python_executable, "scripts/dev/check_example_integrity.py"]),
        AuditStep("public safety audit", [python_executable, "scripts/dev/check_public_safety.py"]),
        AuditStep("dogfood scenarios", [python_executable, "scripts/dev/run_dogfood.py", "--output", str(dogfood_output), "--keep-output"]),
        AuditStep("self-test", [python_executable, "scripts/paper-scaffold.py", "self-test", "--output", str(self_test_output), "--keep-output"]),
        AuditStep("test suite", [python_executable, "scripts/dev/run_tests.py"]),
    ]

    install_matrix = REPO_ROOT / "scripts" / "dev" / "install_matrix_audit.py"
    if command_exists(install_matrix):
        steps.append(
            AuditStep(
                "install matrix audit",
                [
                    python_executable,
                    "scripts/dev/install_matrix_audit.py",
                    "--python",
                    python_executable,
                    "--work-dir",
                    str(install_matrix_output),
                    "--overwrite",
                    "--keep-temp",
                ],
            )
        )
    else:
        steps.append(AuditStep("install matrix audit", None, required=False, skip_reason="scripts/dev/install_matrix_audit.py is not present"))

    clean_install = REPO_ROOT / "scripts" / "dev" / "clean_install_audit.py"
    if not command_exists(clean_install):
        steps.append(AuditStep("clean install audit", None, required=False, skip_reason="scripts/dev/clean_install_audit.py is not present"))
    elif dirty:
        steps.append(
            AuditStep(
                "clean install audit",
                None,
                required=False,
                skip_reason="working tree is dirty; clean-install cloning from local Git source would omit uncommitted files",
            )
        )
    else:
        steps.append(
            AuditStep(
                "clean install audit",
                [
                    python_executable,
                    "scripts/dev/clean_install_audit.py",
                    "--source",
                    str(REPO_ROOT),
                    "--clone-path",
                    str(clean_install_output),
                    "--python",
                    python_executable,
                    "--overwrite",
                ],
            )
        )

    clean_clone = REPO_ROOT / "scripts" / "dev" / "clean_clone_dogfood_audit.py"
    if skip_clean_clone:
        steps.append(AuditStep("clean clone dogfood audit", None, required=False, skip_reason="skipped by --skip-clean-clone"))
    elif command_exists(clean_clone):
        steps.append(
            AuditStep(
                "clean clone dogfood audit",
                [
                    python_executable,
                    "scripts/dev/clean_clone_dogfood_audit.py",
                    "--source",
                    str(REPO_ROOT),
                    "--clone-path",
                    str(clean_clone_output),
                    "--python",
                    python_executable,
                    "--overwrite",
                ],
            )
        )
    else:
        steps.append(AuditStep("clean clone dogfood audit", None, required=False, skip_reason="scripts/dev/clean_clone_dogfood_audit.py is not present"))

    if skip_build:
        steps.append(AuditStep("package build", None, required=False, skip_reason="skipped by --skip-build"))
    else:
        steps.append(
            AuditStep(
                "package build",
                [
                    python_executable,
                    "scripts/dev/build_package.py",
                    "--python",
                    python_executable,
                    "--dist-dir",
                    str(dist_output),
                    "--clean",
                ],
                required=False,
            )
        )

    return steps


def run_command(command: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=REPO_ROOT, env=env, text=True, capture_output=True, check=False)


def run_step(step: AuditStep) -> AuditResult:
    if step.skip_reason:
        print(f"[skip] {step.name}: {step.skip_reason}", flush=True)
        return AuditResult(step.name, "skipped", step.required, detail=step.skip_reason, command=step.command)
    assert step.command is not None
    print(f"[run] {step.name}", flush=True)
    print(f"      {format_command(step.command)}", flush=True)
    completed = run_command(step.command)
    if completed.stdout:
        print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    if completed.stderr:
        print(completed.stderr, end="" if completed.stderr.endswith("\n") else "\n", file=sys.stderr)
    status = "passed" if completed.returncode == 0 else "failed"
    detail = summarize_output(completed.stdout, completed.stderr)
    if step.name == "package build" and completed.returncode == 0 and "Package build skipped" in completed.stdout:
        status = "skipped"
        detail = "Python build frontend is not installed."
    print(f"[{status}] {step.name} (exit {completed.returncode})", flush=True)
    return AuditResult(step.name, status, step.required, completed.returncode, detail, step.command)


def summarize_output(stdout: str, stderr: str) -> str:
    text = "\n".join(part.strip() for part in [stdout, stderr] if part.strip())
    if not text:
        return ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[-1][:220] if lines else ""


def read_pyproject_version() -> str:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"', text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("pyproject.toml version not found")
    return match.group(1)


def read_init_version() -> str:
    text = (SRC_ROOT / "paper_scaffold" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__ = "([^"]+)"', text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("__version__ not found")
    return match.group(1)


def cli_version(python_executable: str) -> tuple[int, str]:
    completed = run_command([python_executable, "scripts/paper-scaffold.py", "--version"])
    return completed.returncode, completed.stdout.strip() or completed.stderr.strip()


def module_help(python_executable: str) -> tuple[int, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(SRC_ROOT) if not existing else str(SRC_ROOT) + os.pathsep + existing
    completed = run_command([python_executable, "-m", "paper_scaffold", "--help"], env=env)
    return completed.returncode, completed.stdout.strip() or completed.stderr.strip()


def check_version_consistency(python_executable: str) -> AuditResult:
    print("[run] version consistency", flush=True)
    try:
        pyproject_version = read_pyproject_version()
        init_version = read_init_version()
        cli_exit, cli_text = cli_version(python_executable)
        module_exit, module_text = module_help(python_executable)
    except RuntimeError as exc:
        return AuditResult("version consistency", "failed", True, 1, str(exc))

    expected_cli = f"paper-scaffold {pyproject_version}"
    problems: list[str] = []
    if pyproject_version != init_version:
        problems.append(f"pyproject.toml={pyproject_version}, __version__={init_version}")
    if cli_exit != 0 or expected_cli not in cli_text:
        problems.append(f"paper-scaffold --version returned {cli_exit}: {cli_text}")
    if module_exit != 0 or "usage:" not in module_text.lower():
        problems.append(f"python -m paper_scaffold --help returned {module_exit}: {module_text[:160]}")

    if problems:
        detail = "; ".join(problems)
        print(f"[failed] version consistency: {detail}", flush=True)
        return AuditResult("version consistency", "failed", True, 1, detail)
    detail = f"version {pyproject_version}; CLI and module help ok"
    print(f"[passed] version consistency: {detail}", flush=True)
    return AuditResult("version consistency", "passed", True, 0, detail)


def git_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, text=True, capture_output=True, check=False)


def git_snapshot() -> dict[str, str]:
    branch = git_command(["branch", "--show-current"]).stdout.strip() or "(detached)"
    head = git_command(["rev-parse", "--short", "HEAD"]).stdout.strip()
    tags = git_command(["tag", "--points-at", "HEAD"]).stdout.strip().replace("\n", ", ")
    status = git_command(["status", "--short"]).stdout.strip()
    return {"branch": branch, "head": head, "tags": tags or "(none)", "status": status}


def check_git_status(allow_dirty: bool) -> tuple[AuditResult, bool, dict[str, str]]:
    print("[run] git status", flush=True)
    snapshot = git_snapshot()
    dirty = bool(snapshot["status"])
    detail = f"branch {snapshot['branch']}; HEAD {snapshot['head']}; tags at HEAD {snapshot['tags']}"
    if dirty:
        detail += "; working tree dirty"
        if not allow_dirty:
            print(f"[failed] git status: {detail}", flush=True)
            return AuditResult("git status", "failed", True, 1, detail), dirty, snapshot
    print(f"[passed] git status: {detail}", flush=True)
    return AuditResult("git status", "passed", True, 0, detail), dirty, snapshot


def plan_lines(steps: list[AuditStep]) -> list[str]:
    lines = ["Release candidate audit plan"]
    for step in steps:
        state = "required" if step.required else "optional"
        if step.skip_reason:
            lines.append(f"- {step.name}: {state}, skipped ({step.skip_reason})")
        else:
            lines.append(f"- {step.name}: {state}, {format_command(step.command)}")
    lines.extend(["- version consistency: required, internal version and invocation check", "- git status: required, dirty tree check"])
    return lines


def write_report(output: Path, results: list[AuditResult], snapshot: dict[str, str], allow_dirty: bool, planned: bool = False) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / REPORT_NAME
    passed = sum(1 for result in results if result.status == "passed")
    failed = sum(1 for result in results if result.status == "failed")
    skipped = sum(1 for result in results if result.status == "skipped")
    lines = [
        "# Release Candidate Audit Report",
        "",
        f"Generated: `{datetime.now().isoformat(timespec='seconds')}`",
        f"Mode: `{'plan' if planned else 'run'}`",
        f"Output folder: `{display_path(output)}`",
        "",
        "## Git Snapshot",
        "",
        f"- Branch: `{snapshot.get('branch', '(unknown)')}`",
        f"- HEAD: `{snapshot.get('head', '(unknown)')}`",
        f"- Tags at HEAD: `{snapshot.get('tags', '(unknown)')}`",
        f"- Dirty working tree allowed: `{str(allow_dirty).lower()}`",
        "",
        "## Summary",
        "",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        f"- Skipped: `{skipped}`",
        "",
        "## Checks",
        "",
        "| Check | Required | Status | Exit | Detail |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in results:
        detail = result.detail.replace("|", "\\|") if result.detail else ""
        exit_text = "" if result.exit_code is None else str(result.exit_code)
        lines.append(f"| {result.name} | {str(result.required).lower()} | {result.status} | {exit_text} | {detail} |")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "- This audit does not push, merge, tag, publish packages, create releases, upload to Overleaf, or require network access by default.",
            "- Optional package build checks create local artifacts only.",
            "- Skips should be reviewed before tagging v1.0. A skipped optional build frontend is acceptable when local package building is not being tested.",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def has_blocking_failure(results: list[AuditResult]) -> bool:
    return any(result.required and result.status == "failed" for result in results)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Paper Scaffold v1.0-style release-candidate dry-run audit.")
    parser.add_argument("--output", type=Path, default=None, help="Audit output folder. Defaults under scratch/release-candidate/<run-id>.")
    parser.add_argument("--allow-dirty", action="store_true", help="Report a dirty working tree without failing the audit.")
    parser.add_argument("--skip-clean-clone", action="store_true", help="Skip clean clone dogfood audit.")
    parser.add_argument("--skip-build", action="store_true", help="Skip optional local package build.")
    parser.add_argument("--python", default=sys.executable, help="Python executable used for subprocess checks.")
    parser.add_argument("--plan", "--dry-run", action="store_true", dest="plan", help="Print the command plan without running expensive checks.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = args.output or default_output_path()
    git_result, dirty, snapshot = check_git_status(args.allow_dirty)
    steps = build_steps(output, args.python, args.skip_clean_clone, args.skip_build, dirty)

    if args.plan:
        lines = plan_lines(steps)
        for line in lines:
            print(line)
        results = [git_result, AuditResult("release candidate command plan", "passed", True, 0, "plan built without running checks")]
        report_path = write_report(output, results, snapshot, args.allow_dirty, planned=True)
        print(f"Report written: {display_path(report_path)}")
        return 0 if not has_blocking_failure(results) else 1

    results = [git_result]
    results.append(check_version_consistency(args.python))
    for step in steps:
        results.append(run_step(step))

    report_path = write_report(output, results, snapshot, args.allow_dirty)
    print("")
    print(f"Release candidate audit report: {display_path(report_path)}")
    if has_blocking_failure(results):
        print("Release candidate audit failed.")
        return 1
    print("Release candidate audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
