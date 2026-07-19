"""Render the RH-46 mesh-law and squared-cloud summary figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "small_noise_mesh_double_pole_certificate.json"
ROW_PILOT = ROOT / "results" / "gaussian_row_projection_pilot.json"
CLOUD_PILOT = ROOT / "results" / "two_step_square_cloud_pilot.json"
FIGURES = ROOT / "figures"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    certificate = load(CERTIFICATE)
    row_pilot = load(ROW_PILOT)
    cloud_pilot = load(CLOUD_PILOT)
    sigmas = np.asarray(
        sorted(
            float(value)
            for value in certificate["uniform_gaussian_envelope"]["rows"]
        )
    )

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "legend.fontsize": 9,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(13.5, 9.8))

    axis = axes[0, 0]
    for power, style in (("1.0", "o-"), ("1.5", "s-"), ("2.0", "^-"), ("2.5", "D-")):
        schedule = certificate["power_schedule_audit"][power]["rows"]
        values = np.asarray(
            [
                schedule[str(sigma)]["fixed_disk"][
                    "galerkin_hilbert_schmidt_error_upper"
                ]
                for sigma in sigmas
            ]
        )
        axis.loglog(sigmas, values, style, label=rf"$p={power}$")
    axis.axhline(1.0, color="0.35", linestyle=":", linewidth=1.0)
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel(r"upper bound for $\|K_{n,\sigma}-K_\sigma\|_{\mathrm{HS}}$")
    axis.set_title("(a) One-step mesh powers")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()

    axis = axes[0, 1]
    for power, style in (("1.5", "s-"), ("2.0", "^-"), ("2.25", "v-"), ("2.5", "D-")):
        schedule = certificate["power_schedule_audit"][power]["rows"]
        values = np.asarray(
            [
                schedule[str(sigma)]["fixed_disk"][
                    "square_trace_norm_error_upper"
                ]
                for sigma in sigmas
            ]
        )
        axis.loglog(sigmas, values, style, label=rf"$p={power}$")
    axis.axhline(1.0, color="0.35", linestyle=":", linewidth=1.0)
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel(r"upper bound for $\|K_{n,\sigma}^2-K_\sigma^2\|_1$")
    axis.set_title("(b) Two-step trace-norm threshold")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()

    axis = axes[1, 0]
    ratios = np.asarray(
        [row["cell_to_sigma_ratio"] for row in row_pilot["rows"]]
    )
    scaled = np.asarray(
        [
            row["mean_error_divided_by_cell_ratio"]
            for row in row_pilot["rows"]
        ]
    )
    constant = float(row_pilot["asymptotic_constant"])
    axis.semilogx(ratios, scaled, "o-", label="exact cell masses")
    axis.axhline(constant, color="#a0273f", linestyle="--", label="asymptotic constant")
    axis.set_xlabel(r"cell ratio $h/\sigma$")
    axis.set_ylabel(r"$\sigma^{1/2}\,\mathrm{error}/(h/\sigma)$")
    axis.set_title("(c) Sharp Gaussian-row exponent")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend()

    axis = axes[1, 1]
    level = cloud_pilot["levels"]["0.0001"]
    coordinates = np.asarray([row["coordinate"] for row in level["rows"]])
    observed = np.asarray([row["observed_real"] for row in level["rows"]])
    finite = np.asarray(
        [row["finite_geometric_real"] for row in level["rows"]]
    )
    universal = np.asarray([row["universal_real"] for row in level["rows"]])
    axis.plot(coordinates, observed, "o-", label="squared noisy cloud")
    axis.plot(coordinates, finite, "s--", label=r"$\Pi_7^2$ finite section")
    axis.plot(coordinates, universal, color="0.25", linestyle=":", label="squared universal profile")
    axis.set_xlabel(r"edge coordinate $s$")
    axis.set_ylabel("normalized two-step cloud factor")
    axis.set_title(r"(d) Two-step scattering at $\sigma=10^{-4}$ (floating)")
    axis.grid(True, alpha=0.25)
    axis.legend()

    figure.suptitle(
        "Small-noise mesh laws and the bulk two-step double-pole obstruction",
        fontsize=14,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    FIGURES.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        FIGURES / "small_noise_mesh_double_pole.png",
        dpi=220,
        bbox_inches="tight",
    )
    figure.savefig(
        FIGURES / "small_noise_mesh_double_pole.pdf",
        bbox_inches="tight",
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
