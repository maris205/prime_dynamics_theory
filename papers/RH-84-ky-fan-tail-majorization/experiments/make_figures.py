"""Make the RH-84 Ky Fan tail-majorization figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "tail_majorization_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["tail_majorization_ratio"] for channel in channels], marker="o", label=side)
    ax.axhline(0.015, color="black", linestyle="--", label="1.5% gate")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("physical / endpoint tail")
    ax.set_title("(a) Clock-rank tail majorization")
    ax.grid(alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["physical_relative_tail_upper"] for channel in channels], marker="o", label=side)
    ax.axvline(0.01, color="gray", linestyle=":", label="interval / stress boundary")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("relative physical tail")
    ax.set_title("(b) Five interval scales plus two stress scales")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    finest = rows[-1]
    for side in ("left", "right"):
        channel = next(channel for channel in finest["channels"] if channel["side"] == side)
        ax.semilogy([item["offset"] for item in channel["offset_comparison"]], [item["relative_postblock_tail"] for item in channel["offset_comparison"]], marker="o", label=side)
    ax.set_xlabel(r"rank offset beyond $\lceil H_\sigma\rceil$")
    ax.set_ylabel("relative postblock tail")
    ax.set_title(r"(c) Offset gain at $\sigma=0.0025$")
    ax.grid(alpha=0.25)
    ax.legend()

    ax = axes[1, 1]
    ax.step(sigma, [row["clock_rank"] for row in rows], where="mid", label="clock rank")
    ax.plot(sigma, [row["fine_dimension"] for row in rows], marker="o", label="fine dimension")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("count")
    ax.set_title("(d) Log rank versus ambient dimension")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.tight_layout()
    output = ROOT / "figures" / "ky_fan_tail_majorization"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
