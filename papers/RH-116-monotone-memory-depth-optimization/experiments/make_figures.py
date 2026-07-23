"""Create the RH-116 depth-cost summary figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "memory_depth_audit.json").read_text(encoding="utf-8"))
    summaries = data["threshold_summary"]
    thresholds = ("1e-04", "1e-06", "1e-08")
    colors = ("tab:green", "tab:orange", "tab:blue")
    depths = np.arange(1, 7)

    fig, axes = plt.subplots(1, 2, figsize=(11.1, 4.35))
    ax = axes[0]
    width = 0.24
    for offset, (key, color) in enumerate(zip(thresholds, colors)):
        histogram = summaries[key]["depth_histogram"]
        counts = [int(histogram.get(str(depth), 0)) for depth in depths]
        ax.bar(depths + (offset - 1) * width, counts, width=width, color=color, alpha=0.8, label=rf"$\tau={float(key):.0e}$")
    ax.set_xlabel("first certifying memory depth")
    ax.set_ylabel("supported records")
    ax.set_title("Exact first-passage depth distribution")
    ax.set_xticks(depths)
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    envelope = [entry for entry in data["depth_envelope"] if entry["depth"] <= 6]
    x = np.asarray([entry["depth"] for entry in envelope])
    tail = np.asarray([entry["infinite_tail_bound"] for entry in envelope])
    cumulative = np.asarray([entry["certified_by_depth"] for entry in envelope]) / data["audit_summary"]["supported_update_count"]
    ax.semilogy(x, tail, marker="o", color="tab:red", label=r"tail budget $\eta^d/(1-\eta)$")
    ax.set_xlabel("memory depth")
    ax.set_ylabel("infinite geometric tail bound", color="tab:red")
    ax.tick_params(axis="y", labelcolor="tab:red")
    ax.grid(True, which="both", alpha=0.25)
    twin = ax.twinx()
    twin.plot(x, cumulative, marker="s", color="tab:purple", label="cumulative certified fraction")
    twin.set_ylim(0.0, 1.05)
    twin.set_ylabel("fraction of 322 supported records", color="tab:purple")
    twin.tick_params(axis="y", labelcolor="tab:purple")
    lines = ax.get_lines() + twin.get_lines()
    ax.legend(lines, [line.get_label() for line in lines], frameon=False, fontsize=8, loc="center right")
    ax.set_title("Tail decay and certificate saturation")

    fig.tight_layout()
    output = ROOT / "figures" / "monotone_memory_depth_optimization"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
