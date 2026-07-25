from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/congruence_audit.json").read_text())
    rows = data["rows"]
    labels = [f"{row['sigma']:g}{row['side'][0].upper()}" for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 7.2), constrained_layout=True)

    ax = axes[0, 0]
    offset = 0
    for row, label in zip(rows, labels):
        values = [item["correlated_pulled_base_lower"] for item in row["transitions"]]
        x = np.arange(len(values)) + offset
        ax.semilogy(x, values, ".-", lw=1, label=label)
        offset += len(values) + 1
    ax.axhline(1e-8, color="black", ls="--", lw=1)
    ax.set_title("A. Every correlated transported base stays positive")
    ax.set_ylabel("outward normalized-base lower")
    ax.set_xlabel("concatenated transition index")

    ax = axes[0, 1]
    counts = [sum(item["independent_positive_definite"] for item in row["transitions"]) for row in rows]
    totals = [len(row["transitions"]) for row in rows]
    ax.bar(np.arange(len(rows)), totals, color="#d9d9d9", label="all transitions")
    ax.bar(np.arange(len(rows)), counts, color="#4c72b0", label="independent-ball positive")
    ax.set_xticks(np.arange(len(rows)), labels, rotation=45, ha="right")
    ax.set_ylabel("transition count")
    ax.set_title("B. Decoupling loses 52 positivity certificates")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    ratios = [
        item["independent_pullback_radius"] / item["nominal_pullback_min"]
        for row in rows for item in row["transitions"]
    ]
    ax.semilogy(np.arange(len(ratios)), ratios, ".", color="#c44e52")
    ax.axhline(1.0, color="black", ls="--", lw=1)
    ax.set_xlabel("concatenated transition index")
    ax.set_ylabel("independent radius / nominal minimum")
    ax.set_title("C. The independent positivity wall is severe")

    ax = axes[1, 1]
    overlap = [item["robust_overlap_lower"] for row in rows for item in row["transitions"]]
    bases = [item["correlated_pulled_base_lower"] for row in rows for item in row["transitions"]]
    colors = [item["independent_positive_definite"] for row in rows for item in row["transitions"]]
    ax.loglog(overlap, bases, "o", ms=4, alpha=0.75, color="#55a868")
    ax.set_xlabel("robust overlap lower")
    ax.set_ylabel("correlated transported-base lower")
    ax.set_title("D. Overlap costs one factor, not a squared radius")

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.18)
    output = ROOT / "figures/congruence_covariant_reset_transport"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
