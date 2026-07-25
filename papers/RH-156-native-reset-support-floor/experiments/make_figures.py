from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/support_audit.json").read_text())
    rows = data["rows"]
    labels = [f"{row['sigma']:g}{row['side'][0].upper()}" for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 7.1), constrained_layout=True)

    ax = axes[0, 0]
    offset = 0
    for row, label in zip(rows, labels):
        values = [item["support_lower"] for item in row["transitions"]]
        x = np.arange(len(values)) + offset
        ax.semilogy(x, values, ".-", lw=1, label=label)
        offset += len(values) + 1
    ax.axhline(1e-8, color="black", ls="--", lw=1)
    ax.set_title("A. All 120 native reset support lowers are positive")
    ax.set_ylabel("support lower")
    ax.set_xlabel("concatenated transition index")

    ax = axes[0, 1]
    bases = [item["recent_base_lower"] for row in rows for item in row["transitions"]]
    factors = [item["tail_factor"] for row in rows for item in row["transitions"]]
    ax.loglog(bases, factors, "o", ms=4, alpha=0.7, color="#4c72b0")
    ax.set_xlabel("transported recent-base lower")
    ax.set_ylabel("tail support factor")
    ax.set_title("B. Base thinning and tail loss are distinct")

    ax = axes[1, 0]
    full_min = [min(item["support_lower"] for item in row["transitions"]) for row in rows]
    half_min = [min(item["support_lower"] for item in row["transitions"] if item["in_half_suffix"]) for row in rows]
    x = np.arange(len(rows))
    ax.semilogy(x - 0.12, full_min, "o", label="full chain", color="#c44e52")
    ax.semilogy(x + 0.12, half_min, "s", label="terminal half", color="#55a868")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("per-channel support floor")
    ax.set_title("C. Delayed conditioning preserves the support floor")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    thresholds = [1e-8, 1e-6, 1e-4]
    values = [sum(item["support_lower"] >= threshold for row in rows for item in row["transitions"]) for threshold in thresholds]
    ax.bar([r"$10^{-8}$", r"$10^{-6}$", r"$10^{-4}$"], values, color=["#55a868", "#4c72b0", "#8172b2"])
    for index, value in enumerate(values):
        ax.text(index, value + 2, str(value), ha="center", fontweight="bold")
    ax.set_ylim(0, 130)
    ax.set_ylabel("transitions above threshold")
    ax.set_title("D. The common finite floor has substantial margin")

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.18)
    output = ROOT / "figures/native_reset_support_floor"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
