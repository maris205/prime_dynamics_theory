from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "metric_balanced_audit.json").read_text(encoding="utf-8"))
    tagged = [
        (row["sigma"], row["side"], step)
        for row in data["rows"]
        for step in row["steps"]
        if step["recurrent"]
    ]
    steps = [step for _, _, step in tagged]
    possible = [step for step in steps if step["orthogonal_contractivity_possible"]]
    impossible = [step for step in steps if not step["orthogonal_contractivity_possible"]]

    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.4))
    axes[0, 0].hist(
        [step["metric_decay_minimum"]["log10"] for step in steps],
        bins=35, color="tab:blue", alpha=0.82,
    )
    axes[0, 0].axvline(0.0, color="tab:red", linestyle="--", label=r"universal wall $A_*=1$")
    axes[0, 0].set_xlabel(r"$log_{10} A_*$, best possible orthogonal metric base")
    axes[0, 0].set_ylabel("recurrent transitions")
    axes[0, 0].set_title("Exact gauge-independent contractivity test")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(True, alpha=0.2)

    axes[0, 1].scatter(
        [step["polar"]["metric_decay"]["log10"] for step in possible],
        [step["balanced"]["metric_decay"]["log10"] for step in possible],
        s=25, alpha=0.65, color="tab:green", label="orthogonally feasible",
    )
    axes[0, 1].scatter(
        [step["polar"]["metric_decay"]["log10"] for step in impossible],
        [step["balanced"]["metric_decay"]["log10"] for step in impossible],
        s=25, alpha=0.6, color="tab:red", label="universally blocked",
    )
    lo = min(step["balanced"]["metric_decay"]["log10"] for step in steps)
    hi = max(step["polar"]["metric_decay"]["log10"] for step in steps)
    axes[0, 1].plot([lo, hi], [lo, hi], color="black", linewidth=1, linestyle=":")
    axes[0, 1].axhline(0.0, color="tab:red", linewidth=1, linestyle="--")
    axes[0, 1].set_xlabel("Euclidean-polar metric base log10")
    axes[0, 1].set_ylabel("balanced metric base log10")
    axes[0, 1].set_title("Metric balancing recovers 132 transitions")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(True, alpha=0.2)

    sigmas = sorted({sigma for sigma, _, _ in tagged}, reverse=True)
    possible_counts = []
    polar_counts = []
    balanced_counts = []
    for sigma in sigmas:
        group = [step for value, _, step in tagged if value == sigma]
        possible_counts.append(sum(step["orthogonal_contractivity_possible"] for step in group))
        polar_counts.append(sum(step["polar"]["optimization"]["contractive_feasible"] for step in group))
        balanced_counts.append(sum(step["balanced"]["optimization"]["contractive_feasible"] for step in group))
    x = np.arange(len(sigmas))
    width = 0.25
    axes[1, 0].bar(x - width, possible_counts, width, label="theoretically possible", color="tab:blue")
    axes[1, 0].bar(x, polar_counts, width, label="Euclidean polar", color="tab:gray")
    axes[1, 0].bar(x + width, balanced_counts, width, label="metric balanced", color="tab:green")
    axes[1, 0].set_xticks(x, [str(value) for value in sigmas])
    axes[1, 0].set_xlabel(r"scale $\sigma$")
    axes[1, 0].set_ylabel("recurrent transitions")
    axes[1, 0].set_title("Balanced gauge attains every feasible count")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, axis="y", alpha=0.2)

    floors = [step["balanced"]["optimization"]["fixed_floor"] for step in possible]
    defect_ratio = [step["balanced"]["frame_defect"] / step["polar"]["frame_defect"] for step in possible]
    axes[1, 1].scatter(np.log10(defect_ratio), np.log10(floors), s=25, alpha=0.65, color="tab:purple")
    axes[1, 1].axhline(0.0, color="tab:red", linestyle="--", linewidth=1)
    axes[1, 1].set_xlabel("log10 balanced/polar frame-defect ratio")
    axes[1, 1].set_ylabel("log10 optimized affine fixed floor")
    axes[1, 1].set_title("Larger frame motion remains forcing-safe here")
    axes[1, 1].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "metric_balanced_packet_gauge"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
