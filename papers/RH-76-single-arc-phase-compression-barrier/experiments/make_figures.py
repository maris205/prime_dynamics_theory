"""Figures for the phase-compression barrier."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads((ROOT / "results" / "phase_compression_audit.json").read_text(encoding="utf-8"))
    rows = payload["rows"]
    levels = np.arange(len(rows))
    left = [row["channels"][0] for row in rows]
    right = [row["channels"][1] for row in rows]
    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.5), constrained_layout=True)

    ax = axes[0, 0]
    for channels, style, label in ((left, "o-", "left"), (right, "s--", "right")):
        ax.plot(levels, [x["weighted_arcs"]["mass_0.9"]["width_upper"] for x in channels], style, label=label + " 90%")
        ax.plot(levels, [x["weighted_arcs"]["mass_0.99"]["width_upper"] for x in channels], style, alpha=0.55, label=label + " 99%")
    ax.axhline(2*np.pi, color="black", linestyle=":", label=r"$2\pi$")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("minimal arc width")
    ax.set_title("Source-weighted phase coverage")
    ax.legend(fontsize=7)

    ax = axes[0, 1]
    ax.plot(levels, [x["moment_gram"]["residual_lower"] for x in left], "o-", label="left")
    ax.plot(levels, [x["moment_gram"]["residual_lower"] for x in right], "s--", label="right")
    ax.axhline(0.1, color="black", linestyle=":", label="10% target")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel(r"residual at depth $M$")
    ax.set_yscale("log")
    ax.set_title("Arb moment-Gram residual")
    ax.legend()

    ax = axes[1, 0]
    width = 0.36
    ax.bar(levels-width/2, [x["required_depth_10_percent_diagnostic"]/(x["horizon"]+1) for x in left], width, label="left")
    ax.bar(levels+width/2, [x["required_depth_10_percent_diagnostic"]/(x["horizon"]+1) for x in right], width, label="right")
    ax.axhline(1.0, color="black", linestyle=":")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("required depth / full depth")
    ax.set_ylim(0, 1.08)
    ax.set_title("10% phase-only depth")
    ax.legend()

    ax = axes[1, 1]
    ax.plot(levels, [x["active_source_phase_count"] for x in left], "o-", label="left active")
    ax.plot(levels, [x["dimension"] for x in left], "o:", alpha=.5, label="left dimension")
    ax.plot(levels, [x["active_source_phase_count"] for x in right], "s--", label="right active")
    ax.plot(levels, [x["dimension"] for x in right], "s:", alpha=.5, label="right dimension")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("phase coordinates")
    ax.set_yscale("log", base=2)
    ax.set_title("No support-count compression")
    ax.legend(fontsize=7)

    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"single_arc_phase_compression_barrier.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
