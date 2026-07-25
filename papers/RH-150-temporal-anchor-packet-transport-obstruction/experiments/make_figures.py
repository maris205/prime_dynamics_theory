from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/packet_transport_audit.json").read_text())
    channels = [
        (row["sigma"], channel)
        for row in data["rows"]
        for channel in row["channels"]
    ]
    labels = [f"{sigma:g}{channel['side'][0].upper()}" for sigma, channel in channels]
    x = np.arange(len(channels))
    colors = {"branch": "#c44e52", "direction_gap": "#8172b2", "ritz_gap": "#4c72b0"}

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.3), constrained_layout=True)
    ax = axes[0, 0]
    transferred = [channel["anchor_compatibility"]["transferred_radius"] for _, channel in channels]
    bars = ax.bar(x, transferred, color=["#dd8452" if channel["clock_rank"] == 4 else "#937860" for _, channel in channels])
    for index, (_, channel) in enumerate(channels):
        text = "time" if channel["clock_rank"] == 4 else f"r4→r{channel['clock_rank']}"
        ax.text(index, 0.52, text, ha="center", va="center", rotation=90, fontsize=8, color="white", fontweight="bold")
    ax.axhline(1.0, color="black", lw=1.0)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("transferred projector radius")
    ax.set_title("A. RH-142 anchors are unusable at RH-96 time zero")
    ax.set_xticks(x, labels, rotation=45, ha="right")

    ax = axes[0, 1]
    seed = [channel["transport"]["source_seed"]["projector_radius"] for _, channel in channels]
    gap = [channel["transport"]["source_seed"]["gap_lower"] for _, channel in channels]
    ax.semilogy(x, seed, "o-", color="#55a868", lw=1.8, label="source projector radius")
    ax.semilogy(x, gap, "s--", color="#4c72b0", lw=1.4, label="source spectral gap")
    ax.set_ylabel("outward value")
    ax.set_title("B. Correct time-zero clock-rank seeds certify 10/10")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    prefix = [channel["transport"]["certified_prefix_updates"] for _, channel in channels]
    gates = [channel["transport"]["first_failure_gate"] for _, channel in channels]
    ax.bar(x, prefix, color=[colors[gate] for gate in gates])
    for index, gate in enumerate(gates):
        ax.text(index, prefix[index] + 0.08, "B" if gate == "branch" else "R", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylim(0, max(prefix) + 0.7)
    ax.set_ylabel("certified updates before stop")
    ax.set_title("C. Every universal chain stops by update three")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.text(0.01, 0.96, "B = branch wall, R = Ritz wall", transform=ax.transAxes, ha="left", va="top", fontsize=8)

    ax = axes[1, 1]
    ratios = []
    for _, channel in channels:
        step = channel["transport"]["steps"][-1]
        ratio = step["branch_radius_ratio"] if step["failure_gate"] == "branch" else step["ritz_gap_ratio"]
        ratios.append(ratio)
    ax.semilogy(x, ratios, "o", ms=7, color="#c44e52")
    ax.axhline(1.0, color="black", lw=1.1, ls="--")
    ax.set_ylabel("decisive radius / admissible radius")
    ax.set_title("D. Decisive failures remain outside their gates")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.grid(axis="y", which="both", alpha=0.2)

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
    output = ROOT / "figures/temporal_anchor_packet_transport"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
