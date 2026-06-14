"""Run the test suite with shell-independent temp-directory handling."""

from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def make_run_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"


def create_run_paths(repo_root: Path = REPO_ROOT, run_id: str | None = None) -> tuple[Path, Path]:
    run_id = run_id or make_run_id()
    run_root = repo_root / "scratch" / "test-runs"
    basetemp = run_root / f"pytest-{run_id}"
    temp = run_root / f"tmp-{run_id}"
    basetemp.mkdir(parents=True, exist_ok=False)
    temp.mkdir(parents=True, exist_ok=False)
    return basetemp, temp


def parse_pytest_args(extra_args: str | None) -> list[str]:
    if not extra_args:
        return []
    return shlex.split(extra_args)


def build_pytest_command(python_executable: str, basetemp: Path, extra_args: list[str] | None = None) -> list[str]:
    command = [
        python_executable,
        "-m",
        "pytest",
        "tests",
        f"--basetemp={basetemp}",
        "-p",
        "no:cacheprovider",
    ]
    command.extend(extra_args or [])
    return command


def build_subprocess_env(temp: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["TMP"] = str(temp)
    env["TEMP"] = str(temp)
    env.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    return env


def format_command(command: list[str]) -> str:
    return shlex.join(command)


def cleanup_path(path: Path) -> None:
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        return
    except OSError as exc:
        print(f"warning: could not remove {path}: {exc}", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Paper Scaffold tests with unique repo-local temp directories.")
    parser.add_argument("--python", default=sys.executable, help="Python executable to use for pytest. Defaults to this interpreter.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep the generated scratch/test-runs temp directories.")
    parser.add_argument("--pytest-args", default="", help='Extra pytest arguments as one quoted string, for example "--maxfail=1 -q".')
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    basetemp, temp = create_run_paths()
    extra_args = parse_pytest_args(args.pytest_args)
    command = build_pytest_command(args.python, basetemp, extra_args)
    env = build_subprocess_env(temp)

    print(f"Python executable: {args.python}", flush=True)
    print(f"TMP/TEMP path: {temp}", flush=True)
    print(f"pytest basetemp: {basetemp}", flush=True)
    print(f"pytest command: {format_command(command)}", flush=True)

    exit_code = 127
    try:
        completed = subprocess.run(command, cwd=REPO_ROOT, env=env, check=False)
        exit_code = completed.returncode
        print(f"pytest exit code: {exit_code}", flush=True)
    except FileNotFoundError as exc:
        print(f"failed to start pytest command: {exc}", file=sys.stderr)
    finally:
        if not args.keep_temp:
            cleanup_path(basetemp)
            cleanup_path(temp)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
