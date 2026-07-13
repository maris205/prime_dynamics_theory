"""Reproduce the exact long-cycle, finite-noise, and determinant audits."""

from __future__ import annotations

import csv
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy

from long_cycle import (
    LAMBDA_FIXED,
    R_FIXED,
    U_CRITICAL,
    audit_length,
    boundary_periodic_point,
    boundary_word,
    bulk_trace_from_spectrum,
    exact_bulk_det2,
    folded_gaussian_matrix,
    inverse_word,
    parity_centered_flat_trace,
    regularized_determinant_from_traces,
    resolve_spectrum,
    trace_from_spectrum,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
MAXIMUM_DETERMINISTIC_LENGTH = 28
NOISE_SETTINGS = (
    (0.080, 256),
    (0.060, 342),
    (0.050, 410),
    (0.040, 512),
    (0.030, 683),
    (0.020, 1024),
    (0.015, 1366),
    (0.012, 1707),
    (0.010, 2048),
)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def deterministic_audit() -> tuple[list[dict[str, object]], dict[int, float]]:
    rows: list[dict[str, object]] = []
    traces: dict[int, float] = {}
    for length in range(1, MAXIMUM_DETERMINISTIC_LENGTH + 1):
        print(f"deterministic length {length}/{MAXIMUM_DETERMINISTIC_LENGTH}", flush=True)
        record = audit_length(length)
        traces[length] = record.flat_trace
        even = length % 2 == 0
        boundary_point = boundary_periodic_point(length) if even else None
        odd_formula = 1.0 / (1.0 + LAMBDA_FIXED**length) if not even else None
        rows.append(
            {
                "length": length,
                "parity": "even" if even else "odd",
                "physical_fixed_point_count": record.fixed_point_count,
                "flat_trace": record.flat_trace,
                "parity_baseline": record.parity_baseline,
                "centered_trace": record.centered_trace,
                "odd_exact_formula": "" if odd_formula is None else odd_formula,
                "odd_formula_error": "" if odd_formula is None else abs(record.flat_trace - odd_formula),
                "minimum_boundary_clearance": record.boundary_clearance,
                "distinguished_boundary_point": "" if boundary_point is None else boundary_point,
                "distinguished_boundary_clearance": "" if boundary_point is None else 1.0 - boundary_point,
                "clearance_times_lambda_power": ""
                if boundary_point is None
                else (1.0 - boundary_point) * LAMBDA_FIXED**length,
                "minimum_abs_multiplier": record.minimum_multiplier,
                "maximum_abs_multiplier": record.maximum_multiplier,
            }
        )
    write_csv(RESULTS / "deterministic_long_cycles.csv", rows)
    return rows, traces


def boundary_audit() -> tuple[list[dict[str, object]], float, float]:
    rows: list[dict[str, object]] = []
    for length in range(2, 50, 2):
        word = boundary_word(length)
        point = boundary_periodic_point(length)
        clearance = 1.0 - point
        rows.append(
            {
                "length": length,
                "word": "".join(word),
                "point": point,
                "clearance": clearance,
                "clearance_times_lambda_power": clearance * LAMBDA_FIXED**length,
                "inverse_fixed_point_residual": abs(inverse_word(word, point) - point),
            }
        )
    write_csv(RESULTS / "boundary_crowding.csv", rows)
    fit_rows = [row for row in rows if 12 <= int(row["length"]) <= 40]
    lengths = np.asarray([float(row["length"]) for row in fit_rows])
    clearances = np.asarray([float(row["clearance"]) for row in fit_rows])
    slope, intercept = np.polyfit(lengths, np.log(clearances), 1)
    return rows, float(slope), float(intercept)


def noisy_audit(
    deterministic_traces: dict[int, float],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[float, object], float, float]:
    spectral_rows: list[dict[str, object]] = []
    trace_rows: list[dict[str, object]] = []
    spectra: dict[float, object] = {}
    for index, (sigma, dimension) in enumerate(NOISE_SETTINGS, start=1):
        print(
            f"finite-noise spectrum {index}/{len(NOISE_SETTINGS)}: sigma={sigma}, n={dimension}",
            flush=True,
        )
        matrix = folded_gaussian_matrix(dimension, sigma)
        row_sum_error = float(np.max(np.abs(np.sum(matrix, axis=1) - 1.0)))
        spectrum = resolve_spectrum(matrix)
        spectra[sigma] = spectrum
        parity_gap = 1.0 + spectrum.parity.real
        lifetime = -1.0 / np.log(abs(spectrum.parity))
        spectral_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "full_dimension": 2 * dimension,
                "dimension_times_sigma": dimension * sigma,
                "row_sum_error": row_sum_error,
                "perron_real": spectrum.perron.real,
                "perron_imag": spectrum.perron.imag,
                "perron_error": abs(spectrum.perron - 1.0),
                "parity_real": spectrum.parity.real,
                "parity_imag": spectrum.parity.imag,
                "parity_gap": parity_gap,
                "gap_over_sigma_two_thirds": parity_gap / sigma ** (2.0 / 3.0),
                "reciprocal_gap_lifetime": 1.0 / parity_gap,
                "exact_efolding_lifetime": float(lifetime.real),
                "bulk_radius": spectrum.bulk_radius,
            }
        )
        for length in range(2, 201):
            raw = trace_from_spectrum(spectrum, length)
            bulk = bulk_trace_from_spectrum(spectrum, length)
            peripheral = spectrum.perron**length + spectrum.parity**length
            target = deterministic_traces.get(length)
            trace_rows.append(
                {
                    "sigma": sigma,
                    "length": length,
                    "raw_trace_real": raw.real,
                    "raw_trace_imag": raw.imag,
                    "perron_parity_real": peripheral.real,
                    "perron_parity_imag": peripheral.imag,
                    "bulk_trace_real": bulk.real,
                    "bulk_trace_imag": bulk.imag,
                    "deterministic_flat_trace": "" if target is None else target,
                    "deterministic_parity_baseline": 1 + (-1) ** length,
                }
            )
        del matrix
    write_csv(RESULTS / "noisy_parity_spectrum.csv", spectral_rows)
    write_csv(RESULTS / "noisy_long_cycle_traces.csv", trace_rows)
    tail = spectral_rows[-5:]
    sigma = np.asarray([float(row["sigma"]) for row in tail])
    gap = np.asarray([float(row["parity_gap"]) for row in tail])
    exponent, log_amplitude = np.polyfit(np.log(sigma), np.log(gap), 1)
    return spectral_rows, trace_rows, spectra, float(exponent), float(np.exp(log_amplitude))


def resolution_audit(spectra: dict[float, object]) -> list[dict[str, object]]:
    sigma = 0.010
    rows: list[dict[str, object]] = []
    local: dict[int, object] = {2048: spectra[sigma]}
    for dimension in (1024, 1536, 2560):
        print(f"resolution spectrum: sigma={sigma}, n={dimension}", flush=True)
        local[dimension] = resolve_spectrum(folded_gaussian_matrix(dimension, sigma))
    reference = local[2560].parity.real
    for dimension in sorted(local):
        spectrum = local[dimension]
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "dimension_times_sigma": dimension * sigma,
                "parity_real": spectrum.parity.real,
                "parity_difference_from_finest": spectrum.parity.real - reference,
                "bulk_radius": spectrum.bulk_radius,
            }
        )
    write_csv(RESULTS / "lowest_noise_resolution.csv", rows)
    return rows


def determinant_audit(
    deterministic_traces: dict[int, float], spectra: dict[float, object]
) -> list[dict[str, object]]:
    centered = {
        length: deterministic_traces[length] - (1 + (-1) ** length)
        for length in range(2, MAXIMUM_DETERMINISTIC_LENGTH + 1)
    }
    z_values = (0.25, 0.50, 0.75, 0.90, 1.00, 1.10)
    deterministic = {
        z: regularized_determinant_from_traces(
            centered, z, maximum_length=MAXIMUM_DETERMINISTIC_LENGTH
        )
        for z in z_values
    }
    rows: list[dict[str, object]] = []
    for sigma, spectrum in spectra.items():
        traces = {length: bulk_trace_from_spectrum(spectrum, length) for length in range(2, 121)}
        for z in z_values:
            exact = exact_bulk_det2(spectrum, z)
            trace_product = regularized_determinant_from_traces(traces, z, maximum_length=120)
            target = deterministic[z]
            rows.append(
                {
                    "sigma": sigma,
                    "z": z,
                    "finite_noise_bulk_det2_real": exact.real,
                    "finite_noise_bulk_det2_imag": exact.imag,
                    "trace_truncation_real": trace_product.real,
                    "trace_truncation_imag": trace_product.imag,
                    "trace_product_error": abs(exact - trace_product),
                    "deterministic_centered_det2_length_28_real": target.real,
                    "deterministic_centered_det2_length_28_imag": target.imag,
                    "noise_to_deterministic_truncation_error": abs(exact - target),
                }
            )
    write_csv(RESULTS / "bulk_determinants.csv", rows)
    return rows


def plot_deterministic(
    rows: list[dict[str, object]], boundary_rows: list[dict[str, object]], boundary_intercept: float
) -> None:
    lengths = np.asarray([int(row["length"]) for row in rows])
    even = lengths % 2 == 0
    odd = ~even
    counts = np.asarray([float(row["physical_fixed_point_count"]) for row in rows])
    traces = np.asarray([float(row["flat_trace"]) for row in rows])
    centered = np.asarray([abs(float(row["centered_trace"])) for row in rows])

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.2))
    axes[0, 0].semilogy(lengths[even], counts[even], "o", ms=4, color="#2455a4", label="physical roots")
    axes[0, 0].semilogy(
        lengths[even],
        2.0 ** (lengths[even] / 2.0 + 1.0) - 1.0,
        color="#a0273f",
        lw=1.3,
        label=r"$2^{m/2+1}-1$",
    )
    axes[0, 0].semilogy(lengths[odd], counts[odd], "s", ms=3, color="0.35", label="odd: one root")
    axes[0, 0].set(xlabel=r"cycle length $m$", ylabel="physical fixed points", title="Exact Markov count")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].plot(lengths[even], traces[even], "o-", ms=3.5, lw=1.0, color="#2455a4", label="even")
    axes[0, 1].semilogy(lengths[odd], traces[odd], "s-", ms=3.2, lw=1.0, color="#a0273f", label="odd")
    axes[0, 1].axhline(2.0, color="0.3", lw=0.9, ls="--")
    axes[0, 1].set(xlabel=r"cycle length $m$", ylabel=r"$P_m$", title="Deterministic flat traces")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    axes[1, 0].semilogy(lengths[even], centered[even], "o", ms=4, color="#2455a4", label="even centered")
    axes[1, 0].semilogy(lengths[odd], centered[odd], "s", ms=3.5, color="#a0273f", label="odd exact")
    odd_reference = 1.0 / (1.0 + LAMBDA_FIXED ** lengths[odd])
    axes[1, 0].semilogy(lengths[odd], odd_reference, color="#a0273f", lw=1.0)
    anchor_length = 14
    anchor = centered[lengths == anchor_length][0]
    reference = anchor * np.exp(-0.5 * np.log(LAMBDA_FIXED) * (lengths[even] - anchor_length))
    axes[1, 0].semilogy(lengths[even], reference, color="#2455a4", lw=1.0, ls="--", label=r"reference $\lambda^{-m/2}$")
    axes[1, 0].set(xlabel=r"cycle length $m$", ylabel=r"$|P_m-1-(-1)^m|$", title="Parity-centered decay")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    b_length = np.asarray([float(row["length"]) for row in boundary_rows])
    clearance = np.asarray([float(row["clearance"]) for row in boundary_rows])
    fit = np.exp(boundary_intercept - np.log(LAMBDA_FIXED) * b_length)
    axes[1, 1].semilogy(b_length, clearance, "o", ms=3.5, color="#3a8f6b", label="distinguished cycle")
    axes[1, 1].semilogy(b_length, fit, color="black", lw=1.1, ls="--", label=r"$C\lambda^{-m}$")
    axes[1, 1].set(xlabel=r"even cycle length $m$", ylabel=r"$1-p_m$", title="Exponential boundary crowding")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"deterministic_long_cycles.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_noncommuting_limits(
    spectral_rows: list[dict[str, object]],
    trace_rows: list[dict[str, object]],
    deterministic_rows: list[dict[str, object]],
    exponent: float,
    amplitude: float,
) -> None:
    sigma = np.asarray([float(row["sigma"]) for row in spectral_rows])
    gap = np.asarray([float(row["parity_gap"]) for row in spectral_rows])
    order = np.argsort(sigma)
    sigma, gap = sigma[order], gap[order]
    lifetime = 1.0 / gap
    localization = np.log(1.0 / sigma) / np.log(LAMBDA_FIXED)

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.2))
    axes[0, 0].loglog(sigma, gap, "o-", color="#2455a4", ms=4, label="resolved parity gap")
    fit_sigma = np.geomspace(sigma.min(), sigma.max(), 200)
    axes[0, 0].loglog(fit_sigma, amplitude * fit_sigma**exponent, "--", color="#a0273f", lw=1.2, label=fr"tail fit $\sigma^{{{exponent:.3f}}}$")
    axes[0, 0].set(xlabel=r"noise $\sigma$", ylabel=r"$1+\lambda_-(\sigma)$", title="Negative-resonance gap")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.22, which="both")

    axes[0, 1].loglog(sigma, lifetime, "o-", color="#a0273f", ms=4, label="parity lifetime")
    axes[0, 1].loglog(sigma, localization, "s-", color="#3a8f6b", ms=4, label="localization horizon")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(xlabel=r"noise $\sigma$", ylabel="cycle scale", title="Two nonuniform scales")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22, which="both")

    colors = {0.08: "#8c8c8c", 0.04: "#cf7b28", 0.02: "#3a8f6b", 0.01: "#2455a4"}
    for selected, color in colors.items():
        chosen = [row for row in trace_rows if float(row["sigma"]) == selected and int(row["length"]) % 2 == 0]
        axes[1, 0].plot(
            [int(row["length"]) for row in chosen],
            [float(row["raw_trace_real"]) for row in chosen],
            color=color,
            lw=1.1,
            label=fr"$\sigma={selected:g}$",
        )
    even_deterministic = [row for row in deterministic_rows if int(row["length"]) % 2 == 0]
    axes[1, 0].plot(
        [int(row["length"]) for row in even_deterministic],
        [float(row["flat_trace"]) for row in even_deterministic],
        "ko",
        ms=3.4,
        label="zero-noise coefficient",
    )
    axes[1, 0].axhline(1.0, color="black", ls=":", lw=0.9)
    axes[1, 0].axhline(2.0, color="black", ls="--", lw=0.9)
    axes[1, 0].set(xlim=(2, 200), xlabel=r"even length $m$", ylabel=r"$\operatorname{tr}K_\sigma^m$", title="Return to the Perron limit")
    axes[1, 0].legend(frameon=False, fontsize=7, ncol=2)
    axes[1, 0].grid(alpha=0.22)

    for selected, color in colors.items():
        chosen = [row for row in trace_rows if float(row["sigma"]) == selected]
        axes[1, 1].semilogy(
            [int(row["length"]) for row in chosen],
            np.maximum(1.0e-18, np.abs([float(row["bulk_trace_real"]) for row in chosen])),
            color=color,
            lw=1.0,
            label=fr"$\sigma={selected:g}$",
        )
    axes[1, 1].set(xlim=(2, 80), ylim=(1.0e-12, 2.0), xlabel=r"length $m$", ylabel="absolute bulk trace", title="After Perron/parity extraction")
    axes[1, 1].legend(frameon=False, fontsize=7)
    axes[1, 1].grid(alpha=0.22, which="both")

    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"noncommuting_long_cycle_limits.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_determinants(rows: list[dict[str, object]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.75))
    sigmas = sorted({float(row["sigma"]) for row in rows}, reverse=True)
    colors = plt.cm.viridis(np.linspace(0.12, 0.90, len(sigmas)))
    for sigma, color in zip(sigmas, colors):
        chosen = [row for row in rows if float(row["sigma"]) == sigma]
        axes[0].plot(
            [float(row["z"]) for row in chosen],
            [float(row["finite_noise_bulk_det2_real"]) for row in chosen],
            "o-",
            ms=3,
            lw=1.0,
            color=color,
            label=fr"$\sigma={sigma:g}$",
        )
    first = [row for row in rows if float(row["sigma"]) == sigmas[0]]
    axes[0].plot(
        [float(row["z"]) for row in first],
        [float(row["deterministic_centered_det2_length_28_real"]) for row in first],
        "k--",
        lw=1.4,
        label="deterministic, 28 terms",
    )
    axes[0].set(xlabel=r"real $z$", ylabel="bulk regularized determinant", title="Parity-renormalized determinant")
    axes[0].legend(frameon=False, fontsize=6.8, ncol=2)
    axes[0].grid(alpha=0.22)

    for z, color, marker in ((0.5, "#3a8f6b", "o"), (0.9, "#cf7b28", "s"), (1.1, "#a0273f", "^")):
        chosen = sorted((row for row in rows if float(row["z"]) == z), key=lambda row: float(row["sigma"]))
        axes[1].loglog(
            [float(row["sigma"]) for row in chosen],
            [float(row["noise_to_deterministic_truncation_error"]) for row in chosen],
            marker=marker,
            color=color,
            lw=1.1,
            ms=4,
            label=fr"$z={z:g}$",
        )
    axes[1].set(xlabel=r"noise $\sigma$", ylabel="difference from 28-term target", title="Coefficientwise approach, not uniformity")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(alpha=0.22, which="both")
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"bulk_determinants.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def build_summary(
    deterministic_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    boundary_slope: float,
    spectral_rows: list[dict[str, object]],
    trace_rows: list[dict[str, object]],
    resolution_rows: list[dict[str, object]],
    determinant_rows: list[dict[str, object]],
    gap_exponent: float,
    gap_amplitude: float,
) -> dict[str, object]:
    even_tail = [row for row in deterministic_rows if int(row["length"]) >= 14 and int(row["length"]) % 2 == 0]
    even_lengths = np.asarray([float(row["length"]) for row in even_tail])
    even_centered = np.asarray([abs(float(row["centered_trace"])) for row in even_tail])
    even_slope = float(np.polyfit(even_lengths, np.log(even_centered), 1)[0])
    boundary_scaled = [float(row["clearance_times_lambda_power"]) for row in boundary_rows if int(row["length"]) >= 32]
    lowest = spectral_rows[-1]
    selected_trace = {
        int(row["length"]): float(row["raw_trace_real"])
        for row in trace_rows
        if float(row["sigma"]) == 0.015 and int(row["length"]) in (2, 4, 6, 20, 100, 200)
    }
    determinant_product_error = max(float(row["trace_product_error"]) for row in determinant_rows)
    resolution_values = [float(row["parity_real"]) for row in resolution_rows]
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "constants": {
            "u_critical": U_CRITICAL,
            "r_fixed": R_FIXED,
            "lambda_fixed": LAMBDA_FIXED,
            "log_lambda": float(np.log(LAMBDA_FIXED)),
        },
        "exact_results": {
            "physical_count_odd": "1",
            "physical_count_even": "2^(m/2+1)-1",
            "odd_flat_trace": "1/(1+lambda^m)",
            "boundary_word": "CA(CB)^(m/2-1)",
            "boundary_clearance_order": "Theta(lambda^(-m))",
            "fixed_positive_noise_long_trace_limit": 1,
            "deterministic_parity_factor": "1-z^2",
        },
        "deterministic_audit": {
            "maximum_enumerated_length": MAXIMUM_DETERMINISTIC_LENGTH,
            "physical_roots_at_maximum_length": int(deterministic_rows[-1]["physical_fixed_point_count"]),
            "flat_trace_at_maximum_length": float(deterministic_rows[-1]["flat_trace"]),
            "centered_trace_at_maximum_length": float(deterministic_rows[-1]["centered_trace"]),
            "boundary_log_slope_fit_12_to_40": boundary_slope,
            "boundary_expected_log_slope": -float(np.log(LAMBDA_FIXED)),
            "boundary_scaled_tail_mean": float(np.mean(boundary_scaled)),
            "even_centered_log_slope_fit_14_to_28": even_slope,
            "even_centered_reference_slope": -0.5 * float(np.log(LAMBDA_FIXED)),
        },
        "conditional_result": {
            "hypothesis": "adapted deterministic flat-trace gap after the two peripheral modes",
            "consequence": "P_(2k) tends to 2 and the two iterated small-noise/long-cycle limits are 1 and 2",
        },
        "finite_noise_evidence": {
            "parity_gap_tail_power_fit": gap_exponent,
            "parity_gap_tail_amplitude": gap_amplitude,
            "power_fit_tail_sigmas": [float(row["sigma"]) for row in spectral_rows[-5:]],
            "smallest_sigma": float(lowest["sigma"]),
            "smallest_sigma_parity_resonance": float(lowest["parity_real"]),
            "smallest_sigma_parity_gap": float(lowest["parity_gap"]),
            "smallest_sigma_reciprocal_gap_lifetime": float(lowest["reciprocal_gap_lifetime"]),
            "sigma_0.015_selected_traces": selected_trace,
            "sigma_0.01_resolution_spread": max(resolution_values) - min(resolution_values),
            "maximum_bulk_det2_trace_product_error": determinant_product_error,
        },
        "scope": {
            "two_thirds_gap_law": "numerical evidence only",
            "even_flat_trace_limit": "conditional unless the adapted flat-trace space is constructed",
            "boundary_crowding_and_fixed_noise_limit": "unconditional",
        },
    }
    with (RESULTS / "long_cycle_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return summary


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    deterministic_rows, deterministic_traces = deterministic_audit()
    boundary_rows, boundary_slope, boundary_intercept = boundary_audit()
    spectral_rows, trace_rows, spectra, gap_exponent, gap_amplitude = noisy_audit(
        deterministic_traces
    )
    resolution_rows = resolution_audit(spectra)
    determinant_rows = determinant_audit(deterministic_traces, spectra)
    plot_deterministic(deterministic_rows, boundary_rows, boundary_intercept)
    plot_noncommuting_limits(
        spectral_rows,
        trace_rows,
        deterministic_rows,
        gap_exponent,
        gap_amplitude,
    )
    plot_determinants(determinant_rows)
    summary = build_summary(
        deterministic_rows,
        boundary_rows,
        boundary_slope,
        spectral_rows,
        trace_rows,
        resolution_rows,
        determinant_rows,
        gap_exponent,
        gap_amplitude,
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
