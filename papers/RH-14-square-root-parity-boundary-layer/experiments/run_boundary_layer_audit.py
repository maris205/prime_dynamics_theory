"""Generate the square-root spectral audit, profiles, tables, and figures."""

from __future__ import annotations

import argparse
import csv
import ctypes
import gc
import hashlib
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy

from parity_boundary import (
    R_FIXED,
    component_density,
    endpoint_density_profile,
    parity_boundary_profile,
    parity_eigenvectors,
    peripheral_spectrum,
    positive_midpoints,
    sparse_folded_gaussian_matrix,
    square_root_gap_constant,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

NOISE_SETTINGS = (
    (0.0300, 683),
    (0.0200, 1024),
    (0.0150, 1366),
    (0.0120, 1707),
    (0.0100, 2048),
    (0.0080, 2560),
    (0.0060, 3414),
    (0.0050, 4096),
    (0.0040, 5120),
    (0.0030, 6827),
    (0.0020, 10240),
    (0.0015, 13654),
    (0.0010, 20480),
    (0.0005, 40960),
    (0.0002, 102400),
    (0.0001, 204800),
)


def release_memory() -> None:
    """Return large sparse-work buffers to glibc between resolutions."""

    gc.collect()
    try:
        ctypes.CDLL(None).malloc_trim(0)
    except (AttributeError, OSError):
        pass


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def spectral_audit(constant: float) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    previous_sigma: float | None = None
    previous_gap: float | None = None
    for index, (sigma, dimension) in enumerate(NOISE_SETTINGS, start=1):
        print(
            f"spectrum {index}/{len(NOISE_SETTINGS)}: sigma={sigma:g}, n={dimension}",
            flush=True,
        )
        started = time.time()
        matrix = sparse_folded_gaussian_matrix(dimension, sigma)
        build_seconds = time.time() - started
        row_error = float(
            np.max(np.abs(np.asarray(matrix.sum(axis=1)).ravel() - 1.0))
        )
        started = time.time()
        spectrum = peripheral_spectrum(matrix)
        eigensolve_seconds = time.time() - started
        gap = spectrum.parity_gap
        if previous_sigma is None or previous_gap is None:
            local_exponent: float | str = ""
        else:
            local_exponent = float(
                np.log(gap / previous_gap) / np.log(sigma / previous_sigma)
            )
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "dimension_times_sigma": dimension * sigma,
                "nonzeros": matrix.nnz,
                "row_sum_error": row_error,
                "perron_real": spectrum.perron.real,
                "perron_imag": spectrum.perron.imag,
                "parity_real": spectrum.parity.real,
                "parity_imag": spectrum.parity.imag,
                "parity_gap": gap,
                "gap_over_sqrt_sigma": gap / np.sqrt(sigma),
                "gap_over_sigma_two_thirds": gap / sigma ** (2.0 / 3.0),
                "relative_error_to_square_root_constant": gap
                / (constant * np.sqrt(sigma))
                - 1.0,
                "local_power_exponent": local_exponent,
                "parity_efolding_lifetime": -1.0 / np.log(abs(spectrum.parity)),
                "observed_bulk_radius": spectrum.bulk_radius_observed,
                "build_seconds": build_seconds,
                "eigensolve_seconds": eigensolve_seconds,
            }
        )
        previous_sigma = sigma
        previous_gap = gap
        del matrix
        release_memory()
    write_csv(RESULTS / "square_root_spectrum.csv", rows)
    return rows


def resolution_audit() -> list[dict[str, object]]:
    sigma = 0.001
    dimensions = (10240, 15360, 20480, 25600, 30720)
    raw: list[tuple[int, float, float]] = []
    for dimension in dimensions:
        print(f"resolution: sigma={sigma:g}, n={dimension}", flush=True)
        matrix = sparse_folded_gaussian_matrix(dimension, sigma)
        spectrum = peripheral_spectrum(matrix, eigenvalue_count=4)
        raw.append((dimension, spectrum.parity.real, spectrum.parity_gap))
        del matrix
        release_memory()
    reference = raw[-1][1]
    rows = [
        {
            "sigma": sigma,
            "folded_dimension": dimension,
            "dimension_times_sigma": dimension * sigma,
            "parity_real": parity,
            "parity_difference_from_finest": parity - reference,
            "gap_over_sqrt_sigma": gap / np.sqrt(sigma),
        }
        for dimension, parity, gap in raw
    ]
    write_csv(RESULTS / "square_root_resolution.csv", rows)
    return rows


def profile_audit(rho_c: float) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    sigma = 0.001
    dimension = 20480
    print(f"profiles: sigma={sigma:g}, n={dimension}", flush=True)
    matrix = sparse_folded_gaussian_matrix(dimension, sigma)
    eigenvectors = parity_eigenvectors(matrix, sigma)
    grid = positive_midpoints(dimension)

    parity_rows: list[dict[str, object]] = []
    for requested in np.linspace(-4.0, 4.0, 33):
        target = R_FIXED + sigma * requested
        index = int(np.argmin(np.abs(grid - target)))
        actual = (grid[index] - R_FIXED) / sigma
        parity_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "requested_xi": requested,
                "actual_xi": actual,
                "observed_parity_observable": eigenvectors.right_observable[index],
                "boundary_layer_profile": float(parity_boundary_profile(actual)),
                "difference": eigenvectors.right_observable[index]
                - float(parity_boundary_profile(actual)),
            }
        )
    write_csv(RESULTS / "parity_boundary_profile.csv", parity_rows)

    density_rows: list[dict[str, object]] = []
    for requested in (0.125, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0):
        target = 1.0 - sigma * requested
        index = int(np.argmin(np.abs(grid - target)))
        actual = (1.0 - grid[index]) / sigma
        observed = (
            -np.sqrt(sigma)
            * eigenvectors.left_cell_masses[index]
            * dimension
        )
        predicted = endpoint_density_profile(actual, rho_c=rho_c)
        density_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "requested_xi": requested,
                "actual_xi": actual,
                "observed_scaled_signed_density": observed,
                "critical_endpoint_profile": predicted,
                "relative_difference": observed / predicted - 1.0,
            }
        )
    write_csv(RESULTS / "critical_endpoint_profile.csv", density_rows)
    del matrix
    release_memory()
    return parity_rows, density_rows


def fit_power(rows: list[dict[str, object]], first_sigma: float, last_sigma: float) -> tuple[float, float]:
    chosen = [
        row
        for row in rows
        if last_sigma <= float(row["sigma"]) <= first_sigma
    ]
    sigma = np.asarray([float(row["sigma"]) for row in chosen])
    gap = np.asarray([float(row["parity_gap"]) for row in chosen])
    exponent, log_amplitude = np.polyfit(np.log(sigma), np.log(gap), 1)
    return float(exponent), float(np.exp(log_amplitude))


def plot_audit(
    spectral_rows: list[dict[str, object]],
    parity_rows: list[dict[str, object]],
    density_rows: list[dict[str, object]],
    constant: float,
) -> None:
    sigma = np.asarray([float(row["sigma"]) for row in spectral_rows])
    gap = np.asarray([float(row["parity_gap"]) for row in spectral_rows])
    scaled = gap / np.sqrt(sigma)
    local_sigma = np.sqrt(sigma[1:] * sigma[:-1])
    local_power = np.asarray(
        [float(row["local_power_exponent"]) for row in spectral_rows[1:]]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))
    order = np.argsort(sigma)
    axes[0, 0].loglog(sigma[order], gap[order], "o-", color="#2455a4", ms=4, label="sparse spectra")
    reference_sigma = np.geomspace(sigma.min(), sigma.max(), 300)
    axes[0, 0].loglog(reference_sigma, constant * np.sqrt(reference_sigma), "--", color="#a0273f", label=fr"$C_*\sigma^{{1/2}}$, $C_*={constant:.6f}$")
    old_amplitude = float(gap[np.argmin(abs(sigma - 0.01))] / 0.01 ** (2.0 / 3.0))
    axes[0, 0].loglog(reference_sigma, old_amplitude * reference_sigma ** (2.0 / 3.0), ":", color="#777777", label=r"old $\sigma^{2/3}$ reference")
    axes[0, 0].set(xlabel=r"noise $\sigma$", ylabel=r"$1+\lambda_-(\sigma)$", title="Parity splitting law")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22, which="both")

    axes[0, 1].semilogx(local_sigma, local_power, "o-", color="#2455a4", ms=4)
    axes[0, 1].axhline(0.5, color="#a0273f", ls="--", label=r"$1/2$")
    axes[0, 1].axhline(2.0 / 3.0, color="#777777", ls=":", label=r"$2/3$")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(xlabel=r"geometric-mean noise", ylabel="local log--log exponent", title="The apparent exponent crosses over")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22, which="both")

    pxi = np.asarray([float(row["actual_xi"]) for row in parity_rows])
    pobs = np.asarray([float(row["observed_parity_observable"]) for row in parity_rows])
    ptheory = np.asarray([float(row["boundary_layer_profile"]) for row in parity_rows])
    profile_sigma = float(parity_rows[0]["sigma"])
    axes[1, 0].plot(pxi, pobs, "o", color="#2455a4", ms=4, label=fr"$\sigma={profile_sigma:g}$")
    axes[1, 0].plot(pxi, ptheory, "-", color="#a0273f", label=r"$-\operatorname{erf}(\kappa\xi)$")
    axes[1, 0].set(xlabel=r"boundary coordinate $\xi=(x-r)/\sigma$", ylabel="parity observable", title="Repelling-boundary eigenprofile")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    dxi = np.asarray([float(row["actual_xi"]) for row in density_rows])
    dobs = np.asarray([float(row["observed_scaled_signed_density"]) for row in density_rows])
    dtheory = np.asarray([float(row["critical_endpoint_profile"]) for row in density_rows])
    axes[1, 1].plot(dxi, dobs, "o", color="#2455a4", ms=4, label=r"$\sqrt{\sigma}\,|\nu_{\sigma,-}|$")
    axes[1, 1].plot(dxi, dtheory, "-", color="#a0273f", label=r"$R(\xi)$")
    axes[1, 1].set(xlabel=r"endpoint coordinate $\xi=(1-x)/\sigma$", ylabel="scaled density", title="Critical-value endpoint layer")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(
            FIGURES / f"square_root_parity_boundary_layer.{suffix}",
            dpi=220,
            bbox_inches="tight",
        )
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(6.5, 4.2))
    axis.plot(np.sqrt(sigma[order]), scaled[order], "o-", color="#2455a4", label=r"$(1+\lambda_-)/\sqrt{\sigma}$")
    axis.axhline(constant, color="#a0273f", ls="--", label=fr"$C_*={constant:.9f}$")
    axis.set(xlabel=r"$\sqrt{\sigma}$", ylabel="scaled parity gap", title="Convergence to the boundary-layer constant")
    axis.legend(frameon=False)
    axis.grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"square_root_constant_convergence.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reuse-results",
        action="store_true",
        help="reuse existing CSV eigendata and regenerate only figures/summary",
    )
    arguments = parser.parse_args()
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    density80 = component_density(80)
    density120 = component_density(120)
    density160 = component_density(160)
    constant_data = square_root_gap_constant(rho_c=density120.interval_density_at_zero)

    if arguments.reuse_results:
        parity_rows = read_csv(RESULTS / "parity_boundary_profile.csv")
        density_rows = read_csv(RESULTS / "critical_endpoint_profile.csv")
        resolution_rows = read_csv(RESULTS / "square_root_resolution.csv")
        spectral_rows = read_csv(RESULTS / "square_root_spectrum.csv")
    else:
        parity_rows, density_rows = profile_audit(constant_data.rho_c)
        resolution_rows = resolution_audit()
        spectral_rows = spectral_audit(constant_data.value)
    old_exponent, old_amplitude = fit_power(spectral_rows, 0.03, 0.01)
    new_exponent, new_amplitude = fit_power(spectral_rows, 0.002, 0.0001)
    plot_audit(spectral_rows, parity_rows, density_rows, constant_data.value)

    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "source_sha256": {
            "operators.py": source_hash(ROOT / "src" / "parity_boundary" / "operators.py"),
            "boundary_layer.py": source_hash(ROOT / "src" / "parity_boundary" / "boundary_layer.py"),
        },
        "deterministic_density": {
            "degree_80": density80.interval_density_at_zero,
            "degree_120": density120.interval_density_at_zero,
            "degree_160": density160.interval_density_at_zero,
            "analytic_factor_at_zero": density120.analytic_value_at_zero,
        },
        "boundary_layer_constant": {
            "rho_c": constant_data.rho_c,
            "kappa": constant_data.kappa,
            "endpoint_rate": constant_data.endpoint_rate,
            "value": constant_data.value,
            "quadrature_error_estimate": constant_data.quadrature_error,
        },
        "spectral_crossover": {
            "old_window": [0.03, 0.01],
            "old_window_power": old_exponent,
            "old_window_amplitude": old_amplitude,
            "new_window": [0.002, 0.0001],
            "new_window_power": new_exponent,
            "new_window_amplitude": new_amplitude,
            "smallest_sigma": float(spectral_rows[-1]["sigma"]),
            "smallest_gap": float(spectral_rows[-1]["parity_gap"]),
            "smallest_scaled_gap": float(spectral_rows[-1]["gap_over_sqrt_sigma"]),
            "smallest_local_power": float(spectral_rows[-1]["local_power_exponent"]),
        },
        "resolution": {
            "sigma": 0.001,
            "maximum_parity_spread": max(
                abs(float(row["parity_difference_from_finest"]))
                for row in resolution_rows
            ),
        },
        "theorem_target": {
            "law": "1+lambda_-(sigma)=C_* sqrt(sigma)+o(sqrt(sigma))",
            "constant_positive": constant_data.value > 0.0,
            "two_thirds_consequence": "(1+lambda_-)/sigma^(2/3) diverges",
            "parity_lifetime": "m_parity ~ 1/(C_* sqrt(sigma))",
        },
    }
    with (RESULTS / "square_root_boundary_layer_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
