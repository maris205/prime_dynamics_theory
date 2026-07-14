"""Generate Riccati, critical-profile, and branch-return audits for RH-18."""

from __future__ import annotations

import csv
import ctypes
import gc
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.sparse.linalg import LinearOperator, eigs

from gaussian_return import (
    affine_critical_profile,
    bipartite_root_ring,
    conditioned_critical_profile,
    effective_noise_scales,
    packet_masks,
    periodic_packet_tube,
    positive_midpoints,
    principal_return_eigenpair,
    sparse_folded_gaussian_matrix,
    unconditioned_critical_profile,
)


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH17 = PAPERS / "RH-17-time-ordered-boundary-monodromy"
sys.path.insert(0, str(RH16 / "src"))
sys.path.insert(0, str(RH17 / "src"))

from endpoint_rank import (  # noqa: E402
    HALF_ENERGY_THRESHOLD,
    boundary_clearances,
    threshold_rank,
)
from time_ordered_monodromy import (  # noqa: E402
    balancing_condition_number,
    boundary_cycle,
    critical_constants,
    ideal_reciprocal_cloud,
)


WINDOW_MULTIPLE = 6.0
POWER_ITERATIONS = 9
MAX_PERIOD = 100
CRITICAL_SHAPE_SIGMA = 1.0e-3
SPECTRUM_SIGMAS = (1.0e-3, 1.0e-4)


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


def cycle_data(period: int):
    constants = critical_constants(130)
    cycle = boundary_cycle(int(period), 130)
    points = np.asarray([float(value) for value in cycle.orbit])
    multipliers = np.abs(
        np.asarray([float(value) for value in cycle.two_step_derivatives])
    )
    noise = effective_noise_scales(points, float(constants.u))
    tube = periodic_packet_tube(multipliers, noise)
    return constants, cycle, points, multipliers, noise, tube


def riccati_rows() -> list[dict[str, object]]:
    constants = critical_constants(130)
    lambda_fixed = float(constants.lambda_fixed)
    rows: list[dict[str, object]] = []
    for period in range(2, MAX_PERIOD + 1):
        _, cycle, _, _, _, tube = cycle_data(period)
        raw_condition = balancing_condition_number(cycle)
        rows.append(
            {
                "component_period": period,
                "original_period": 2 * period,
                "cycle_two_step_radius": float(cycle.inverse_jacobian_radius),
                "packet_two_step_radius": tube.spectral_radius,
                "radius_identity_error": tube.spectral_radius
                - float(cycle.inverse_jacobian_radius),
                "endpoint_width": tube.widths[0],
                "critical_source_width": tube.widths[-1],
                "critical_width_over_lambda_k": tube.widths[-1]
                / lambda_fixed**period,
                "minimum_channel_coefficient": float(np.min(tube.coefficients)),
                "maximum_channel_coefficient": float(np.max(tube.coefficients)),
                "raw_balancing_condition": raw_condition,
                "packet_balancing_condition": tube.balancing_condition,
                "packet_eigenvalue_condition": tube.eigenvalue_condition,
                "raw_condition_exponent": np.log(raw_condition)
                / (period * np.log(lambda_fixed)),
                "packet_condition_exponent": np.log(tube.balancing_condition)
                / (period * np.log(lambda_fixed)),
                "riccati_residual": tube.recurrence_residual,
            }
        )
    write_csv(RESULTS / "riccati_packet_asymptotics.csv", rows)
    return rows


def intrinsic_degree(clearances: np.ndarray, sigma: float, power: float) -> int:
    return threshold_rank(
        clearances,
        sigma,
        threshold=HALF_ENERGY_THRESHOLD,
        power=power,
    )


def local_context(sigma: float, dimension: int, period: int, matrix=None):
    constants, cycle, points, _, _, tube = cycle_data(period)
    grid = positive_midpoints(dimension)
    if matrix is None:
        matrix = sparse_folded_gaussian_matrix(
            dimension, sigma, u=float(constants.u)
        )
    masks = packet_masks(
        grid,
        points,
        sigma * tube.widths,
        window_multiple=WINDOW_MULTIPLE,
        critical_partition=float(constants.first_interior_point),
    )
    initial = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    pair = principal_return_eigenpair(
        matrix, masks, initial, iterations=POWER_ITERATIONS
    )
    radius = pair.eigenvalue ** (1.0 / (2.0 * period))
    return constants, cycle, points, tube, grid, matrix, masks, pair, radius


def profile_errors(
    sigma: float,
    cycle,
    points: np.ndarray,
    tube,
    grid: np.ndarray,
    matrix,
    masks: list[np.ndarray],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    endpoint = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    observed = matrix @ (matrix @ endpoint)
    coordinate = (grid - points[-1]) / np.sqrt(sigma)
    clearance = float(cycle.clearance) / sigma
    exact = conditioned_critical_profile(
        coordinate, clearance, tube.widths[0], float(critical_constants(100).u)
    )
    unconditioned = unconditioned_critical_profile(
        coordinate, clearance, tube.widths[0], float(critical_constants(100).u)
    )
    affine = affine_critical_profile(
        coordinate, clearance, tube.widths[0], float(critical_constants(100).u)
    )
    mask = masks[-1]

    def diagnostics(model: np.ndarray) -> tuple[float, float, float]:
        amplitude = float(np.dot(model[mask], observed[mask]) / np.dot(model[mask], model[mask]))
        fitted = float(
            np.linalg.norm(observed[mask] - amplitude * model[mask])
            / np.linalg.norm(observed[mask])
        )
        direct = float(
            np.linalg.norm(observed[mask] - model[mask])
            / np.linalg.norm(observed[mask])
        )
        return direct, fitted, amplitude

    exact_direct, exact_fitted, exact_amplitude = diagnostics(exact)
    unconditioned_direct, _, _ = diagnostics(unconditioned)
    affine_direct, _, _ = diagnostics(affine)
    summary = {
        "sigma": sigma,
        "component_period": cycle.component_period,
        "clearance_over_sigma": clearance,
        "endpoint_dimensionless_width": tube.widths[0],
        "critical_window_nodes": int(np.count_nonzero(mask)),
        "conditioned_profile_direct_error": exact_direct,
        "conditioned_profile_fitted_error": exact_fitted,
        "conditioned_profile_fitted_amplitude": exact_amplitude,
        "unconditioned_profile_direct_error": unconditioned_direct,
        "affine_profile_direct_error": affine_direct,
    }
    shape_rows: list[dict[str, object]] = []
    if abs(sigma - CRITICAL_SHAPE_SIGMA) < 1.0e-15:
        indices = np.flatnonzero(mask)
        stride = max(1, indices.size // 350)
        for index in indices[::stride]:
            shape_rows.append(
                {
                    "sigma": sigma,
                    "scaled_coordinate": coordinate[index],
                    "observed": observed[index],
                    "conditioned_profile": exact[index],
                    "unconditioned_profile": unconditioned[index],
                    "affine_profile": affine[index],
                }
            )
    return summary, shape_rows


def compressed_return_spectrum(
    matrix,
    masks: list[np.ndarray],
    period: int,
    sigma: float,
    count: int = 5,
) -> list[dict[str, object]]:
    endpoint_indices = np.flatnonzero(masks[0])
    dimension = matrix.shape[0]

    def matvec(vector: np.ndarray) -> np.ndarray:
        full = np.zeros(dimension, dtype=np.float64)
        full[endpoint_indices] = vector
        for index in range(period - 1, -1, -1):
            full = matrix @ (matrix @ full)
            full[~masks[index]] = 0.0
        return full[endpoint_indices]

    operator = LinearOperator(
        (endpoint_indices.size, endpoint_indices.size),
        matvec=matvec,
        dtype=np.float64,
    )
    values = eigs(
        operator,
        k=min(int(count), endpoint_indices.size - 2),
        which="LM",
        tol=1.0e-8,
        maxiter=2000,
        return_eigenvectors=False,
    )
    values = values[np.argsort(-np.abs(values))]
    leading = abs(values[0])
    rows: list[dict[str, object]] = []
    for index, value in enumerate(values):
        rows.append(
            {
                "sigma": sigma,
                "component_period": period,
                "return_order": index,
                "return_real": value.real,
                "return_imag": value.imag,
                "return_modulus": abs(value),
                "modulus_ratio_to_principal": abs(value) / leading,
                "one_step_root_radius": abs(value) ** (1.0 / (2.0 * period)),
            }
        )
    return rows


def window_rows(
    sigma: float,
    cycle,
    points: np.ndarray,
    tube,
    grid: np.ndarray,
    matrix,
) -> list[dict[str, object]]:
    constants = critical_constants(100)
    rows: list[dict[str, object]] = []
    for window in (2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0):
        masks = packet_masks(
            grid,
            points,
            sigma * tube.widths,
            window_multiple=window,
            critical_partition=float(constants.first_interior_point),
        )
        initial = np.exp(
            -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
        )
        pair = principal_return_eigenpair(
            matrix, masks, initial, iterations=POWER_ITERATIONS
        )
        rows.append(
            {
                "sigma": sigma,
                "component_period": cycle.component_period,
                "window_multiple": window,
                "endpoint_nodes": int(np.count_nonzero(masks[0])),
                "critical_branch_nodes": int(np.count_nonzero(masks[-1])),
                "return_eigenvalue": pair.eigenvalue,
                "one_step_edge_radius": pair.eigenvalue
                ** (1.0 / (2.0 * cycle.component_period)),
                "return_residual": pair.residual,
            }
        )
    return rows


def spectral_and_profile_audit():
    archived = read_csv(RH15 / "results" / "cloud_summary.csv")
    clearances = boundary_clearances(70, decimal_digits=110)
    edge_rows: list[dict[str, object]] = []
    critical_rows: list[dict[str, object]] = []
    shape_rows: list[dict[str, object]] = []
    spectrum_rows: list[dict[str, object]] = []
    all_window_rows: list[dict[str, object]] = []

    for row in archived:
        sigma = float(row["sigma"])
        dimension = int(float(row["folded_dimension"]))
        hellinger_degree = intrinsic_degree(clearances, sigma, 0.5)
        linear_degree = intrinsic_degree(clearances, sigma, 1.0)
        print(
            f"local return sigma={sigma:g}, n={dimension}, "
            f"N_H={hellinger_degree}, N_L={linear_degree}",
            flush=True,
        )
        started = time.time()
        matrix = sparse_folded_gaussian_matrix(
            dimension, sigma, u=float(critical_constants(100).u)
        )
        row_error = float(
            np.max(np.abs(np.asarray(matrix.sum(axis=1)).ravel() - 1.0))
        )
        (
            constants,
            cycle,
            points,
            tube,
            grid,
            _,
            masks,
            pair,
            hellinger_radius,
        ) = local_context(
            sigma, dimension, hellinger_degree + 1, matrix=matrix
        )
        critical, shapes = profile_errors(
            sigma, cycle, points, tube, grid, matrix, masks
        )
        critical_rows.append(critical)
        shape_rows.extend(shapes)

        if linear_degree == hellinger_degree:
            linear_radius = hellinger_radius
        else:
            linear_context = local_context(
                sigma, dimension, linear_degree + 1, matrix=matrix
            )
            linear_radius = linear_context[-1]

        edge_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "dimension_times_sigma": dimension * sigma,
                "row_sum_error": row_error,
                "hellinger_degree": hellinger_degree,
                "linear_row_degree": linear_degree,
                "cloud_degree": int(float(row["effective_cloud_degree"])),
                "component_period": hellinger_degree + 1,
                "principal_return_eigenvalue": pair.eigenvalue,
                "local_one_step_edge_radius": hellinger_radius,
                "linear_degree_local_radius": linear_radius,
                "deterministic_cycle_radius": float(cycle.one_step_radius),
                "archived_bulk_radius": float(row["bulk_radius"]),
                "archived_cloud_mean_radius": float(row["cloud_radial_mean"]),
                "local_minus_bulk_radius": hellinger_radius
                - float(row["bulk_radius"]),
                "deterministic_minus_bulk_radius": float(cycle.one_step_radius)
                - float(row["bulk_radius"]),
                "return_residual": pair.residual,
                "endpoint_window_nodes": int(np.count_nonzero(masks[0])),
                "critical_branch_nodes": int(np.count_nonzero(masks[-1])),
                "build_and_return_seconds": time.time() - started,
            }
        )

        if sigma in SPECTRUM_SIGMAS:
            print(f"return spectrum sigma={sigma:g}", flush=True)
            spectrum_rows.extend(
                compressed_return_spectrum(
                    matrix, masks, cycle.component_period, sigma
                )
            )
        if abs(sigma - CRITICAL_SHAPE_SIGMA) < 1.0e-15:
            all_window_rows.extend(
                window_rows(sigma, cycle, points, tube, grid, matrix)
            )
        del matrix
        release_memory()

    write_csv(RESULTS / "local_return_edge.csv", edge_rows)
    write_csv(RESULTS / "critical_profile_audit.csv", critical_rows)
    write_csv(RESULTS / "critical_profile_shape.csv", shape_rows)
    write_csv(RESULTS / "local_return_spectrum.csv", spectrum_rows)
    write_csv(RESULTS / "window_robustness.csv", all_window_rows)
    return edge_rows, critical_rows, shape_rows, spectrum_rows, all_window_rows


def resolution_rows() -> list[dict[str, object]]:
    sigma = 1.0e-3
    period = 6
    rows: list[dict[str, object]] = []
    for dimension in (10240, 20480, 40960):
        print(f"resolution sigma={sigma:g}, n={dimension}", flush=True)
        context = local_context(sigma, dimension, period)
        pair = context[-2]
        radius = context[-1]
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "dimension_times_sigma": dimension * sigma,
                "component_period": period,
                "principal_return_eigenvalue": pair.eigenvalue,
                "one_step_edge_radius": radius,
                "return_residual": pair.residual,
            }
        )
        del context
        release_memory()
    write_csv(RESULTS / "local_return_resolution.csv", rows)
    return rows


def selected_cloud(sigma: float) -> np.ndarray:
    values: list[complex] = []
    for row in read_csv(RH15 / "results" / "outer_resonance_cloud.csv"):
        if abs(float(row["sigma"]) - sigma) > 1.0e-15:
            continue
        if not row["expected_radius"]:
            continue
        value = complex(float(row["real"]), float(row["imag"]))
        values.extend((value, np.conjugate(value)))
    return np.asarray(values, dtype=np.complex128)


def plot_riccati_critical(
    riccati: list[dict[str, object]],
    critical: list[dict[str, object]],
    shape: list[dict[str, object]],
) -> None:
    _, _, points, _, _, tube = cycle_data(20)
    indices = np.arange(points.size)
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axis = axes[0, 0]
    axis.semilogy(indices, tube.widths, "o-", color="#2455a4", label=r"width $t_{k,j}$")
    second = axis.twinx()
    second.plot(indices, tube.coefficients, "s--", color="#a0273f", label=r"coefficient $c_{k,j}$")
    axis.set(xlabel=r"time index $j$", ylabel="dimensionless width", title=r"Periodic Riccati tube ($k=20$)")
    second.set_ylabel("channel coefficient")
    lines = axis.get_lines() + second.get_lines()
    axis.legend(lines, [line.get_label() for line in lines], frameon=False, fontsize=8, loc="center left")
    axis.grid(alpha=0.22)

    periods = np.asarray([int(row["component_period"]) for row in riccati])
    raw = np.asarray([float(row["raw_balancing_condition"]) for row in riccati])
    packet = np.asarray([float(row["packet_balancing_condition"]) for row in riccati])
    lambda_fixed = float(critical_constants(100).lambda_fixed)
    axes[0, 1].semilogy(periods, raw, label="raw inverse-Jacobian", color="#2455a4")
    axes[0, 1].semilogy(periods, packet, label="Riccati packet", color="#a0273f")
    axes[0, 1].semilogy(periods, 0.40 * lambda_fixed**periods, ":", color="0.25", label=r"$0.40\lambda^k$")
    axes[0, 1].semilogy(periods, 0.66 * lambda_fixed ** (0.5 * periods), "--", color="0.45", label=r"$0.66\lambda^{k/2}$")
    axes[0, 1].set(xlabel=r"component period $k$", ylabel="balancing condition", title="Gaussian adaptation halves the exponent")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    q = np.asarray([float(row["scaled_coordinate"]) for row in shape])
    axes[1, 0].plot(q, [float(row["observed"]) for row in shape], color="black", lw=2.0, label="folded operator")
    axes[1, 0].plot(q, [float(row["conditioned_profile"]) for row in shape], "--", color="#2455a4", label="conditioned critical profile")
    axes[1, 0].plot(q, [float(row["unconditioned_profile"]) for row in shape], ":", color="#25865f", label="unconditioned quartic")
    axes[1, 0].plot(q, [float(row["affine_profile"]) for row in shape], "-.", color="#a0273f", label="affine Gaussian")
    axes[1, 0].set(xlabel=r"critical coordinate $q$", ylabel="pulled-back observable", title=r"Critical closure at $\sigma=10^{-3}$")
    axes[1, 0].legend(frameon=False, fontsize=7)
    axes[1, 0].grid(alpha=0.22)

    sigma = np.asarray([float(row["sigma"]) for row in critical])
    exact_error = np.asarray([float(row["conditioned_profile_direct_error"]) for row in critical])
    unconditioned_error = np.asarray([float(row["unconditioned_profile_direct_error"]) for row in critical])
    affine_error = np.asarray([float(row["affine_profile_direct_error"]) for row in critical])
    order = np.argsort(sigma)[::-1]
    axes[1, 1].loglog(sigma[order], exact_error[order], "o-", label="conditioned critical", color="#2455a4")
    axes[1, 1].loglog(sigma[order], unconditioned_error[order], "s--", label="unconditioned quartic", color="#25865f")
    axes[1, 1].loglog(sigma[order], affine_error[order], "^:", label="affine Gaussian", color="#a0273f")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(xlabel=r"noise $\sigma$", ylabel="relative profile error", title="Only the conditioned profile converges")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)
    fig.tight_layout()
    fig.savefig(FIGURES / "riccati_packet_critical_closure.pdf")
    fig.savefig(FIGURES / "riccati_packet_critical_closure.png", dpi=220)
    plt.close(fig)


def plot_local_edge(
    edge: list[dict[str, object]], spectrum: list[dict[str, object]]
) -> None:
    sigma = np.asarray([float(row["sigma"]) for row in edge])
    local = np.asarray([float(row["local_one_step_edge_radius"]) for row in edge])
    linear = np.asarray([float(row["linear_degree_local_radius"]) for row in edge])
    deterministic = np.asarray([float(row["deterministic_cycle_radius"]) for row in edge])
    bulk = np.asarray([float(row["archived_bulk_radius"]) for row in edge])
    order = np.argsort(sigma)[::-1]
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].semilogx(sigma[order], bulk[order], "o-", color="black", label="archived bulk radius")
    axes[0, 0].semilogx(sigma[order], local[order], "s--", color="#2455a4", label="Hellinger-rank local return")
    axes[0, 0].semilogx(sigma[order], linear[order], "^:", color="#25865f", label="linear-rank local return")
    axes[0, 0].semilogx(sigma[order], deterministic[order], "d-.", color="#a0273f", label="RH-17 deterministic cycle")
    axes[0, 0].invert_xaxis()
    axes[0, 0].set(xlabel=r"noise $\sigma$", ylabel="one-step radius", title="Branch-isolated return locates the bulk edge")
    axes[0, 0].legend(frameon=False, fontsize=7)
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].loglog(sigma[order], np.abs(local - bulk)[order], "o-", color="#2455a4", label="local return error")
    axes[0, 1].loglog(sigma[order], np.abs(deterministic - bulk)[order], "s--", color="#a0273f", label="deterministic-cycle error")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(xlabel=r"noise $\sigma$", ylabel="absolute radial error", title="The nonlinear local correction wins in the tail")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    smallest = edge[int(np.argmin(sigma))]
    selected_sigma = float(smallest["sigma"])
    period = int(smallest["component_period"])
    observed = selected_cloud(selected_sigma)
    local_ring = bipartite_root_ring(
        float(smallest["principal_return_eigenvalue"]), period
    )
    local_ring = local_ring[np.abs(local_ring.imag) > 1.0e-10]
    deterministic_cloud = ideal_reciprocal_cloud(boundary_cycle(period, 120))
    axes[1, 0].scatter(observed.real, observed.imag, facecolors="none", edgecolors="black", s=38, label="archived cloud")
    axes[1, 0].scatter(local_ring.real, local_ring.imag, marker="x", color="#2455a4", s=42, label="local-return outer ring")
    axes[1, 0].scatter(deterministic_cloud.real, deterministic_cloud.imag, marker="+", color="#a0273f", s=34, label="RH-17 finite ring")
    axes[1, 0].axhline(0.0, color="0.8", lw=0.7)
    axes[1, 0].axvline(0.0, color="0.8", lw=0.7)
    axes[1, 0].set_aspect("equal")
    axes[1, 0].set(xlabel=r"$\operatorname{Re}\mu$", ylabel=r"$\operatorname{Im}\mu$", title=rf"Two radial roles at $\sigma={selected_sigma:g}$")
    axes[1, 0].legend(frameon=False, fontsize=7, loc="lower left")
    axes[1, 0].grid(alpha=0.15)

    grouped: dict[float, list[dict[str, object]]] = {}
    for row in spectrum:
        grouped.setdefault(float(row["sigma"]), []).append(row)
    for selected_sigma, rows in sorted(grouped.items(), reverse=True):
        rows = sorted(rows, key=lambda row: int(row["return_order"]))
        axes[1, 1].semilogy(
            [int(row["return_order"]) for row in rows],
            [float(row["modulus_ratio_to_principal"]) for row in rows],
            "o-",
            label=rf"$\sigma={selected_sigma:g}$",
        )
    axes[1, 1].set(xlabel="return eigenvalue order", ylabel="modulus / principal modulus", title="The branch return is asymptotically rank one")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)
    fig.tight_layout()
    fig.savefig(FIGURES / "branch_isolated_bulk_edge.pdf")
    fig.savefig(FIGURES / "branch_isolated_bulk_edge.png", dpi=220)
    plt.close(fig)


def write_summary(
    riccati,
    edge,
    critical,
    spectrum,
    window,
    resolution,
) -> None:
    local_error = np.asarray([abs(float(row["local_minus_bulk_radius"])) for row in edge])
    deterministic_error = np.asarray([abs(float(row["deterministic_minus_bulk_radius"])) for row in edge])
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "window_multiple": WINDOW_MULTIPLE,
        "power_iterations": POWER_ITERATIONS,
        "packet_condition_exponent_at_k100": float(riccati[-1]["packet_condition_exponent"]),
        "raw_condition_exponent_at_k100": float(riccati[-1]["raw_condition_exponent"]),
        "smallest_noise_local_edge_error": float(local_error[-1]),
        "smallest_noise_critical_profile_error": float(critical[-1]["conditioned_profile_direct_error"]),
        "tail_three_local_edge_rms_error": float(np.sqrt(np.mean(local_error[-3:] ** 2))),
        "tail_three_deterministic_edge_rms_error": float(np.sqrt(np.mean(deterministic_error[-3:] ** 2))),
        "smallest_noise_return_gap_ratio": float(
            [row for row in spectrum if float(row["sigma"]) == 1.0e-4 and int(row["return_order"]) == 1][0]["modulus_ratio_to_principal"]
        ),
        "window_radius_range_L4_to_L10": float(
            np.ptp([
                float(row["one_step_edge_radius"])
                for row in window
                if float(row["window_multiple"]) >= 4.0
            ])
        ),
        "resolution_radius_range": float(
            np.ptp([float(row["one_step_edge_radius"]) for row in resolution])
        ),
        "source_hashes": {
            "riccati.py": source_hash(ROOT / "src" / "gaussian_return" / "riccati.py"),
            "critical.py": source_hash(ROOT / "src" / "gaussian_return" / "critical.py"),
            "cyclic.py": source_hash(ROOT / "src" / "gaussian_return" / "cyclic.py"),
            "operators.py": source_hash(ROOT / "src" / "gaussian_return" / "operators.py"),
            "audit.py": source_hash(Path(__file__)),
            "rh15_cloud_summary.csv": source_hash(RH15 / "results" / "cloud_summary.csv"),
        },
    }
    with (RESULTS / "gaussian_return_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    riccati = riccati_rows()
    edge, critical, shape, spectrum, window = spectral_and_profile_audit()
    resolution = resolution_rows()
    plot_riccati_critical(riccati, critical, shape)
    plot_local_edge(edge, spectrum)
    write_summary(riccati, edge, critical, spectrum, window, resolution)
    print("generated RH-18 data, figures, spectra, and summary", flush=True)


if __name__ == "__main__":
    main()
