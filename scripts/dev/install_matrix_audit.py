"""Audit source, editable, wheel, sdist, and fallback install modes."""

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


@dataclass(frozen=True)
class MatrixStep:
    name: str
    command: list[str]
    cwd: Path
    required: bool = True
    env: dict[str, str] | None = None


@dataclass(frozen=True)
class MatrixResult:
    name: str
    exit_code: int | None
    required: bool
    skipped: bool = False


def make_run_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{uuid.uuid4().hex[:8]}"


def default_work_dir(repo_root: Path = REPO_ROOT, run_id: str | None = None) -> Path:
    run_id = run_id or make_run_id()
    return repo_root / "scratch" / "install-matrix" / f"paper-scaffold-{run_id}"


def handle_remove_readonly(func, path, exc_info) -> None:
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except OSError:
        raise exc_info[1]


def remove_tree(path: Path) -> None:
    shutil.rmtree(path, onerror=handle_remove_readonly)


def ensure_work_dir(path: Path, overwrite: bool) -> None:
    if path.exists():
        if not overwrite:
            raise FileExistsError(f"work directory already exists: {path}")
        remove_tree(path)
    path.mkdir(parents=True, exist_ok=True)


def source_env() -> dict[str, str]:
    env = os.environ.copy()
    src = str(REPO_ROOT / "src")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src if not existing else src + os.pathsep + existing
    return env


def venv_python(venv_dir: Path) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def venv_scripts_dir(venv_dir: Path) -> Path:
    return venv_dir / "Scripts" if sys.platform == "win32" else venv_dir / "bin"


def console_script_name() -> str:
    return "paper-scaffold.exe" if sys.platform == "win32" else "paper-scaffold"


def console_path(venv_dir: Path) -> Path:
    return venv_scripts_dir(venv_dir) / console_script_name()


def format_command(command: list[str]) -> str:
    return subprocess.list2cmdline(command) if sys.platform == "win32" else " ".join(command)


def no_install_wrapper_step(python_executable: str) -> MatrixStep:
    return MatrixStep("source no-install wrapper help", [python_executable, "scripts/paper-scaffold.py", "--help"], REPO_ROOT)


def source_module_fallback_step(python_executable: str) -> MatrixStep:
    return MatrixStep("source module fallback help", [python_executable, "-m", "paper_scaffold", "--help"], REPO_ROOT, env=source_env())


def create_venv_step(python_executable: str, venv_dir: Path, name: str) -> MatrixStep:
    return MatrixStep(name, [python_executable, "-m", "venv", str(venv_dir)], REPO_ROOT)


def editable_install_step(python_executable: Path, allow_deps: bool) -> MatrixStep:
    command = [str(python_executable), "-m", "pip", "install", "--no-build-isolation"]
    if not allow_deps:
        command.append("--no-deps")
    command.extend(["-e", ".[dev]"])
    return MatrixStep("editable install", command, REPO_ROOT)


def installed_module_help_step(python_executable: Path, name: str, cwd: Path = REPO_ROOT, required: bool = True) -> MatrixStep:
    return MatrixStep(name, [str(python_executable), "-m", "paper_scaffold", "--help"], cwd, required=required)


def installed_console_help_step(venv_dir: Path, name: str, cwd: Path = REPO_ROOT, required: bool = True) -> MatrixStep:
    return MatrixStep(name, [str(console_path(venv_dir)), "--help"], cwd, required=required)


def installed_self_test_step(python_executable: Path, output: Path) -> MatrixStep:
    return MatrixStep(
        "editable installed self-test",
        [str(python_executable), "-m", "paper_scaffold", "self-test", "--output", str(output), "--keep-output"],
        REPO_ROOT,
    )


def package_install_step(python_executable: Path, artifact: Path, name: str) -> MatrixStep:
    return MatrixStep(
        name,
        [str(python_executable), "-m", "pip", "install", "--no-deps", "--no-build-isolation", str(artifact)],
        REPO_ROOT,
        required=False,
    )


def latest_artifact(dist_dir: Path, pattern: str) -> Path | None:
    matches = sorted(dist_dir.glob(pattern), key=lambda path: path.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def run_step(step: MatrixStep) -> MatrixResult:
    print(f"\n[run] {step.name}", flush=True)
    print(f"cwd: {step.cwd}", flush=True)
    print(f"cmd: {format_command(step.command)}", flush=True)
    env = os.environ.copy()
    if step.env:
        env.update(step.env)
    env.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")
    completed = subprocess.run(step.command, cwd=step.cwd, env=env, check=False)
    state = "pass" if completed.returncode == 0 else "fail"
    print(f"[{state}] {step.name}: exit code {completed.returncode}", flush=True)
    return MatrixResult(step.name, completed.returncode, step.required)


def skip_result(name: str, required: bool = False, reason: str = "") -> MatrixResult:
    suffix = f": {reason}" if reason else ""
    print(f"\n[skip] {name}{suffix}", flush=True)
    return MatrixResult(name, None, required=required, skipped=True)


def run_artifact_install_mode(
    *,
    artifact: Path | None,
    artifact_label: str,
    work_dir: Path,
    python_executable: str,
) -> list[MatrixResult]:
    if artifact is None:
        return [skip_result(f"{artifact_label} install", reason=f"no {artifact_label} artifact found")]
    venv_dir = work_dir / f"{artifact_label}-venv"
    venv_result = run_step(create_venv_step(python_executable, venv_dir, f"{artifact_label} venv"))
    results = [venv_result]
    if venv_result.exit_code != 0:
        return results
    package_python = venv_python(venv_dir)
    install_result = run_step(package_install_step(package_python, artifact, f"{artifact_label} install"))
    results.append(install_result)
    if install_result.exit_code != 0:
        return results
    results.append(run_step(installed_module_help_step(package_python, f"{artifact_label} module fallback help", required=False)))
    if console_path(venv_dir).exists():
        results.append(run_step(installed_console_help_step(venv_dir, f"{artifact_label} console script help", required=False)))
    else:
        results.append(skip_result(f"{artifact_label} console script help", reason="console script not created"))
    return results


def run_install_matrix(
    *,
    python_executable: str,
    work_dir: Path,
    dist_dir: Path,
    allow_deps: bool,
    overwrite: bool,
) -> list[MatrixResult]:
    ensure_work_dir(work_dir, overwrite=overwrite)
    print("Paper Scaffold install matrix audit", flush=True)
    print(f"Python executable: {python_executable}", flush=True)
    print(f"Work directory: {work_dir}", flush=True)
    print(f"Dist directory: {dist_dir}", flush=True)
    print(f"Dependency install: {'allowed' if allow_deps else 'disabled with --no-deps'}", flush=True)
    print("Publish step: disabled", flush=True)

    results: list[MatrixResult] = []
    for step in [no_install_wrapper_step(python_executable), source_module_fallback_step(python_executable)]:
        results.append(run_step(step))

    editable_venv = work_dir / "editable-venv"
    results.append(run_step(create_venv_step(python_executable, editable_venv, "editable install venv")))
    if results[-1].exit_code == 0:
        editable_python = venv_python(editable_venv)
        for step in [
            editable_install_step(editable_python, allow_deps=allow_deps),
            installed_module_help_step(editable_python, "editable module fallback help"),
        ]:
            results.append(run_step(step))
        if console_path(editable_venv).exists():
            results.append(run_step(installed_console_help_step(editable_venv, "editable console script help")))
        else:
            results.append(skip_result("editable console script help", required=True, reason="console script not created"))
        results.append(run_step(installed_self_test_step(editable_python, work_dir / "editable-self-test")))

    wheel = latest_artifact(dist_dir, "*.whl")
    sdist = latest_artifact(dist_dir, "*.tar.gz")
    results.extend(run_artifact_install_mode(artifact=wheel, artifact_label="wheel", work_dir=work_dir, python_executable=python_executable))
    results.extend(run_artifact_install_mode(artifact=sdist, artifact_label="sdist", work_dir=work_dir, python_executable=python_executable))
    return results


def summarize_results(results: list[MatrixResult]) -> int:
    failed_required = [result for result in results if result.required and not result.skipped and result.exit_code != 0]
    failed_optional = [result for result in results if not result.required and not result.skipped and result.exit_code not in {0, None}]
    print("\nInstall matrix summary", flush=True)
    for result in results:
        if result.skipped:
            state = "skipped"
        elif result.exit_code == 0:
            state = "passed"
        else:
            state = "failed"
        requirement = "required" if result.required else "optional"
        print(f"- {result.name}: {state} ({requirement})", flush=True)
    if failed_optional:
        print(f"- optional failures: {len(failed_optional)}", flush=True)
    return 1 if failed_required else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit Paper Scaffold source, editable, wheel, sdist, and fallback install modes.")
    parser.add_argument("--python", default=sys.executable, help="Python executable used to create virtual environments.")
    parser.add_argument("--work-dir", type=Path, default=None, help="Temporary audit directory. Defaults under scratch/install-matrix/.")
    parser.add_argument("--dist-dir", type=Path, default=REPO_ROOT / "dist", help="Folder containing optional wheel/sdist artifacts.")
    parser.add_argument("--allow-deps", action="store_true", help="Allow dependency installation. Default uses --no-deps for network-free audits.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing --work-dir.")
    parser.add_argument("--keep-temp", action="store_true", help="Keep the generated work directory.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    work_dir = args.work_dir or default_work_dir()
    cleanup_owned_work_dir = args.overwrite or not work_dir.exists()
    try:
        results = run_install_matrix(
            python_executable=args.python,
            work_dir=work_dir,
            dist_dir=args.dist_dir,
            allow_deps=args.allow_deps,
            overwrite=args.overwrite,
        )
        return summarize_results(results)
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    finally:
        if cleanup_owned_work_dir and not args.keep_temp and work_dir.exists():
            remove_tree(work_dir)


if __name__ == "__main__":
    raise SystemExit(main())
