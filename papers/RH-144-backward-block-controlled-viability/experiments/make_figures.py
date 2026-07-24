from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "backward_viability_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.2))
    for row in rows:
        color = "tab:red" if not row["viable_from_zero"] else "tab:blue"
        alpha = 0.9 if not row["viable_from_zero"] else 0.18
        axes[0, 0].plot(range(len(row["backward_radii"])), row["backward_radii"], color=color, alpha=alpha)
    axes[0, 0].set_xlabel("time index")
    axes[0, 0].set_ylabel("backward viability radius")
    axes[0, 0].set_title("Two kernels collapse before an unavoidable coarse floor")
    axes[0, 0].grid(True, alpha=0.2)

    labels = ["viable", "obstructed", "full unit start"]
    summary = data["audit_summary"]
    axes[0, 1].bar(labels, [summary["viable_chain_count"], summary["obstructed_chain_count"], summary["full_unit_start_radius_count"]], color=["tab:blue", "tab:red", "tab:green"])
    axes[0, 1].set_ylabel("chains / 30")
    axes[0, 1].set_title("Backward and forward finite classifications agree")
    axes[0, 1].grid(True, axis="y", alpha=0.2)

    viable = [row for row in rows if row["viable_from_zero"]]
    by_scale = sorted({row["sigma"] for row in viable}, reverse=True)
    minima = [min(row["minimum_positive_backward_radius"] for row in viable if row["sigma"] == sigma) for sigma in by_scale]
    axes[1, 0].semilogy([str(value) for value in by_scale], minima, "o-", color="tab:purple")
    axes[1, 0].set_xlabel(r"scale $\sigma$")
    axes[1, 0].set_ylabel("minimum positive reset radius")
    axes[1, 0].set_title("Safe blocks can contain narrow interior reset gates")
    axes[1, 0].grid(True, which="both", alpha=0.2)

    obstructed = [row for row in rows if not row["viable_from_zero"]]
    x = np.arange(len(obstructed))
    axes[1, 1].bar(x, [row["obstruction_minimum_floor"] for row in obstructed], color="tab:red", label="least control floor")
    axes[1, 1].bar(x, [row["obstruction_target_radius"] for row in obstructed], color="tab:gray", alpha=0.6, label="required target radius")
    axes[1, 1].axhline(1.0, color="black", linestyle=":")
    axes[1, 1].set_xticks(x, [f"{row['threshold']:.0e}" for row in obstructed])
    axes[1, 1].set_ylabel("squared-tail envelope")
    axes[1, 1].set_title("Birth floor alone exceeds the support wall")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(True, axis="y", alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "backward_block_viability"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

