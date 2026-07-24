from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "snapshot_enclosure_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.2))
    colors = {1: "tab:red", 2: "tab:orange", 4: "tab:blue"}
    markers = {"left": "o", "right": "s"}
    for rank in (1, 2, 4):
        selected = [row for row in rows if row["rank"] == rank]
        for side in ("left", "right"):
            group = [row for row in selected if row["side"] == side]
            axes[0, 0].loglog(
                [row["sigma"] for row in group],
                [row["certified_operator_snapshot_radius"] for row in group],
                marker=markers[side], color=colors[rank], linestyle="-" if side == "left" else "--",
                label=f"rank {rank}, {side}",
            )
    axes[0, 0].invert_xaxis()
    axes[0, 0].set_xlabel(r"scale $\sigma$")
    axes[0, 0].set_ylabel("Arb-certified operator radius")
    axes[0, 0].set_title("Normalized snapshot enclosure by rank")
    axes[0, 0].grid(True, which="both", alpha=0.2)
    axes[0, 0].legend(frameon=False, fontsize=7, ncol=2)

    rank4 = [row for row in rows if row["rank"] == 4]
    axes[0, 1].loglog(
        [row["certified_operator_snapshot_radius"] for row in rank4],
        [row["direct_proxy_distances"]["operator"] for row in rank4],
        "o", color="tab:blue",
    )
    grid = np.logspace(-9, -3, 300)
    axes[0, 1].plot(grid, grid, color="black", linestyle=":", label="universal bound")
    axes[0, 1].plot(grid, grid**2, color="tab:green", linestyle="--", label="orthogonal-SVD scale")
    axes[0, 1].set_xlabel("certified universal radius")
    axes[0, 1].set_ylabel("direct float proxy distance")
    axes[0, 1].set_title("Rank-four proxy exhibits quadratic cancellation")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(True, which="both", alpha=0.2)

    delta = np.linspace(0.0, 0.999, 400)
    axes[1, 0].plot(delta, delta, label="operator", color="tab:blue")
    axes[1, 0].plot(delta, np.sqrt(2.0) * delta, label="Frobenius", color="tab:orange")
    axes[1, 0].plot(delta, 2.0 * delta, label="trace", color="tab:red")
    axes[1, 0].axvline(1.0, color="black", linestyle=":")
    axes[1, 0].set_xlabel(r"relative state radius $\delta$")
    axes[1, 0].set_ylabel("sharp snapshot radius")
    axes[1, 0].set_title("All constants are attained by one-row witnesses")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, alpha=0.2)

    labels = ["rank 1", "rank 2", "rank 4"]
    cutoffs = [1e-1, 1e-2, 1e-3]
    counts = []
    for rank, cutoff in zip((1, 2, 4), cutoffs):
        group = [row for row in rows if row["rank"] == rank]
        counts.append(sum(row["certified_operator_snapshot_radius"] < cutoff for row in group))
    axes[1, 1].bar(labels, counts, color=["tab:red", "tab:orange", "tab:blue"])
    axes[1, 1].axhline(10, color="black", linestyle=":")
    axes[1, 1].set_ylim(0, 10.8)
    axes[1, 1].set_ylabel("channels passing rank-dependent gate / 10")
    axes[1, 1].set_title(r"All rank-four balls are below $10^{-3}$")
    axes[1, 1].grid(True, axis="y", alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "normalized_snapshot_enclosure"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

