from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/memory_pair_audit.json").read_text())
    rows = data["rows"]
    labels = [f"{row['sigma']:g}{row['side'][0].upper()}" for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 7.1), constrained_layout=True)

    ax = axes[0, 0]
    offset = 0
    for row, label in zip(rows, labels):
        values = [item["recent_memory_tail_ratio_upper"] for item in row["snapshots"]]
        x = np.arange(len(values)) + offset
        ax.semilogy(x, np.maximum(values, 1e-18), ".-", lw=1, label=label)
        offset += len(values) + 1
    ax.axhline(1.0, color="black", ls="--", lw=1)
    ax.set_title("A. All 130 native recent/tail ratios are subunit")
    ax.set_ylabel("outward recent-tail ratio upper")
    ax.set_xlabel("concatenated snapshot index")

    ax = axes[0, 1]
    maxima = [max(item["recent_memory_tail_ratio_upper"] for item in row["snapshots"]) for row in rows]
    ax.semilogy(np.arange(len(rows)), np.maximum(maxima, 1e-18), "o-", color="#c44e52")
    ax.set_xticks(np.arange(len(rows)), labels, rotation=45, ha="right")
    ax.set_ylabel("maximum ratio upper")
    ax.set_title("B. The finest left packet is the certified wall")

    ax = axes[1, 0]
    margins = [
        item["selected_eigenvalue_to_twice_tail_margin"]
        for row in rows for item in row["snapshots"] if item["tail_active"]
    ]
    ax.semilogy(np.arange(len(margins)), margins, ".", color="#55a868")
    ax.axhline(1.0, color="black", ls="--", lw=1)
    ax.set_xlabel("tail-active snapshot index")
    ax.set_ylabel("selected eigenvalue / twice tail mass")
    ax.set_title("C. Every sharp subunit gate clears")

    ax = axes[1, 1]
    certified = [item["recent_memory_tail_ratio_upper"] for row in rows for item in row["snapshots"] if item["tail_active"]]
    nominal = [item["nominal_native_recent_tail_ratio"] for row in rows for item in row["snapshots"] if item["tail_active"]]
    ax.loglog(np.maximum(nominal, 1e-18), certified, "o", ms=4, alpha=0.7, color="#4c72b0")
    low = min(min(nominal), min(certified)); high = max(max(nominal), max(certified))
    ax.loglog([max(low, 1e-18), high], [max(low, 1e-18), high], "--", color="black", lw=1)
    ax.set_xlabel("nominal native ratio")
    ax.set_ylabel("outward universal upper")
    ax.set_title("D. The universal bound is conservative but usable")

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.18)
    output = ROOT / "figures/native_spectral_reset_memory_pair"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
