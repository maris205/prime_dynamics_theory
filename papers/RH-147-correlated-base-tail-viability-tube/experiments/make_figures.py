from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/correlated_tube_audit.json").read_text())
    rows = data["rows"]
    positive = [row for row in rows if row["positive_tube"]]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8))

    betas = [row["maximal_common_tube_beta"] for row in rows]
    colors = [row["sigma"] for row in rows]
    axes[0].scatter(range(len(rows)), np.maximum(betas, 1e-60), c=colors, cmap="viridis", s=28)
    for beta, label in ((1e-10, r"$10^{-10}$"), (1e-8, r"$10^{-8}$"), (1e-6, r"$10^{-6}$"), (1e-4, r"$10^{-4}$")):
        axes[0].axhline(beta, color="gray", linewidth=0.6, linestyle="--")
    axes[0].set_yscale("log")
    axes[0].set_xlabel("frozen chain")
    axes[0].set_ylabel(r"maximal tube level $\beta$")
    axes[0].set_title("28 complete positive tubes")

    multipliers = [value for row in positive for value in row["local_support_multipliers"]]
    axes[1].hist(np.log10(multipliers), bins=28, color="#4169a1", alpha=0.85)
    axes[1].axvline(0.0, color="black", linewidth=0.8)
    axes[1].set_xlabel(r"$\log_{10}$ local support multiplier")
    axes[1].set_ylabel("count")
    axes[1].set_title("Losses and recoveries coexist")

    projective = np.array([row["projective_terminal_lower"] for row in positive])
    tube = np.array([row["maximal_common_tube_beta"] for row in positive])
    axes[2].scatter(projective, tube, c=[row["sigma"] for row in positive], cmap="viridis", s=30)
    lo = min(projective.min(), tube.min())
    hi = max(projective.max(), tube.max())
    axes[2].plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=0.8)
    axes[2].set_xscale("log")
    axes[2].set_yscale("log")
    axes[2].set_xlabel("RH-146 projective product")
    axes[2].set_ylabel("correlated tube floor")
    axes[2].set_title("Reanchoring restores 16--48 orders")

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(ROOT / f"figures/correlated_base_tail_tube.{suffix}", dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()

