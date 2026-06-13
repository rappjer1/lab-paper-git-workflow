"""Word/docx conversion helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess


WORD_REVIEW_MESSAGE = (
    "Word conversion is a starting point. You must manually check equations, "
    "references, figures, tables, and captions."
)


@dataclass(frozen=True)
class ImportWordResult:
    ok: bool
    message: str
    command: list[str]
    output_path: Path | None = None


def build_pandoc_command(input_path: str | Path, output_path: str | Path, output_format: str = "latex") -> list[str]:
    command = ["pandoc", str(input_path)]
    if output_format == "markdown":
        command.extend(["-t", "markdown"])
    command.extend(["-o", str(output_path)])
    return command


def import_word(
    input_path: str | Path,
    output_path: str | Path,
    output_format: str = "latex",
    dry_run: bool = False,
    overwrite: bool = False,
) -> ImportWordResult:
    input_path = Path(input_path)
    output_path = Path(output_path)
    command = build_pandoc_command(input_path, output_path, output_format)

    if shutil.which("pandoc") is None:
        return ImportWordResult(
            ok=False,
            message=(
                "Pandoc is not installed or not on PATH. Install Pandoc, or use the manual workflow in "
                "docs/word_to_overleaf.md. "
                + WORD_REVIEW_MESSAGE
            ),
            command=command,
        )

    if not input_path.exists():
        return ImportWordResult(False, f"Input file does not exist: {input_path}", command)

    if output_path.exists() and not overwrite:
        return ImportWordResult(False, f"Output exists; pass --overwrite to replace it: {output_path}", command, output_path)

    if dry_run:
        return ImportWordResult(True, "Dry run only. Pandoc command was not executed.", command, output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "Pandoc failed without output."
        return ImportWordResult(False, detail, command, output_path)

    return ImportWordResult(True, f"Created {output_path}. {WORD_REVIEW_MESSAGE}", command, output_path)
