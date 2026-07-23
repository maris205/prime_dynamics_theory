"""Create the RH-107 source-seeded quotient-support figure."""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "source_seeded_support_audit.json").read_text(encoding="utf-8"))
    records = data["thresholds"]
    sigmas = [item["sigma"] for item in records[0]["scale_records"]]
    labels = [f"$\\sigma={sigma:g}$" for sigma in sigmas]
    colors = ["tab:blue", "tab:orange", "tab:green"]

    def threshold_label(value: float) -> str:
        exponent = int(round(math.log10(value)))
        return rf"$\tau=10^{{{exponent}}}$"

    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.2))

    ax = axes[0]
    x = list(range(len(sigmas)))
    width = 0.24
    for offset, record, color in zip((-width, 0.0, width), records, colors):
        ax.bar(
            [value + offset for value in x],
            record["event_count_by_scale"],
            width=width,
            color=color,
            label=threshold_label(record["threshold"]),
        )
    ax.set_xticks(x, labels)
    ax.set_ylabel("weak-mode quotient events")
    ax.set_title("Support is confined to coarse scales")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)

    ax = axes[1]
    for record, color in zip(records, colors):
        minimums = [item["minimum_fourth_cross_ratio"] for item in record["scale_records"]]
        ax.semilogy(x, minimums, marker="o", linewidth=2.0, color=color, label=threshold_label(record["threshold"]))
        ax.axhline(record["threshold"], color=color, linestyle="--", linewidth=1.0, alpha=0.6)
    ax.set_xticks(x, labels)
    ax.set_ylabel(r"minimum $s_4/s_1$ over updates")
    ax.set_title(r"Fine-scale fourth mode clears the cutoff")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)

    fig.tight_layout()
    output = ROOT / "figures" / "source_seeded_quotient_support"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
