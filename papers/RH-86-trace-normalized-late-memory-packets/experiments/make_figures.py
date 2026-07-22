"""Make the RH-86 late-memory figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "late_memory_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["interval_relative_terminal_residual_upper"] for channel in channels], marker="o", label=side)
    ax.axhline(1.2e-5, color="black", linestyle="--", label="memory gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("relative terminal residual")
    ax.set_title("(a) 192-bit normalized-memory packet"); ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["unweighted_to_weighted_improvement_factor"] for channel in channels], marker="o", label=side)
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("unweighted / weighted residual")
    ax.set_title("(b) Gain from trace normalization and forgetting"); ax.legend()

    ax = axes[1, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["angle_perturbation_gap_ratio"] for channel in channels], marker="o", label=side)
    ax.axhline(1.0, color="black", linestyle="--", label="angle threshold")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("perturbation / packet gap")
    ax.set_title("(c) Davis--Kahan route is unusable"); ax.legend(fontsize=8)

    ax = axes[1, 1]
    current = [max(channel["binary64_terminal_point_packet_relative_tail"] for channel in row["channels"]) for row in rows]
    memory = [max(channel["binary64_terminal_weighted_packet_relative_tail"] for channel in row["channels"]) for row in rows]
    unweighted = [max(channel["binary64_terminal_unweighted_prefix_relative_tail"] for channel in row["channels"]) for row in rows]
    ax.semilogy(sigma, current, marker="o", label="point packet")
    ax.semilogy(sigma, memory, marker="s", label="late memory")
    ax.semilogy(sigma, unweighted, marker="^", label="unweighted prefix")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("worst channel residual")
    ax.set_title("(d) Energy, not subspace angle"); ax.legend(fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "trace_normalized_late_memory"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
