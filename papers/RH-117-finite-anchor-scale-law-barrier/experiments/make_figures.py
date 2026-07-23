"""Create the RH-117 physical-envelope and continuation figure."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from scale_law import bounded_anchor_matching_extension  # noqa: E402


def series(rows: list[dict[str, object]], metric: str, statistic: str) -> np.ndarray:
    return np.asarray([row[metric][statistic] for row in rows], dtype=float)


def main() -> None:
    data = json.loads((ROOT / "results" / "scale_law_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    scales = np.asarray([row["sigma"] for row in rows], dtype=float)

    fig, axes = plt.subplots(2, 2, figsize=(11.1, 8.1))
    ax = axes[0, 0]
    lower = series(rows, "capacity", "minimum")
    upper = series(rows, "capacity", "maximum")
    median = series(rows, "capacity", "median")
    ax.fill_between(scales, lower, upper, color="tab:blue", alpha=0.18, label="min--max envelope")
    ax.loglog(scales, median, marker="o", color="tab:blue", label="median")
    ax.invert_xaxis()
    ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel(r"capacity $\Lambda_{23}$")
    ax.set_title("Three-mode capacity envelope")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    lower = series(rows, "concentration", "minimum")
    upper = series(rows, "concentration", "maximum")
    median = series(rows, "concentration", "median")
    ax.fill_between(scales, lower, upper, color="tab:orange", alpha=0.2, label="min--max envelope")
    ax.semilogx(scales, median, marker="s", color="tab:orange", label="median")
    ax.invert_xaxis()
    ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel("exterior concentration")
    ax.set_title("Tail-energy concentration envelope")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    lower = series(rows, "fourth_mode_ratio", "minimum")
    upper = series(rows, "fourth_mode_ratio", "maximum")
    median = series(rows, "fourth_mode_ratio", "median")
    ax.fill_between(scales, lower, upper, color="tab:green", alpha=0.18, label=r"$q_4$ min--max")
    ax.loglog(scales, median, marker="o", color="tab:green", label=r"median $q_4$")
    ax.invert_xaxis()
    ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel(r"fourth-mode ratio $q_4$")
    ax.grid(True, which="both", alpha=0.25)
    twin = ax.twinx()
    depths = np.asarray([row["maximum_certifying_depth"] for row in rows], dtype=float)
    twin.plot(scales, depths, marker="D", linestyle="--", color="tab:purple", label="maximum depth")
    twin.set_ylabel("maximum certifying depth", color="tab:purple")
    twin.tick_params(axis="y", labelcolor="tab:purple")
    twin.set_ylim(0.0, 7.0)
    lines = ax.get_lines() + twin.get_lines()
    ax.legend(lines, [line.get_label() for line in lines], frameon=False, fontsize=8)
    ax.set_title("Support envelope and observed depth")

    ax = axes[1, 1]
    anchor_values = series(rows, "capacity", "median")
    probe = float(data["continuation_barrier"]["probe_scale"])
    grid = np.logspace(np.log10(probe), np.log10(np.max(scales)), 800)
    germs = {
        r"limit $0$": (lambda x: x, "tab:blue"),
        r"limit $1/2$": (lambda x: np.full_like(x, 0.5), "tab:orange"),
        r"limit $1$": (lambda x: 1.0 - x, "tab:red"),
    }
    for label, (germ, color) in germs.items():
        extension = bounded_anchor_matching_extension(scales, anchor_values, grid, germ)
        ax.loglog(grid, extension, color=color, linewidth=1.7, label=label)
    ax.loglog(scales, anchor_values, linestyle="none", marker="o", color="black", markersize=4.5, label="same five anchors")
    ax.set_ylim(1e-10, 1.1)
    ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel("bounded positive continuation")
    ax.set_title("Finite-anchor asymptotic barrier")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "finite_anchor_scale_law_barrier"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
