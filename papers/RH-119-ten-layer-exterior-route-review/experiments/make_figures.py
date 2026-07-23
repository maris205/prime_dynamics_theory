"""Create the RH-119 ten-layer timeline and proof-frontier diagram."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def box(ax, center: tuple[float, float], text: str, color: str, *, width: float = 0.25, height: float = 0.1, dashed: bool = False) -> None:
    x, y = center
    patch = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.015",
        facecolor="white",
        edgecolor=color,
        linewidth=1.8,
        linestyle="--" if dashed else "-",
    )
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", fontsize=8.2, color=color)


def arrow(ax, start: tuple[float, float], end: tuple[float, float], color: str = "0.35") -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=12, linewidth=1.25, color=color))


def main() -> None:
    data = json.loads((ROOT / "results" / "ten_layer_review_audit.json").read_text(encoding="utf-8"))
    layers = data["layers"]
    colors = {"constructive": "seagreen", "negative": "firebrick", "synthesis": "mediumpurple"}

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.0), gridspec_kw={"width_ratios": [1.12, 1.0]})
    ax = axes[0]
    numbers = np.asarray([layer["number"] for layer in layers])
    ax.plot(numbers, np.zeros_like(numbers), color="0.65", linewidth=2.0, zorder=1)
    offsets = (0.23, -0.25, 0.30, -0.31, 0.21, -0.23, 0.30, -0.30, 0.22, -0.20)
    short = (
        "capacity\nfactor",
        "trace /\nconcentration",
        "global wedge\nclosed",
        "directional\nframe",
        "PSD\nRayleigh",
        "composite +\noutward filter",
        "optimal\ndepth",
        "finite-anchor\nbarrier",
        "conditional\nliminf gate",
        "frontier\nreview",
    )
    for layer, y, label in zip(layers, offsets, short):
        number = layer["number"]
        color = colors[layer["category"]]
        ax.scatter([number], [0], s=95, color=color, edgecolor="white", linewidth=0.8, zorder=3)
        ax.plot([number, number], [0, y * 0.72], color=color, linewidth=1.0)
        ax.text(number, y, f"RH-{number}\n{label}", ha="center", va="center", fontsize=7.7, color=color)
    ax.set_xlim(109.3, 119.7)
    ax.set_ylim(-0.48, 0.48)
    ax.set_yticks([])
    ax.set_xticks(numbers)
    ax.set_xlabel("paper layer")
    ax.set_title("RH-110--RH-119: ten-layer route audit")
    for spine in ("left", "right", "top"):
        ax.spines[spine].set_visible(False)
    handles = [
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=colors[name], markersize=8, label=name)
        for name in ("constructive", "negative", "synthesis")
    ]
    ax.legend(handles=handles, frameon=False, loc="lower center", ncol=3, fontsize=8)

    ax = axes[1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Current AND/OR proof frontier")
    box(ax, (0.16, 0.83), "exact factor ledger\n+ liminf theorem", "seagreen", width=0.27, height=0.12)
    box(ax, (0.17, 0.18), "finite archive\n322 / 322", "seagreen", width=0.22, height=0.10)
    packet_centers = ((0.46, 0.66), (0.46, 0.47), (0.46, 0.28))
    packet_labels = ("direct-margin\npacket", "directional-Rayleigh\npacket", "trace-concentration\npacket")
    for center, label in zip(packet_centers, packet_labels):
        box(ax, center, label, "darkorange", width=0.27, height=0.105, dashed=True)
    or_center = (0.69, 0.47)
    ax.add_patch(Circle(or_center, 0.045, facecolor="white", edgecolor="0.35", linewidth=1.6))
    ax.text(*or_center, "OR", ha="center", va="center", fontsize=8, color="0.3")
    box(ax, (0.87, 0.47), "eventual $q_4$\nsupport", "0.45", width=0.20, height=0.11, dashed=True)
    box(ax, (0.85, 0.18), "all-level outward\nadmissibility", "firebrick", width=0.24, height=0.10, dashed=True)
    arrow(ax, (0.29, 0.80), (0.64, 0.52), "seagreen")
    for center in packet_centers:
        arrow(ax, (center[0] + 0.14, center[1]), (0.645, 0.47), "darkorange")
    arrow(ax, (0.735, 0.47), (0.765, 0.47))
    arrow(ax, (0.85, 0.235), (0.86, 0.405), "firebrick")
    ax.plot([0.28, 0.59], [0.18, 0.18], color="firebrick", linestyle=":", linewidth=1.4)
    ax.text(0.615, 0.18, r"$\times$", ha="center", va="center", fontsize=16, color="firebrick")
    ax.text(0.46, 0.205, "RH-117: no extrapolation edge", ha="center", va="bottom", fontsize=8, color="firebrick")
    ax.text(0.47, 0.06, "proved frontier packets: 0 / 3", ha="center", color="firebrick", fontsize=9,
            bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "firebrick"})

    fig.tight_layout()
    output = ROOT / "figures" / "ten_layer_exterior_route_review"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
