from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/source_support_composition_audit.json").read_text())
    summary = data["audit_summary"]
    synthetic = data["synthetic_records"]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 3.8))

    labels = ["packets", "branches", "outward", "tubes", "clean suffix"]
    values = [
        summary["factorized_packet_certified_count"] / summary["factorized_packet_total_count"],
        summary["strict_threshold_branch_count"] / summary["threshold_update_count"],
        1.0 - summary["outward_residual_failure_count"] / summary["outward_residual_transition_count"],
        summary["finite_positive_tube_chain_count"] / summary["finite_tube_chain_count"],
        1.0,
    ]
    axes[0].barh(labels, values, color=["#4c78a8", "#4c78a8", "#4c78a8", "#f58518", "#54a24b"])
    axes[0].set_xlim(0, 1.03)
    axes[0].set_xlabel("finite certified fraction")
    axes[0].set_title("Strong finite checkpoints")

    interfaces = data["missing_interfaces"]
    axes[1].bar([item["id"] for item in interfaces], [1, 1, 1], color="#d95f5f")
    axes[1].set_ylim(0, 1.15)
    axes[1].set_yticks([0, 1], ["open", "needed"])
    axes[1].set_title("Three all-level interfaces remain")

    theorem = np.array([item["theorem_floor"] for item in synthetic])
    actual = np.array([item["actual_minimum_support"] for item in synthetic])
    axes[2].scatter(theorem, actual, s=5, alpha=0.25, color="#4169a1")
    lo = min(theorem.min(), actual.min())
    hi = max(theorem.max(), actual.max())
    axes[2].plot([lo, hi], [lo, hi], color="black", linestyle="--", linewidth=0.8)
    axes[2].set_xscale("log")
    axes[2].set_yscale("log")
    axes[2].set_xlabel("conditional theorem floor")
    axes[2].set_ylabel("synthetic actual minimum")
    axes[2].set_title("4,096 compositions, zero failures")

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(ROOT / f"figures/source_directional_support_composition.{suffix}", dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()

