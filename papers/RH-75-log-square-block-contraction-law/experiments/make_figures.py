"""Figures for the log-square block law."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads((ROOT / "results" / "log_square_block_audit.json").read_text(encoding="utf-8"))
    rows = payload["rows"]
    levels = np.asarray([row["level"] for row in rows])
    sigmas = np.asarray([row["sigma"] for row in rows])
    left = [row["channels"][0] for row in rows]
    right = [row["channels"][1] for row in rows]
    constants = payload["constants"]

    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.5), constrained_layout=True)

    ax = axes[0, 0]
    ax.plot(levels, [x["selected_horizon"] for x in left], "o-", label="selected")
    ax.plot(levels, [x["allowed_log_square_horizon"] for x in left], "s--", label=r"$(k+2)^2$")
    ax.set_xlabel("dyadic level k")
    ax.set_ylabel("block horizon")
    ax.set_title("Admissible growing depth")
    ax.legend()

    ax = axes[0, 1]
    ax.plot(levels, [x["normalized_q_over_sqrt_sigma_upper"] for x in left], "o-", label="left")
    ax.plot(levels, [x["normalized_q_over_sqrt_sigma_upper"] for x in right], "s--", label="right")
    ax.axhline(constants["q_constant"], color="black", linestyle=":", label=r"$C_q$")
    ax.set_xlabel("dyadic level k")
    ax.set_ylabel(r"$\|A^{M_k}\|/\sqrt{\sigma_k}$")
    ax.set_title("Square-root block law")
    ax.legend()

    ax = axes[1, 0]
    ax.plot(levels, [x["observation_density_upper"] for x in left], "o-", label=r"left $\sigma\|Y\|_F^2$")
    ax.plot(levels, [x["observation_density_upper"] for x in right], "s--", label=r"right $\sigma\|Y\|_F^2$")
    ax.plot(levels, [x["source_block_upper"] for x in left], "^-", label="left source block")
    ax.plot(levels, [x["source_block_upper"] for x in right], "v--", label="right source block")
    ax.set_xlabel("dyadic level k")
    ax.set_ylabel("certified scalar")
    ax.set_title("Dimension cancellation inputs")
    ax.legend(fontsize=7)

    ax = axes[1, 1]
    for channels, style, label in ((left, "o-", "left"), (right, "s--", "right")):
        ax.plot(levels, [x["actual_tail_energy_squared_upper"] for x in channels], style, label=label + " tail")
    ax.axhline(left[0]["uniform_tail_envelope_upper"], color="black", linestyle=":", label="common envelope")
    ax.set_xlabel("dyadic level k")
    ax.set_ylabel("tail energy squared")
    ax.set_title("Uniform tail target")
    ax.legend(fontsize=7)

    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"log_square_block_contraction.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
