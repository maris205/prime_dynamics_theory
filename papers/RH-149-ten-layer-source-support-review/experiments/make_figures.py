from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/ten_layer_source_support_review.json").read_text())
    summary = data["audit_summary"]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8))

    labels = ["packets", "branches", "outward", "tubes", "clean suffix"]
    numerators = [10, 360, 330, 28, 18]
    denominators = [10, 360, 330, 30, 18]
    axes[0].barh(labels, np.array(numerators) / np.array(denominators), color=["#4c78a8"] * 3 + ["#f58518", "#54a24b"])
    axes[0].set_xlim(0, 1.03)
    axes[0].set_xlabel("finite certified fraction")
    axes[0].set_title("Ten-layer finite progression")

    gains = [
        summary["minimum_correlated_reanchoring_gain_orders"],
        summary["median_correlated_reanchoring_gain_orders"],
        summary["maximum_correlated_reanchoring_gain_orders"],
    ]
    axes[1].bar(["min", "median", "max"], gains, color="#4169a1")
    axes[1].set_ylabel("orders recovered over projective product")
    axes[1].set_title("Why the correlated route is primary")

    priorities = data["priority_ranking"]
    axes[2].barh([item["interface"] for item in reversed(priorities)], [item["priority_score"] for item in reversed(priorities)], color="#d95f5f")
    axes[2].set_xlim(0, 16)
    axes[2].set_xlabel("planning score (0--15)")
    axes[2].set_title("Next-interface priority")

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(ROOT / f"figures/ten_layer_source_support_review.{suffix}", dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()

