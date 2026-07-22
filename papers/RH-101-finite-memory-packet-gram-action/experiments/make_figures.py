"""Create the RH-101 finite-memory audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "finite_memory_gram_audit.json"


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    depths = payload["depths"]
    channels = [channel for row in payload["rows"] for channel in row["channels"]]
    summary = payload["audit_summary"]["depth_summary"]

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.1))
    ax = axes[0]
    for channel in channels:
        values = [channel["depth_chains"][str(depth)]["interval_endpoint_to_reference_upper"] for depth in depths]
        ax.plot(depths, values, marker="o", linewidth=1.0, markersize=3.2, alpha=0.7)
    worst = [summary[str(depth)]["maximum_endpoint_to_reference_ratio"] for depth in depths]
    ax.plot(depths, worst, color="black", marker="s", linewidth=2.2, markersize=4.2, label="worst channel")
    ax.axhline(payload["endpoint_ratio_target"], color="tab:red", linestyle="--", linewidth=1.4, label="1.01 gate")
    ax.set_yscale("log")
    ax.set_xlabel("retained memory depth $m$")
    ax.set_ylabel("endpoint / leading-packet tail")
    ax.set_title("Recursive endpoint audit")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    actual = [summary[str(depth)]["maximum_action_error"] for depth in depths]
    ranks = [channel["clock_rank"] for channel in channels]
    eta = payload["eta"]
    bound = [eta**depth * np.sqrt(max(ranks)) / (1.0 - eta) for depth in depths]
    ax.semilogy(depths, bound, color="tab:orange", marker="s", linewidth=2.0, label="uniform theorem bound")
    ax.semilogy(depths, actual, color="tab:blue", marker="o", linewidth=2.0, label="largest discarded action")
    ax.set_xlabel("retained memory depth $m$")
    ax.set_ylabel("Frobenius norm")
    ax.set_title("Geometric action tail")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "finite_memory_packet_gram_action"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
