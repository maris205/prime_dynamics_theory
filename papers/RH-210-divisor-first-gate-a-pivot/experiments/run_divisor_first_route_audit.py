"""Assemble the evidence for a divisor-first Gate-A pivot."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH202 = PAPERS / "RH-202-adjacent-edge-quartet-transport"
RH204 = PAPERS / "RH-204-conjugate-branch-correspondence"
RH206 = PAPERS / "RH-206-residue-cocycle-renormalization-obstruction"
RH207 = PAPERS / "RH-207-dual-channel-quartic-divisor-flow"
RH208 = PAPERS / "RH-208-endpoint-isolation-transport-certification"
RH209 = PAPERS / "RH-209-expanding-edge-cloud-transport-obstruction"
sys.path.insert(0, str(ROOT / "src"))

from divisor_first import rotating_similarity_example, route_coordinate  # noqa: E402


def load(directory: Path, name: str) -> dict[str, object]:
    return json.loads((directory / "results" / name).read_text(encoding="utf-8"))


def run() -> dict[str, object]:
    transport = load(RH202, "adjacent_transport_audit.json")
    branches = load(RH204, "branch_correspondence_audit.json")
    residues = load(RH206, "residue_cocycle_audit.json")
    divisor = load(RH207, "quartic_divisor_flow.json")
    certification = load(RH208, "transport_certification_feasibility.json")
    clouds = load(RH209, "expanding_cloud_audit.json")

    counterexample_rows = []
    reference_coefficients = None
    for index, angle in enumerate(np.linspace(0.0, 0.5 * np.pi, 81)):
        example = rotating_similarity_example(float(angle))
        coefficients = np.asarray(example["characteristic_coefficients"])
        if reference_coefficients is None:
            reference_coefficients = coefficients
        counterexample_rows.append({
            "index": index,
            "angle": float(angle),
            "projector_distance": example["projector_distance"],
            "coefficient_error": float(np.linalg.norm(coefficients - reference_coefficients)),
        })

    statuses = {
        "finite_branch_correspondence": int(branches["unique_assignment_case_count"]) == int(branches["adjacent_case_count"]),
        "finite_dual_channel_divisor": float(divisor["maximum_left_right_coefficient_relative_error"]) < 0.01,
        "naive_state_transport_rejected": max(float(transport["maximum_right_subspace_sine"]), float(transport["maximum_left_subspace_sine"])) > 0.8,
        "scalar_residue_renormalization_rejected": float(residues["maximum_common_scalar_relative_residual"]) > 0.9,
        "endpoint_isolation_feasible": int(certification["endpoint_case_below_one_count"]) == int(certification["endpoint_case_count"]),
        "naive_transport_certification_failed": int(certification["transport_case_below_one_count"]) == 0,
        "expanded_modulus_cloud_failed": int(clouds["expanded_two_sided_green_count"]) == 0,
        "all_level_divisor_limit": False,
    }
    coordinate = route_coordinate(statuses)
    return {
        "status": "rh210_divisor_first_gate_a_pivot",
        "route_coordinate": coordinate,
        "statuses": statuses,
        "maximum_counterexample_projector_distance": max(float(row["projector_distance"]) for row in counterexample_rows),
        "maximum_counterexample_coefficient_error": max(float(row["coefficient_error"]) for row in counterexample_rows),
        "finite_evidence": {
            "maximum_left_right_divisor_error": divisor["maximum_left_right_coefficient_relative_error"],
            "maximum_haar_subspace_sine": max(transport["maximum_right_subspace_sine"], transport["maximum_left_subspace_sine"]),
            "maximum_common_scalar_residue_error": residues["maximum_common_scalar_relative_residual"],
            "endpoint_green_count": certification["endpoint_case_below_one_count"],
            "transport_green_count": certification["transport_case_below_one_count"],
            "expanded_cloud_green_count": clouds["expanded_two_sided_green_count"],
        },
        "counterexample_rows": counterexample_rows,
        "theorem_boundary": {
            "state_transport_not_necessary_for_divisor_stability": True,
            "finite_divisor_first_pivot_supported": True,
            "all_level_divisor_compactness": False,
            "canonical_renormalization_map": False,
            "fredholm_determinant": False,
            "gate_A": False,
            "gates_B_to_E": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/divisor_first_route_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "route": payload["route_coordinate"],
        "projector_drift": payload["maximum_counterexample_projector_distance"],
        "divisor_error": payload["maximum_counterexample_coefficient_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
