"""Generate boundary-ladder, Hellinger-rank, and cloud-comparison audits."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath
import numpy as np
import scipy

from endpoint_rank import (
    CONTRACTION_FIXED,
    HALF_ENERGY_THRESHOLD,
    LAMBDA_FIXED,
    boundary_clearances,
    boundary_ratios,
    endpoint_residual_energy,
    half_logarithmic_clock,
    hilbert_schmidt_energy,
    resolution_singular_values,
    scaled_boundary_constants,
    threshold_rank,
)


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RANK_NOISE = np.logspace(-2.0, -14.0, 49)
SPECTRUM_NOISE = (1.0e-2, 1.0e-4, 1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12)
THRESHOLD_AUDIT = (0.60, HALF_ENERGY_THRESHOLD, 0.80)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def boundary_rows(clearances: np.ndarray) -> list[dict[str, object]]:
    ratios = boundary_ratios(clearances)
    scaled = scaled_boundary_constants(clearances)
    rows: list[dict[str, object]] = []
    for offset, clearance in enumerate(clearances, start=1):
        rows.append(
            {
                "component_index": offset,
                "original_period": 2 * offset,
                "clearance": clearance,
                "successive_ratio": "" if offset == 1 else ratios[offset - 2],
                "limiting_ratio": CONTRACTION_FIXED,
                "clearance_times_lambda_2k": scaled[offset - 1],
            }
        )
    return rows


def rank_rows(clearances: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sigma in RANK_NOISE:
        clock = float(half_logarithmic_clock(sigma))
        singular_values = resolution_singular_values(clearances, sigma)
        rank = int(np.count_nonzero(singular_values > HALF_ENERGY_THRESHOLD))
        energy = hilbert_schmidt_energy(clearances, sigma)
        linear_values = resolution_singular_values(clearances, sigma, power=1.0)
        linear_rank = int(
            np.count_nonzero(linear_values > HALF_ENERGY_THRESHOLD)
        )
        linear_energy = hilbert_schmidt_energy(clearances, sigma, power=1.0)
        above = singular_values[rank - 1] if rank else np.nan
        below = singular_values[rank] if rank < singular_values.size else np.nan
        rows.append(
            {
                "sigma": sigma,
                "half_logarithmic_clock": clock,
                "half_energy_rank": rank,
                "rank_defect": rank - clock,
                "hilbert_schmidt_energy": energy,
                "energy_defect": energy - clock,
                "linear_row_half_energy_rank": linear_rank,
                "linear_row_rank_defect": linear_rank - clock,
                "linear_row_hilbert_schmidt_energy": linear_energy,
                "linear_row_energy_defect": linear_energy - clock,
                "last_singular_above_threshold": above,
                "first_singular_below_threshold": below,
                "threshold": HALF_ENERGY_THRESHOLD,
            }
        )
    return rows


def spectrum_rows(clearances: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sigma in SPECTRUM_NOISE:
        values = resolution_singular_values(clearances, sigma)
        for index, value in enumerate(values[:40], start=1):
            rows.append(
                {
                    "sigma": sigma,
                    "singular_index": index,
                    "singular_value": value,
                    "above_half_energy": int(value > HALF_ENERGY_THRESHOLD),
                }
            )
    return rows


def cloud_comparison_rows(clearances: np.ndarray) -> list[dict[str, object]]:
    source = (
        PAPERS
        / "RH-15-parity-extracted-bulk-scattering"
        / "results"
        / "cloud_summary.csv"
    )
    rows: list[dict[str, object]] = []
    for archived in read_csv(source):
        sigma = float(archived["sigma"])
        cloud_degree = int(float(archived["effective_cloud_degree"]))
        model_rank = threshold_rank(clearances, sigma)
        row: dict[str, object] = {
            "sigma": sigma,
            "folded_dimension": int(float(archived["folded_dimension"])),
            "half_logarithmic_clock": float(half_logarithmic_clock(sigma)),
            "cloud_degree": cloud_degree,
            "half_energy_rank": model_rank,
            "rank_minus_cloud_degree": model_rank - cloud_degree,
            "cloud_phase_rms": float(archived["cloud_phase_rms_error"]),
        }
        for threshold in THRESHOLD_AUDIT:
            label = f"rank_at_{threshold:.6f}".replace(".", "p")
            row[label] = threshold_rank(
                clearances,
                sigma,
                threshold=threshold,
            )
        rows.append(row)
    return rows


def truncation_rows(clearances: np.ndarray) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sigma = 1.0e-8
    for tail_ratio in (1.0e-4, 1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12):
        values = resolution_singular_values(
            clearances,
            sigma,
            tail_ratio=tail_ratio,
        )
        rows.append(
            {
                "sigma": sigma,
                "tail_ratio": tail_ratio,
                "retained_columns": int(np.count_nonzero(clearances / sigma >= tail_ratio)),
                "half_energy_rank": int(
                    np.count_nonzero(values > HALF_ENERGY_THRESHOLD)
                ),
                "largest_singular_value": values[0],
            }
        )
    return rows


def plot_audit(
    clearances: np.ndarray,
    ranks: list[dict[str, object]],
    spectra: list[dict[str, object]],
    cloud: list[dict[str, object]],
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.7))
    indices = np.arange(1, clearances.size + 1)
    scaled = scaled_boundary_constants(clearances)
    asymptotic_constant = float(np.mean(scaled[-10:]))
    asymptotic = asymptotic_constant * CONTRACTION_FIXED**indices
    axes[0, 0].semilogy(indices, clearances, "o-", ms=3.2, label=r"exact $\delta_k$")
    axes[0, 0].semilogy(indices, asymptotic, "--", label=rf"${asymptotic_constant:.6f}\,\lambda^{{-2k}}$")
    axes[0, 0].set(
        xlabel=r"component index $k$",
        ylabel=r"endpoint clearance $\delta_k$",
        title="Geometric boundary ladder",
    )
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    ratio = np.logspace(-4.0, 1.3, 400)
    energy = endpoint_residual_energy(ratio)
    coefficient = (np.pi - 2.0) / (4.0 * np.pi)
    axes[0, 1].loglog(ratio, energy, color="#2455a4", label=r"$F(t)=\|Q\psi_t\|_2^2$")
    axes[0, 1].loglog(ratio, coefficient * ratio**2, "--", color="#a0273f", label=r"$[(\pi-2)/(4\pi)]t^2$")
    axes[0, 1].axhline(0.5, color="0.35", ls=":", label="half energy")
    axes[0, 1].set(
        xlabel=r"dimensionless clearance $t=\delta/\sigma$",
        ylabel="endpoint-projected energy",
        title="Exact conditioned-Gaussian transition",
        ylim=(1.0e-9, 1.3),
    )
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    colors = plt.cm.viridis(np.linspace(0.08, 0.90, len(SPECTRUM_NOISE)))
    for sigma, color in zip(SPECTRUM_NOISE, colors):
        selected = [row for row in spectra if float(row["sigma"]) == sigma]
        axes[1, 0].plot(
            [int(row["singular_index"]) for row in selected],
            [float(row["singular_value"]) for row in selected],
            "o-",
            ms=2.8,
            color=color,
            label=rf"$\sigma={sigma:.0e}$",
        )
    axes[1, 0].axhline(HALF_ENERGY_THRESHOLD, color="#a0273f", ls="--", label=r"$2^{-1/2}$")
    axes[1, 0].set(
        xlabel="singular-value index",
        ylabel=r"$s_j(\mathcal{R}_\sigma)$",
        title="Growing unit singular-value plateau",
        xlim=(0.5, 31),
        ylim=(-0.03, 1.18),
    )
    axes[1, 0].legend(frameon=False, fontsize=7, ncol=2)
    axes[1, 0].grid(alpha=0.22)

    sigma = np.asarray([float(row["sigma"]) for row in ranks])
    order = np.argsort(sigma)[::-1]
    clock = np.asarray([float(row["half_logarithmic_clock"]) for row in ranks])
    rank = np.asarray([float(row["half_energy_rank"]) for row in ranks])
    hs_energy = np.asarray([float(row["hilbert_schmidt_energy"]) for row in ranks])
    axes[1, 1].semilogx(sigma[order], clock[order], "k--", label=r"$\log(1/\sigma)/(2\log\lambda)$")
    axes[1, 1].semilogx(sigma[order], hs_energy[order], color="#3a8f6b", label=r"$\|\mathcal{R}_\sigma\|_{S_2}^2$")
    axes[1, 1].step(sigma[order], rank[order], where="post", color="#2455a4", label="half-energy rank")
    cloud_sigma = np.asarray([float(row["sigma"]) for row in cloud])
    cloud_degree = np.asarray([float(row["cloud_degree"]) for row in cloud])
    axes[1, 1].plot(cloud_sigma, cloud_degree, "x", ms=6, mew=1.5, color="#a0273f", label="RH-15 cloud degree")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="effective dimension",
        title="Analytic clock and archived cloud counts",
    )
    axes[1, 1].legend(frameon=False, fontsize=7.5)
    axes[1, 1].grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"endpoint_gaussian_resolution_rank.{suffix}",
            dpi=220,
            bbox_inches="tight",
        )
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.0))
    phase = np.mod(half_logarithmic_clock(sigma), 1.0)
    axes[0].plot(phase, rank - clock, "o", ms=4, label="rank defect")
    axes[0].plot(phase, hs_energy - clock, ".", ms=5, label=r"$S_2$-energy defect")
    axes[0].set(
        xlabel="fractional half-logarithmic phase",
        ylabel="quantity minus clock",
        title="Bounded log-periodic staircase defect",
    )
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(alpha=0.22)

    model = np.asarray([float(row["half_energy_rank"]) for row in cloud])
    axes[1].plot([2, 8], [2, 8], "k--", lw=1.0, label="equality")
    axes[1].plot(cloud_degree, model, "o", color="#2455a4")
    for row in cloud:
        sigma_value = float(row["sigma"])
        offset = (4, 4)
        if abs(sigma_value - 1.0e-3) < 1.0e-14:
            offset = (4, -12)
        elif abs(sigma_value - 5.0e-4) < 1.0e-14:
            offset = (4, 12)
        elif abs(sigma_value - 1.0e-4) < 1.0e-14:
            offset = (-36, 8)
        axes[1].annotate(
            f"{sigma_value:.0e}",
            (float(row["cloud_degree"]), float(row["half_energy_rank"])),
            xytext=offset,
            textcoords="offset points",
            fontsize=7,
        )
    axes[1].set(
        xlabel="archived RH-15 cloud degree",
        ylabel="half-energy endpoint rank",
        title="No fitted scale or threshold",
        xlim=(1.7, 7.4),
        ylim=(1.7, 7.4),
        aspect="equal",
    )
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"rank_defect_cloud_comparison.{suffix}",
            dpi=220,
            bbox_inches="tight",
        )
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    clearances = boundary_clearances(80, decimal_digits=110)
    boundary = boundary_rows(clearances[:60])
    ranks = rank_rows(clearances)
    spectra = spectrum_rows(clearances)
    cloud = cloud_comparison_rows(clearances)
    truncation = truncation_rows(clearances)

    write_csv(RESULTS / "boundary_ladder.csv", boundary)
    write_csv(RESULTS / "endpoint_rank_summary.csv", ranks)
    write_csv(RESULTS / "endpoint_singular_values.csv", spectra)
    write_csv(RESULTS / "cloud_rank_comparison.csv", cloud)
    write_csv(RESULTS / "rank_tail_resolution.csv", truncation)
    plot_audit(clearances, ranks, spectra, cloud)

    rank_defects = np.asarray([float(row["rank_defect"]) for row in ranks])
    energy_defects = np.asarray([float(row["energy_defect"]) for row in ranks])
    linear_rank_defects = np.asarray(
        [float(row["linear_row_rank_defect"]) for row in ranks]
    )
    linear_energy_defects = np.asarray(
        [float(row["linear_row_energy_defect"]) for row in ranks]
    )
    cloud_differences = np.asarray(
        [int(row["rank_minus_cloud_degree"]) for row in cloud]
    )
    scaled = scaled_boundary_constants(clearances)
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "mpmath": mpmath.__version__,
            "platform": platform.platform(),
        },
        "source_sha256": {
            "experiments/run_endpoint_rank_audit.py": source_hash(Path(__file__)),
            **{
                f"src/endpoint_rank/{name}": source_hash(
                    ROOT / "src" / "endpoint_rank" / name
                )
                for name in ("boundary.py", "hellinger.py")
            },
        },
        "analytic_results": {
            "boundary_ladder": "delta_k=C_b*lambda^(-2k)*(1+o(1))",
            "exact_affinity": "A(t,s)=exp(-(t-s)^2/8)Phi((t+s)/2)/sqrt(Phi(t)Phi(s))",
            "power_universality": "the same energy and rank laws hold for every fixed beta>0, including linear rows beta=1",
            "hilbert_schmidt_energy": "||R_sigma||_S2^2=log(1/sigma)/(2log(lambda))+O(1)",
            "threshold_rank": "#{j:s_j(R_sigma)>eta}=log(1/sigma)/(2log(lambda))+O_eta(1), 0<eta<1",
            "actual_markov_resonance_count": "not proved",
        },
        "boundary_numerics": {
            "limiting_ratio": float(CONTRACTION_FIXED),
            "asymptotic_constant": float(np.mean(scaled[-10:])),
        },
        "rank_audit": {
            "threshold": float(HALF_ENERGY_THRESHOLD),
            "rank_defect_range": [float(rank_defects.min()), float(rank_defects.max())],
            "energy_defect_range": [float(energy_defects.min()), float(energy_defects.max())],
            "linear_row_rank_defect_range": [
                float(linear_rank_defects.min()),
                float(linear_rank_defects.max()),
            ],
            "linear_row_energy_defect_range": [
                float(linear_energy_defects.min()),
                float(linear_energy_defects.max()),
            ],
            "tail_resolution_counts": [
                int(row["half_energy_rank"]) for row in truncation
            ],
        },
        "cloud_comparison": {
            "noise_levels": len(cloud),
            "exact_matches": int(np.count_nonzero(cloud_differences == 0)),
            "maximum_absolute_difference": int(np.max(np.abs(cloud_differences))),
            "differences_model_minus_cloud": cloud_differences.tolist(),
            "status": "floating-point comparison to archived RH-15 cloud selections",
        },
        "status": {
            "endpoint_rank_theorem": "analytic",
            "boundary_constant_decimal": "high-precision numerical evaluation",
            "cloud_rank_identification": "diagnostic, not a theorem",
            "shift_block_reduction": "open",
        },
    }
    with (RESULTS / "endpoint_rank_audit.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
