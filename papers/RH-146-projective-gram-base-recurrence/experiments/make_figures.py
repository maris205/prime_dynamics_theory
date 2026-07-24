from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/projective_gram_audit.json").read_text())
    rows = data["rows"]
    sigmas = sorted({row["sigma"] for row in rows}, reverse=True)
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8))

    distributions = [
        [step["projective_distance"] for row in rows if row["sigma"] == sigma for step in row["steps"]]
        for sigma in sigmas
    ]
    axes[0].boxplot(distributions, tick_labels=[str(sigma) for sigma in sigmas], showfliers=False)
    axes[0].set_xlabel(r"anchor $\sigma$")
    axes[0].set_ylabel("projective step distance")
    axes[0].set_title("Shape increments stay macroscopic")

    for side, marker in (("left", "o"), ("right", "s")):
        selected = [row for row in rows if row["side"] == side and row["threshold"] == 1e-8]
        axes[1].plot([row["transition_count"] for row in selected], [row["total_projective_variation"] for row in selected], marker=marker, label=side)
    axes[1].set_xlabel("transitions in chain")
    axes[1].set_ylabel("total projective variation")
    axes[1].set_title("Variation does not stabilize")
    axes[1].legend(frameon=False)

    exact = np.array([row["terminal_base"] for row in rows])
    lower = np.array([row["terminal_projective_lower"] for row in rows])
    axes[2].scatter(exact, lower, c=[row["sigma"] for row in rows], cmap="viridis", s=30)
    lo = min(exact.min(), lower.min())
    hi = max(exact.max(), lower.max())
    axes[2].plot([lo, hi], [lo, hi], color="black", linewidth=0.8, linestyle="--")
    axes[2].set_xscale("log")
    axes[2].set_yscale("log")
    axes[2].set_xlabel("exact terminal base")
    axes[2].set_ylabel("projective product lower")
    axes[2].set_title("Universal product is highly lossy")

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(ROOT / f"figures/projective_gram_base_recurrence.{suffix}", dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()

