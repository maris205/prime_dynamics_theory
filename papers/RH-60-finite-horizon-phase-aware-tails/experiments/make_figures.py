"""Create the RH-60 finite-horizon phase-aware audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    payload = load(ROOT / "results" / "phase_tail_pilot.json")
    rows = payload["rows"]
    sigma = np.asarray([row["sigma"] for row in rows])
    horizons = np.asarray(payload["horizons"], dtype=int)
    figure, axes = plt.subplots(2, 2, figsize=(10.8, 7.3))
    styles = {
        "left": ("#174a7e", "o"),
        "right": ("#c44e52", "s"),
    }

    ax = axes[0, 0]
    for side, (color, marker) in styles.items():
        ax.semilogx(
            sigma,
            [row[side]["exact_hardy_energy"] for row in rows],
            marker + "-",
            color=color,
            label=side + " exact",
        )
        ax.semilogx(
            sigma,
            [row[side]["selected_phase_aware_upper"] for row in rows],
            marker + "--",
            color=color,
            alpha=0.82,
            label=side + r" $L=32$ completion",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"Hardy magnitude at $r=0.85$")
    ax.set_title("(a) Fixed-horizon phase-aware upper")
    ax.legend(fontsize=7)

    ax = axes[0, 1]
    selected = rows[-1]
    x = np.log2(horizons + 1)
    for side, (color, marker) in styles.items():
        values = [
            selected[side]["horizons"][str(h)]["phase_aware_upper"]
            for h in horizons
        ]
        ax.semilogy(
            x,
            values,
            marker + "-",
            color=color,
            label=side + " completion",
        )
        ax.axhline(
            selected[side]["exact_hardy_energy"],
            color=color,
            linestyle=":",
            alpha=0.72,
            label=side + " exact",
        )
    ax.set_xticks(x, [str(h) for h in horizons])
    ax.set_xlabel("finite horizon $L$")
    ax.set_ylabel("Hardy magnitude")
    ax.set_title(r"(b) Tail collapse at $\sigma=0.01$")
    ax.legend(fontsize=7, ncol=2)

    ax = axes[1, 0]
    for side, (color, marker) in styles.items():
        finite = [
            row[side]["horizons"][str(payload["selected_horizon"])]
            ["finite_fused_energy"]
            for row in rows
        ]
        tails = [
            row[side]["horizons"][str(payload["selected_horizon"])]
            ["tail_sum"]
            for row in rows
        ]
        ax.semilogx(
            sigma,
            finite,
            marker + "-",
            color=color,
            label=side + " finite phase",
        )
        ax.semilogx(
            sigma,
            tails,
            marker + "--",
            color=color,
            alpha=0.78,
            label=side + " Stein tail",
        )
    ax.invert_xaxis()
    ax.set_yscale("log")
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("completion components")
    ax.set_title(r"(c) $L=32$: phase term dominates the tail")
    ax.legend(fontsize=7)

    ax = axes[1, 1]
    for side, (color, marker) in styles.items():
        ratios = [
            row[side]["selected_phase_aware_upper_over_exact"]
            for row in rows
        ]
        old = [
            row[side]["rh59_metric_absolute_upper"]
            / row[side]["exact_hardy_energy"]
            for row in rows
        ]
        ax.semilogx(
            sigma,
            ratios,
            marker + "-",
            color=color,
            label=side + r" RH-60 $L=32$",
        )
        ax.semilogx(
            sigma,
            old,
            marker + ":",
            color=color,
            alpha=0.7,
            label=side + " RH-59 metric",
        )
    ax.invert_xaxis()
    ax.axhline(1.0, color="#333333", linewidth=0.8)
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("upper / exact Hardy energy")
    ax.set_title("(d) Completion removes the endpoint wall")
    ax.legend(fontsize=7)

    figure.tight_layout()
    output = ROOT / "figures" / "finite_horizon_phase_tail"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    figure.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(str(output.relative_to(ROOT)))


if __name__ == "__main__":
    main()
