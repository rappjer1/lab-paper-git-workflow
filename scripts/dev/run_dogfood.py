"""Run lightweight dogfood scenarios against synthetic examples."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI = REPO_ROOT / "scripts" / "paper-scaffold.py"


@dataclass(frozen=True)
class DogfoodStep:
    name: str
    command: list[str]


@dataclass(frozen=True)
class DogfoodResult:
    name: str
    command: list[str]
    exit_code: int


def report_path_for(output: Path) -> Path:
    if output.name == "dogfood":
        return output.parent / "dogfood_report.md"
    return output.parent / f"{output.name}_report.md"


def build_steps(output: Path, python_executable: str) -> list[DogfoodStep]:
    demo = output / "demo_manuscript"
    lock = demo / "metadata" / "artifact_lock.json"
    return [
        DogfoodStep("self-test", [python_executable, str(CLI), "self-test", "--output", str(output / "self_test"), "--keep-output"]),
        DogfoodStep("demo", [python_executable, str(CLI), "demo", "--output", str(demo), "--overwrite"]),
        DogfoodStep("release-check", [python_executable, str(CLI), "release-check", "--manuscript-repo", str(demo), "--write-report", str(demo / "release_check.md")]),
        DogfoodStep("provenance-report", [python_executable, str(CLI), "provenance-report", "--manuscript-repo", str(demo), "--write-md", str(output / "provenance_report.md"), "--write-json", str(output / "provenance_ledger.json")]),
        DogfoodStep("freeze-artifacts", [python_executable, str(CLI), "freeze-artifacts", "--manuscript-repo", str(demo), "--write-lock", str(lock)]),
        DogfoodStep("compare-lock", [python_executable, str(CLI), "compare-lock", "--manuscript-repo", str(demo), "--lock", str(lock), "--write-report", str(output / "lock_comparison.md"), "--write-json", str(output / "lock_comparison.json")]),
        DogfoodStep("package-submission", [python_executable, str(CLI), "package-submission", "--manuscript-repo", str(demo), "--output", str(output / "submission_package"), "--overwrite"]),
        DogfoodStep("reviewer-binder", [python_executable, str(CLI), "reviewer-binder", "--manuscript-repo", str(demo), "--round", "1", "--output", str(output / "reviewer_response_round_1"), "--overwrite"]),
        DogfoodStep("audit-project", [python_executable, str(CLI), "audit-project", "--path", "examples/dogfood/messy_project_audit/project", "--write-report", str(output / "messy_project_audit.md")]),
    ]


def run_step(step: DogfoodStep) -> DogfoodResult:
    print(f"[run] {step.name}", flush=True)
    completed = subprocess.run(step.command, cwd=REPO_ROOT, check=False)
    print(f"[exit {completed.returncode}] {step.name}", flush=True)
    return DogfoodResult(step.name, step.command, completed.returncode)


def write_report(path: Path, output: Path, results: list[DogfoodResult]) -> None:
    failures = [result for result in results if result.exit_code != 0]
    lines = [
        "# Dogfood Report",
        "",
        f"- Output folder: `{output.as_posix()}`",
        f"- Steps: {len(results)}",
        f"- Passed: {len(results) - len(failures)}",
        f"- Failed: {len(failures)}",
        "",
        "## Steps",
        "",
    ]
    for result in results:
        status = "passed" if result.exit_code == 0 else "failed"
        command = " ".join(str(part) for part in result.command)
        lines.extend([f"- `{result.name}`: {status} (exit {result.exit_code})", f"  - `{command}`"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run lightweight Paper Scaffold dogfood scenarios.")
    parser.add_argument("--output", type=Path, default=Path("scratch/dogfood"), help="Output folder for generated dogfood files.")
    parser.add_argument("--keep-output", action="store_true", help="Keep generated dogfood output folder after the run.")
    parser.add_argument("--python", default=sys.executable, help="Python executable used to run Paper Scaffold.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = args.output
    report = report_path_for(output)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)
    results = [run_step(step) for step in build_steps(output, args.python)]
    write_report(report, output, results)
    failures = [result for result in results if result.exit_code != 0]
    print("")
    print(f"Dogfood report: {report}")
    print(f"Dogfood summary: {len(results) - len(failures)} passed, {len(failures)} failed")
    if not args.keep_output:
        shutil.rmtree(output, ignore_errors=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
