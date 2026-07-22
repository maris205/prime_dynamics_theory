"""Create RH-70 frozen-production audit figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "frozen_production_interval_audit.json"
PDF = ROOT / "figures" / "frozen_production_block_hardy_audit.pdf"
PNG = ROOT / "figures" / "frozen_production_block_hardy_audit.png"


def midpoint(ball: str) -> float:
    return float(ball.split()[0].lstrip("["))


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    rows = payload["rows"]
    sigmas = [row["sigma"] for row in rows]
    horizons = [row["selected_horizon"] for row in rows]

    figure, axes = plt.subplots(2, 2, figsize=(11.8, 7.4))
    colors = {"left": "#9c2f2f", "right": "#4f7cac"}
    markers = {"left": "o", "right": "s"}

    axes[0, 0].loglog(
        sigmas,
        horizons,
        marker="o",
        linewidth=1.9,
        color="#5a4a78",
    )
    axes[0, 0].invert_xaxis()
    axes[0, 0].set_xlabel(r"$\sigma$")
    axes[0, 0].set_ylabel(r"block horizon $M$")
    axes[0, 0].set_title("Selected block horizons")
    axes[0, 0].grid(True, which="both", alpha=0.24)

    for side in ("left", "right"):
        channels = [
            next(channel for channel in row["channels"] if channel["side"] == side)
            for row in rows
        ]
        axes[0, 1].loglog(
            sigmas,
            [midpoint(channel["block_power_frobenius_ball"]) for channel in channels],
            marker=markers[side],
            linewidth=1.8,
            color=colors[side],
            label=side,
        )
        axes[1, 0].semilogx(
            sigmas,
            [
                100.0 * (channel["relative_enclosure_width_upper"] - 1.0)
                for channel in channels
            ],
            marker=markers[side],
            linewidth=1.8,
            color=colors[side],
            label=side,
        )
    axes[0, 1].invert_xaxis()
    axes[0, 1].set_xlabel(r"$\sigma$")
    axes[0, 1].set_ylabel(r"certified $\Vert A^M\Vert_F$")
    axes[0, 1].set_title("Block contraction")
    axes[0, 1].grid(True, which="both", alpha=0.24)
    axes[0, 1].legend(frameon=False)

    axes[1, 0].invert_xaxis()
    axes[1, 0].axhline(1.0, color="#333333", linestyle="--", linewidth=1.2)
    axes[1, 0].set_xlabel(r"$\sigma$")
    axes[1, 0].set_ylabel("certified completion excess (%)")
    axes[1, 0].set_title("Full upper versus finite prefix")
    axes[1, 0].grid(True, which="both", alpha=0.24)
    axes[1, 0].legend(frameon=False)

    layers = [
        ("Block-tail theorem", "green", "#2f7d5b"),
        ("Frozen dyadic execution", "green", "#2f7d5b"),
        ("Folded-Gaussian assembly", "amber", "#d07a22"),
        ("Deflation and transfer", "amber", "#d07a22"),
        ("End-to-end Stage A1", "amber", "#d07a22"),
    ]
    positions = list(range(len(layers)))
    axes[1, 1].barh(
        positions,
        [1.0] * len(layers),
        color=[entry[2] for entry in layers],
        height=0.62,
    )
    axes[1, 1].set_yticks(positions, [entry[0] for entry in layers])
    axes[1, 1].invert_yaxis()
    axes[1, 1].set_xlim(0.0, 1.0)
    axes[1, 1].set_xticks([])
    axes[1, 1].set_title("Two-layer validation ledger")
    for position, (_, status, _) in zip(positions, layers, strict=True):
        axes[1, 1].text(
            0.5,
            position,
            status,
            ha="center",
            va="center",
            color="white",
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
