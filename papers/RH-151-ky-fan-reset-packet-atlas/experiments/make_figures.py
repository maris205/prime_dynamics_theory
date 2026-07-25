from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/reset_packet_audit.json").read_text())
    channels = [(row["sigma"], channel) for row in data["rows"] for channel in row["channels"]]
    labels = [f"{sigma:g}{channel['side'][0].upper()}" for sigma, channel in channels]
    snapshots = [item for _, channel in channels for item in channel["snapshots"]]

    fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.2), constrained_layout=True)
    ax = axes[0, 0]
    offset = 0
    for index, (sigma, channel) in enumerate(channels):
        values = [item["direct_reset_gap_ratio"] for item in channel["snapshots"]]
        times = np.arange(len(values)) + offset
        ax.semilogy(times, values, marker=".", lw=1.0, label=labels[index])
        offset += len(values) + 1
    ax.axhline(1.0, color="black", ls="--", lw=1)
    ax.set_title("A. All 130 direct reset gaps clear their balls")
    ax.set_ylabel("gap / twice matrix radius")
    ax.set_xlabel("concatenated snapshot index")

    ax = axes[0, 1]
    maxima = [max(item["direct_reset_projector_radius"] for item in channel["snapshots"]) for _, channel in channels]
    ax.semilogy(np.arange(len(channels)), maxima, "o-", color="#55a868")
    ax.set_xticks(np.arange(len(channels)), labels, rotation=45, ha="right")
    ax.set_ylabel("maximum reset projector radius")
    ax.set_title("B. Worst channel radius remains below 0.009")

    ax = axes[1, 0]
    actual = [max(item["recursive_actual_projector_distance"] for item in channel["snapshots"]) for _, channel in channels]
    bound = [max(item["recursive_ky_fan_operator_radius"] for item in channel["snapshots"]) for _, channel in channels]
    x = np.arange(len(channels))
    ax.plot(x, actual, "o-", label="recursive/global distance", color="#c44e52")
    ax.plot(x, bound, "s--", label="Ky--Fan outward bound", color="#4c72b0")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylim(-0.04, 1.05)
    ax.set_ylabel("operator projector distance")
    ax.set_title("C. Recursive packets can leave the global packet")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    summary = data["audit_summary"]
    names = ["direct reset", "actual Ky--Fan", "universal scalar"]
    counts = [
        summary["direct_reset_certificate_count"],
        summary["recursive_ky_fan_informative_count"],
        summary["universal_branch_free_informative_count"],
    ]
    ax.bar(names, counts, color=["#55a868", "#4c72b0", "#c44e52"])
    for index, value in enumerate(counts):
        ax.text(index, value + 2, str(value), ha="center", fontweight="bold")
    ax.set_ylim(0, 140)
    ax.set_ylabel("informative snapshots out of 130")
    ax.set_title("D. Independent resets avoid cumulative loss")
    ax.tick_params(axis="x", rotation=20)

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.18)
    output = ROOT / "figures/ky_fan_reset_packet_atlas"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
