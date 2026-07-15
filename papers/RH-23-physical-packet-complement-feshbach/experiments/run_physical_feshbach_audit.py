"""Build physical packet/complement closures for selected noise scales."""

from __future__ import annotations

import argparse
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
from scipy.sparse.linalg import LinearOperator, eigs, gmres


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH17 = PAPERS / "RH-17-time-ordered-boundary-monodromy"
RH18 = PAPERS / "RH-18-branch-isolated-gaussian-return"
RH19 = PAPERS / "RH-19-complement-excursion-self-energy"
RH20 = PAPERS / "RH-20-sector-resolved-critical-branches"
RH21 = PAPERS / "RH-21-peripheral-biorthogonal-branch-collapse"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH17 / "src"),
    str(RH18 / "src"),
    str(RH19 / "src"),
    str(RH20 / "src"),
    str(RH21 / "src"),
]

from biorthogonal_branches import (  # noqa: E402
    canonical_biorthogonal_pair,
    propagate_branch_histories,
)
from complement_excursions import critical_branch_masks  # noqa: E402
from gaussian_return import (  # noqa: E402
    effective_noise_scales,
    packet_masks,
    periodic_packet_tube,
    positive_midpoints,
    sparse_folded_gaussian_matrix,
)
from physical_feshbach import (  # noqa: E402
    bright_history_trial,
    critical_bright_trial,
    eigenmode_closure,
    external_project,
    label_resolved_trial,
    single_label_trial,
)
from sector_branches import branch_profile_basis  # noqa: E402
from time_ordered_monodromy import boundary_cycle, critical_constants  # noqa: E402


WINDOW_MULTIPLE = 6.0
WINDOW_MULTIPLES = (4.5, 5.0, 6.0, 7.0, 8.0)
DEFAULT_SIGMAS = (1.0e-2, 4.0e-3, 2.0e-3, 1.0e-3, 5.0e-4, 2.0e-4, 1.0e-4)
EIGENVALUE_COUNT = 20


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_memory() -> None:
    gc.collect()
    try:
        ctypes.CDLL(None).malloc_trim(0)
    except (AttributeError, OSError):
        pass


def deterministic_start(dimension: int, phase: float = 0.0) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    vector = np.sin((index + 0.5) * np.sqrt(2.0) + phase)
    vector += 0.37 * np.cos((index + 0.5) * np.sqrt(3.0) - phase)
    return vector / np.linalg.norm(vector)


def archived_settings() -> dict[float, dict[str, object]]:
    cloud = {
        float(row["sigma"]): row
        for row in read_csv(RH15 / "results" / "cloud_summary.csv")
    }
    periods = {
        float(row["sigma"]): int(row["component_period"])
        for row in read_csv(RH20 / "results" / "two_branch_matrix_audit.csv")
    }
    points = read_csv(RH15 / "results" / "outer_resonance_cloud.csv")
    output: dict[float, dict[str, object]] = {}
    for sigma, row in cloud.items():
        selected = [
            item
            for item in points
            if float(item["sigma"]) == sigma
            and item["positive_order"] == "selected"
            and float(item["imag"]) > 0.0
        ]
        target = max(selected, key=lambda item: float(item["radius"]))
        output[sigma] = {
            "dimension": int(row["folded_dimension"]),
            "period": periods[sigma],
            "archived_mu": complex(float(target["real"]), float(target["imag"])),
            "archived_radius": float(row["bulk_radius"]),
        }
    return output


def resolve_eigensystem(matrix, archived_mu: complex, count: int):
    dimension = matrix.shape[0]
    count = min(int(count), dimension - 2)
    print(f"  right eigensystem k={count}", flush=True)
    values_r, vectors_r = eigs(
        matrix,
        k=count,
        which="LM",
        tol=2.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension),
    )
    print(f"  left eigensystem k={count}", flush=True)
    values_l, vectors_l = eigs(
        matrix.T,
        k=count,
        which="LM",
        tol=2.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension, 0.37),
    )

    real_indices = np.flatnonzero(np.abs(values_r.imag) < 2.0e-8)
    perron_index = int(real_indices[np.argmin(np.abs(values_r[real_indices] - 1.0))])
    remaining_real = real_indices[real_indices != perron_index]
    parity_index = int(remaining_real[np.argmin(values_r[remaining_real].real)])
    right_modes = []
    left_modes = []
    peripheral_values = []
    peripheral_residuals = []
    for index in (perron_index, parity_index):
        eigenvalue = float(values_r[index].real)
        left_index = int(np.argmin(np.abs(values_l - eigenvalue)))
        right = np.asarray(vectors_r[:, index].real)
        left = np.asarray(vectors_l[:, left_index].real)
        pairing = np.dot(left, right)
        left = left / pairing
        right_modes.append(right)
        left_modes.append(left)
        peripheral_values.append(eigenvalue)
        peripheral_residuals.extend(
            (
                np.linalg.norm(matrix @ right - eigenvalue * right) / np.linalg.norm(right),
                np.linalg.norm(matrix.T @ left - eigenvalue * left) / np.linalg.norm(left),
            )
        )

    positive = np.flatnonzero(values_r.imag > 1.0e-8)
    target_index = int(positive[np.argmin(np.abs(values_r[positive] - archived_mu))])
    mu = complex(values_r[target_index])
    right = np.asarray(vectors_r[:, target_index], dtype=np.complex128)
    right /= np.linalg.norm(right)
    left_index = int(np.argmin(np.abs(values_l - np.conjugate(mu))))
    left = np.asarray(vectors_l[:, left_index], dtype=np.complex128)
    pairing = np.vdot(left, right)
    left /= np.conjugate(pairing)
    right_residual = np.linalg.norm(matrix @ right - mu * right) / np.linalg.norm(right)
    left_residual = np.linalg.norm(matrix.T @ left - np.conjugate(mu) * left) / np.linalg.norm(left)
    return {
        "mu": mu,
        "right": right,
        "left": left,
        "right_modes": np.column_stack(right_modes),
        "left_modes": np.column_stack(left_modes),
        "peripheral_values": np.asarray(peripheral_values),
        "maximum_peripheral_residual": float(max(peripheral_residuals)),
        "right_residual": float(right_residual),
        "left_residual": float(left_residual),
        "left_right_pairing": complex(np.vdot(left, right)),
        "eigenvalue_condition": float(np.linalg.norm(left) * np.linalg.norm(right)),
        "archived_eigenvalue_error": float(abs(mu - archived_mu)),
    }


def packet_trial(
    matrix,
    sigma: float,
    dimension: int,
    period: int,
    *,
    window_multiple: float = WINDOW_MULTIPLE,
):
    constants = critical_constants(130)
    cycle = boundary_cycle(period, 130)
    points = np.asarray([float(value) for value in cycle.orbit])
    multipliers = np.abs(
        np.asarray([float(value) for value in cycle.two_step_derivatives])
    )
    tube = periodic_packet_tube(
        multipliers, effective_noise_scales(points, float(constants.u))
    )
    grid = positive_midpoints(dimension)
    base = packet_masks(
        grid,
        points,
        sigma * tube.widths,
        window_multiple=float(window_multiple),
        critical_partition=float(constants.first_interior_point),
    )
    left, right, both = critical_branch_masks(
        grid,
        base,
        points[-1],
        sigma * tube.widths[-1],
        window_multiple=float(window_multiple),
        partition=float(constants.first_interior_point),
    )

    def two_step(values):
        return matrix @ (matrix @ values)

    endpoint = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    endpoint[~left[0]] = 0.0
    endpoint /= np.linalg.norm(endpoint)
    critical = two_step(endpoint)
    basis = branch_profile_basis(critical, left[-1], right[-1])
    histories = propagate_branch_histories(two_step, left[:-1], basis)
    trial = bright_history_trial(histories)
    return {
        "trial": trial,
        "histories": histories,
        "left": left,
        "right": right,
        "both": both,
        "points": points,
        "tube": tube,
    }


def bulk_operator(matrix, eigensystem):
    right = eigensystem["right_modes"]
    left = eigensystem["left_modes"]
    values = eigensystem["peripheral_values"]

    def one_step(source):
        array = np.asarray(source)
        coefficients = left.T @ array
        if array.ndim == 1:
            return matrix @ array - right @ (values * coefficients)
        return matrix @ array - right @ (values[:, None] * coefficients)

    def two_step(source):
        return one_step(one_step(source))

    return one_step, two_step


def gmres_external_solve(
    two_step,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    zeta: complex,
    forcing: np.ndarray,
    exact_external: np.ndarray,
    *,
    rtol: float = 2.0e-8,
    restart: int = 80,
    maxiter: int = 20,
) -> dict[str, object]:
    dimension = synthesis.shape[0]

    def action(vector):
        source = external_project(vector, synthesis, analysis)
        return zeta * vector - external_project(
            two_step(source), synthesis, analysis
        )

    operator = LinearOperator(
        (dimension, dimension),
        matvec=action,
        dtype=np.complex128,
    )
    history: list[float] = []
    started = time.time()
    solution, info = gmres(
        operator,
        forcing,
        rtol=rtol,
        atol=0.0,
        restart=restart,
        maxiter=maxiter,
        callback=lambda residual: history.append(float(residual)),
        callback_type="pr_norm",
    )
    elapsed = time.time() - started
    residual = np.linalg.norm(action(solution) - forcing) / max(
        np.linalg.norm(forcing), np.finfo(float).tiny
    )
    exact_error = np.linalg.norm(solution - exact_external) / max(
        np.linalg.norm(exact_external), np.finfo(float).tiny
    )
    return {
        "gmres_info": int(info),
        "gmres_iterations": len(history),
        "gmres_final_callback_residual": history[-1] if history else np.nan,
        "gmres_true_residual": float(residual),
        "gmres_external_solution_error": float(exact_error),
        "gmres_elapsed_seconds": elapsed,
    }


def audit_scale(sigma: float, setting: dict[str, object], run_gmres: bool):
    dimension = int(setting["dimension"])
    period = int(setting["period"])
    archived_mu = complex(setting["archived_mu"])
    print(f"physical Feshbach sigma={sigma:g}, n={dimension}, k={period}", flush=True)
    started = time.time()
    constants = critical_constants(130)
    matrix = sparse_folded_gaussian_matrix(
        dimension, sigma, u=float(constants.u)
    )
    build_seconds = time.time() - started
    started = time.time()
    modes = resolve_eigensystem(matrix, archived_mu, EIGENVALUE_COUNT)
    eigensolve_seconds = time.time() - started
    packet = packet_trial(matrix, sigma, dimension, period)
    pair = canonical_biorthogonal_pair(
        packet["trial"], modes["right_modes"], modes["left_modes"]
    )
    _, two_step = bulk_operator(matrix, modes)
    mu = modes["mu"]
    zeta = mu * mu
    closure = eigenmode_closure(
        two_step,
        pair.synthesis,
        pair.analysis,
        zeta,
        modes["right"],
    )
    direct_values = np.linalg.eigvals(closure.reduced)
    direct_closest = direct_values[np.argmin(np.abs(direct_values - zeta))]
    pencil = zeta * np.eye(closure.reduced.shape[0]) - closure.reduced
    pencil_singular = np.linalg.svd(pencil, compute_uv=False)
    packet_projection = closure.packet_component
    physical_self_energy = pair.synthesis @ closure.external_self_energy_action
    spectral_weight = np.vdot(modes["left"], packet_projection)
    t_residual = np.linalg.norm(
        two_step(modes["right"]) - zeta * modes["right"]
    ) / np.linalg.norm(modes["right"])
    row: dict[str, object] = {
        "sigma": sigma,
        "folded_dimension": dimension,
        "component_period": period,
        "packet_rank": pair.synthesis.shape[1],
        "archived_mu_real": archived_mu.real,
        "archived_mu_imag": archived_mu.imag,
        "physical_mu_real": mu.real,
        "physical_mu_imag": mu.imag,
        "physical_mu_radius": abs(mu),
        "physical_mu_phase": np.angle(mu),
        "two_step_target_real": zeta.real,
        "two_step_target_imag": zeta.imag,
        "two_step_target_radius": abs(zeta),
        "two_step_target_phase": np.angle(zeta),
        "return_target_phase": np.angle(mu ** (2 * period)),
        "archived_eigenvalue_error": modes["archived_eigenvalue_error"],
        "right_eigen_residual": modes["right_residual"],
        "left_eigen_residual": modes["left_residual"],
        "left_right_pairing_error": abs(modes["left_right_pairing"] - 1.0),
        "two_step_eigen_residual": t_residual,
        "target_eigenvalue_condition": modes["eigenvalue_condition"],
        "maximum_peripheral_residual": modes["maximum_peripheral_residual"],
        "packet_gram_condition": float(np.linalg.cond(pair.gram)),
        "packet_pair_residual": max(
            pair.biorthogonality_residual,
            pair.right_annihilation_residual,
            pair.left_annihilation_residual,
        ),
        "packet_component_norm": closure.packet_component_norm,
        "external_component_norm": closure.external_component_norm,
        "external_to_packet_component_ratio": closure.external_component_norm
        / closure.packet_component_norm,
        "external_forcing_to_packet_component_ratio": closure.forcing_norm
        / closure.packet_component_norm,
        "coordinate_norm": closure.coordinate_norm,
        "spectral_packet_weight_real": spectral_weight.real,
        "spectral_packet_weight_imag": spectral_weight.imag,
        "spectral_packet_weight_modulus": abs(spectral_weight),
        "direct_closest_real": direct_closest.real,
        "direct_closest_imag": direct_closest.imag,
        "direct_closest_distance": abs(direct_closest - zeta),
        "direct_pencil_smallest_singular": float(pencil_singular[-1]),
        "direct_pencil_largest_singular": float(pencil_singular[0]),
        "self_energy_action_norm": float(
            np.linalg.norm(closure.external_self_energy_action)
        ),
        "packet_defect_norm": float(np.linalg.norm(closure.packet_defect)),
        "self_energy_to_target_coordinate_ratio": float(
            np.linalg.norm(closure.external_self_energy_action)
            / max(abs(zeta) * closure.coordinate_norm, np.finfo(float).tiny)
        ),
        "physical_self_energy_to_target_packet_ratio": float(
            np.linalg.norm(physical_self_energy)
            / max(
                abs(zeta) * closure.packet_component_norm,
                np.finfo(float).tiny,
            )
        ),
        "external_forcing_norm": closure.forcing_norm,
        "external_resolvent_lower_bound": closure.resolvent_lower_bound,
        "projection_resolvent_compensation": closure.packet_component_norm
        * closure.resolvent_lower_bound,
        "packet_closure_residual": closure.packet_closure_residual,
        "external_equation_residual": closure.external_equation_residual,
        "matrix_build_seconds": build_seconds,
        "eigensolve_seconds": eigensolve_seconds,
    }
    if run_gmres:
        row.update(
            gmres_external_solve(
                two_step,
                pair.synthesis,
                pair.analysis,
                zeta,
                closure.external_forcing,
                closure.external_component,
            )
        )
    variants = {
        "branch_complete": packet["trial"],
        "critical_bright": critical_bright_trial(packet["histories"]),
        "left_label": single_label_trial(packet["histories"], 0),
        "right_label": single_label_trial(packet["histories"], 1),
        "all_labels": label_resolved_trial(packet["histories"]),
    }
    variant_rows: list[dict[str, object]] = []
    for model, trial in variants.items():
        variant_pair = canonical_biorthogonal_pair(
            trial, modes["right_modes"], modes["left_modes"]
        )
        variant_closure = eigenmode_closure(
            two_step,
            variant_pair.synthesis,
            variant_pair.analysis,
            zeta,
            modes["right"],
        )
        variant_values = np.linalg.eigvals(variant_closure.reduced)
        variant_closest = variant_values[np.argmin(np.abs(variant_values - zeta))]
        variant_weight = np.vdot(modes["left"], variant_closure.packet_component)
        variant_physical_self_energy = (
            variant_pair.synthesis @ variant_closure.external_self_energy_action
        )
        variant_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "component_period": period,
                "packet_model": model,
                "packet_rank": trial.shape[1],
                "packet_gram_condition": float(np.linalg.cond(variant_pair.gram)),
                "synthesis_norm": float(np.linalg.norm(variant_pair.synthesis, ord=2)),
                "analysis_norm": float(np.linalg.norm(variant_pair.analysis, ord=2)),
                "packet_pair_residual": max(
                    variant_pair.biorthogonality_residual,
                    variant_pair.right_annihilation_residual,
                    variant_pair.left_annihilation_residual,
                ),
                "packet_component_norm": variant_closure.packet_component_norm,
                "external_component_norm": variant_closure.external_component_norm,
                "external_to_packet_component_ratio": variant_closure.external_component_norm
                / variant_closure.packet_component_norm,
                "spectral_packet_weight_real": variant_weight.real,
                "spectral_packet_weight_imag": variant_weight.imag,
                "spectral_packet_weight_modulus": abs(variant_weight),
                "direct_closest_distance": abs(variant_closest - zeta),
                "self_energy_action_norm": float(
                    np.linalg.norm(variant_closure.external_self_energy_action)
                ),
                "self_energy_to_target_coordinate_ratio": float(
                    np.linalg.norm(variant_closure.external_self_energy_action)
                    / max(
                        abs(zeta) * variant_closure.coordinate_norm,
                        np.finfo(float).tiny,
                    )
                ),
                "physical_self_energy_to_target_packet_ratio": float(
                    np.linalg.norm(variant_physical_self_energy)
                    / max(
                        abs(zeta) * variant_closure.packet_component_norm,
                        np.finfo(float).tiny,
                    )
                ),
                "external_forcing_norm": variant_closure.forcing_norm,
                "external_resolvent_lower_bound": variant_closure.resolvent_lower_bound,
                "packet_closure_residual": variant_closure.packet_closure_residual,
                "external_equation_residual": variant_closure.external_equation_residual,
            }
        )
    window_rows: list[dict[str, object]] = []
    for window_multiple in WINDOW_MULTIPLES:
        window_packet = (
            packet
            if window_multiple == WINDOW_MULTIPLE
            else packet_trial(
                matrix,
                sigma,
                dimension,
                period,
                window_multiple=window_multiple,
            )
        )
        window_pair = canonical_biorthogonal_pair(
            window_packet["trial"], modes["right_modes"], modes["left_modes"]
        )
        window_closure = eigenmode_closure(
            two_step,
            window_pair.synthesis,
            window_pair.analysis,
            zeta,
            modes["right"],
        )
        window_values = np.linalg.eigvals(window_closure.reduced)
        window_closest = window_values[np.argmin(np.abs(window_values - zeta))]
        window_weight = np.vdot(modes["left"], window_closure.packet_component)
        window_physical_self_energy = (
            window_pair.synthesis @ window_closure.external_self_energy_action
        )
        window_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "component_period": period,
                "window_multiple": window_multiple,
                "packet_rank": window_pair.synthesis.shape[1],
                "packet_gram_condition": float(np.linalg.cond(window_pair.gram)),
                "analysis_norm": float(np.linalg.norm(window_pair.analysis, ord=2)),
                "packet_component_norm": window_closure.packet_component_norm,
                "external_to_packet_component_ratio": window_closure.external_component_norm
                / window_closure.packet_component_norm,
                "spectral_packet_weight_modulus": abs(window_weight),
                "direct_closest_distance": abs(window_closest - zeta),
                "self_energy_to_target_coordinate_ratio": float(
                    np.linalg.norm(window_closure.external_self_energy_action)
                    / max(
                        abs(zeta) * window_closure.coordinate_norm,
                        np.finfo(float).tiny,
                    )
                ),
                "physical_self_energy_to_target_packet_ratio": float(
                    np.linalg.norm(window_physical_self_energy)
                    / max(
                        abs(zeta) * window_closure.packet_component_norm,
                        np.finfo(float).tiny,
                    )
                ),
                "external_resolvent_lower_bound": window_closure.resolvent_lower_bound,
                "packet_closure_residual": window_closure.packet_closure_residual,
                "external_equation_residual": window_closure.external_equation_residual,
            }
        )
    del matrix, packet, pair, modes, closure
    release_memory()
    return row, variant_rows, window_rows


def scaling_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    fields = (
        "packet_component_norm",
        "external_to_packet_component_ratio",
        "target_eigenvalue_condition",
        "external_resolvent_lower_bound",
        "spectral_packet_weight_modulus",
        "direct_closest_distance",
        "physical_self_energy_to_target_packet_ratio",
    )
    output: list[dict[str, object]] = []
    for domain, selected in (
        ("all", rows),
        ("tail_sigma_le_1e-3", [row for row in rows if float(row["sigma"]) <= 1.0e-3]),
    ):
        if len(selected) < 3:
            continue
        x = np.log(np.asarray([float(row["sigma"]) for row in selected]))
        for field in fields:
            y = np.log(np.asarray([float(row[field]) for row in selected]))
            slope, intercept = np.polyfit(x, y, 1)
            predicted = slope * x + intercept
            denominator = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1.0 - np.sum((y - predicted) ** 2) / denominator
            output.append(
                {
                    "domain": domain,
                    "field": field,
                    "point_count": len(selected),
                    "minimum_sigma": min(float(row["sigma"]) for row in selected),
                    "maximum_sigma": max(float(row["sigma"]) for row in selected),
                    "log_log_slope": slope,
                    "log_intercept": intercept,
                    "r_squared": r_squared,
                }
            )
    return output


def plot_physical_closure(rows: list[dict[str, object]]) -> None:
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in ordered])
    mu = np.asarray(
        [complex(float(row["physical_mu_real"]), float(row["physical_mu_imag"])) for row in ordered]
    )
    return_phase = np.asarray([float(row["return_target_phase"]) for row in ordered])
    direct_distance = np.asarray([float(row["direct_closest_distance"]) for row in ordered])
    pencil_min = np.asarray([float(row["direct_pencil_smallest_singular"]) for row in ordered])
    self_energy = np.asarray(
        [float(row["physical_self_energy_to_target_packet_ratio"]) for row in ordered]
    )
    packet_residual = np.asarray([float(row["packet_closure_residual"]) for row in ordered])
    external_residual = np.asarray([float(row["external_equation_residual"]) for row in ordered])

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    scatter = axes[0, 0].scatter(mu.real, mu.imag, c=np.log10(sigma), cmap="viridis", s=48)
    axes[0, 0].plot(mu.real, mu.imag, color="0.55", lw=0.8)
    axes[0, 0].set(
        xlabel=r"$\Re\mu_\sigma$",
        ylabel=r"$\Im\mu_\sigma$",
        title="The physical target is a complex outer resonance",
        aspect="equal",
    )
    colorbar = fig.colorbar(scatter, ax=axes[0, 0], fraction=0.046)
    colorbar.set_label(r"$\log_{10}\sigma$")
    axes[0, 0].grid(alpha=0.2)

    axes[0, 1].semilogx(sigma, return_phase, "o-", color="#6b3fa0")
    axes[0, 1].axhline(0.0, color="0.45", lw=0.8)
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel=r"$\arg(\mu_\sigma^{2k})$",
        title="A positive return target is only asymptotic",
    )
    axes[0, 1].grid(alpha=0.2)

    axes[1, 0].loglog(sigma, direct_distance, "o-", label="nearest direct packet eigenvalue")
    axes[1, 0].loglog(sigma, pencil_min, "s--", label="direct pencil smallest singular value")
    axes[1, 0].invert_xaxis()
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="two-step spectral defect",
        title="The static packet matrix approaches but misses the target",
    )
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.2, which="both")

    axes[1, 1].loglog(sigma, self_energy, "o-", label="physical packet self-energy ratio")
    axes[1, 1].loglog(sigma, packet_residual, "s--", label="packet closure residual")
    axes[1, 1].loglog(sigma, external_residual, "^:", label="external equation residual")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="dimensionless ratio",
        title="Exact physical eigenmode closure",
    )
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "physical_eigenmode_closure.pdf")
    fig.savefig(FIGURES / "physical_eigenmode_closure.png", dpi=220)
    plt.close(fig)


def plot_conditioning(rows: list[dict[str, object]]) -> None:
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in ordered])
    packet = np.asarray([float(row["packet_component_norm"]) for row in ordered])
    external_ratio = np.asarray(
        [float(row["external_to_packet_component_ratio"]) for row in ordered]
    )
    resolvent = np.asarray(
        [float(row["external_resolvent_lower_bound"]) for row in ordered]
    )
    condition = np.asarray([float(row["target_eigenvalue_condition"]) for row in ordered])
    weight = np.asarray([float(row["spectral_packet_weight_modulus"]) for row in ordered])
    compensation = np.asarray(
        [float(row["projection_resolvent_compensation"]) for row in ordered]
    )
    forcing_ratio = np.asarray(
        [float(row["external_forcing_to_packet_component_ratio"]) for row in ordered]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].loglog(sigma, packet, "o-", label=r"$\|P r\|$")
    axes[0, 0].loglog(sigma, external_ratio, "s--", label=r"$\|Q r\|/\|P r\|$")
    axes[0, 0].invert_xaxis()
    axes[0, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="projection ratio",
        title="Right packet capture decreases",
    )
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.2, which="both")

    axes[0, 1].loglog(sigma, resolvent, "o-", label="external resolvent lower bound")
    axes[0, 1].loglog(sigma, condition, "s--", label="physical eigenvalue condition")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="condition scale",
        title="Nonnormal conditioning grows",
    )
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.2, which="both")

    axes[1, 0].semilogx(sigma, weight, "o-", label=r"$|\ell^* P r|$")
    axes[1, 0].semilogx(sigma, compensation, "s--", label=r"$\|P r\|\,R_{\rm lb}$")
    axes[1, 0].invert_xaxis()
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="gauge-invariant diagnostic",
        title="Spectral visibility survives by resolvent compensation",
    )
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.2)

    axes[1, 1].semilogx(sigma, forcing_ratio, "o-", color="#a0263f")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel=r"$\|Q A V\alpha\|/\|P r\|$",
        title="The forcing ratio stabilizes near 0.41",
    )
    axes[1, 1].grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURES / "resolvent_compensation_scaling.pdf")
    fig.savefig(FIGURES / "resolvent_compensation_scaling.png", dpi=220)
    plt.close(fig)


def plot_packet_routes(rows: list[dict[str, object]]) -> None:
    endpoints = (1.0e-3, 1.0e-4)
    models = ("branch_complete", "critical_bright", "left_label", "right_label", "all_labels")
    labels = ("branch complete", "critical bright", "left label", "right label", "all labels")
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    for column, sigma in enumerate(endpoints):
        selected = {
            str(row["packet_model"]): row
            for row in rows
            if float(row["sigma"]) == sigma
        }
        position = np.arange(len(models))
        gram = np.asarray([float(selected[model]["packet_gram_condition"]) for model in models])
        distance = np.asarray([float(selected[model]["direct_closest_distance"]) for model in models])
        resolvent = np.asarray([float(selected[model]["external_resolvent_lower_bound"]) for model in models])
        weight = np.asarray([float(selected[model]["spectral_packet_weight_modulus"]) for model in models])
        axes[0, column].bar(position - 0.18, gram, 0.36, label="Gram condition")
        axes[0, column].bar(position + 0.18, resolvent, 0.36, label="resolvent lower bound")
        axes[0, column].set_yscale("log")
        axes[0, column].set_xticks(position, labels, rotation=24, ha="right", fontsize=8)
        axes[0, column].set(
            ylabel="condition scale",
            title=rf"Route conditioning, $\sigma={sigma:.0e}$",
        )
        if column == 0:
            axes[0, column].legend(frameon=False, fontsize=8)
        axes[0, column].grid(axis="y", alpha=0.2)

        axes[1, column].bar(position - 0.18, distance, 0.36, label="direct target distance")
        axes[1, column].bar(position + 0.18, weight, 0.36, label="spectral packet weight")
        axes[1, column].set_yscale("log")
        axes[1, column].set_xticks(position, labels, rotation=24, ha="right", fontsize=8)
        axes[1, column].set(
            ylabel="spectral diagnostic",
            title="Closer direct roots can require a riskier complement",
        )
        if column == 0:
            axes[1, column].legend(frameon=False, fontsize=8)
        axes[1, column].grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURES / "packet_route_comparison.pdf")
    fig.savefig(FIGURES / "packet_route_comparison.png", dpi=220)
    plt.close(fig)


def plot_window_robustness(rows: list[dict[str, object]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1))
    for axis, sigma in zip(axes, (1.0e-3, 1.0e-4)):
        selected = sorted(
            [row for row in rows if float(row["sigma"]) == sigma],
            key=lambda row: float(row["window_multiple"]),
        )
        window = np.asarray([float(row["window_multiple"]) for row in selected])
        packet = np.asarray([float(row["packet_component_norm"]) for row in selected])
        weight = np.asarray([float(row["spectral_packet_weight_modulus"]) for row in selected])
        resolvent = np.asarray([float(row["external_resolvent_lower_bound"]) for row in selected])
        axis.plot(window, packet, "o-", label=r"$\|P r\|$")
        axis.plot(window, weight, "s--", label=r"$|\ell^*Pr|$")
        axis.plot(window, resolvent / np.max(resolvent), "^:", label="normalized resolvent lower bound")
        axis.set(
            xlabel="packet half-width in local standard deviations",
            ylabel="diagnostic",
            title=rf"Window robustness, $\sigma={sigma:.0e}$",
        )
        axis.grid(alpha=0.2)
        axis.legend(frameon=False, fontsize=8, loc="center right")
    fig.tight_layout()
    fig.savefig(FIGURES / "packet_window_robustness.pdf")
    fig.savefig(FIGURES / "packet_window_robustness.png", dpi=220)
    plt.close(fig)


def plot_gmres_validation(rows: list[dict[str, object]]) -> None:
    if not rows or "gmres_iterations" not in rows[0]:
        return
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in ordered])
    iterations = np.asarray([int(float(row["gmres_iterations"])) for row in ordered])
    elapsed = np.asarray([float(row["gmres_elapsed_seconds"]) for row in ordered])
    true_residual = np.asarray([float(row["gmres_true_residual"]) for row in ordered])
    solution_error = np.asarray(
        [float(row["gmres_external_solution_error"]) for row in ordered]
    )
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1))
    axes[0].semilogx(sigma, iterations, "o-", label="GMRES iterations")
    second = axes[0].twinx()
    second.loglog(sigma, elapsed, "s--", color="#a0263f", label="elapsed seconds")
    axes[0].invert_xaxis()
    axes[0].set(
        xlabel=r"noise $\sigma$",
        ylabel="iterations",
        title="The shifted solve remains convergent",
    )
    second.set_ylabel("elapsed seconds", color="#a0263f")
    lines = axes[0].get_lines() + second.get_lines()
    axes[0].legend(lines, [line.get_label() for line in lines], frameon=False, fontsize=8)
    axes[0].grid(alpha=0.2)

    axes[1].loglog(sigma, true_residual, "o-", label="true shifted-solve residual")
    axes[1].loglog(sigma, solution_error, "s--", label="error against eigenmode exterior")
    axes[1].invert_xaxis()
    axes[1].set(
        xlabel=r"noise $\sigma$",
        ylabel="relative error",
        title="Independent resolvent reconstruction",
    )
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "shifted_solve_validation.pdf")
    fig.savefig(FIGURES / "shifted_solve_validation.png", dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sigmas",
        nargs="*",
        type=float,
        default=list(DEFAULT_SIGMAS),
    )
    parser.add_argument(
        "--skip-gmres",
        action="store_true",
        help="skip the independent shifted solves",
    )
    parser.add_argument(
        "--reuse",
        action="store_true",
        help="reuse committed CSV data and regenerate fits, plots, and metadata",
    )
    arguments = parser.parse_args()
    settings = archived_settings()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    if arguments.reuse:
        rows = read_csv(RESULTS / "physical_eigenmode_closure.csv")
        variant_rows = read_csv(RESULTS / "packet_model_comparison.csv")
        window_rows = read_csv(RESULTS / "packet_window_comparison.csv")
    else:
        outputs = [
            audit_scale(
                float(sigma),
                settings[float(sigma)],
                not arguments.skip_gmres,
            )
            for sigma in arguments.sigmas
        ]
        rows = [output[0] for output in outputs]
        variant_rows = [row for output in outputs for row in output[1]]
        window_rows = [row for output in outputs for row in output[2]]
        write_csv(RESULTS / "physical_eigenmode_closure.csv", rows)
        write_csv(RESULTS / "packet_model_comparison.csv", variant_rows)
        write_csv(RESULTS / "packet_window_comparison.csv", window_rows)
    fits = scaling_rows(rows)
    write_csv(RESULTS / "physical_closure_scaling.csv", fits)
    if len(rows) == len(settings):
        plot_physical_closure(rows)
        plot_conditioning(rows)
        plot_gmres_validation(rows)
    available_variant_sigmas = {float(row["sigma"]) for row in variant_rows}
    if {1.0e-3, 1.0e-4}.issubset(available_variant_sigmas):
        plot_packet_routes(variant_rows)
    available_window_sigmas = {float(row["sigma"]) for row in window_rows}
    if {1.0e-3, 1.0e-4}.issubset(available_window_sigmas):
        plot_window_robustness(window_rows)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sigmas": [float(row["sigma"]) for row in rows],
        "maximum_packet_closure_residual": max(
            float(row["packet_closure_residual"]) for row in rows
        ),
        "maximum_external_equation_residual": max(
            float(row["external_equation_residual"]) for row in rows
        ),
        "minimum_spectral_packet_weight": min(
            float(row["spectral_packet_weight_modulus"]) for row in rows
        ),
        "maximum_external_resolvent_lower_bound": max(
            float(row["external_resolvent_lower_bound"]) for row in rows
        ),
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "algebra.py": source_hash(ROOT / "src" / "physical_feshbach" / "algebra.py"),
            "packets.py": source_hash(ROOT / "src" / "physical_feshbach" / "packets.py"),
            "rh15_outer_resonance_cloud.csv": source_hash(
                RH15 / "results" / "outer_resonance_cloud.csv"
            ),
            "rh18_gaussian_operators.py": source_hash(
                RH18 / "src" / "gaussian_return" / "operators.py"
            ),
            "rh19_complement_returns.py": source_hash(
                RH19 / "src" / "complement_excursions" / "returns.py"
            ),
            "rh20_sector_operators.py": source_hash(
                RH20 / "src" / "sector_branches" / "operators.py"
            ),
            "rh21_biorthogonal_algebra.py": source_hash(
                RH21 / "src" / "biorthogonal_branches" / "algebra.py"
            ),
        },
    }
    with (RESULTS / "physical_feshbach_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated physical packet/complement closure audit", flush=True)


if __name__ == "__main__":
    main()
