"""Make figures from the archived RH-28 arcwise tables."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summary_figure(summaries: list[dict[str, str]]) -> None:
    rows = sorted(summaries, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    eta = np.asarray(
        [float(row["maximum_correction_ratio_upper"]) for row in rows]
    )
    budget = np.asarray(
        [float(row["minimum_resolvent_budget_lower"]) for row in rows]
    )
    leaves = np.asarray(
        [int(row["accepted_arc_count"]) for row in rows], dtype=float
    )
    levels = np.asarray(
        [int(row["maximum_refinement_level"]) for row in rows], dtype=float
    )
    family = np.asarray(
        [float(row["maximum_projected_family_neumann_product"]) for row in rows]
    )
    contraction = np.asarray(
        [float(row["maximum_coordinate_contraction"]) for row in rows]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.6))
    axes[0, 0].semilogx(sigma, eta, "o-", color="#1f77b4")
    axes[0, 0].axhline(1.0, color="0.35", ls="--", lw=0.9)
    axes[0, 0].set(
        xlabel=r"noise scale $\sigma$",
        ylabel=r"full-contour $\max\bar\eta$",
        title="Conditional Rouché ratio",
    )
    axes[0, 0].set_ylim(0.0, 1.06)

    axes[0, 1].loglog(sigma, budget, "s-", color="#d62728")
    axes[0, 1].set(
        xlabel=r"noise scale $\sigma$",
        ylabel=r"full-contour $\min M_*^-$",
        title="Remaining resolvent gate",
    )

    twin = axes[1, 0].twinx()
    axes[1, 0].semilogx(sigma, leaves, "o-", color="#2ca02c", label="leaves")
    twin.semilogx(
        sigma, levels, "d--", color="#9467bd", label="max level"
    )
    axes[1, 0].set(
        xlabel=r"noise scale $\sigma$",
        ylabel="accepted subarcs",
        title="Adaptive dyadic cover",
    )
    twin.set_ylabel("maximum refinement level")
    axes[1, 0].grid(alpha=0.2)

    axes[1, 1].semilogx(sigma, family, "o-", label=r"$q_F$")
    axes[1, 1].semilogx(sigma, contraction, "s--", label=r"$q_H$")
    axes[1, 1].axhline(1.0, color="0.35", ls="--", lw=0.9)
    axes[1, 1].set(
        xlabel=r"noise scale $\sigma$",
        ylabel="maximum contraction product",
        title="Local Neumann gates",
        ylim=(0.0, 1.06),
    )
    axes[1, 1].legend(frameon=False)

    for axis in axes.flat:
        axis.grid(alpha=0.2, which="both")
        axis.invert_xaxis()
    fig.tight_layout()
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / "arcwise_scale_summary.pdf")
    fig.savefig(FIGURES / "arcwise_scale_summary.png", dpi=240)
    plt.close(fig)


def finest_cover_figure(arcs: list[dict[str, str]], sigma: float) -> None:
    rows = sorted(
        [row for row in arcs if float(row["sigma"]) == float(sigma)],
        key=lambda row: int(row["arc"]),
    )
    theta = np.asarray([float(row["theta_midpoint"]) for row in rows])
    eta = np.asarray([float(row["correction_ratio_upper"]) for row in rows])
    levels = np.asarray(
        [int(row["refinement_level"]) for row in rows], dtype=float
    )
    widths = np.asarray(
        [float(row["theta_end"]) - float(row["theta_start"]) for row in rows]
    )
    q = np.asarray(
        [float(row["projected_family_neumann_product"]) for row in rows]
    )

    fig, axes = plt.subplots(2, 1, figsize=(10.0, 6.4), sharex=True)
    axes[0].plot(theta, eta, ".", ms=2.5, color="#1f77b4")
    axes[0].axhline(1.0, color="0.35", ls="--", lw=0.9)
    axes[0].set_ylabel(r"arcwise $\bar\eta$")
    axes[0].set_title(rf"Adaptive full-contour cover, $\sigma={sigma:.0e}$")
    axes[1].step(theta, levels, where="mid", color="#9467bd", label="level")
    axes[1].set(
        xlabel=r"arc midpoint angle $\theta$",
        ylabel="refinement level",
    )
    q_axis = axes[1].twinx()
    q_axis.plot(theta, q, ".", ms=2.2, color="#d62728", label=r"$q_F$")
    q_axis.set_ylabel(r"projected-family product $q_F$")
    q_axis.set_ylim(0.0, 1.05)
    handles = [
        axes[1].lines[0],
        q_axis.lines[0],
    ]
    axes[1].legend(handles, ["level", r"$q_F$"], frameon=False, ncol=2)
    for axis in axes:
        axis.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURES / "arcwise_finest_cover.pdf")
    fig.savefig(FIGURES / "arcwise_finest_cover.png", dpi=240)
    plt.close(fig)


def main() -> None:
    summaries = read_csv(RESULTS / "arcwise_scale_summary.csv")
    arcs = read_csv(RESULTS / "arcwise_contour_arcs.csv")
    summary_figure(summaries)
    finest_cover_figure(arcs, min(float(row["sigma"]) for row in summaries))
    print("generated RH-28 figures")


if __name__ == "__main__":
    main()
