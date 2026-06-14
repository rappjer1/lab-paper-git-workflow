"""Build local wheel and sdist artifacts without publishing them."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class BuildArtifacts:
    wheels: list[Path]
    sdists: list[Path]


def handle_remove_readonly(func, path, exc_info) -> None:
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        raise exc_info[1]


def remove_tree(path: Path) -> None:
    shutil.rmtree(path, onerror=handle_remove_readonly)


def format_command(command: list[str]) -> str:
    return subprocess.list2cmdline(command) if sys.platform == "win32" else " ".join(command)


def build_availability_command(python_executable: str) -> list[str]:
    return [python_executable, "-m", "build", "--version"]


def package_build_command(python_executable: str, dist_dir: Path, isolated: bool = False) -> list[str]:
    command = [python_executable, "-m", "build", "--outdir", str(dist_dir)]
    if not isolated:
        command.append("--no-isolation")
    return command


def find_artifacts(dist_dir: Path) -> BuildArtifacts:
    wheels = sorted(dist_dir.glob("*.whl"))
    sdists = sorted(dist_dir.glob("*.tar.gz"))
    return BuildArtifacts(wheels=wheels, sdists=sdists)


def validate_artifacts(dist_dir: Path) -> BuildArtifacts:
    artifacts = find_artifacts(dist_dir)
    missing: list[str] = []
    if not artifacts.wheels:
        missing.append("wheel (*.whl)")
    if not artifacts.sdists:
        missing.append("sdist (*.tar.gz)")
    if missing:
        raise FileNotFoundError("dist missing: " + ", ".join(missing))
    return artifacts


def display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build local Paper Scaffold wheel and sdist artifacts without publishing.")
    parser.add_argument("--python", default=sys.executable, help="Python executable used for the build frontend.")
    parser.add_argument("--dist-dir", type=Path, default=REPO_ROOT / "dist", help="Build output folder. Defaults to ./dist.")
    parser.add_argument("--clean", action="store_true", help="Remove the output folder before building.")
    parser.add_argument("--isolated", action="store_true", help="Use build isolation. Default is --no-isolation to avoid package-index access.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    dist_dir = args.dist_dir
    availability = build_availability_command(args.python)
    print("Paper Scaffold package build")
    print(f"Python executable: {args.python}")
    print(f"Output folder: {dist_dir}")
    print("Publish step: disabled")

    probe = subprocess.run(availability, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    if probe.returncode != 0:
        print("Package build skipped: Python build frontend is not installed.")
        print("Install the optional build extra, then retry:")
        print(f"  {format_command([args.python, '-m', 'pip', 'install', '-e', '.[build]'])}")
        print(f"  {format_command([args.python, 'scripts/dev/build_package.py', '--clean'])}")
        print("No files were published.")
        return 0

    if dist_dir.exists() and args.clean:
        remove_tree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)

    command = package_build_command(args.python, dist_dir, isolated=args.isolated)
    print(f"Build command: {format_command(command)}")
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
    if completed.returncode != 0:
        print(f"Package build failed with exit code {completed.returncode}.")
        return completed.returncode

    try:
        artifacts = validate_artifacts(dist_dir)
    except FileNotFoundError as exc:
        print(f"Package build validation failed: {exc}")
        return 1

    print("Package build artifacts:")
    for wheel in artifacts.wheels:
        print(f"- wheel: {display_path(wheel)}")
    for sdist in artifacts.sdists:
        print(f"- sdist: {display_path(sdist)}")
    print("No files were published.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
