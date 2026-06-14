"""v0.8 workflow helpers for manuscript CI, packages, locks, and binders."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any

from .provenance import build_artifact_lock, build_provenance_ledger, provenance_markdown_report, write_json
from .release import format_release_check, run_release_check

LATEX_BUILD_EXTENSIONS = {
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".run.xml",
    ".synctex.gz",
    ".toc",
}
SOURCE_EXTENSIONS = {".tex", ".bib", ".bst", ".cls", ".sty"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "scratch", "build", "dist"}
PACKAGE_SKIP_PARTS = SKIP_PARTS | {".github"}


@dataclass(frozen=True)
class WorkflowResult:
    ok: bool
    message: str
    path: Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _is_latex_build_file(path: Path) -> bool:
    name = path.name.lower()
    return any(name.endswith(suffix) for suffix in LATEX_BUILD_EXTENSIONS)


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _replace_directory(path: Path, overwrite: bool) -> WorkflowResult | None:
    if path.exists():
        if not overwrite:
            return WorkflowResult(False, f"Output exists: {path}. Pass --overwrite to replace it.", path)
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    path.mkdir(parents=True, exist_ok=True)
    return None


def _path_in_parts(path: Path, blocked: set[str]) -> bool:
    return any(part in blocked for part in path.parts)


def _resolve_lock_path(root: Path, lock_path: str | Path) -> Path:
    lock_file = Path(lock_path)
    if lock_file.is_absolute():
        return lock_file
    if lock_file.exists():
        return lock_file
    return root / lock_file


def manuscript_ci_workflow_text() -> str:
    return """name: manuscript-checks

on:
  push:
  pull_request:

jobs:
  manuscript-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Manuscript repository checks
        run: |
          python - <<'PY'
          from pathlib import Path
          import sys

          root = Path(".")
          errors = []
          warnings = []
          if not (root / "main.tex").exists():
              errors.append("main.tex is missing")
          if not (root / "references.bib").exists():
              warnings.append("references.bib is missing")
          forbidden_suffixes = {".npz", ".pt", ".pth", ".pkl", ".pickle", ".nc", ".zarr", ".zip", ".parquet", ".h5"}
          latex_build_suffixes = {".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".out", ".run.xml", ".synctex.gz", ".toc"}
          skip_parts = {".git", "__pycache__", ".pytest_cache"}
          for path in root.rglob("*"):
              if path.is_dir() or any(part in skip_parts for part in path.parts):
                  continue
              name = path.name.lower()
              suffix = path.suffix.lower()
              if suffix in forbidden_suffixes:
                  errors.append(f"forbidden raw/generated output: {path}")
              if any(name.endswith(item) for item in latex_build_suffixes):
                  errors.append(f"LaTeX build artifact should not be committed: {path}")
              if path.stat().st_size > 25 * 1024 * 1024:
                  errors.append(f"file exceeds 25 MB: {path}")
          for warning in warnings:
              print(f"WARNING: {warning}")
          if errors:
              for error in errors:
                  print(f"ERROR: {error}")
              sys.exit(1)
          print("Manuscript checks passed.")
          PY
"""


def add_manuscript_ci(manuscript_repo: str | Path, *, overwrite: bool = False) -> WorkflowResult:
    root = Path(manuscript_repo)
    if not root.exists():
        return WorkflowResult(False, f"E030 Manuscript repository does not exist: {root}", root)
    workflow_path = root / ".github" / "workflows" / "manuscript-checks.yml"
    if workflow_path.exists() and not overwrite:
        return WorkflowResult(False, f"E030 Workflow exists: {workflow_path}. Pass --overwrite to replace it.", workflow_path)
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(manuscript_ci_workflow_text(), encoding="utf-8")
    return WorkflowResult(True, f"I040 Wrote manuscript CI workflow: {workflow_path}", workflow_path)


def _source_files(root: Path) -> set[Path]:
    files: set[Path] = set()
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if path.is_dir() or _path_in_parts(rel, PACKAGE_SKIP_PARTS):
            continue
        if _is_latex_build_file(path):
            continue
        if path.suffix.lower() in SOURCE_EXTENSIONS:
            files.add(path)
    return files


def _artifact_entries_for_package(ledger: dict[str, object], include_unreferenced: bool) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    for entry in ledger.get("artifacts", []):
        if not isinstance(entry, dict) or not entry.get("manuscript_exists"):
            continue
        used = bool(entry.get("used_in_tex_files"))
        if used or include_unreferenced:
            selected.append(entry)
    for entry in ledger.get("untracked_artifacts", []):
        if isinstance(entry, dict) and entry.get("manuscript_exists") and entry.get("used_in_tex_files"):
            selected.append(entry)
    return selected


def package_submission(manuscript_repo: str | Path, output: str | Path, *, overwrite: bool = False, include_unreferenced: bool = False) -> WorkflowResult:
    root = Path(manuscript_repo)
    if not root.exists():
        return WorkflowResult(False, f"E034 Manuscript repository does not exist: {root}", root)
    output_path = Path(output)
    existing = _replace_directory(output_path, overwrite)
    if existing is not None:
        return WorkflowResult(False, f"E031 {existing.message}", existing.path)

    ledger = build_provenance_ledger(root)
    copied: set[str] = set()
    excluded_unreferenced: list[str] = []
    excluded_untracked: list[str] = []
    package_warnings: list[dict[str, str]] = []
    for src in sorted(_source_files(root), key=lambda item: item.as_posix().lower()):
        rel = _relative(src, root)
        _copy_file(src, output_path / rel)
        copied.add(rel)
    for entry in ledger.get("artifacts", []):
        if not isinstance(entry, dict) or not entry.get("manuscript_exists"):
            continue
        if not include_unreferenced and not entry.get("used_in_tex_files"):
            excluded = str(entry.get("manuscript_path") or entry.get("artifact_id") or "")
            excluded_unreferenced.append(excluded)
            package_warnings.append({"code": "W043", "path": excluded, "message": "unreferenced manifest artifact excluded from package"})
    for entry in ledger.get("untracked_artifacts", []):
        if not isinstance(entry, dict) or not entry.get("manuscript_exists") or entry.get("used_in_tex_files"):
            continue
        excluded = str(entry.get("manuscript_path") or entry.get("artifact_id") or "")
        excluded_untracked.append(excluded)
        package_warnings.append({"code": "W042", "path": excluded, "message": "untracked artifact excluded from package"})
    for entry in _artifact_entries_for_package(ledger, include_unreferenced):
        rel = str(entry.get("manuscript_path") or "")
        if not rel:
            continue
        src = root / rel
        if src.exists() and src.is_file() and not _is_latex_build_file(src):
            _copy_file(src, output_path / rel)
            copied.add(rel)

    manifest = {
        "tool": "Paper Scaffold",
        "created_at": utc_now(),
        "source_manuscript_repo": root.as_posix(),
        "include_unreferenced": include_unreferenced,
        "copied_files": sorted(copied),
        "excluded_unreferenced_artifacts": sorted(item for item in excluded_unreferenced if item),
        "excluded_untracked_artifacts": sorted(item for item in excluded_untracked if item),
        "warnings": package_warnings,
        "provenance_summary": ledger.get("summary", {}),
    }
    write_json(output_path / "submission_package_manifest.json", manifest)
    (output_path / "README_SUBMISSION.md").write_text(
        "# Submission Package\n\n"
        "This folder was generated by `paper-scaffold package-submission`.\n\n"
        "It contains manuscript source files and referenced manuscript artifacts. "
        "Review journal requirements before upload.\n",
        encoding="utf-8",
    )
    return WorkflowResult(True, f"I041 Wrote submission package: {output_path}", output_path)


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def compare_artifact_lock(manuscript_repo: str | Path, lock_path: str | Path) -> dict[str, object]:
    root = Path(manuscript_repo)
    lock_file = _resolve_lock_path(root, lock_path)
    if not lock_file.exists():
        raise FileNotFoundError(lock_file)
    lock = load_json(lock_file)
    current_lock = build_artifact_lock(build_provenance_ledger(root))
    current_by_id = {str(entry.get("artifact_id")): entry for entry in current_lock.get("artifacts", []) if isinstance(entry, dict)}
    locked_by_id = {str(entry.get("artifact_id")): entry for entry in lock.get("artifacts", []) if isinstance(entry, dict)}
    unchanged = []
    changed = []
    missing = []
    new = []
    for artifact_id, locked in sorted(locked_by_id.items()):
        current = current_by_id.get(artifact_id)
        if current is None:
            missing.append(locked)
            continue
        if current.get("manuscript_sha256") == locked.get("manuscript_sha256"):
            unchanged.append(current)
        else:
            changed.append(
                {
                    "artifact_id": artifact_id,
                    "manuscript_path": current.get("manuscript_path") or locked.get("manuscript_path"),
                    "locked_sha256": locked.get("manuscript_sha256"),
                    "current_sha256": current.get("manuscript_sha256"),
                }
            )
    for artifact_id, current in sorted(current_by_id.items()):
        if artifact_id not in locked_by_id:
            new.append(current)
    summary = {
        "locked_artifacts": len(locked_by_id),
        "unchanged": len(unchanged),
        "changed": len(changed),
        "missing": len(missing),
        "new": len(new),
    }
    return {
        "tool": "Paper Scaffold",
        "created_at": utc_now(),
        "manuscript_repo": root.as_posix(),
        "lock_path": lock_file.as_posix(),
        "summary": summary,
        "unchanged": unchanged,
        "changed": changed,
        "missing": missing,
        "new": new,
    }


def lock_comparison_markdown(comparison: dict[str, object]) -> str:
    summary = comparison.get("summary", {}) if isinstance(comparison.get("summary"), dict) else {}
    lines = [
        "# Artifact Lock Comparison",
        "",
        f"- Manuscript repo: {comparison.get('manuscript_repo')}",
        f"- Lock path: {comparison.get('lock_path')}",
        f"- Locked artifacts: {summary.get('locked_artifacts', 0)}",
        f"- Unchanged: {summary.get('unchanged', 0)}",
        f"- Changed: {summary.get('changed', 0)}",
        f"- Missing: {summary.get('missing', 0)}",
        f"- New: {summary.get('new', 0)}",
        "",
        "## Changed Artifacts",
    ]
    changed = [entry for entry in comparison.get("changed", []) if isinstance(entry, dict)]
    lines.extend(
        [f"- W040 `{entry.get('artifact_id')}` -> `{entry.get('manuscript_path')}`" for entry in changed]
        if changed
        else ["- None."]
    )
    lines.append("")
    lines.append("## Missing Artifacts")
    missing = [entry for entry in comparison.get("missing", []) if isinstance(entry, dict)]
    lines.extend(
        [f"- E033 `{entry.get('artifact_id')}` -> `{entry.get('manuscript_path')}`" for entry in missing]
        if missing
        else ["- None."]
    )
    lines.append("")
    lines.append("## New Artifacts")
    new = [entry for entry in comparison.get("new", []) if isinstance(entry, dict)]
    lines.extend(
        [f"- W041 `{entry.get('artifact_id')}` -> `{entry.get('manuscript_path')}`" for entry in new]
        if new
        else ["- None."]
    )
    return "\n".join(lines) + "\n"


def comparison_has_drift(comparison: dict[str, object]) -> bool:
    summary = comparison.get("summary", {}) if isinstance(comparison.get("summary"), dict) else {}
    return bool(summary.get("changed", 0) or summary.get("missing", 0))


def reviewer_binder(manuscript_repo: str | Path, round_id: str, output: str | Path, *, overwrite: bool = False) -> WorkflowResult:
    root = Path(manuscript_repo)
    if not root.exists():
        return WorkflowResult(False, f"E034 Manuscript repository does not exist: {root}", root)
    output_path = Path(output)
    existing = _replace_directory(output_path, overwrite)
    if existing is not None:
        return WorkflowResult(False, f"E035 {existing.message}", existing.path)
    ledger = build_provenance_ledger(root)
    release = run_release_check(root)
    lock = build_artifact_lock(ledger)
    safe_round = str(round_id).strip() or "1"
    (output_path / "README.md").write_text(
        f"# Reviewer Response Binder Round {safe_round}\n\n"
        "This folder collects lightweight revision evidence, provenance snapshots, and response checklists.\n",
        encoding="utf-8",
    )
    (output_path / "response_checklist.md").write_text(
        f"# Response Checklist Round {safe_round}\n\n"
        "- [ ] Map each reviewer point to a manuscript change or response note.\n"
        "- [ ] Confirm response artifacts are listed in the artifact manifest when they belong in the manuscript.\n"
        "- [ ] Run `paper-scaffold release-check` before resubmission.\n"
        "- [ ] Run `paper-scaffold compare-lock` against the submission lock if one exists.\n",
        encoding="utf-8",
    )
    (output_path / "response_artifact_manifest.yaml").write_text(
        "response_artifacts:\n"
        "  - id: response_artifact_1\n"
        f"    round: {safe_round}\n"
        "    reviewer_point: R1.1\n"
        "    manuscript_path: figures/example_response_artifact.pdf\n"
        "    status: planned\n",
        encoding="utf-8",
    )
    (output_path / "provenance_snapshot.md").write_text(provenance_markdown_report(ledger), encoding="utf-8")
    (output_path / "release_check.md").write_text(format_release_check(release), encoding="utf-8")
    (output_path / "artifact_status.txt").write_text(
        "\n".join(
            [
                "Artifact status",
                f"- current: {ledger.get('summary', {}).get('current', 0) if isinstance(ledger.get('summary'), dict) else 0}",
                f"- stale: {ledger.get('summary', {}).get('stale', 0) if isinstance(ledger.get('summary'), dict) else 0}",
                f"- missing source: {ledger.get('summary', {}).get('missing_source', 0) if isinstance(ledger.get('summary'), dict) else 0}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    write_json(output_path / "artifact_lock_snapshot.json", lock)
    return WorkflowResult(True, f"I043 Wrote reviewer response binder: {output_path}", output_path)
