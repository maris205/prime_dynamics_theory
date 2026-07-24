"""Create the RH-121 scale-edge tail-inflation figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "optimal_gauge_audit.json").read_text(encoding="utf-8"))
    pairs = data["pairs"]
    edges = [(0.16, 0.08), (0.08, 0.04), (0.04, 0.02), (0.02, 0.01)]
    labels = [".16→.08", ".08→.04", ".04→.02", ".02→.01"]
    groups = [[p for p in pairs if (p["source_sigma"], p["target_sigma"]) == edge] for edge in edges]
    fig, axes = plt.subplots(1, 2, figsize=(10.9, 4.35))
    rng = np.random.default_rng(121)
    for index, group in enumerate(groups):
        values = np.asarray([p["optimal_tail_factor"] for p in group])
        axes[0].scatter(index + rng.uniform(-0.16, 0.16, len(values)), np.log10(values), s=25, alpha=0.72)
    axes[0].axhline(0.0, color="black", lw=1.0, ls="--")
    axes[0].set_xticks(range(4), labels)
    axes[0].set_ylabel(r"$\log_{10} b_{\mathrm{opt}}$")
    axes[0].set_title("Optimal tail inflation by scale edge")
    axes[0].grid(True, axis="y", alpha=0.24)
    efficiencies = [[p["gamma_transfer_efficiency"] for p in group] for group in groups]
    axes[1].boxplot(efficiencies, tick_labels=labels, showfliers=True)
    axes[1].axhline(1.0, color="black", lw=1.0, ls="--")
    axes[1].set_ylabel(r"actual $\gamma'$ / optimal transferred upper")
    axes[1].set_title("Sharpness of the induced gamma bound")
    axes[1].grid(True, axis="y", alpha=0.24)
    fig.tight_layout()
    output = ROOT / "figures" / "optimal_gram_gauge_pairing"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

