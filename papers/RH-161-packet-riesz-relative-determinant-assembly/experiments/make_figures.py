from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def box(ax, x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.025",
        facecolor=color, edgecolor="#333333", linewidth=1.0,
    ))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8)


def arrow(ax, start, end):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10, color="#444444"))


def main() -> None:
    data = json.loads((ROOT / "results/typed_assembly_audit.json").read_text())
    fig, axes = plt.subplots(2, 2, figsize=(11.8, 7.4), constrained_layout=True)

    ax = axes[0, 0]
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    labels = ["S\nreset seed", "R\nRiesz lift", "Q\ncloud ledger", "U_p\ncomplement", "Z\ncanonical", "T\nmarked traces"]
    xs = np.linspace(0.02, 0.85, len(labels))
    for i, (x, label) in enumerate(zip(xs, labels)):
        box(ax, x, 0.40, 0.13, 0.22, label, "#ddaa44" if i == 0 else "#d0d0d0")
        if i + 1 < len(labels):
            arrow(ax, (x + 0.13, 0.51), (xs[i + 1], 0.51))
    ax.text(0.5, 0.84, "A. Typed Gate-A assembly", ha="center", fontsize=11, fontweight="bold")
    ax.text(0.5, 0.16, "p=1 (Fredholm) or p=2 (regularized); S is conditional and R, Q, U_p, Z, T are open.", ha="center", fontsize=8)

    ax = axes[0, 1]
    rows = data["packet_riesz_examples"]
    x = [row["coupling_upper"] for row in rows]
    y = [row["projector_error_upper"] if row["projector_error_upper"] != float("inf") else 3.0 for row in rows]
    colors = ["#55a868" if row["packet_bridge_certified"] else "#c44e52" for row in rows]
    ax.plot(x, y, color="#4c72b0", lw=1.5)
    ax.scatter(x, y, color=colors, s=55, zorder=3)
    ax.axhline(1.0, color="black", ls="--", lw=1.0, label="stable packet-bridge threshold")
    ax.set_xlabel("coupling upper $\\varepsilon$")
    ax.set_ylabel("Riesz-projector error upper")
    ax.set_title("B. Packet-to-Riesz threshold (illustrative constants)")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    rows = data["determinant_examples"]
    x = [row["trace_norm_error_upper"] for row in rows]
    y = [row["determinant_error_upper"] for row in rows]
    y2 = [row["regularized_determinant_error_upper"] for row in rows]
    ax.loglog(x, y, "o-", color="#8172b2", label="$p=1$")
    ax.loglog(x, y2, "s--", color="#ccb974", label="$p=2$")
    ax.set_xlabel("complement Schatten-norm error")
    ax.set_ylabel("$\\det_p$ error upper on $|z|\\leq1/2$")
    ax.set_title("C. Complement convergence transfers quantitatively")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    rows = [("omit R", "packet support is not spectral isolation"),
            ("omit Q", "cloud zeros do not fix the residual"),
            ("omit $U_p$", "$\det_p$ normality can fail"),
            ("omit Z", "schedule-dependent entire factor"),
            ("omit T", "temporal order can disappear")]
    for i, (left, right) in enumerate(rows):
        y0 = 0.78 - 0.16 * i
        box(ax, 0.04, y0, 0.16, 0.10, left, "#c44e52")
        arrow(ax, (0.20, y0 + 0.05), (0.27, y0 + 0.05))
        box(ax, 0.27, y0, 0.68, 0.10, right, "#f0f0f0")
    ax.text(0.5, 0.94, "D. Independent failure modes", ha="center", fontsize=11, fontweight="bold")

    output = ROOT / "figures/typed_moving_cloud_assembly"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
