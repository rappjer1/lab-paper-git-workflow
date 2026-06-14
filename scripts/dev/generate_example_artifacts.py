"""Generate deterministic tiny synthetic example artifacts."""

from __future__ import annotations

import argparse
import struct
import zlib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


PDF_TARGETS = {
    "examples/minimal_python_artifacts/outputs/example_metric_plot.pdf": "Minimal Python Artifact",
    "examples/dogfood/python_outputs_to_manuscript/input/outputs/summary_plot.pdf": "Dogfood Python Output",
    "examples/dogfood/existing_latex_cleanup/project/figures/summary_plot.pdf": "Dogfood LaTeX Figure",
    "examples/dogfood/messy_project_audit/project/outputs/figure_final.pdf": "Dogfood Final Figure",
    "examples/dogfood/messy_project_audit/project/outputs/figure_final2.pdf": "Dogfood Duplicate Figure",
}

PNG_TARGETS = {
    "examples/messy_project_archaeology/outputs/fig1_final.png": (46, 118, 182),
    "examples/messy_project_archaeology/outputs/fig1_final2.png": (67, 154, 112),
    "examples/messy_project_archaeology/overleaf_export/figures/fig1_final.png": (156, 117, 95),
}


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf(title: str) -> bytes:
    content = f"BT /F1 14 Tf 72 720 Td ({escape_pdf_text(title)}) Tj 0 -24 Td (Synthetic example artifact.) Tj ET"
    stream = content.encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    chunks = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(sum(len(chunk) for chunk in chunks))
        chunks.append(f"{index} 0 obj\n".encode("ascii"))
        chunks.append(obj)
        chunks.append(b"\nendobj\n")
    xref_offset = sum(len(chunk) for chunk in chunks)
    chunks.append(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    chunks.append(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        chunks.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    chunks.append(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return b"".join(chunks)


def generate_pdf_targets(repo_root: Path = REPO_ROOT) -> list[Path]:
    written: list[Path] = []
    for rel, title in PDF_TARGETS.items():
        path = repo_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(build_pdf(title))
        written.append(path)
    return written


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def build_png(color: tuple[int, int, int]) -> bytes:
    width = 8
    height = 8
    row = b"\x00" + bytes(color) * width
    raw = row * height
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_chunk(b"IHDR", header),
            png_chunk(b"IDAT", zlib.compress(raw)),
            png_chunk(b"IEND", b""),
        ]
    )


def generate_png_targets(repo_root: Path = REPO_ROOT) -> list[Path]:
    written: list[Path] = []
    for rel, color in PNG_TARGETS.items():
        path = repo_root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(build_png(color))
        written.append(path)
    return written


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate deterministic tiny synthetic example artifacts.")
    parser.add_argument("--check", action="store_true", help="Report target files without writing them.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.check:
        for rel in list(PDF_TARGETS) + list(PNG_TARGETS):
            print(rel)
        return 0
    written = generate_pdf_targets() + generate_png_targets()
    print("Generated example artifacts:")
    for path in written:
        print(f"- {path.relative_to(REPO_ROOT).as_posix()} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
