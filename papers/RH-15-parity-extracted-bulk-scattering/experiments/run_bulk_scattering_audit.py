"""Generate exact pole, resonance-cloud, scattering, and determinant audits."""

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

from bulk_scattering import (
    LAMBDA_FIXED,
    beta_one_reduced_matrix,
    bulk_determinant,
    cloud_det2,
    fit_outer_cloud,
    full_even_physical_trace,
    geometric_section,
    pole_removed_bulk_determinant,
    resolve_bulk_spectrum,
    scattering_profile,
    sparse_folded_gaussian_matrix,
)


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"

NOISE_SETTINGS = (
    (0.0100, 2048),
    (0.0040, 5120),
    (0.0020, 10240),
    (0.0010, 20480),
    (0.0005, 40960),
    (0.0002, 102400),
    (0.0001, 204800),
)
SCATTERING_COORDINATES = (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0)
DETERMINANT_TARGETS = (0.50, 0.75, 0.90, 1.00, 1.10, 1.20)


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


def release_memory() -> None:
    gc.collect()
    try:
        ctypes.CDLL(None).malloc_trim(0)
    except (AttributeError, OSError):
        pass


def direct_flat_trace_data() -> dict[int, float]:
    path = (
        PAPERS
        / "RH-11-collet-eckmann-flat-trace-completion"
        / "results"
        / "flat_weighted_trace_comparison.csv"
    )
    return {
        int(row["length"]): float(row["flat_trace"])
        for row in read_csv(path)
    }


def deterministic_audit() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    direct = direct_flat_trace_data()
    reduced_values = np.linalg.eigvals(beta_one_reduced_matrix(120))
    trace_rows: list[dict[str, object]] = []
    for iterate in range(1, 15):
        length = 2 * iterate
        centered_sector = float(np.sum(reduced_values**iterate).real)
        even_trace = 1.0 + centered_sector
        reconstructed = full_even_physical_trace(even_trace, iterate)
        a = LAMBDA_FIXED ** (-iterate)
        leading = -2.0 * a + a * a
        centered = reconstructed - 2.0
        reference = direct[length]
        trace_rows.append(
            {
                "component_iterate": iterate,
                "original_length": length,
                "even_beta_one_centered_trace": centered_sector,
                "reconstructed_physical_trace": reconstructed,
                "direct_periodic_physical_trace": reference,
                "reconstruction_difference": reconstructed - reference,
                "parity_centered_trace": centered,
                "endpoint_two_term_law": leading,
                "two_term_remainder": centered - leading,
                "absolute_remainder_times_three_power": abs(centered - leading)
                * 3.0**iterate,
            }
        )
    write_csv(RESULTS / "physical_trace_reconstruction.csv", trace_rows)

    pole = np.sqrt(LAMBDA_FIXED)
    z_values = np.concatenate(
        (
            np.linspace(0.0, 1.15, 60),
            np.linspace(1.16, 0.9975 * pole, 45),
        )
    )
    pole_rows: list[dict[str, object]] = []
    for z in z_values:
        determinant = bulk_determinant(float(z))
        residual = pole_removed_bulk_determinant(float(z))
        pole_rows.append(
            {
                "z": z,
                "bulk_determinant_real": determinant.real,
                "bulk_determinant_imag": determinant.imag,
                "pole_removed_real": residual.real,
                "pole_removed_imag": residual.imag,
                "pole_factor": 1.0 - z * z / LAMBDA_FIXED,
            }
        )
    write_csv(RESULTS / "deterministic_pole_factor.csv", pole_rows)
    return trace_rows, pole_rows


def _selected(value: complex, selected: np.ndarray) -> bool:
    return bool(np.min(np.abs(selected - value), initial=np.inf) < 2.0e-7)


def conjugate_complete(values: np.ndarray, tolerance: float = 1.0e-7) -> np.ndarray:
    """Keep complete conjugate pairs from a real-matrix ARPACK output."""

    values = np.asarray(values, dtype=np.complex128)
    real = values[np.abs(values.imag) <= tolerance].real.astype(np.complex128)
    positive = values[values.imag > tolerance]
    return np.concatenate((real, positive, np.conjugate(positive)))


def spectral_audit() -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    summary_rows: list[dict[str, object]] = []
    point_rows: list[dict[str, object]] = []
    scattering_rows: list[dict[str, object]] = []
    determinant_rows: list[dict[str, object]] = []

    for index, (sigma, dimension) in enumerate(NOISE_SETTINGS, start=1):
        print(
            f"cloud {index}/{len(NOISE_SETTINGS)}: sigma={sigma:g}, n={dimension}",
            flush=True,
        )
        started = time.time()
        matrix = sparse_folded_gaussian_matrix(dimension, sigma)
        build_seconds = time.time() - started
        row_error = float(
            np.max(np.abs(np.asarray(matrix.sum(axis=1)).ravel() - 1.0))
        )
        started = time.time()
        spectrum = resolve_bulk_spectrum(matrix, eigenvalue_count=80)
        eigensolve_seconds = time.time() - started
        fit = fit_outer_cloud(spectrum.bulk)
        selected = fit.selected_full
        threshold = LAMBDA_FIXED ** -0.5
        half_horizon = np.log(1.0 / sigma) / (2.0 * np.log(LAMBDA_FIXED))
        completed_bulk = conjugate_complete(spectrum.bulk)
        captured_trace_two = complex(np.sum(completed_bulk**2))
        summary_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "dimension_times_sigma": dimension * sigma,
                "nonzeros": matrix.nnz,
                "row_sum_error": row_error,
                "parity_real": spectrum.parity.real,
                "effective_cloud_degree": fit.effective_degree,
                "cloud_eigenvalue_count": 2 * fit.effective_degree,
                "half_localization_horizon": half_horizon,
                "degree_defect_from_half_horizon": half_horizon
                - fit.effective_degree,
                "threshold_radius": threshold,
                "cloud_radial_mean": fit.radial_mean,
                "cloud_center_zero_radius": 1.0 / fit.radial_mean,
                "cloud_radial_mean_error": fit.radial_mean - threshold,
                "cloud_radial_rms_error": fit.radial_rms_from_threshold,
                "cloud_phase_rms_error": fit.phase_rms,
                "cloud_separating_radial_gap": fit.radial_gap,
                "bulk_radius": float(np.max(np.abs(spectrum.bulk))),
                "exact_bulk_trace_two": spectrum.exact_bulk_trace_two,
                "captured_bulk_trace_two_real": captured_trace_two.real,
                "captured_bulk_trace_two_imag": captured_trace_two.imag,
                "trace_two_capture_error": captured_trace_two.real
                - spectrum.exact_bulk_trace_two,
                "build_seconds": build_seconds,
                "eigensolve_seconds": eigensolve_seconds,
            }
        )

        expected_angles = (
            np.arange(1, fit.effective_degree + 1)
            * np.pi
            / (fit.effective_degree + 1)
        )
        for order, value in enumerate(fit.selected_positive, start=1):
            point_rows.append(
                {
                    "sigma": sigma,
                    "folded_dimension": dimension,
                    "effective_cloud_degree": fit.effective_degree,
                    "positive_order": order,
                    "real": value.real,
                    "imag": value.imag,
                    "radius": abs(value),
                    "angle": np.angle(value),
                    "expected_radius": threshold,
                    "expected_angle": expected_angles[order - 1],
                    "radial_error": abs(value) - threshold,
                    "phase_error": np.angle(value) - expected_angles[order - 1],
                }
            )

        for value in spectrum.bulk:
            all_selected = np.concatenate((selected,))
            point_rows_marker = {
                "sigma": sigma,
                "folded_dimension": dimension,
                "effective_cloud_degree": fit.effective_degree,
                "positive_order": "all" if not _selected(value, all_selected) else "selected",
                "real": value.real,
                "imag": value.imag,
                "radius": abs(value),
                "angle": np.angle(value),
                "expected_radius": "",
                "expected_angle": "",
                "radial_error": "",
                "phase_error": "",
            }
            point_rows.append(point_rows_marker)

        root = 1.0 / fit.radial_mean
        base = cloud_det2(selected, root)
        for coordinate in SCATTERING_COORDINATES:
            q = np.exp(coordinate / (fit.effective_degree + 1))
            z = root * np.sqrt(q)
            observed = cloud_det2(selected, z) / base
            finite_model = geometric_section(fit.effective_degree, q) / (
                fit.effective_degree + 1
            )
            universal = scattering_profile(coordinate)
            scattering_rows.append(
                {
                    "sigma": sigma,
                    "effective_cloud_degree": fit.effective_degree,
                    "scattering_coordinate": coordinate,
                    "observed_real": observed.real,
                    "observed_imag": observed.imag,
                    "finite_geometric_real": finite_model.real,
                    "finite_geometric_imag": finite_model.imag,
                    "universal_real": universal.real,
                    "universal_imag": universal.imag,
                    "observed_to_finite_error": abs(observed - finite_model),
                    "observed_to_universal_error": abs(observed - universal),
                }
            )

        top_trace_two = np.sum(completed_bulk**2)
        missing_trace_two = spectrum.exact_bulk_trace_two - top_trace_two
        for z in DETERMINANT_TARGETS:
            product = cloud_det2(completed_bulk, z)
            corrected = product * np.exp(-0.5 * z * z * missing_trace_two)
            target = bulk_determinant(z)
            determinant_rows.append(
                {
                    "sigma": sigma,
                    "z": z,
                    "leading_eigenvalue_det2_real": product.real,
                    "leading_eigenvalue_det2_imag": product.imag,
                    "trace_two_corrected_real": corrected.real,
                    "trace_two_corrected_imag": corrected.imag,
                    "deterministic_target_real": target.real,
                    "deterministic_target_imag": target.imag,
                    "corrected_target_error": abs(corrected - target),
                }
            )
        del matrix
        release_memory()

    write_csv(RESULTS / "cloud_summary.csv", summary_rows)
    write_csv(RESULTS / "outer_resonance_cloud.csv", point_rows)
    write_csv(RESULTS / "scattering_collapse.csv", scattering_rows)
    write_csv(RESULTS / "bulk_determinant_convergence.csv", determinant_rows)
    return summary_rows, point_rows, scattering_rows, determinant_rows


def resolution_audit() -> list[dict[str, object]]:
    sigma = 0.001
    rows: list[dict[str, object]] = []
    for dimension in (10240, 20480, 30720):
        print(f"resolution: sigma={sigma:g}, n={dimension}", flush=True)
        matrix = sparse_folded_gaussian_matrix(dimension, sigma)
        spectrum = resolve_bulk_spectrum(matrix, eigenvalue_count=50)
        fit = fit_outer_cloud(spectrum.bulk)
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "dimension_times_sigma": dimension * sigma,
                "effective_cloud_degree": fit.effective_degree,
                "cloud_radial_mean": fit.radial_mean,
                "cloud_phase_rms_error": fit.phase_rms,
                "bulk_radius": float(np.max(np.abs(spectrum.bulk))),
            }
        )
        del matrix
        release_memory()
    write_csv(RESULTS / "cloud_resolution.csv", rows)
    return rows


def _float_rows(rows: list[dict[str, object]], key: str) -> np.ndarray:
    return np.asarray([float(row[key]) for row in rows])


def plot_audit(
    trace_rows: list[dict[str, object]],
    pole_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    point_rows: list[dict[str, object]],
    scattering_rows: list[dict[str, object]],
    determinant_rows: list[dict[str, object]],
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.5))
    iterate = _float_rows(trace_rows, "component_iterate")
    centered = np.abs(_float_rows(trace_rows, "parity_centered_trace"))
    leading = np.abs(_float_rows(trace_rows, "endpoint_two_term_law"))
    remainder = np.abs(_float_rows(trace_rows, "two_term_remainder"))
    axes[0, 0].semilogy(iterate, centered, "o-", ms=4, label=r"$|P_{2n}-2|$")
    axes[0, 0].semilogy(iterate, leading, "--", label=r"$|-2\lambda^{-n}+\lambda^{-2n}|$")
    axes[0, 0].semilogy(iterate, remainder, "s-", ms=3, label="two-term remainder")
    axes[0, 0].semilogy(iterate, remainder[0] * 3.0 ** (-(iterate - 1)), ":", label=r"$3^{-n}$ reference")
    axes[0, 0].set(xlabel=r"component iterate $n$", ylabel="absolute coefficient", title="Exact physical flat-trace law")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    z = _float_rows(pole_rows, "z")
    determinant = _float_rows(pole_rows, "bulk_determinant_real")
    residual = _float_rows(pole_rows, "pole_removed_real")
    root = np.sqrt(LAMBDA_FIXED)
    axes[0, 1].plot(z, determinant, color="#2455a4", label=r"$\widehat D_{0,\mathrm{bulk},2}$")
    axes[0, 1].plot(z, residual, color="#a0273f", label=r"$(1-z^2/\lambda)\widehat D$")
    axes[0, 1].axvline(root, color="0.35", ls="--", label=r"$\sqrt{\lambda}$")
    axes[0, 1].set(xlabel=r"real $z$", ylabel="determinant value", title="The exact endpoint pole")
    axes[0, 1].set_ylim(bottom=min(-0.2, residual.min() * 1.1), top=min(18.0, determinant.max() * 1.05))
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    threshold = LAMBDA_FIXED ** -0.5
    colors = {0.01: "#929292", 0.001: "#3a8f6b", 0.0001: "#2455a4"}
    for sigma, color in colors.items():
        all_rows = [
            row
            for row in point_rows
            if abs(float(row["sigma"]) - sigma) < 1.0e-12
            and str(row["positive_order"]) in {"all", "selected"}
        ]
        all_values = np.asarray(
            [complex(float(row["real"]), float(row["imag"])) for row in all_rows]
        )
        selected_rows = [
            row
            for row in point_rows
            if abs(float(row["sigma"]) - sigma) < 1.0e-12
            and str(row["positive_order"]).isdigit()
        ]
        selected_positive = np.asarray(
            [complex(float(row["real"]), float(row["imag"])) for row in selected_rows]
        )
        selected_values = np.concatenate((selected_positive, np.conjugate(selected_positive)))
        axes[1, 0].plot(all_values.real, all_values.imag, ".", ms=3, alpha=0.20, color=color)
        axes[1, 0].plot(
            selected_values.real,
            selected_values.imag,
            "o",
            ms=4.5,
            mfc="none",
            mec=color,
            label=fr"$\sigma={sigma:g}$",
        )
        if sigma == 0.0001:
            degree_value = len(selected_positive)
            expected_angles = np.arange(1, degree_value + 1) * np.pi / (degree_value + 1)
            expected_positive = threshold * np.exp(1j * expected_angles)
            expected = np.concatenate((expected_positive, np.conjugate(expected_positive)))
            axes[1, 0].plot(expected.real, expected.imag, "x", ms=5, color="#a0273f", label="geometric phases")
    angle = np.linspace(0.0, 2.0 * np.pi, 500)
    axes[1, 0].plot(threshold * np.cos(angle), threshold * np.sin(angle), "--", color="#a0273f", lw=1.0, label=r"$|\mu|=\lambda^{-1/2}$")
    axes[1, 0].set(xlabel=r"$\Re\mu$", ylabel=r"$\Im\mu$", title="Parity-extracted resonance clouds", aspect="equal")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    sigma = _float_rows(summary_rows, "sigma")
    degree = _float_rows(summary_rows, "effective_cloud_degree")
    half_horizon = _float_rows(summary_rows, "half_localization_horizon")
    order = np.argsort(sigma)
    axes[1, 1].semilogx(sigma[order], degree[order], "o-", label=r"effective $N_\sigma$")
    axes[1, 1].semilogx(sigma[order], half_horizon[order], "--", label=r"$\log(1/\sigma)/(2\log\lambda)$")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(xlabel=r"noise $\sigma$", ylabel="cloud degree", title="Logarithmic growth of the pole section")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"exact_pole_resonance_cloud.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(7.0, 4.5))
    coordinates = sorted({float(row["scattering_coordinate"]) for row in scattering_rows})
    axis.plot(coordinates, [scattering_profile(value).real for value in coordinates], "k--", lw=1.5, label=r"$(e^s-1)/s$")
    for sigma_value in (0.004, 0.001, 0.0002, 0.0001):
        chosen = [row for row in scattering_rows if abs(float(row["sigma"]) - sigma_value) < 1.0e-12]
        axis.plot(
            [float(row["scattering_coordinate"]) for row in chosen],
            [float(row["observed_real"]) for row in chosen],
            "o-",
            ms=3.5,
            label=fr"$\sigma={sigma_value:g}$, $N={int(float(chosen[0]['effective_cloud_degree']))}$",
        )
        axis.plot(
            [float(row["scattering_coordinate"]) for row in chosen],
            [float(row["finite_geometric_real"]) for row in chosen],
            ":",
            lw=1.0,
            color=axis.lines[-1].get_color(),
        )
    axis.set(xlabel=r"radially centered coordinate $s=(N_\sigma+1)\log(z^2\bar r_\sigma^2)$", ylabel="normalized cloud determinant", title="Geometric pole-resolution scaling")
    axis.legend(frameon=False, fontsize=8)
    axis.grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"geometric_scattering_collapse.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(7.0, 4.5))
    for z_target in (0.5, 0.9, 1.1, 1.2):
        chosen = [row for row in determinant_rows if abs(float(row["z"]) - z_target) < 1.0e-12]
        chosen.sort(key=lambda row: float(row["sigma"]), reverse=True)
        axis.semilogx(
            [float(row["sigma"]) for row in chosen],
            [float(row["trace_two_corrected_real"]) for row in chosen],
            "o-",
            ms=3.5,
            label=fr"$z={z_target:g}$",
        )
        axis.axhline(float(chosen[0]["deterministic_target_real"]), color=axis.lines[-1].get_color(), ls="--", lw=0.8)
    axis.invert_xaxis()
    axis.set(xlabel=r"noise $\sigma$", ylabel=r"$D_{\sigma,\mathrm{bulk},2}(z)$", title="Coefficientwise target and slowing near the pole")
    axis.legend(frameon=False, fontsize=8)
    axis.grid(alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"bulk_determinant_pole_approach.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reuse-results",
        action="store_true",
        help="reuse archived CSV spectra and regenerate only figures/summary",
    )
    arguments = parser.parse_args()
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)

    if arguments.reuse_results:
        trace_rows = read_csv(RESULTS / "physical_trace_reconstruction.csv")
        pole_rows = read_csv(RESULTS / "deterministic_pole_factor.csv")
        summary_rows = read_csv(RESULTS / "cloud_summary.csv")
        point_rows = read_csv(RESULTS / "outer_resonance_cloud.csv")
        scattering_rows = read_csv(RESULTS / "scattering_collapse.csv")
        determinant_rows = read_csv(RESULTS / "bulk_determinant_convergence.csv")
        resolution_rows = read_csv(RESULTS / "cloud_resolution.csv")
    else:
        trace_rows, pole_rows = deterministic_audit()
        summary_rows, point_rows, scattering_rows, determinant_rows = spectral_audit()
        resolution_rows = resolution_audit()

    plot_audit(
        trace_rows,
        pole_rows,
        summary_rows,
        point_rows,
        scattering_rows,
        determinant_rows,
    )
    smallest = min(summary_rows, key=lambda row: float(row["sigma"]))
    payload = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "source_sha256": {
            **{
                f"src/bulk_scattering/{name}": source_hash(
                    ROOT / "src" / "bulk_scattering" / name
                )
                for name in ("deterministic.py", "operators.py", "cloud.py")
            },
            "experiments/run_bulk_scattering_audit.py": source_hash(Path(__file__)),
        },
        "analytic_results": {
            "even_trace": "P_2n=2E_1,n-2a_n/(1+a_n)-a_n^2/(1-a_n^2)",
            "sharp_law": "P_2n=2-2lambda^(-n)+lambda^(-2n)+O(3^(-n))",
            "bulk_factorization": "D_bulk,2(z)=G(z)/(1-z^2/lambda)",
            "nearest_poles": [-float(np.sqrt(LAMBDA_FIXED)), float(np.sqrt(LAMBDA_FIXED))],
            "threshold_radius": float(LAMBDA_FIXED ** -0.5),
            "naive_entire_limit": False,
        },
        "smallest_noise_cloud": {
            "sigma": float(smallest["sigma"]),
            "dimension": int(float(smallest["folded_dimension"])),
            "effective_degree": int(float(smallest["effective_cloud_degree"])),
            "eigenvalue_count": int(float(smallest["cloud_eigenvalue_count"])),
            "radial_mean": float(smallest["cloud_radial_mean"]),
            "phase_rms": float(smallest["cloud_phase_rms_error"]),
            "bulk_radius": float(smallest["bulk_radius"]),
        },
        "resolution": {
            "sigma": 0.001,
            "degrees": [int(float(row["effective_cloud_degree"])) for row in resolution_rows],
            "radial_mean_spread": max(float(row["cloud_radial_mean"]) for row in resolution_rows)
            - min(float(row["cloud_radial_mean"]) for row in resolution_rows),
        },
        "status": {
            "exact_poles_and_normal_family_obstruction": "analytic",
            "geometric_finite_section": "exact model theorem",
            "noisy_cloud_matching": "floating-point diagnostic and conjectural scaling",
        },
    }
    with (RESULTS / "bulk_scattering_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
