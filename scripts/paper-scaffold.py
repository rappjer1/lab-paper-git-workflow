#!/usr/bin/env python
"""Run paper_scaffold from a source checkout without installing it."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_scaffold.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
