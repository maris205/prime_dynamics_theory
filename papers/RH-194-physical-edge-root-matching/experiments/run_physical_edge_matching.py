"""Match the surviving RH-185 packet roots to physical base eigenmodes."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH182 = PAPERS / "RH-182-finite-temporal-clock-physical-audit"
RH184 = PAPERS / "RH-184-balanced-biorthogonal-temporal-realization"
RH185 = PAPERS / "RH-185-physical-bi-krylov-cycle-calibration"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH182 / "src"),
    str(RH184 / "src"),
    str(RH185 / "src"),
]

from bi_krylov_calibration import adjoint, apply_left  # noqa: E402
from biorthogonal_clock import balanced_biorthogonal_frames  # noqa: E402
from finite_clock import normalized_orbit, temporal_synthesis  # noqa: E402
from physical_matching import (  # noqa: E402
    contour_count,
    contour_spectral_clearance,
    nearest_unique_matching,
    normalize_left_eigenvector,
    source_observation_mode,
    subspace_gap,
    trace_power_errors,
)
from run_effective_rank_audit import HORIZONS, build_models  # noqa: E402


SIGMA = 0.01
LENGTH = 4
RESIDUAL_GATE = 0.10
CONTOUR_FRACTION = 0.4


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {f"{prefix}_real": float(value.real), f"{prefix}_imag": float(value.imag)}


def run() -> dict[str, object]:
    started = time.perf_counter()
    _, models = build_models(SIGMA)
    frozen = json.loads((RH185 / "results/bi_krylov_audit.json").read_text(encoding="utf-8"))
    starts_by_side = {
        side: sorted({
            int(item["start"])
            for item in frozen["records"]
            if float(item["sigma"]) == SIGMA
            and int(item["candidate_length"]) == LENGTH
            and str(item["side"]) == side
            and bool(item["two_sided_0_10_gate"])
        })
        for side in ("left", "right")
    }
    windows = []
    unique_modes = []
    for model in models:
        side = str(model["side"])
        operator = np.asarray(model["operator"], dtype=complex)
        source = np.asarray(model["source"], dtype=complex)
        observation = np.asarray(model["observation"], dtype=complex)
        observation_seed = observation.conj().T
        eigenvalues, left_vectors, right_vectors = eig(operator, left=True, right=True, check_finite=False)
        endpoint = max(4, int(math.ceil(2.0 * HORIZONS[SIGMA] / 3.0)))
        _, right_norms, right_units = normalized_orbit(operator, source, endpoint)
        _, _, left_units = normalized_orbit(operator.conj().T, observation_seed, endpoint)
        side_mode_indices: set[int] = set()
        for start in starts_by_side[side]:
            right_synthesis = temporal_synthesis(right_units, start, LENGTH)
            left_synthesis = temporal_synthesis(left_units, start, LENGTH)
            frames = balanced_biorthogonal_frames(right_synthesis, left_synthesis)
            right_frame = np.asarray(frames["right_frame"])
            left_frame = np.asarray(frames["left_frame"])
            forward = apply_left(operator, right_frame, source.shape)
            backward = apply_left(operator, left_frame, source.shape, dual=True)
            compressed = adjoint(left_frame) @ forward
            right_residual = float(np.linalg.norm(forward - right_frame @ compressed, 2) / np.linalg.norm(forward, 2))
            left_residual = float(np.linalg.norm(backward - left_frame @ adjoint(compressed), 2) / np.linalg.norm(backward, 2))
            if right_residual > RESIDUAL_GATE or left_residual > RESIDUAL_GATE:
                raise RuntimeError("frozen accepted window no longer passes the declared gate")
            packet_values = np.linalg.eigvals(compressed)
            matched_indices = nearest_unique_matching(packet_values, eigenvalues)
            side_mode_indices.update(matched_indices)
            radius = float((right_norms[start + LENGTH] / right_norms[start]) ** (1.0 / LENGTH))
            contour_radius = CONTOUR_FRACTION * radius * math.sin(math.pi / LENGTH)
            root_records = []
            canonical_right = []
            canonical_left = []
            matched_values = []
            for packet_index, physical_index in enumerate(matched_indices):
                packet_value = complex(packet_values[packet_index])
                physical_value = complex(eigenvalues[physical_index])
                normalized_left = normalize_left_eigenvector(
                    right_vectors[:, physical_index], left_vectors[:, physical_index]
                )
                mode = source_observation_mode(
                    right_vectors[:, physical_index], normalized_left, source, observation
                )
                canonical_right.append(np.asarray(mode["right_state"]).reshape(-1))
                canonical_left.append(np.asarray(mode["left_state"]).reshape(-1))
                matched_values.append(physical_value)
                count = contour_count(eigenvalues, packet_value, contour_radius)
                residue = complex(mode["residue"])
                root_records.append({
                    "packet_root_index": packet_index,
                    "physical_eigenvalue_index": physical_index,
                    **complex_fields("packet_root", packet_value),
                    **complex_fields("physical_eigenvalue", physical_value),
                    "absolute_matching_error": float(abs(packet_value - physical_value)),
                    "contour_radius": contour_radius,
                    "base_eigenvalue_count_inside_contour": count,
                    "full_frobenius_count_inside_contour": int(source.shape[1]) * count,
                    "contour_spectral_clearance": contour_spectral_clearance(eigenvalues, packet_value, contour_radius),
                    **complex_fields("source_observation_residue", residue),
                    "source_observation_residue_modulus": float(abs(residue)),
                    "source_activation_norm": float(mode["source_activation_norm"]),
                    "observation_activation_norm": float(mode["observation_activation_norm"]),
                    "right_source_mode_norm": float(mode["right_state_norm"]),
                    "left_observation_mode_norm": float(mode["left_state_norm"]),
                    "normalized_cross_overlap": float(mode["normalized_cross_overlap"]),
                    "spectral_projector_norm": float(mode["spectral_projector_norm"]),
                    "source_observable": abs(residue) > 1e-12,
                })
            canonical_right_matrix = np.column_stack(canonical_right)
            canonical_left_matrix = np.column_stack(canonical_left)
            right_alignment = subspace_gap(right_synthesis, canonical_right_matrix)
            left_alignment = subspace_gap(left_synthesis, canonical_left_matrix)
            canonical_right_basis = np.linalg.qr(canonical_right_matrix, mode="reduced")[0]
            canonical_left_basis = np.linalg.qr(canonical_left_matrix, mode="reduced")[0]
            canonical_cross_singular = np.linalg.svd(
                canonical_left_basis.conj().T @ canonical_right_basis,
                compute_uv=False,
            )
            determinant_packet = complex(np.linalg.det(compressed))
            determinant_physical = complex(np.prod(np.asarray(matched_values)))
            trace_records = trace_power_errors(compressed, np.asarray(matched_values), 8)
            windows.append({
                "sigma": SIGMA,
                "side": side,
                "start": start,
                "candidate_length": LENGTH,
                "operator_dimension": int(operator.shape[0]),
                "source_columns": int(source.shape[1]),
                "right_relative_residual": right_residual,
                "left_relative_residual": left_residual,
                "source_cycle_radius": radius,
                "contour_radius": contour_radius,
                "right_temporal_to_spectral_alignment": right_alignment,
                "left_temporal_to_spectral_alignment": left_alignment,
                "canonical_cross_singular_values": [float(value) for value in canonical_cross_singular],
                "canonical_minimum_cross_singular_value": float(canonical_cross_singular[-1]),
                "canonical_optimal_norm_product": float(1.0 / canonical_cross_singular[-1]),
                **complex_fields("packet_determinant", determinant_packet),
                **complex_fields("physical_mode_determinant", determinant_physical),
                "relative_determinant_error": float(abs(determinant_packet - determinant_physical) / max(1.0, abs(determinant_physical))),
                "maximum_relative_trace_power_error": max(float(item["relative_error"]) for item in trace_records),
                "trace_power_records": trace_records,
                "roots": root_records,
            })
        if len(side_mode_indices) != LENGTH:
            raise RuntimeError(f"expected one common quartet on {side}, found {len(side_mode_indices)} modes")
        for physical_index in sorted(side_mode_indices, key=lambda index: (float(eigenvalues[index].imag), float(eigenvalues[index].real))):
            normalized_left = normalize_left_eigenvector(right_vectors[:, physical_index], left_vectors[:, physical_index])
            mode = source_observation_mode(right_vectors[:, physical_index], normalized_left, source, observation)
            value = complex(eigenvalues[physical_index])
            residue = complex(mode["residue"])
            unique_modes.append({
                "sigma": SIGMA,
                "side": side,
                "operator_dimension": int(operator.shape[0]),
                "source_columns": int(source.shape[1]),
                "physical_eigenvalue_index": physical_index,
                **complex_fields("physical_eigenvalue", value),
                "physical_eigenvalue_modulus": float(abs(value)),
                **complex_fields("source_observation_residue", residue),
                "source_observation_residue_modulus": float(abs(residue)),
                "source_activation_norm": float(mode["source_activation_norm"]),
                "observation_activation_norm": float(mode["observation_activation_norm"]),
                "normalized_cross_overlap": float(mode["normalized_cross_overlap"]),
                "spectral_projector_norm": float(mode["spectral_projector_norm"]),
            })
    roots = [root for window in windows for root in window["roots"]]
    return {
        "status": "rh194_physical_edge_root_matching",
        "sigma": SIGMA,
        "candidate_length": LENGTH,
        "residual_gate": RESIDUAL_GATE,
        "contour_fraction_of_half_spacing": CONTOUR_FRACTION,
        "accepted_window_count": len(windows),
        "root_case_count": len(roots),
        "unique_physical_mode_count": len(unique_modes),
        "base_single_count_contour_count": sum(int(item["base_eigenvalue_count_inside_contour"]) == 1 for item in roots),
        "source_observable_root_count": sum(bool(item["source_observable"]) for item in roots),
        "maximum_absolute_matching_error": max(float(item["absolute_matching_error"]) for item in roots),
        "minimum_contour_spectral_clearance": min(float(item["contour_spectral_clearance"]) for item in roots),
        "minimum_residue_modulus": min(float(item["source_observation_residue_modulus"]) for item in roots),
        "minimum_normalized_cross_overlap": min(float(item["normalized_cross_overlap"]) for item in roots),
        "maximum_spectral_projector_norm": max(float(item["spectral_projector_norm"]) for item in roots),
        "right_alignment_sine_range": {
            "minimum": min(float(item["right_temporal_to_spectral_alignment"]["maximum_principal_sine"]) for item in windows),
            "maximum": max(float(item["right_temporal_to_spectral_alignment"]["maximum_principal_sine"]) for item in windows),
        },
        "left_alignment_sine_range": {
            "minimum": min(float(item["left_temporal_to_spectral_alignment"]["maximum_principal_sine"]) for item in windows),
            "maximum": max(float(item["left_temporal_to_spectral_alignment"]["maximum_principal_sine"]) for item in windows),
        },
        "maximum_relative_determinant_error": max(float(item["relative_determinant_error"]) for item in windows),
        "maximum_relative_trace_power_error": max(float(item["maximum_relative_trace_power_error"]) for item in windows),
        "elapsed_seconds": time.perf_counter() - started,
        "unique_modes": unique_modes,
        "windows": windows,
        "theorem_boundary": {
            "finite_floating_physical_eigendecomposition": True,
            "all_accepted_roots_match_unique_base_modes": all(int(item["base_eigenvalue_count_inside_contour"]) == 1 for item in roots),
            "all_matched_modes_source_observable": all(bool(item["source_observable"]) for item in roots),
            "validated_interval_eigenvalue_enclosures": False,
            "uniform_all_level_quartet": False,
            "canonical_packet": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/physical_edge_matching.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["accepted_window_count"],
        "roots": payload["root_case_count"],
        "unique_modes": payload["unique_physical_mode_count"],
        "max_match_error": payload["maximum_absolute_matching_error"],
        "single_count_contours": payload["base_single_count_contour_count"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
