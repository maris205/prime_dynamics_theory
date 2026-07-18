"""Render the fixed-window and adaptive-cutoff bridge diagnostics."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cutoff_bridge import adaptive_cutoff_multiple, cutoff_bound  # noqa: E402


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(ROOT / "results" / "cutoff_pilot_sigma_1e-02.json")
    certificate = load(
        ROOT / "results" / "uniform_gaussian_cutoff_bridge_certificate.json"
    )
    rows = pilot["dimensions"]
    dimensions = np.asarray([int(row["dimension"]) for row in rows])
    continuum_tail = certificate["fixed_eight_sigma_nonvanishing_limit"][
        "mean_zero_continuum_omitted_mass_upper"
    ]
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 160,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.2), constrained_layout=True)

    axis = axes[0, 0]
    axis.plot(
        dimensions,
        [row["maximum_omitted_mass"] for row in rows],
        marker="o",
        label="floating maximum",
    )
    axis.plot(
        dimensions,
        [row["analytic_omitted_mass_upper"] for row in rows],
        marker="s",
        label="analytic upper",
    )
    axis.axhline(
        continuum_tail,
        color="black",
        linestyle="--",
        linewidth=0.9,
        label=r"fixed-$8\sigma$ continuum tail",
    )
    axis.set_yscale("log")
    axis.set_xticks(dimensions, [str(value) for value in dimensions])
    axis.set_xlabel("dimension")
    axis.set_ylabel("omitted full-row mass")
    axis.set_title("(a) The fixed cutoff has a nonzero tail floor")
    axis.legend(frameon=False)

    axis = axes[0, 1]
    axis.plot(
        dimensions,
        [row["schur_two_norm_upper"] for row in rows],
        marker="o",
        label="floating Schur upper",
    )
    axis.plot(
        dimensions,
        [row["frobenius_norm"] for row in rows],
        marker="^",
        label="floating Frobenius",
    )
    axis.plot(
        dimensions,
        [row["analytic_two_norm_upper"] for row in rows],
        marker="s",
        label="Arb analytic upper",
    )
    axis.set_yscale("log")
    axis.set_xticks(dimensions, [str(value) for value in dimensions])
    axis.set_xlabel("dimension")
    axis.set_ylabel(r"full-versus-cutoff norm")
    axis.set_title(r"(b) The Euclidean bridge is below $2\times10^{-13}$")
    axis.legend(frameon=False)

    axis = axes[1, 0]
    schedule_dimensions = np.logspace(2.1, 8.0, 240)
    adaptive = np.sqrt(4.0 * np.log(schedule_dimensions))
    adaptive = np.maximum(5.0, adaptive)
    axis.semilogx(
        schedule_dimensions,
        adaptive,
        color="tab:blue",
        label=r"$L(h)=\max\{5,2\sqrt{\log(1/h)}\}$",
    )
    axis.axhline(8.0, color="tab:red", linestyle="--", label="archived $L=8$")
    crossover = float(np.exp(16.0))
    axis.axvline(crossover, color="gray", linestyle=":", linewidth=1.0)
    axis.text(
        crossover * 0.93,
        5.15,
        r"$e^{16}\approx8.89\times10^6$",
        rotation=90,
        va="bottom",
        ha="right",
        color="dimgray",
    )
    axis.scatter(dimensions, [8.0] * len(dimensions), color="black", s=16, zorder=4)
    axis.set_xlabel("dimension $n=1/h$")
    axis.set_ylabel("support multiple $L$")
    axis.set_title("(c) Eight sigma dominates the sufficient schedule so far")
    axis.legend(frameon=False, loc="upper left")

    axis = axes[1, 1]
    powers = np.arange(10, 25)
    scaling_dimensions = 2**powers
    fixed_ratios = []
    adaptive_ratios = []
    for dimension in scaling_dimensions:
        h = 1.0 / int(dimension)
        fixed_ratios.append(cutoff_bound(int(dimension), 0.01, 8.0).two_norm_upper / h**2)
        multiple = adaptive_cutoff_multiple(h)
        adaptive_ratios.append(
            cutoff_bound(int(dimension), 0.01, multiple).two_norm_upper / h**2
        )
    axis.loglog(
        scaling_dimensions,
        fixed_ratios,
        marker="o",
        markersize=3,
        label=r"fixed $L=8$",
    )
    axis.loglog(
        scaling_dimensions,
        adaptive_ratios,
        marker="s",
        markersize=3,
        label="adaptive schedule",
    )
    axis.set_xlabel("dimension $n=1/h$")
    axis.set_ylabel(r"analytic $\varepsilon_h/h^2$")
    axis.set_title("(d) Adaptive growth restores a second-order bridge")
    axis.legend(frameon=False)

    output_dir = ROOT / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_dir / "uniform_gaussian_cutoff_bridge.png", dpi=220)
    figure.savefig(output_dir / "uniform_gaussian_cutoff_bridge.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
