"""Create RH-69 adaptive portfolio figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "certificate_portfolio.json"
PDF = ROOT / "figures" / "adaptive_certificate_portfolio.pdf"
PNG = ROOT / "figures" / "adaptive_certificate_portfolio.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    figure, axes = plt.subplots(1, 3, figsize=(12.5, 3.9))

    phase = payload["phase_horizon_portfolio"]
    for side, color, marker in (
        ("left", "#9c2f2f", "o"),
        ("right", "#4f7cac", "s"),
    ):
        rows = [row for row in phase if row["side"] == side]
        sigmas = [row["sigma"] for row in rows]
        axes[0].loglog(
            sigmas,
            [row["selected"]["costs"]["horizon"] for row in rows],
            marker=marker,
            linewidth=1.9,
            color=color,
            label=f"{side}: phase selected",
        )
        axes[0].loglog(
            sigmas,
            [row["geometric_horizon_for_same_tolerance"] for row in rows],
            marker=marker,
            linestyle="--",
            linewidth=1.5,
            color=color,
            alpha=0.72,
            label=f"{side}: geometric",
        )
    axes[0].invert_xaxis()
    axes[0].set_xlabel(r"$\sigma$")
    axes[0].set_ylabel("1% horizon")
    axes[0].set_title("Physical phase branch")
    axes[0].grid(True, which="both", alpha=0.24)
    axes[0].legend(frameon=False, fontsize=7.5)

    covariance = payload["covariance_portfolio"]
    colors = ("#9c2f2f", "#2f7d5b", "#4f7cac")
    for model, color in zip(covariance, colors, strict=True):
        frontier = model["pareto_frontier"]
        short = (
            "cancel"
            if "cancellation" in model["name"]
            else "chain"
            if "chain" in model["name"]
            else "phase"
        )
        axes[1].loglog(
            [row["costs"]["global_gain"] for row in frontier],
            [row["upper"] for row in frontier],
            marker="o",
            linewidth=1.7,
            color=color,
            label=short,
        )
    axes[1].set_xlabel("global PSD gain")
    axes[1].set_ylabel("physical upper gain")
    axes[1].set_title("Covariance Pareto fronts")
    axes[1].grid(True, which="both", alpha=0.24)
    axes[1].legend(frameon=False, fontsize=8)

    arcs = payload["depth_triage"]["phase_arcs"]
    status_color = {"green": "#2f7d5b", "amber": "#d07a22"}
    axes[2].scatter(
        [row["arc_width_radians"] for row in arcs],
        [row["required_depth"] for row in arcs],
        c=[status_color[row["status"]] for row in arcs],
        s=42,
        zorder=3,
    )
    axes[2].plot(
        [row["arc_width_radians"] for row in arcs],
        [row["required_depth"] for row in arcs],
        color="#777777",
        linewidth=1.2,
    )
    axes[2].axhline(8, linestyle="--", color="#333333", linewidth=1.2)
    axes[2].set_xlabel("phase arc width")
    axes[2].set_ylabel("required depth")
    axes[2].set_title("Green/amber depth triage")
    axes[2].grid(True, alpha=0.24)
    figure.tight_layout()
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(PDF.relative_to(ROOT))
    print(PNG.relative_to(ROOT))


if __name__ == "__main__":
    main()
