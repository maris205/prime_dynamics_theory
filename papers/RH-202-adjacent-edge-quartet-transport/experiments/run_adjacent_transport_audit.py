"""Audit the outer-edge quartet under adjacent small-noise refinement."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH200 = PAPERS / "RH-200-conjugate-pair-edge-quartet-selection"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH200 / "src")]

from edge_quartet import outer_edge_indices, radial_edge_gap  # noqa: E402
from quartet_transport import (  # noqa: E402
    biorthogonal_eigenpacket,
    channel_state,
    coefficient_error,
    haar_embedding,
    matched_assignment,
    principal_data,
    relative_frobenius_defect,
)
from run_effective_rank_audit import build_models  # noqa: E402


SIGMAS = (0.04, 0.02, 0.01)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {f"{prefix}_real": float(value.real), f"{prefix}_imag": float(value.imag)}


def packet(model: dict[str, object]) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=complex)
    values, left_raw, right_raw = eig(operator, left=True, right=True, check_finite=False)
    indices = outer_edge_indices(values, 4)
    selected_values = values[indices]
    right, left, projector = biorthogonal_eigenpacket(right_raw[:, indices], left_raw[:, indices])
    modes = []
    for column in range(4):
        x_state, y_state, residue = channel_state(
            right[:, column], left[:, column], model["source"], model["observation"]
        )
        modes.append({"x": x_state, "y": y_state, "residue": residue})
    return {
        "operator": operator,
        "source": np.asarray(model["source"], dtype=complex),
        "observation": np.asarray(model["observation"], dtype=complex),
        "all_values": values,
        "values": selected_values,
        "right": right,
        "left": left,
        "projector": projector,
        "modes": modes,
        "edge_gap": radial_edge_gap(values, 4),
    }


def mode_direction_data(reference: np.ndarray, candidate: np.ndarray) -> dict[str, float]:
    first = np.asarray(reference, dtype=complex).reshape(-1)
    second = np.asarray(candidate, dtype=complex).reshape(-1)
    cosine = float(
        abs(np.vdot(first, second))
        / max(np.linalg.norm(first) * np.linalg.norm(second), np.finfo(float).tiny)
    )
    cosine = float(np.clip(cosine, 0.0, 1.0))
    return {
        "direction_cosine": cosine,
        "direction_sine": float(np.sqrt(max(0.0, 1.0 - cosine**2))),
        "relative_norm_change": float(
            abs(np.linalg.norm(second) - np.linalg.norm(first))
            / max(np.linalg.norm(second), np.finfo(float).tiny)
        ),
    }


def adjacent_record(
    *, side: str, coarse_sigma: float, fine_sigma: float, coarse: dict[str, object], fine: dict[str, object]
) -> dict[str, object]:
    coarse_operator = np.asarray(coarse["operator"])
    fine_operator = np.asarray(fine["operator"])
    row_embedding = haar_embedding(fine_operator.shape[0])
    coarse_source = np.asarray(coarse["source"])
    fine_source = np.asarray(fine["source"])
    column_embedding = haar_embedding(fine_source.shape[1])
    assignment = matched_assignment(coarse["values"], fine["values"])
    fine_values = np.asarray(fine["values"])[assignment]
    fine_right = np.asarray(fine["right"])[:, assignment]
    fine_left = np.asarray(fine["left"])[:, assignment]
    lifted_right = row_embedding @ np.asarray(coarse["right"])
    lifted_left = row_embedding @ np.asarray(coarse["left"])
    lifted_projector = row_embedding @ np.asarray(coarse["projector"]) @ row_embedding.conj().T
    fine_projector = fine_right @ fine_left.conj().T

    intertwining = fine_operator @ row_embedding - row_embedding @ coarse_operator
    restricted_intertwining = intertwining @ np.asarray(coarse["right"])
    source_lift = row_embedding @ coarse_source @ column_embedding.conj().T
    observation_lift = column_embedding @ np.asarray(coarse["observation"]) @ row_embedding.conj().T

    modes = []
    for coarse_index, fine_index in enumerate(assignment):
        coarse_mode = coarse["modes"][coarse_index]
        fine_mode = fine["modes"][fine_index]
        lifted_x = row_embedding @ coarse_mode["x"] @ column_embedding.conj().T
        lifted_y = row_embedding @ coarse_mode["y"] @ column_embedding.conj().T
        coarse_residue = complex(coarse_mode["residue"])
        fine_residue = complex(fine_mode["residue"])
        modes.append({
            "coarse_mode_index": coarse_index,
            "fine_mode_index": fine_index,
            **complex_fields("coarse_eigenvalue", complex(np.asarray(coarse["values"])[coarse_index])),
            **complex_fields("fine_eigenvalue", complex(fine_values[coarse_index])),
            "eigenvalue_displacement": float(abs(fine_values[coarse_index] - np.asarray(coarse["values"])[coarse_index])),
            **complex_fields("coarse_residue", coarse_residue),
            **complex_fields("fine_residue", fine_residue),
            "residue_absolute_displacement": float(abs(fine_residue - coarse_residue)),
            "residue_relative_displacement": float(abs(fine_residue - coarse_residue) / max(abs(fine_residue), np.finfo(float).tiny)),
            "right_mode_direction": mode_direction_data(lifted_right[:, coarse_index], fine_right[:, coarse_index]),
            "left_mode_direction": mode_direction_data(lifted_left[:, coarse_index], fine_left[:, coarse_index]),
            "source_state_direction": mode_direction_data(lifted_x, fine_mode["x"]),
            "observation_state_direction": mode_direction_data(lifted_y, fine_mode["y"]),
        })

    coefficient = coefficient_error(coarse["values"], fine_values)
    return {
        "side": side,
        "coarse_sigma": coarse_sigma,
        "fine_sigma": fine_sigma,
        "coarse_dimension": int(coarse_operator.shape[0]),
        "fine_dimension": int(fine_operator.shape[0]),
        "coarse_source_columns": int(coarse_source.shape[1]),
        "fine_source_columns": int(fine_source.shape[1]),
        "matching_assignment": assignment,
        "coarse_edge_gap": float(coarse["edge_gap"]),
        "fine_edge_gap": float(fine["edge_gap"]),
        "right_subspace_transport": principal_data(lifted_right, fine_right),
        "left_subspace_transport": principal_data(lifted_left, fine_left),
        "relative_oblique_projector_transport_defect": relative_frobenius_defect(fine_projector, lifted_projector),
        "full_operator_intertwining_relative_frobenius_defect": float(np.linalg.norm(intertwining, "fro") / max(np.linalg.norm(fine_operator @ row_embedding, "fro"), np.finfo(float).tiny)),
        "quartet_restricted_intertwining_relative_defect": float(np.linalg.norm(restricted_intertwining, 2) / max(np.linalg.norm(fine_operator @ lifted_right, 2), np.finfo(float).tiny)),
        "source_relative_transport_defect": relative_frobenius_defect(fine_source, source_lift),
        "observation_relative_transport_defect": relative_frobenius_defect(np.asarray(fine["observation"]), observation_lift),
        "characteristic_polynomial_transport": coefficient,
        "modes": modes,
    }


def run() -> dict[str, object]:
    started = time.perf_counter()
    packets: dict[tuple[float, str], dict[str, object]] = {}
    endpoint_rows = []
    for sigma in SIGMAS:
        _, models = build_models(sigma)
        for model in models:
            side = str(model["side"])
            data = packet(model)
            packets[(sigma, side)] = data
            endpoint_rows.append({
                "sigma": sigma,
                "side": side,
                "operator_dimension": int(np.asarray(data["operator"]).shape[0]),
                "source_columns": int(np.asarray(data["source"]).shape[1]),
                "edge_gap": float(data["edge_gap"]),
                "quartet_values_real": [float(value.real) for value in data["values"]],
                "quartet_values_imag": [float(value.imag) for value in data["values"]],
            })
    records = []
    for coarse_sigma, fine_sigma in zip(SIGMAS[:-1], SIGMAS[1:]):
        for side in ("left", "right"):
            records.append(adjacent_record(
                side=side,
                coarse_sigma=coarse_sigma,
                fine_sigma=fine_sigma,
                coarse=packets[(coarse_sigma, side)],
                fine=packets[(fine_sigma, side)],
            ))
    mode_rows = [mode for record in records for mode in record["modes"]]
    return {
        "status": "rh202_adjacent_edge_quartet_transport",
        "adjacent_case_count": len(records),
        "mode_transport_count": len(mode_rows),
        "maximum_right_subspace_sine": max(float(record["right_subspace_transport"]["maximum_principal_sine"]) for record in records),
        "maximum_left_subspace_sine": max(float(record["left_subspace_transport"]["maximum_principal_sine"]) for record in records),
        "maximum_oblique_projector_defect": max(float(record["relative_oblique_projector_transport_defect"]) for record in records),
        "maximum_quartet_intertwining_defect": max(float(record["quartet_restricted_intertwining_relative_defect"]) for record in records),
        "maximum_eigenvalue_displacement": max(float(mode["eigenvalue_displacement"]) for mode in mode_rows),
        "maximum_relative_residue_displacement": max(float(mode["residue_relative_displacement"]) for mode in mode_rows),
        "minimum_source_state_direction_cosine": min(float(mode["source_state_direction"]["direction_cosine"]) for mode in mode_rows),
        "minimum_observation_state_direction_cosine": min(float(mode["observation_state_direction"]["direction_cosine"]) for mode in mode_rows),
        "maximum_relative_polynomial_coefficient_error": max(float(record["characteristic_polynomial_transport"]["relative_l2_coefficient_error"]) for record in records),
        "endpoint_rows": endpoint_rows,
        "records": records,
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "common_dyadic_coordinates": True,
            "minimum_cost_quartet_correspondence": True,
            "finite_floating_projector_transport": True,
            "validated_contour_projectors": False,
            "small_uniform_transport_defect": False,
            "all_level_shell_map": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/adjacent_transport_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cases": payload["adjacent_case_count"],
        "right_sine_max": payload["maximum_right_subspace_sine"],
        "left_sine_max": payload["maximum_left_subspace_sine"],
        "projector_defect_max": payload["maximum_oblique_projector_defect"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
