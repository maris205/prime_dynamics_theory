"""Blind contour-Feshbach root counts for the physical two-step operator."""

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
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
MODELS = RESULTS / "models"
FIGURES = ROOT / "figures"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH17 = PAPERS / "RH-17-time-ordered-boundary-monodromy"
RH18 = PAPERS / "RH-18-branch-isolated-gaussian-return"
RH19 = PAPERS / "RH-19-complement-excursion-self-energy"
RH20 = PAPERS / "RH-20-sector-resolved-critical-branches"
RH21 = PAPERS / "RH-21-peripheral-biorthogonal-branch-collapse"
RH23 = PAPERS / "RH-23-physical-packet-complement-feshbach"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH17 / "src"),
    str(RH18 / "src"),
    str(RH19 / "src"),
    str(RH20 / "src"),
    str(RH21 / "src"),
    str(RH23 / "src"),
]

from biorthogonal_branches import (  # noqa: E402
    canonical_biorthogonal_pair,
    propagate_branch_histories,
)
from complement_excursions import critical_branch_masks  # noqa: E402
from contour_feshbach import (  # noqa: E402
    BatchedArnoldiFeshbach,
    build_batched_arnoldi_feshbach,
    circle_contour_audit,
    determinant_newton_root,
    sampled_rouche_audit,
)
from gaussian_return import (  # noqa: E402
    effective_noise_scales,
    packet_masks,
    periodic_packet_tube,
    positive_midpoints,
    sparse_folded_gaussian_matrix,
)
from physical_feshbach import bright_history_trial  # noqa: E402
from sector_branches import branch_profile_basis  # noqa: E402
from time_ordered_monodromy import boundary_cycle, critical_constants  # noqa: E402


DEFAULT_SIGMAS = (1.0e-2, 4.0e-3, 2.0e-3, 1.0e-3, 5.0e-4, 2.0e-4, 1.0e-4)
ARNOLDI_DEPTHS = {
    1.0e-2: 36,
    4.0e-3: 42,
    2.0e-3: 46,
    1.0e-3: 50,
    5.0e-4: 54,
    2.0e-4: 58,
    1.0e-4: 62,
}
RADIUS_FACTORS = tuple(np.round(np.arange(0.04, 0.481, 0.01), 3))
SCAN_NODES = 128
FINAL_CONTOUR_NODES = 512
REFERENCE_EIGENVALUE_COUNT = 24
PERIPHERAL_EIGENVALUE_COUNT = 8
WINDOW_MULTIPLE = 6.0


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


def physical_settings() -> dict[float, dict[str, int]]:
    dimensions = {
        float(row["sigma"]): int(row["folded_dimension"])
        for row in read_csv(RH15 / "results" / "cloud_summary.csv")
    }
    periods = {
        float(row["sigma"]): int(row["component_period"])
        for row in read_csv(RH20 / "results" / "two_branch_matrix_audit.csv")
    }
    return {
        sigma: {"dimension": dimension, "period": periods[sigma]}
        for sigma, dimension in dimensions.items()
    }


def resolve_peripheral_modes(matrix, count: int = PERIPHERAL_EIGENVALUE_COUNT):
    """Resolve only the two real modes needed to define the bulk operator."""

    dimension = matrix.shape[0]
    selected_count = min(int(count), dimension - 2)
    print(f"  construction right eigensystem k={selected_count}", flush=True)
    values_r, vectors_r = eigs(
        matrix,
        k=selected_count,
        which="LM",
        tol=2.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension),
    )
    print(f"  construction left eigensystem k={selected_count}", flush=True)
    values_l, vectors_l = eigs(
        matrix.T,
        k=selected_count,
        which="LM",
        tol=2.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension, 0.37),
    )
    real_indices = np.flatnonzero(np.abs(values_r.imag) < 2.0e-8)
    if real_indices.size < 2:
        raise RuntimeError("the two real peripheral modes were not resolved")
    perron_index = int(real_indices[np.argmin(np.abs(values_r[real_indices] - 1.0))])
    remaining = real_indices[real_indices != perron_index]
    parity_index = int(remaining[np.argmax(np.abs(values_r[remaining]))])
    right_modes = []
    left_modes = []
    peripheral_residuals = []
    for index in (perron_index, parity_index):
        eigenvalue = float(values_r[index].real)
        left_index = int(np.argmin(np.abs(values_l - eigenvalue)))
        right = np.asarray(vectors_r[:, index].real)
        left = np.asarray(vectors_l[:, left_index].real)
        left /= np.dot(left, right)
        right_modes.append(right)
        left_modes.append(left)
        peripheral_residuals.extend(
            (
                np.linalg.norm(matrix @ right - eigenvalue * right) / np.linalg.norm(right),
                np.linalg.norm(matrix.T @ left - eigenvalue * left) / np.linalg.norm(left),
            )
        )
    return {
        "right_modes": np.column_stack(right_modes),
        "left_modes": np.column_stack(left_modes),
        "peripheral_values": np.asarray(
            (values_r[perron_index].real, values_r[parity_index].real)
        ),
        "maximum_peripheral_residual": float(max(peripheral_residuals)),
    }


def resolve_reference_spectrum(matrix, count: int = REFERENCE_EIGENVALUE_COUNT):
    """Resolve outer modes only after the contour prediction has been frozen."""

    dimension = matrix.shape[0]
    selected_count = min(int(count), dimension - 2)
    print(f"  blind-reference right eigensystem k={selected_count}", flush=True)
    values_r, vectors_r = eigs(
        matrix,
        k=selected_count,
        which="LM",
        tol=2.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension),
    )
    print(f"  blind-reference left eigensystem k={selected_count}", flush=True)
    values_l, vectors_l = eigs(
        matrix.T,
        k=selected_count,
        which="LM",
        tol=2.0e-10,
        maxiter=18000,
        v0=deterministic_start(dimension, 0.37),
    )
    real_indices = np.flatnonzero(np.abs(values_r.imag) < 2.0e-8)
    if real_indices.size < 2:
        raise RuntimeError("the two real peripheral modes were not resolved")
    perron_index = int(real_indices[np.argmin(np.abs(values_r[real_indices] - 1.0))])
    remaining = real_indices[real_indices != perron_index]
    parity_index = int(remaining[np.argmax(np.abs(values_r[remaining]))])
    right_modes = []
    left_modes = []
    peripheral_residuals = []
    for index in (perron_index, parity_index):
        eigenvalue = float(values_r[index].real)
        left_index = int(np.argmin(np.abs(values_l - eigenvalue)))
        right = np.asarray(vectors_r[:, index].real)
        left = np.asarray(vectors_l[:, left_index].real)
        left /= np.dot(left, right)
        right_modes.append(right)
        left_modes.append(left)
        peripheral_residuals.extend(
            (
                np.linalg.norm(matrix @ right - eigenvalue * right) / np.linalg.norm(right),
                np.linalg.norm(matrix.T @ left - eigenvalue * left) / np.linalg.norm(left),
            )
        )
    return {
        "right_values": np.asarray(values_r),
        "right_vectors": np.asarray(vectors_r),
        "left_values": np.asarray(values_l),
        "left_vectors": np.asarray(vectors_l),
        "peripheral_indices": (perron_index, parity_index),
        "right_modes": np.column_stack(right_modes),
        "left_modes": np.column_stack(left_modes),
        "peripheral_values": np.asarray(
            (values_r[perron_index].real, values_r[parity_index].real)
        ),
        "maximum_peripheral_residual": float(max(peripheral_residuals)),
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
    left, right, _ = critical_branch_masks(
        grid,
        base,
        points[-1],
        sigma * tube.widths[-1],
        window_multiple=float(window_multiple),
        partition=float(constants.first_interior_point),
    )

    def raw_two_step(values):
        return matrix @ (matrix @ values)

    endpoint = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    endpoint[~left[0]] = 0.0
    endpoint /= np.linalg.norm(endpoint)
    critical = raw_two_step(endpoint)
    branch_basis = branch_profile_basis(critical, left[-1], right[-1])
    histories = propagate_branch_histories(raw_two_step, left[:-1], branch_basis)
    return bright_history_trial(histories)


def bulk_operator(matrix, spectrum):
    right = spectrum["right_modes"]
    left = spectrum["left_modes"]
    values = spectrum["peripheral_values"]

    def one_step(source):
        array = np.asarray(source)
        coefficients = left.T @ array
        if array.ndim == 1:
            return matrix @ array - right @ (values * coefficients)
        return matrix @ array - right @ (values[:, None] * coefficients)

    def two_step(source):
        return one_step(one_step(source))

    return one_step, two_step


def select_direct_center(reduced: np.ndarray) -> tuple[complex, np.ndarray]:
    """Select the rightmost lower-half-plane packet root without a full target."""

    roots = np.linalg.eigvals(np.asarray(reduced))
    candidates = roots[roots.imag < -1.0e-9]
    if candidates.size == 0:
        raise RuntimeError("the direct packet matrix has no lower-half-plane root")
    order = np.lexsort((np.abs(candidates), candidates.real))
    return complex(candidates[order[-1]]), roots


def save_model(path: Path, model: BatchedArnoldiFeshbach) -> None:
    payload: dict[str, np.ndarray] = {
        "reduced": np.asarray(model.reduced),
        "forcing_norms": np.asarray(model.forcing_norms),
        "orthogonality": np.asarray(model.arnoldi_orthogonality_errors),
        "packet_rank": np.asarray((model.packet_rank,), dtype=np.int64),
    }
    for index, (hessenberg, coupling) in enumerate(
        zip(model.hessenbergs, model.output_couplings)
    ):
        payload[f"hessenberg_{index}"] = np.asarray(hessenberg)
        payload[f"coupling_{index}"] = np.asarray(coupling)
        if model.arnoldi_relation_defect_norms is not None:
            payload[f"relation_defects_{index}"] = np.asarray(
                model.arnoldi_relation_defect_norms[index]
            )
    np.savez_compressed(path, **payload)


def load_model(path: Path) -> BatchedArnoldiFeshbach:
    with np.load(path) as archive:
        rank = int(archive["packet_rank"][0])
        return BatchedArnoldiFeshbach(
            reduced=np.asarray(archive["reduced"]),
            forcing_norms=np.asarray(archive["forcing_norms"]),
            hessenbergs=tuple(
                np.asarray(archive[f"hessenberg_{index}"]) for index in range(rank)
            ),
            output_couplings=tuple(
                np.asarray(archive[f"coupling_{index}"]) for index in range(rank)
            ),
            arnoldi_orthogonality_errors=np.asarray(archive["orthogonality"]),
            arnoldi_relation_defect_norms=tuple(
                np.asarray(archive[f"relation_defects_{index}"])
                for index in range(rank)
            ),
        )


def contour_row(
    sigma: float,
    factor: float,
    audit,
    *,
    role: str = "discovery_scan",
) -> dict[str, object]:
    return {
        "sigma": sigma,
        "contour_role": role,
        "radius_factor": factor,
        "center_real": audit.center.real,
        "center_imag": audit.center.imag,
        "radius": audit.radius,
        "arnoldi_depth": audit.depth,
        "contour_nodes": audit.points.size,
        "winding_float": audit.winding_float,
        "winding_integer": audit.winding_integer,
        "projected_pole_count": audit.projected_pole_count,
        "projected_zero_count": audit.projected_zero_count,
        "cauchy_count_real": audit.cauchy_count.real,
        "cauchy_count_imag": audit.cauchy_count.imag,
        "cauchy_centroid_real": audit.cauchy_centroid.real,
        "cauchy_centroid_imag": audit.cauchy_centroid.imag,
        "maximum_relative_arnoldi_residual": float(np.max(audit.relative_residuals)),
        "minimum_feshbach_singular_value": float(
            np.min(audit.smallest_singular_values)
        ),
        "minimum_logabs_determinant": float(np.min(audit.determinant_logabs)),
        "maximum_logabs_determinant": float(np.max(audit.determinant_logabs)),
        "maximum_phase_increment": audit.maximum_phase_increment,
        "minimum_projected_pole_boundary_distance": audit.minimum_pole_boundary_distance,
    }


def reveal_reference(spectrum, matrix, predicted_root: complex, contour_center, contour_radius):
    values = np.asarray(spectrum["right_values"])
    vectors = np.asarray(spectrum["right_vectors"])
    left_values = np.asarray(spectrum["left_values"])
    left_vectors = np.asarray(spectrum["left_vectors"])
    peripheral = set(int(index) for index in spectrum["peripheral_indices"])
    eligible = np.asarray(
        [index for index, value in enumerate(values) if value.imag > 1.0e-8]
    )
    target_index = int(
        eligible[np.argmin(np.abs(values[eligible] ** 2 - predicted_root))]
    )
    mu = complex(values[target_index])
    target = mu * mu
    right = np.asarray(vectors[:, target_index], dtype=np.complex128)
    right /= np.linalg.norm(right)
    left_index = int(np.argmin(np.abs(left_values - np.conjugate(mu))))
    left = np.asarray(left_vectors[:, left_index], dtype=np.complex128)
    pairing = np.vdot(left, right)
    left /= np.conjugate(pairing)
    right_residual = np.linalg.norm(matrix @ right - mu * right)
    left_residual = np.linalg.norm(matrix.T @ left - np.conjugate(mu) * left) / max(
        np.linalg.norm(left), np.finfo(float).tiny
    )
    bulk_indices = [index for index in range(values.size) if index not in peripheral]
    bulk_values = values[bulk_indices]
    two_step_values = bulk_values**2
    inside = np.abs(two_step_values - contour_center) < contour_radius
    cutoff = float(np.min(np.abs(two_step_values)))
    radial_floor = max(0.0, abs(contour_center) - contour_radius)
    reference_rows = []
    for order, (one_step, two_step, contained) in enumerate(
        zip(bulk_values, two_step_values, inside)
    ):
        reference_rows.append(
            {
                "outer_mode_order": order,
                "mu_real": one_step.real,
                "mu_imag": one_step.imag,
                "mu_modulus": abs(one_step),
                "two_step_real": two_step.real,
                "two_step_imag": two_step.imag,
                "two_step_modulus": abs(two_step),
                "inside_selected_contour": int(contained),
                "selected_reference_target": int(
                    abs(two_step - target) < 2.0e-10
                ),
            }
        )
    return {
        "mu": mu,
        "target": target,
        "right_residual": float(right_residual),
        "left_residual": float(left_residual),
        "condition": float(np.linalg.norm(left) * np.linalg.norm(right)),
        "pairing_error": float(abs(np.vdot(left, right) - 1.0)),
        "captured_count_inside": int(np.count_nonzero(inside)),
        "outer_capture_cutoff": cutoff,
        "contour_radial_floor": radial_floor,
        "outer_count_radially_complete": int(radial_floor > cutoff),
        "rows": reference_rows,
    }


def audit_scale(
    sigma: float,
    setting: dict[str, int],
    *,
    depth_override: int | None = None,
):
    dimension = int(setting["dimension"])
    period = int(setting["period"])
    depth = ARNOLDI_DEPTHS[sigma] if depth_override is None else int(depth_override)
    print(
        f"contour Feshbach sigma={sigma:g}, n={dimension}, k={period}, J={depth}",
        flush=True,
    )
    started = time.time()
    constants = critical_constants(130)
    matrix = sparse_folded_gaussian_matrix(
        dimension, sigma, u=float(constants.u)
    )
    matrix_seconds = time.time() - started
    started = time.time()
    spectrum = resolve_peripheral_modes(matrix)
    peripheral_eigensolve_seconds = time.time() - started
    trial = packet_trial(matrix, sigma, dimension, period)
    pair = canonical_biorthogonal_pair(
        trial, spectrum["right_modes"], spectrum["left_modes"]
    )
    _, two_step = bulk_operator(matrix, spectrum)
    synthesis = np.asarray(pair.synthesis)
    analysis = np.asarray(pair.analysis)

    def packet_projection(values):
        array = np.asarray(values)
        return synthesis @ (analysis @ array)

    def external_projection(values):
        array = np.asarray(values)
        return array - packet_projection(array)

    reduced = analysis @ two_step(synthesis)
    forcing = external_projection(two_step(synthesis))
    direct_center, direct_roots = select_direct_center(reduced)
    action_counter = 0

    def observed_action(values):
        nonlocal action_counter
        action_counter += 1
        source = external_projection(values)
        applied = two_step(source)
        if action_counter == 1 or action_counter % 5 == 0 or action_counter == depth:
            print(f"  batched Arnoldi step {action_counter}/{depth}", flush=True)
        return external_projection(applied), analysis @ applied

    started = time.time()
    model = build_batched_arnoldi_feshbach(
        observed_action,
        forcing,
        reduced,
        steps=depth,
        reorthogonalizations=2,
    )
    arnoldi_seconds = time.time() - started
    model_path = MODELS / f"contour_model_sigma_{sigma:.0e}.npz"
    save_model(model_path, model)
    release_memory()

    contour_rows = []
    audits = []
    center_scale = abs(direct_center)
    for factor in RADIUS_FACTORS:
        audit = circle_contour_audit(
            model,
            direct_center,
            factor * center_scale,
            nodes=SCAN_NODES,
            depth=depth,
        )
        audits.append((factor, audit))
        contour_rows.append(contour_row(sigma, factor, audit))
    eligible = [
        (factor, audit)
        for factor, audit in audits
        if audit.winding_integer == 1
        and audit.projected_pole_count == 0
        and audit.projected_zero_count == 1
        and audit.maximum_phase_increment < 0.85 * np.pi
    ]
    if not eligible:
        raise RuntimeError("no pole-free one-zero discovery contour was found")
    discovery_factor, discovery = max(
        eligible,
        key=lambda item: float(np.min(item[1].smallest_singular_values)),
    )
    initial = discovery.cauchy_centroid
    root = determinant_newton_root(
        model,
        initial,
        depth=depth,
        trust_radius=discovery.radius,
    )
    if not root.converged:
        raise RuntimeError("projected Feshbach Newton refinement did not converge")

    augmented = model.augmented_matrix(depth=depth)
    augmented_values = np.linalg.eigvals(augmented)
    projected_poles = model.projected_poles(depth=depth)
    root_radius = abs(root.root - direct_center)
    closest_augmented_index = int(np.argmin(np.abs(augmented_values - root.root)))
    other_zero_radii = np.delete(
        np.abs(augmented_values - direct_center), closest_augmented_index
    )
    pole_radii = np.abs(projected_poles - direct_center)
    zero_candidates = other_zero_radii[other_zero_radii > root_radius + 1.0e-9]
    pole_candidates = pole_radii[pole_radii > root_radius + 1.0e-9]
    next_zero_radius = float(np.min(zero_candidates)) if zero_candidates.size else float("inf")
    next_pole_radius = float(np.min(pole_candidates)) if pole_candidates.size else float("inf")
    next_event_radius = min(next_zero_radius, next_pole_radius)
    if abs(next_zero_radius - next_pole_radius) <= 1.0e-6 * max(
        1.0, min(next_zero_radius, next_pole_radius)
    ):
        next_event_type = "projected_pole_zero_cluster"
    else:
        next_event_type = (
            "projected_zero" if next_zero_radius < next_pole_radius else "projected_pole"
        )
    if not np.isfinite(next_event_radius):
        next_event_radius = discovery.radius
        next_event_type = "discovery_boundary"
    if next_event_radius <= root_radius:
        raise RuntimeError("the projected target has no positive isolation corridor")
    optimized_radius = 0.5 * (root_radius + next_event_radius)
    selected = circle_contour_audit(
        model,
        direct_center,
        optimized_radius,
        nodes=FINAL_CONTOUR_NODES,
        depth=depth,
    )
    if (
        selected.winding_integer != 1
        or selected.projected_pole_count != 0
        or selected.projected_zero_count != 1
    ):
        raise RuntimeError("the optimized isolation contour failed its root-count audit")
    selected_factor = optimized_radius / center_scale
    contour_rows.append(
        contour_row(
            sigma,
            selected_factor,
            selected,
            role="selected_optimized",
        )
    )
    root = determinant_newton_root(
        model,
        selected.cauchy_centroid,
        depth=depth,
        trust_radius=selected.radius,
    )
    if not root.converged:
        raise RuntimeError("optimized-contour Newton refinement did not converge")
    augmented_count = int(
        np.count_nonzero(np.abs(augmented_values - direct_center) < selected.radius)
    )
    augmented_closest = augmented_values[
        np.argmin(np.abs(augmented_values - root.root))
    ]
    factorization_residual = model.determinant_factorization_residual(
        selected.points[0], depth=min(12, depth)
    )

    depth_rows = []
    depth_values = sorted(
        set(max(8, value) for value in (depth - 16, depth - 8, depth))
    )
    for selected_depth in depth_values:
        audit = circle_contour_audit(
            model,
            direct_center,
            selected.radius,
            nodes=SCAN_NODES,
            depth=selected_depth,
        )
        depth_root = determinant_newton_root(
            model,
            audit.cauchy_centroid if audit.projected_zero_count == 1 else direct_center,
            depth=selected_depth,
            trust_radius=selected.radius,
        )
        depth_rows.append(
            {
                "sigma": sigma,
                "arnoldi_depth": selected_depth,
                "winding_integer": audit.winding_integer,
                "projected_pole_count": audit.projected_pole_count,
                "projected_zero_count": audit.projected_zero_count,
                "cauchy_count_error": abs(audit.cauchy_count - 1.0),
                "root_real": depth_root.root.real,
                "root_imag": depth_root.root.imag,
                "root_converged": int(depth_root.converged),
                "distance_to_maximum_depth_root": abs(depth_root.root - root.root),
                "maximum_relative_arnoldi_residual": float(
                    np.max(audit.relative_residuals)
                ),
                "minimum_feshbach_singular_value": float(
                    np.min(audit.smallest_singular_values)
                ),
                "maximum_phase_increment": audit.maximum_phase_increment,
            }
        )
    shallow_depth = depth_values[-2] if len(depth_values) > 1 else depth_values[-1]
    rouche = sampled_rouche_audit(
        model,
        model,
        direct_center,
        selected.radius,
        nodes=SCAN_NODES,
        base_depth=shallow_depth,
        comparison_depth=depth,
    )

    node_rows = []
    for nodes in (64, 96, 128, 192, 256, 384, 512):
        audit = circle_contour_audit(
            model,
            direct_center,
            selected.radius,
            nodes=nodes,
            depth=depth,
        )
        node_rows.append(
            {
                "sigma": sigma,
                "contour_nodes": nodes,
                "winding_float": audit.winding_float,
                "winding_integer": audit.winding_integer,
                "projected_zero_count": audit.projected_zero_count,
                "cauchy_count_error": abs(audit.cauchy_count - 1.0),
                "cauchy_centroid_error": abs(audit.cauchy_centroid - root.root),
                "maximum_phase_increment": audit.maximum_phase_increment,
            }
        )

    started = time.time()
    reference_spectrum = resolve_reference_spectrum(matrix)
    reference_eigensolve_seconds = time.time() - started
    reference = reveal_reference(
        reference_spectrum,
        matrix,
        root.root,
        direct_center,
        selected.radius,
    )
    for row in reference["rows"]:
        row["sigma"] = sigma
    direct_error = abs(direct_center - reference["target"])
    prediction_error = abs(root.root - reference["target"])
    summary = {
        "sigma": sigma,
        "folded_dimension": dimension,
        "component_period": period,
        "packet_rank": model.packet_rank,
        "arnoldi_depth": depth,
        "direct_center_real": direct_center.real,
        "direct_center_imag": direct_center.imag,
        "direct_center_modulus": abs(direct_center),
        "direct_lower_half_root_count": int(np.count_nonzero(direct_roots.imag < -1.0e-9)),
        "discovery_radius_factor": discovery_factor,
        "selected_radius_factor": selected_factor,
        "selected_contour_radius": selected.radius,
        "root_radial_distance_from_direct": root_radius,
        "next_projected_event_radius": next_event_radius,
        "next_projected_zero_radius": next_zero_radius,
        "next_projected_pole_radius": next_pole_radius,
        "next_projected_event_type": next_event_type,
        "isolation_corridor_width": next_event_radius - root_radius,
        "relative_isolation_corridor_width": (next_event_radius - root_radius)
        / center_scale,
        "selected_contour_event_clearance": min(
            selected.radius - root_radius,
            next_event_radius - selected.radius,
        ),
        "selected_winding_float": selected.winding_float,
        "selected_winding_integer": selected.winding_integer,
        "selected_projected_pole_count": selected.projected_pole_count,
        "selected_projected_zero_count": selected.projected_zero_count,
        "selected_cauchy_count_error": abs(selected.cauchy_count - 1.0),
        "selected_cauchy_centroid_real": selected.cauchy_centroid.real,
        "selected_cauchy_centroid_imag": selected.cauchy_centroid.imag,
        "predicted_root_real": root.root.real,
        "predicted_root_imag": root.root.imag,
        "predicted_root_newton_iterations": root.iterations,
        "predicted_root_relative_singular": root.relative_smallest_singular_value,
        "projected_augmented_count": augmented_count,
        "projected_augmented_closest_error": abs(augmented_closest - root.root),
        "projected_determinant_factorization_residual": factorization_residual,
        "reference_mu_real": reference["mu"].real,
        "reference_mu_imag": reference["mu"].imag,
        "reference_root_real": reference["target"].real,
        "reference_root_imag": reference["target"].imag,
        "direct_root_reference_error": direct_error,
        "feshbach_root_reference_error": prediction_error,
        "prediction_improvement_factor": direct_error
        / max(prediction_error, np.finfo(float).tiny),
        "reference_right_residual": reference["right_residual"],
        "reference_left_residual": reference["left_residual"],
        "reference_pairing_error": reference["pairing_error"],
        "reference_eigenvalue_condition": reference["condition"],
        "captured_outer_reference_count": reference["captured_count_inside"],
        "outer_capture_cutoff": reference["outer_capture_cutoff"],
        "selected_contour_radial_floor": reference["contour_radial_floor"],
        "outer_count_radially_complete": reference["outer_count_radially_complete"],
        "maximum_relative_arnoldi_residual": float(
            np.max(selected.relative_residuals)
        ),
        "minimum_feshbach_singular_value": float(
            np.min(selected.smallest_singular_values)
        ),
        "maximum_contour_phase_increment": selected.maximum_phase_increment,
        "maximum_arnoldi_orthogonality_error": float(
            np.max(model.arnoldi_orthogonality_errors)
        ),
        "sampled_rouche_base_depth": shallow_depth,
        "sampled_rouche_maximum_relative_perturbation": rouche.maximum_relative_perturbation,
        "sampled_rouche_criterion_on_mesh": int(rouche.criterion_satisfied_on_mesh),
        "matrix_build_seconds": matrix_seconds,
        "peripheral_eigensolve_seconds": peripheral_eigensolve_seconds,
        "reference_eigensolve_seconds": reference_eigensolve_seconds,
        "total_eigensolve_seconds": peripheral_eigensolve_seconds
        + reference_eigensolve_seconds,
        "arnoldi_build_seconds": arnoldi_seconds,
    }
    del (
        augmented,
        augmented_values,
        model,
        matrix,
        spectrum,
        reference_spectrum,
        pair,
        trial,
    )
    release_memory()
    return summary, contour_rows, depth_rows, node_rows, reference["rows"]


def complex_column(rows, real_field: str, imag_field: str) -> np.ndarray:
    return np.asarray(
        [complex(float(row[real_field]), float(row[imag_field])) for row in rows]
    )


def plot_summary(rows: list[dict[str, object]], contour_rows: list[dict[str, object]]) -> None:
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in ordered])
    direct = complex_column(ordered, "direct_center_real", "direct_center_imag")
    predicted = complex_column(ordered, "predicted_root_real", "predicted_root_imag")
    reference = complex_column(ordered, "reference_root_real", "reference_root_imag")
    direct_error = np.asarray([float(row["direct_root_reference_error"]) for row in ordered])
    predicted_error = np.asarray(
        [float(row["feshbach_root_reference_error"]) for row in ordered]
    )
    residual = np.asarray(
        [float(row["maximum_relative_arnoldi_residual"]) for row in ordered]
    )
    rouche = np.asarray(
        [float(row["sampled_rouche_maximum_relative_perturbation"]) for row in ordered]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 8.0))
    axes[0, 0].plot(direct.real, direct.imag, "x--", label="direct packet center")
    axes[0, 0].plot(predicted.real, predicted.imag, "o-", label="contour-Feshbach prediction")
    axes[0, 0].plot(reference.real, reference.imag, "+:", label="full-operator blind reference")
    axes[0, 0].set(
        xlabel=r"$\Re z$",
        ylabel=r"$\Im z$",
        title="Blind two-step root continuation",
    )
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.2)

    axes[0, 1].loglog(sigma, direct_error, "s--", label="direct packet error")
    axes[0, 1].loglog(sigma, predicted_error, "o-", label="Feshbach prediction error")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="distance to blind reference",
        title="Complement closure upgrades prediction",
    )
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.2, which="both")

    position = np.arange(len(ordered))
    root_factor = np.asarray(
        [
            float(row["root_radial_distance_from_direct"])
            / float(row["direct_center_modulus"])
            for row in ordered
        ]
    )
    event_factor = np.asarray(
        [
            float(row["next_projected_event_radius"])
            / float(row["direct_center_modulus"])
            for row in ordered
        ]
    )
    selected_factor = np.asarray(
        [float(row["selected_radius_factor"]) for row in ordered]
    )
    for y, left, middle, right in zip(
        position, root_factor, selected_factor, event_factor
    ):
        axes[1, 0].plot((left, right), (y, y), color="#486a9b", lw=4, alpha=0.72)
        axes[1, 0].scatter(left, y, marker=">", color="#a0263f", s=38)
        axes[1, 0].scatter(middle, y, marker="o", color="#f28e2b", s=38)
        axes[1, 0].scatter(right, y, marker="|", color="#202020", s=70)
    axes[1, 0].set_yticks(
        position,
        [rf"$\sigma={float(row['sigma']):.0e}$" for row in ordered],
    )
    axes[1, 0].invert_yaxis()
    axes[1, 0].set(
        xlabel=r"radius / $|z_{\rm direct}|$",
        ylabel="noise scale",
        title="Pole-free one-root isolation corridors",
    )
    axes[1, 0].scatter([], [], marker=">", color="#a0263f", label="predicted root radius")
    axes[1, 0].scatter([], [], marker="o", color="#f28e2b", label="selected contour")
    axes[1, 0].scatter([], [], marker="|", color="#202020", label="next projected event")
    axes[1, 0].legend(frameon=False, fontsize=7)
    axes[1, 0].grid(alpha=0.2)

    axes[1, 1].loglog(sigma, residual, "o-", label="maximum Arnoldi residual")
    axes[1, 1].loglog(sigma, rouche, "s--", label="sampled depth-change Rouché ratio")
    axes[1, 1].axhline(1.0, color="0.45", lw=0.8)
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="contour diagnostic",
        title="Projection convergence on the selected contour",
    )
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "contour_feshbach_summary.pdf")
    fig.savefig(FIGURES / "contour_feshbach_summary.png", dpi=220)
    plt.close(fig)


def plot_selected_contours(rows: list[dict[str, object]]) -> None:
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    chosen = [ordered[0], ordered[len(ordered) // 2], ordered[-1]] if len(ordered) >= 3 else ordered
    fig, axes = plt.subplots(1, len(chosen), figsize=(4.0 * len(chosen), 3.8), squeeze=False)
    for axis, row in zip(axes[0], chosen):
        center = complex(float(row["direct_center_real"]), float(row["direct_center_imag"]))
        radius = float(row["selected_contour_radius"])
        predicted = complex(float(row["predicted_root_real"]), float(row["predicted_root_imag"]))
        reference = complex(float(row["reference_root_real"]), float(row["reference_root_imag"]))
        theta = np.linspace(0.0, 2.0 * np.pi, 300)
        contour = center + radius * np.exp(1.0j * theta)
        axis.plot(contour.real, contour.imag, color="#486a9b", lw=1.1)
        axis.scatter(center.real, center.imag, marker="x", s=55, label="direct center")
        axis.scatter(predicted.real, predicted.imag, marker="o", s=38, label="Feshbach root")
        axis.scatter(reference.real, reference.imag, marker="+", s=65, label="blind reference")
        axis.set(
            xlabel=r"$\Re z$",
            ylabel=r"$\Im z$",
            title=rf"One-root contour, $\sigma={float(row['sigma']):.0e}$",
            aspect="equal",
        )
        axis.grid(alpha=0.2)
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "selected_one_root_contours.pdf")
    fig.savefig(FIGURES / "selected_one_root_contours.png", dpi=220)
    plt.close(fig)


def plot_depth_convergence(rows: list[dict[str, object]]) -> None:
    sigmas = sorted({float(row["sigma"]) for row in rows}, reverse=True)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    for sigma in sigmas:
        selected = sorted(
            [row for row in rows if float(row["sigma"]) == sigma],
            key=lambda row: int(float(row["arnoldi_depth"])),
        )
        depth = np.asarray([int(float(row["arnoldi_depth"])) for row in selected])
        error = np.asarray(
            [float(row["distance_to_maximum_depth_root"]) for row in selected]
        )
        residual = np.asarray(
            [float(row["maximum_relative_arnoldi_residual"]) for row in selected]
        )
        axes[0].semilogy(depth, np.maximum(error, 1.0e-17), "o-", label=rf"$\sigma={sigma:.0e}$")
        axes[1].semilogy(depth, residual, "o-", label=rf"$\sigma={sigma:.0e}$")
    axes[0].set(
        xlabel="Arnoldi depth per right-hand side",
        ylabel="root change from maximum depth",
        title="Projected root stabilization",
    )
    axes[1].set(
        xlabel="Arnoldi depth per right-hand side",
        ylabel="maximum contour residual",
        title="Holomorphic shifted-solve convergence",
    )
    for axis in axes:
        axis.grid(alpha=0.2, which="both")
        axis.legend(frameon=False, fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "arnoldi_depth_convergence.pdf")
    fig.savefig(FIGURES / "arnoldi_depth_convergence.png", dpi=220)
    plt.close(fig)


def plot_node_stability(rows: list[dict[str, object]]) -> None:
    sigmas = sorted({float(row["sigma"]) for row in rows}, reverse=True)
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    for sigma in sigmas:
        selected = sorted(
            [row for row in rows if float(row["sigma"]) == sigma],
            key=lambda row: int(float(row["contour_nodes"])),
        )
        nodes = np.asarray([int(float(row["contour_nodes"])) for row in selected])
        count_error = np.asarray(
            [float(row["cauchy_count_error"]) for row in selected]
        )
        centroid_error = np.asarray(
            [float(row["cauchy_centroid_error"]) for row in selected]
        )
        phase = np.asarray(
            [float(row["maximum_phase_increment"]) for row in selected]
        )
        label = rf"$\sigma={sigma:.0e}$"
        axes[0].semilogy(nodes, count_error, "o-", label=label)
        axes[0].semilogy(nodes, centroid_error, "x--", alpha=0.7)
        axes[1].plot(nodes, phase, "o-", label=label)
    axes[0].set(
        xlabel="contour nodes",
        ylabel="Cauchy quadrature error",
        title="Count (circles) and centroid (crosses) converge",
    )
    axes[1].set(
        xlabel="contour nodes",
        ylabel="maximum determinant phase increment",
        title="Phase sampling remains well below $\pi$",
    )
    axes[1].axhline(np.pi, color="0.4", lw=0.8, ls="--")
    for axis in axes:
        axis.grid(alpha=0.2, which="both")
        axis.legend(frameon=False, fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES / "contour_node_stability.pdf")
    fig.savefig(FIGURES / "contour_node_stability.png", dpi=220)
    plt.close(fig)


def regenerate_outputs() -> None:
    summaries = read_csv(RESULTS / "scale_summary.csv")
    contours = read_csv(RESULTS / "contour_scan.csv")
    depths = read_csv(RESULTS / "depth_convergence.csv")
    nodes = read_csv(RESULTS / "node_stability.csv")
    plot_summary(summaries, contours)
    plot_selected_contours(summaries)
    plot_depth_convergence(depths)
    plot_node_stability(nodes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigmas", nargs="*", type=float, default=list(DEFAULT_SIGMAS))
    parser.add_argument("--depth", type=int, default=None, help="override all Arnoldi depths")
    parser.add_argument(
        "--reuse",
        action="store_true",
        help="regenerate figures and metadata from committed CSV files",
    )
    arguments = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    MODELS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    if not arguments.reuse:
        settings = physical_settings()
        outputs = []
        for sigma in arguments.sigmas:
            outputs.append(
                audit_scale(
                    float(sigma),
                    settings[float(sigma)],
                    depth_override=arguments.depth,
                )
            )
            summaries = [output[0] for output in outputs]
            contour_rows = [row for output in outputs for row in output[1]]
            depth_rows = [row for output in outputs for row in output[2]]
            node_rows = [row for output in outputs for row in output[3]]
            reference_rows = [row for output in outputs for row in output[4]]
            write_csv(RESULTS / "scale_summary.csv", summaries)
            write_csv(RESULTS / "contour_scan.csv", contour_rows)
            write_csv(RESULTS / "depth_convergence.csv", depth_rows)
            write_csv(RESULTS / "node_stability.csv", node_rows)
            write_csv(RESULTS / "outer_reference_spectrum.csv", reference_rows)
    regenerate_outputs()
    summaries = read_csv(RESULTS / "scale_summary.csv")
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sigmas": [float(row["sigma"]) for row in summaries],
        "maximum_prediction_error": max(
            float(row["feshbach_root_reference_error"]) for row in summaries
        ),
        "minimum_prediction_improvement_factor": min(
            float(row["prediction_improvement_factor"]) for row in summaries
        ),
        "maximum_contour_residual": max(
            float(row["maximum_relative_arnoldi_residual"]) for row in summaries
        ),
        "all_selected_windings": [
            int(float(row["selected_winding_integer"])) for row in summaries
        ],
        "all_projected_augmented_counts": [
            int(float(row["projected_augmented_count"])) for row in summaries
        ],
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "model.py": source_hash(ROOT / "src" / "contour_feshbach" / "model.py"),
            "rh23_packets.py": source_hash(
                RH23 / "src" / "physical_feshbach" / "packets.py"
            ),
            "rh18_gaussian_operators.py": source_hash(
                RH18 / "src" / "gaussian_return" / "operators.py"
            ),
            "rh21_biorthogonal_algebra.py": source_hash(
                RH21 / "src" / "biorthogonal_branches" / "algebra.py"
            ),
        },
    }
    with (RESULTS / "contour_feshbach_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated contour Feshbach root-count audit", flush=True)


if __name__ == "__main__":
    main()
