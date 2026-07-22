"""Figures for the two-corridor Stage-A composition."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads((ROOT / "results" / "stage_composition_audit.json").read_text(encoding="utf-8"))
    rows = payload["rows"]
    levels = np.asarray([row["level"] for row in rows])
    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.4), constrained_layout=True)

    ax = axes[0, 0]
    ax.plot(levels, [row["conditional_hardy_upper"] for row in rows], "o-", label="common conditional upper")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("Hardy energy")
    ax.set_title("Polylogarithmic Hardy envelope")
    ax.legend()

    ax = axes[0, 1]
    ax.plot(levels, [row["conditional_hardy_product_upper"] for row in rows], "o-", label="conditional product")
    ax.plot(levels, [row["actual_frozen_hardy_product_upper"] for row in rows], "s--", label="frozen product")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel(r"$E_B E_C$")
    ax.set_title("RH-54 input product")
    ax.legend()

    ax = axes[1, 0]
    ax.semilogy(levels, [row["rank4_future_error_upper"] for row in rows], "o-")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("rank-4 future error")
    ax.set_title("Effective-rank corridor remainder")

    ax = axes[1, 1]
    ax.semilogy(levels, [row["identification_stress_envelope_upper"] for row in rows], "o-")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("identification envelope")
    ax.set_title(r"Stress mesh $n=\sigma^{-2}(k+2)$")

    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"two_corridor_stage_A1_composition.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
