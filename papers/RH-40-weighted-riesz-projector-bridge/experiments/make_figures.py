"""Render the weighted-Riesz bridge and stored-factor diagnostics."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter, FixedLocator, NullFormatter
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(ROOT / "results" / "weighted_projector_pilot_sigma_1e-02.json")
    certificate = load(
        ROOT / "results" / "weighted_riesz_projector_bridge_certificate.json"
    )
    dimensions = np.asarray([2048, 4096, 8192])
    level_labels = [str(value) for value in dimensions]
    levels = [pilot["levels"][label] for label in level_labels]

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 160,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.4, 7.4), constrained_layout=True)

    axis = axes[0, 0]
    parity = np.asarray([row["peripheral_values"][1] for row in levels])
    richardson = float(
        pilot["parity_convergence"]["second_richardson_extrapolate"]
    )
    error = np.abs(parity - richardson)
    reference = error[-1] * (dimensions[-1] / dimensions) ** 2
    axis.loglog(dimensions, error, marker="o", label="stored branch")
    axis.loglog(dimensions, reference, linestyle="--", color="black", label=r"$n^{-2}$ reference")
    axis.xaxis.set_major_locator(FixedLocator(dimensions))
    axis.xaxis.set_major_formatter(FixedFormatter(level_labels))
    axis.xaxis.set_minor_formatter(NullFormatter())
    axis.set_xlabel("dimension $n$")
    axis.set_ylabel(r"$|\lambda_n-\lambda_{\rm R}|$")
    axis.set_title("(a) The negative branch is numerically second order")
    axis.legend(frameon=False)
    ratio = certificate["parity_convergence"]["increment_ratio_upper"]
    disagreement = certificate["parity_convergence"][
        "richardson_disagreement_upper"
    ]
    axis.text(
        0.04,
        0.05,
        rf"$\Delta_2/\Delta_1\leq {ratio:.9f}$" + "\n" + rf"$|R_2-R_1|\leq {disagreement:.2e}$",
        transform=axis.transAxes,
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "0.8", "alpha": 0.9},
    )

    axis = axes[0, 1]
    names = [
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    ]
    short = ["$E$", "$C$", "$B$", "$D$"]
    ratio_rows = certificate["exact_stored_frobenius_ratios"]
    lower = np.asarray([ratio_rows[name]["lower"] for name in names])
    upper = np.asarray([ratio_rows[name]["upper"] for name in names])
    center = 0.5 * (lower + upper)
    target = np.asarray([0.25, 0.5, 0.5, 0.25])
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    axis.bar(np.arange(4), center, color=colors, alpha=0.82)
    axis.errorbar(
        np.arange(4),
        center,
        yerr=np.vstack((center - lower, upper - center)),
        fmt="none",
        color="black",
        capsize=3,
        linewidth=1.0,
    )
    axis.scatter(np.arange(4), target, marker="_", s=420, color="black", label="quarter/half target")
    axis.set_xticks(np.arange(4), short)
    axis.set_ylim(0.0, 0.56)
    axis.set_ylabel("second/first Frobenius ratio")
    axis.set_title("(b) Arb closes the exact-stored quarter--half ledger")
    axis.legend(frameon=False, loc="upper center")

    axis = axes[1, 0]
    renormalized = certificate["renormalized_exact_stored_frobenius"]
    refinements = ["2048_to_4096", "4096_to_8192"]
    for name, label, color in zip(names, short, colors, strict=True):
        values = [
            0.5
            * (
                renormalized[refinement][name]["lower"]
                + renormalized[refinement][name]["upper"]
            )
            for refinement in refinements
        ]
        exponent = 2 if name in {"coarse_consistency", "detail_block"} else 1
        axis.plot(
            [0, 1],
            values,
            marker="o",
            color=color,
            label=rf"{label} / $h^{exponent}$",
        )
    axis.set_yscale("log")
    axis.set_xticks([0, 1], [r"$2048\to4096$", r"$4096\to8192$"])
    axis.set_ylabel("renormalized exact-stored Frobenius norm")
    axis.set_title("(c) The renormalized constants are level-stable")
    axis.legend(frameon=False, ncol=2)

    axis = axes[1, 1]
    parity_radius = np.abs(parity)
    bulk_radius = np.asarray([row["observed_bulk_radius"] for row in levels])
    axis.plot(dimensions, parity_radius, marker="o", color="tab:blue", label=r"$|\lambda_{\rm parity}|$")
    axis.plot(dimensions, bulk_radius, marker="s", color="tab:orange", label="observed bulk radius")
    axis.fill_between(dimensions, bulk_radius, parity_radius, color="tab:blue", alpha=0.08)
    axis.set_xticks(dimensions, level_labels)
    axis.set_xlabel("dimension $n$")
    axis.set_ylabel("spectral radius")
    axis.set_ylim(0.62, 1.02)
    second = axis.twinx()
    residual = np.asarray(
        [
            max(
                value
                for mode in row["residuals"].values()
                for value in mode.values()
            )
            for row in levels
        ]
    )
    gram = np.asarray(
        [
            certificate["exact_stored_biorthogonality"][label][
                "two_norm_defect_upper"
            ]
            for label in level_labels
        ]
    )
    second.semilogy(dimensions, residual, marker="^", linestyle=":", color="tab:green", label="max eigen residual")
    second.semilogy(dimensions, gram, marker="v", linestyle=":", color="tab:red", label=r"$\|L^TR-I\|_2$ upper")
    second.set_ylabel("floating / exact-stored diagnostic")
    second.set_ylim(3.0e-16, 2.0e-14)
    handles, labels = axis.get_legend_handles_labels()
    handles2, labels2 = second.get_legend_handles_labels()
    axis.legend(handles + handles2, labels + labels2, frameon=False, loc="center right")
    axis.set_title("(d) Observed isolation is stable but remains non-validated")

    output_dir = ROOT / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_dir / "weighted_riesz_projector_bridge.png", dpi=220)
    figure.savefig(output_dir / "weighted_riesz_projector_bridge.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
