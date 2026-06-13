"""Generate small example artifacts for Paper Scaffold demos."""

from __future__ import annotations

from pathlib import Path
import csv

import matplotlib.pyplot as plt


def main() -> None:
    root = Path(__file__).resolve().parent
    outputs = root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)

    x = [1, 2, 3, 4, 5]
    y = [0.42, 0.55, 0.61, 0.70, 0.76]

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y, marker="o", color="#2458a6")
    ax.set_xlabel("Experiment")
    ax.set_ylabel("Example metric")
    ax.set_title("Example Metric Plot")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(outputs / "example_metric_plot.pdf", bbox_inches="tight")
    fig.savefig(outputs / "example_metric_plot.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    rows = [
        {"model": "baseline", "metric": "0.55"},
        {"model": "candidate", "metric": "0.76"},
    ]
    csv_path = outputs / "example_summary_table.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["model", "metric"])
        writer.writeheader()
        writer.writerows(rows)

    table = (
        "\\begin{tabular}{lr}\n"
        "\\hline\n"
        "Model & Metric \\\\\n"
        "\\hline\n"
        "Baseline & 0.55 \\\\\n"
        "Candidate & 0.76 \\\\\n"
        "\\hline\n"
        "\\end{tabular}\n"
    )
    (outputs / "example_table.tex").write_text(table, encoding="utf-8")


if __name__ == "__main__":
    main()
