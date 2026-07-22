"""Figures for determinant diagonal transfer."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads((ROOT / "results" / "determinant_transfer_audit.json").read_text(encoding="utf-8"))
    rows = payload["rows"]
    levels = np.asarray([row["level"] for row in rows])
    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.4), constrained_layout=True)

    ax = axes[0, 0]
    ax.semilogy(levels, [row["conditional_intrinsic_hs_error_upper"] for row in rows], "o-")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("intrinsic HS error")
    ax.set_title("Conditional A4 identification")

    ax = axes[0, 1]
    ax.semilogy(levels, [row["square_trace_error_upper"] for row in rows], "o-")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("trace-norm square error")
    ax.set_title("Bulk-square transfer")

    ax = axes[1, 0]
    ax.semilogy(levels, [row["shrinking_disk_determinant_error_upper"] for row in rows], "o-", label=r"$R=0.01\sigma$")
    ax.semilogy(levels, [row["fixed_disk_determinant_error_upper"] for row in rows], "s--", label=r"$R=0.01$")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("determinant error upper")
    ax.set_title("Shrinking versus fixed disk")
    ax.legend()

    ax = axes[1, 1]
    ax.plot(levels, [row["fixed_disk_determinant_error_upper"]/row["shrinking_disk_determinant_error_upper"] for row in rows], "o-")
    ax.set_xlabel("dyadic level")
    ax.set_ylabel("fixed / shrinking bound")
    ax.set_yscale("log")
    ax.set_title("Exponential continuity penalty")

    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"intrinsic_determinant_diagonal_transfer.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
