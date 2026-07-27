"""Audit conjugate-pair parity and outer-edge quartet selection."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH185 = PAPERS / "RH-185-physical-bi-krylov-cycle-calibration"
RH194 = PAPERS / "RH-194-physical-edge-root-matching"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH77 / "experiments"))
sys.path.insert(0, str(RH194 / "src"))

from edge_quartet import nearest_conjugate_errors, nonreal_count, outer_edge_indices, radial_edge_gap  # noqa: E402
from physical_matching import normalize_left_eigenvector, source_observation_mode  # noqa: E402
from run_effective_rank_audit import build_models  # noqa: E402


SIGMAS = (0.04, 0.02, 0.01)


def run() -> dict[str, object]:
    physical_rows = []
    source = json.loads((RH185 / "results/bi_krylov_audit.json").read_text(encoding="utf-8"))
    temporal_rows = []
    for sigma in SIGMAS:
        for length in sorted({int(item["candidate_length"]) for item in source["records"] if float(item["sigma"]) == sigma}):
            records = [item for item in source["records"] if float(item["sigma"]) == sigma and int(item["candidate_length"]) == length]
            temporal_rows.append({
                "sigma": sigma,
                "candidate_length": length,
                "window_count": len(records),
                "two_sided_gate_count": sum(bool(item["two_sided_0_10_gate"]) for item in records),
                "minimum_right_residual": min(float(item["right_relative_residual"]) for item in records),
                "minimum_left_residual": min(float(item["left_relative_residual"]) for item in records),
            })
        _, models = build_models(sigma)
        for model in models:
            operator = np.asarray(model["operator"], dtype=complex)
            source_matrix = np.asarray(model["source"], dtype=complex)
            observation = np.asarray(model["observation"], dtype=complex)
            values, left, right = eig(operator, left=True, right=True, check_finite=False)
            indices = outer_edge_indices(values, 4)
            selected = values[indices]
            pair_errors = nearest_conjugate_errors(values, indices)
            residues = []
            for index in indices:
                normalized_left = normalize_left_eigenvector(right[:, index], left[:, index])
                mode = source_observation_mode(right[:, index], normalized_left, source_matrix, observation)
                residues.append(abs(complex(mode["residue"])))
            physical_rows.append({
                "sigma": sigma,
                "side": str(model["side"]),
                "operator_dimension": int(operator.shape[0]),
                "selected_indices": indices,
                "selected_eigenvalues_real": [float(value.real) for value in selected],
                "selected_eigenvalues_imag": [float(value.imag) for value in selected],
                "selected_moduli": [float(abs(value)) for value in selected],
                "selected_conjugate_pair_error_max": max(pair_errors),
                "selected_nonreal_count": nonreal_count(selected),
                "radial_gap_after_quartet": radial_edge_gap(values, 4),
                "minimum_selected_residue_modulus": min(residues),
                "all_selected_source_observable": min(residues) > 1e-12,
            })
    return {
        "status": "rh200_conjugate_pair_edge_quartet_selection",
        "physical_case_count": len(physical_rows),
        "temporal_case_count": len(temporal_rows),
        "physical_quartet_conjugate_closed_count": sum(float(item["selected_conjugate_pair_error_max"]) < 1e-10 for item in physical_rows),
        "physical_quartet_all_nonreal_count": sum(int(item["selected_nonreal_count"]) == 4 for item in physical_rows),
        "physical_quartet_all_visible_count": sum(bool(item["all_selected_source_observable"]) for item in physical_rows),
        "minimum_radial_gap_after_quartet": min(float(item["radial_gap_after_quartet"]) for item in physical_rows),
        "minimum_selected_residue_modulus": min(float(item["minimum_selected_residue_modulus"]) for item in physical_rows),
        "physical_rows": physical_rows,
        "temporal_rows": temporal_rows,
        "theorem_boundary": {
            "real_operator_conjugate_pair_parity": True,
            "outer_edge_quartet_rule": True,
            "finite_three_scale_quartet_audit": True,
            "uniform_edge_gap": False,
            "length_three_clock_explanation_all_levels": False,
            "arithmetic_prime_pair_identification": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/edge_quartet_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "physical_cases": payload["physical_case_count"],
        "quartet_gap_min": payload["minimum_radial_gap_after_quartet"],
        "quartet_visible": payload["physical_quartet_all_visible_count"],
        "temporal_rows": payload["temporal_case_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
