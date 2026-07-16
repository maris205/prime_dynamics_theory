"""Render the compact RH-32 certificate ledger figure."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with (ROOT / "results" / "composition_summary.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    labels = [r"$10^{-2}$", r"$4\times10^{-3}$", r"$2\times10^{-3}$"]
    x = np.arange(len(rows))

    figure, axes = plt.subplots(1, 2, figsize=(11.2, 4.35))
    first = axes[0]
    first.semilogy(
        x,
        [float(row["lifted_inverse_upper"]) for row in rows],
        "o-",
        linewidth=1.8,
        label=r"RH-31 $K$",
        color="#3b6ea8",
    )
    first.semilogy(
        x,
        [float(row["center_inverse_upper"]) for row in rows],
        "s-",
        linewidth=1.8,
        label=r"RH-29 $\Phi(K)$",
        color="#7b4fa3",
    )
    first.semilogy(
        x,
        [float(row["selected_arc_inverse_upper"]) for row in rows],
        "^-",
        linewidth=1.8,
        label="selected-arc bound",
        color="#ce6d2d",
    )
    first.semilogy(
        x,
        [float(row["selected_arc_budget_lower"]) for row in rows],
        "D--",
        linewidth=1.6,
        label="RH-28 budget",
        color="#2c8c5a",
    )
    first.set_xticks(x, labels)
    first.set_xlabel(r"noise scale $\sigma$")
    first.set_ylabel("certified norm bound / admissible budget")
    first.set_title("Selected-arc composition")
    first.grid(True, which="both", alpha=0.24)
    first.legend(frameon=False, fontsize=8.7, loc="best")

    second = axes[1]
    matrix = np.asarray(
        [
            [1, 1, 1],
            [1, 1, 1],
            [0, 0, 0],
            [0, 0, 0],
        ],
        dtype=float,
    )
    second.imshow(
        matrix,
        cmap=ListedColormap(["#f4c7c3", "#b7dfc5"]),
        vmin=0,
        vmax=1,
        aspect="auto",
    )
    row_labels = [
        "projected zero/pole count",
        "selected-arc resolvent",
        "full-contour resolvent",
        "complement interior poles",
    ]
    second.set_xticks(x, labels)
    second.set_yticks(np.arange(4), row_labels)
    second.set_title("End-to-end gate ledger")
    for row_index in range(4):
        for column_index, row in enumerate(rows):
            if row_index == 1:
                annotation = (
                    f"certified\n1/{int(row['accepted_arc_count'])} arcs"
                )
            else:
                annotation = "certified" if matrix[row_index, column_index] else "open"
            second.text(
                column_index,
                row_index,
                annotation,
                ha="center",
                va="center",
                fontsize=8.4,
                color="#193a2a" if matrix[row_index, column_index] else "#7b2821",
            )
    second.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    second.set_yticks(np.arange(-0.5, 4, 1), minor=True)
    second.grid(which="minor", color="white", linewidth=2)
    second.tick_params(which="minor", bottom=False, left=False)

    figure.tight_layout(w_pad=2.4)
    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    figure.savefig(output / "end_to_end_ledger.pdf", bbox_inches="tight")
    figure.savefig(output / "end_to_end_ledger.png", dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
