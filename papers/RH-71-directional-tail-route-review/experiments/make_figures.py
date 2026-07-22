"""Create RH-71 route-review figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "results" / "route_review.json"
ARB = ROOT / "results" / "arb_bridge_slack_audit.json"
PDF = ROOT / "figures" / "directional_tail_route_review.pdf"
PNG = ROOT / "figures" / "directional_tail_route_review.png"


def box(axis, xy, width, height, text, color) -> None:
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        facecolor=color,
        edgecolor="none",
        alpha=0.95,
    )
    axis.add_patch(patch)
    axis.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        color="white",
        fontsize=8.5,
        fontweight="bold",
    )


def arrow(axis, start, end) -> None:
    axis.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.4},
    )


def main() -> None:
    route = json.loads(ROUTE.read_text(encoding="utf-8"))
    arb = json.loads(ARB.read_text(encoding="utf-8"))
    figure, axes = plt.subplots(2, 2, figsize=(12.2, 7.6))

    effect_colors = {
        "advance": "#2f7d5b",
        "no_go_boundary": "#a33a33",
        "advance_and_correct": "#d07a22",
        "exact_no_go": "#a33a33",
        "synthesis": "#6b5b95",
        "validated_advance": "#2f6f9f",
    }
    ledger = route["paper_ledger"]
    numbers = [row["paper"] for row in ledger]
    axes[0, 0].plot(numbers, [0.0] * len(numbers), color="#777777", lw=1.2)
    for row in ledger:
        number = row["paper"]
        effect = row["route_effect"]
        axes[0, 0].scatter(
            [number],
            [0.0],
            s=90,
            color=effect_colors[effect],
            zorder=3,
        )
        axes[0, 0].text(
            number,
            0.13 if number % 2 == 0 else -0.13,
            f"RH-{number}",
            ha="center",
            va="center",
            fontsize=8,
        )
    axes[0, 0].set_xlim(61.4, 70.6)
    axes[0, 0].set_ylim(-0.28, 0.28)
    axes[0, 0].set_yticks([])
    axes[0, 0].set_xticks(numbers)
    axes[0, 0].set_title("Nine inputs to the RH-71 synthesis")
    for spine in axes[0, 0].spines.values():
        spine.set_visible(False)

    for side, color, marker in (
        ("left", "#9c2f2f", "o"),
        ("right", "#4f7cac", "s"),
    ):
        rows = [row for row in arb["rows"] if row["side"] == side]
        axes[0, 1].semilogx(
            [row["sigma"] for row in rows],
            [
                100.0
                * row["budgets"]["1_percent"]["relative_slack_lower"]
                for row in rows
            ],
            marker=marker,
            linewidth=1.8,
            color=color,
            label=side,
        )
    axes[0, 1].invert_xaxis()
    axes[0, 1].axhline(0.0, color="#333333", lw=1.0)
    axes[0, 1].set_xlabel(r"$\sigma$")
    axes[0, 1].set_ylabel("certified bridge slack (% of prefix)")
    axes[0, 1].set_title("Headroom inside a 1% total target")
    axes[0, 1].grid(True, which="both", alpha=0.24)
    axes[0, 1].legend(frameon=False)

    axis = axes[1, 0]
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.0, 1.0)
    axis.axis("off")
    green = "#2f7d5b"
    amber = "#d07a22"
    box(axis, (0.05, 0.68), 0.31, 0.16, "Frozen terminal\nupper", green)
    box(axis, (0.05, 0.34), 0.31, 0.16, "Upstream interval\ntriple", amber)
    box(axis, (0.47, 0.51), 0.34, 0.16, "Finite-scale\nend-to-end bound", amber)
    box(axis, (0.47, 0.14), 0.34, 0.16, "Uniform family\nscaling", amber)
    box(axis, (0.84, 0.32), 0.13, 0.20, "Stage\nA1", amber)
    arrow(axis, (0.36, 0.76), (0.47, 0.62))
    arrow(axis, (0.36, 0.42), (0.47, 0.58))
    arrow(axis, (0.81, 0.59), (0.84, 0.45))
    arrow(axis, (0.81, 0.22), (0.84, 0.37))
    axis.set_title("First-open dependency frontier")

    stages = [
        ("A1 terminal", "green", green),
        ("A1 upstream", "amber", amber),
        ("A1 uniform", "amber", amber),
        ("A2 factors", "green", green),
        ("A3 analytic", "green", green),
        ("A3 production", "amber", amber),
        ("A4 unconditional", "amber", amber),
        ("A5 / B / C / D", "not started", "#888888"),
    ]
    positions = list(range(len(stages)))
    axes[1, 1].barh(
        positions,
        [1.0] * len(stages),
        color=[stage[2] for stage in stages],
        height=0.62,
    )
    axes[1, 1].set_yticks(positions, [stage[0] for stage in stages])
    axes[1, 1].invert_yaxis()
    axes[1, 1].set_xlim(0.0, 1.0)
    axes[1, 1].set_xticks([])
    axes[1, 1].set_title("Revised roadmap status after RH-70")
    for position, (_, status, _) in zip(positions, stages, strict=True):
        axes[1, 1].text(
            0.5,
            position,
            status,
            ha="center",
            va="center",
            color="white",
            fontsize=8.5,
            fontweight="bold",
        )
    for spine in axes[1, 1].spines.values():
        spine.set_visible(False)

    figure.tight_layout()
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(PDF.relative_to(ROOT))
    print(PNG.relative_to(ROOT))


if __name__ == "__main__":
    main()
