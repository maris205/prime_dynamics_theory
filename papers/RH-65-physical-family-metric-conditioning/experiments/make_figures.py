"""Create the RH-65 family-conditioning figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "family_conditioning_pilot.json"
PDF = ROOT / "figures" / "physical_family_metric_conditioning.pdf"
PNG = ROOT / "figures" / "physical_family_metric_conditioning.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    cases = [case for case in payload["cases"] if case["dimension"] == 4]
    colors = ("#9c2f2f", "#d07a22", "#4f7cac", "#2f7d5b")
    figure, axes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    for case, color in zip(cases, colors, strict=True):
        rows = case["rows"]
        gaps = [row["gap"] for row in rows]
        label = rf"$\alpha={case['coupling_power']:g}$"
        axes[0].loglog(
            gaps,
            [row["condition_number"] for row in rows],
            marker="o",
            linewidth=1.8,
            markersize=4,
            color=color,
            label=label,
        )
        axes[1].loglog(
            gaps,
            [row["metric_contraction_gap"] for row in rows],
            marker="o",
            linewidth=1.8,
            markersize=4,
            color=color,
            label=label,
        )
    axes[0].set_title(r"Metric conditioning, $d=4$")
    axes[0].set_ylabel(r"$\operatorname{cond}(M_s)$")
    axes[1].set_title(r"Weighted contraction gap, $d=4$")
    axes[1].set_ylabel(r"$1-q_{M,s}$")
    for axis in axes:
        axis.set_xlabel(r"peripheral gap $s=1-q^2$")
        axis.grid(True, which="both", alpha=0.24)
        axis.invert_xaxis()
        axis.legend(frameon=False, fontsize=9)
    figure.tight_layout()
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(PDF.relative_to(ROOT))
    print(PNG.relative_to(ROOT))


if __name__ == "__main__":
    main()
