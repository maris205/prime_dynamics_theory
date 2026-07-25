from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/suffix_audit.json").read_text())
    frontier = data["frontier"]
    half = data["half_suffix"]
    full = data["full_atlas"]
    labels = [f"{item['sigma']:g}{item['side'][0].upper()}" for item in half["channels"]]
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 7.1), constrained_layout=True)

    fractions = [item["retained_fraction"] for item in frontier]
    ax = axes[0, 0]
    ax.semilogy(fractions, [item["common_overlap_floor"] for item in frontier], "o-", color="#4c72b0")
    ax.axvline(0.5, color="black", ls="--", lw=1)
    ax.set_xlabel("required terminal retention fraction")
    ax.set_ylabel("sharp common overlap floor")
    ax.set_title("A. Retention--conditioning frontier")

    ax = axes[0, 1]
    ax.semilogy(fractions, [item["common_inverse_overlap_upper"] for item in frontier], "o-", color="#c44e52")
    ax.axvline(0.5, color="black", ls="--", lw=1)
    ax.set_xlabel("required terminal retention fraction")
    ax.set_ylabel("common inverse-overlap upper")
    ax.set_title("B. Half-horizon delay removes the large spike")

    ax = axes[1, 0]
    ax.plot(fractions, [item["maximum_chain_log_inverse_drawdown"] for item in frontier], "o-", color="#8172b2")
    ax.axvline(0.5, color="black", ls="--", lw=1)
    ax.set_xlabel("required terminal retention fraction")
    ax.set_ylabel("maximum chain log drawdown")
    ax.set_title("C. Cumulative conditioning also improves")

    ax = axes[1, 1]
    x = np.arange(len(labels))
    full_floor = [item["overlap_floor"] for item in full["channels"]]
    half_floor = [item["overlap_floor"] for item in half["channels"]]
    width = 0.38
    ax.semilogy(x - width / 2, full_floor, "o", label="full atlas", color="#c44e52")
    ax.semilogy(x + width / 2, half_floor, "s", label="terminal half", color="#55a868")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("per-channel overlap floor")
    ax.set_title("D. The gain is concentrated in finite births")
    ax.legend(frameon=False, fontsize=8)

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.18)
    output = ROOT / "figures/half_horizon_delayed_reset_suffix"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
