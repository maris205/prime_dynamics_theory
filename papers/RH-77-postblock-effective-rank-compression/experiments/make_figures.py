"""Figures for validated postblock effective rank."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads((ROOT / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    rows = payload["rows"]
    levels = np.arange(len(rows))
    left = [row["channels"][0] for row in rows]
    right = [row["channels"][1] for row in rows]
    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.5), constrained_layout=True)

    ax = axes[0, 0]
    ax.plot(levels, [x["rank_diagnostics"]["participation_rank_diagnostic"] for x in left], "o-", label="left")
    ax.plot(levels, [x["rank_diagnostics"]["participation_rank_diagnostic"] for x in right], "s--", label="right")
    ax.axhline(2.0, color="black", linestyle=":", label="rank 2")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("participation rank")
    ax.set_title("Postblock effective rank")
    ax.legend()

    ax = axes[0, 1]
    for channels, style, label in ((left, "o-", "left"), (right, "s--", "right")):
        ax.semilogy(levels, [1.0-x["validated_rank_compression"]["rank_2"]["energy_capture_lower"] for x in channels], style, label=label)
    ax.axhline(0.01, color="black", linestyle=":", label="1% loss")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("rank-2 lost energy")
    ax.set_title("Validated rank-2 capture")
    ax.legend()

    ax = axes[1, 0]
    for channels, style, label in ((left, "o-", "left"), (right, "s--", "right")):
        ax.semilogy(levels, [1.0-x["validated_rank_compression"]["rank_4"]["energy_capture_lower"] for x in channels], style, label=label)
    ax.axhline(1e-6, color="black", linestyle=":", label=r"$10^{-6}$ loss")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("rank-4 lost energy")
    ax.set_title("Validated rank-4 capture")
    ax.legend()

    ax = axes[1, 1]
    ax.semilogy(levels, [x["validated_rank_compression"]["rank_4"]["full_future_hardy_perturbation_upper"] for x in left], "o-", label="left")
    ax.semilogy(levels, [x["validated_rank_compression"]["rank_4"]["full_future_hardy_perturbation_upper"] for x in right], "s--", label="right")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("full-future Hardy error")
    ax.set_title("Observability-transferred rank-4 error")
    ax.legend()

    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"postblock_effective_rank_compression.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
