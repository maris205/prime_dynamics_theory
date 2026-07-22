"""Make the RH-85 snapshot-packet figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "snapshot_packet_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["interval_relative_terminal_residual_upper"] for channel in channels], marker="o", label=side)
    ax.axhline(4.5e-6, color="black", linestyle="--", label="packet gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("relative terminal residual")
    ax.set_title("(a) 192-bit strict-prefix packet certificate"); ax.legend()

    ax = axes[0, 1]
    names = [("binary64_source_packet_relative_tail", "source"), ("binary64_unweighted_prefix_gram_relative_tail", "prefix Gram"), ("binary64_midpoint_packet_relative_tail", "two-thirds snapshot")]
    for key, label in names:
        values = [max(channel[key] for channel in row["channels"]) for row in rows]
        ax.semilogy(sigma, values, marker="o", label=label)
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("worst channel residual")
    ax.set_title("(b) Why temporal localization matters"); ax.legend(fontsize=8)

    ax = axes[1, 0]
    example = audit["prefix_gram_counterexample"]
    ax.semilogy([row["horizon"] for row in example], [1.0 - row["terminal_missed_relative"] for row in example], marker="o")
    ax.set_xlabel("horizon"); ax.set_ylabel("one minus missed relative energy")
    ax.set_title("(c) Explicit prefix-Gramian no-go"); ax.grid(alpha=0.25)

    ax = axes[1, 1]
    ax.step(sigma, [row["clock_rank"] for row in rows], where="mid", label="clock rank")
    ax.plot(sigma, [row["fine_dimension"] for row in rows], marker="o", label="fine dimension")
    ax.plot(sigma, [row["channels"][0]["packet_time"] for row in rows], marker="s", label="packet time")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("count")
    ax.set_title("(d) Prefix cost versus ambient size"); ax.legend(fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "midblock_snapshot_packets"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
