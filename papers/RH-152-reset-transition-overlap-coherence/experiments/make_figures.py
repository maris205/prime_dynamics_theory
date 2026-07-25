from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/overlap_audit.json").read_text())
    rows = data["rows"]
    labels = [f"{row['sigma']:g}{row['side'][0].upper()}" for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 7.1), constrained_layout=True)

    ax = axes[0, 0]
    offset = 0
    for row, label in zip(rows, labels):
        values = [item["robust_lower"] for item in row["transitions"]]
        x = np.arange(len(values)) + offset
        ax.semilogy(x, values, ".-", lw=1, label=label)
        offset += len(values) + 1
    ax.axhline(1e-3, color="black", ls="--", lw=1)
    ax.set_title("A. All 120 robust overlap maps stay invertible")
    ax.set_ylabel("smallest overlap singular value")
    ax.set_xlabel("concatenated transition index")

    ax = axes[0, 1]
    inverse = [max(item["inverse_overlap_upper"] for item in row["transitions"]) for row in rows]
    ax.semilogy(np.arange(len(rows)), inverse, "o-", color="#c44e52")
    ax.set_xticks(np.arange(len(rows)), labels, rotation=45, ha="right")
    ax.set_ylabel("maximum inverse overlap upper")
    ax.set_title("B. Fine right channel carries a conditioning spike")

    ax = axes[1, 0]
    polar = [max(item["polar_radius"] for item in row["transitions"]) for row in rows]
    ax.semilogy(np.arange(len(rows)), polar, "s-", color="#4c72b0")
    ax.set_xticks(np.arange(len(rows)), labels, rotation=45, ha="right")
    ax.set_ylabel("polar transition radius")
    ax.set_title("C. Canonical transition rotations remain stable")

    ax = axes[1, 1]
    drawdown = [sum(-np.log(item["robust_lower"]) for item in row["transitions"]) for row in rows]
    ax.bar(np.arange(len(rows)), drawdown, color="#8172b2")
    ax.set_xticks(np.arange(len(rows)), labels, rotation=45, ha="right")
    ax.set_ylabel("cumulative log inverse overlap")
    ax.set_title("D. Finite coherence is strongly nonuniform")
    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.18)
    output = ROOT / "figures/reset_transition_overlap_coherence"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
