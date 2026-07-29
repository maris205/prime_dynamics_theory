"""Audit polynomial coordinates for invariant idempotent selectors."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH254 = PAPERS / "RH-254-expanded-resolved-candidate-window-atlas"
RH255 = PAPERS / "RH-255-expanded-window-anchored-zonotope-obstruction"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src")]

from polynomial_selector import (  # noqa: E402
    interpolation_coefficients,
    nodal_idempotence_error,
    polynomial_values,
)
from resonance_cloud import conjugate_shells  # noqa: E402


SAMPLE_SHELL_COUNT = 6
SELECTED_SAMPLE_SHELL_COUNT = 3


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    expanded = json.loads((RH254 / "results/expanded_window_atlas.json").read_text())
    reachability = json.loads((RH255 / "results/expanded_reachability_audit.json").read_text())
    rows = []
    for endpoint in expanded["endpoint_rows"]:
        shells = conjugate_shells(values(endpoint["expanded_candidate_roots"]))
        sample_shells = shells[:SAMPLE_SHELL_COUNT]
        roots = np.concatenate(sample_shells)
        mask = np.concatenate([
            np.full(np.asarray(shell).size, 1.0 if index < SELECTED_SAMPLE_SHELL_COUNT else 0.0)
            for index, shell in enumerate(sample_shells)
        ])
        vandermonde = np.vander(roots, N=roots.size, increasing=True)
        coefficients = interpolation_coefficients(roots, mask)
        interpolated = polynomial_values(coefficients, roots)
        rows.append({
            "sigma": float(endpoint["sigma"]),
            "side": str(endpoint["side"]),
            "sample_shell_count": len(sample_shells),
            "sample_root_count": int(roots.size),
            "selected_sample_shell_count": SELECTED_SAMPLE_SHELL_COUNT,
            "maximum_interpolation_residual": float(np.max(np.abs(interpolated - mask))),
            "nodal_idempotence_error": nodal_idempotence_error(coefficients, roots),
            "coefficient_l1_norm": float(np.sum(np.abs(coefficients))),
            "coefficient_imaginary_leakage": float(np.max(np.abs(coefficients.imag))),
            "vandermonde_condition_number": float(np.linalg.cond(vandermonde)),
        })

    return {
        "status": "rh256_invariant_polynomial_selector_binary_collapse",
        "endpoint_count": len(rows),
        "sample_shell_count": SAMPLE_SHELL_COUNT,
        "selected_sample_shell_count": SELECTED_SAMPLE_SHELL_COUNT,
        "eligible_binary_mask_count": reachability["total_eligible_binary_subset_count"],
        "real_conjugate_closed_idempotent_selector_pass_count": reachability[
            "box_zonotope_pass_count"
        ],
        "maximum_interpolation_residual": max(row["maximum_interpolation_residual"] for row in rows),
        "maximum_nodal_idempotence_error": max(row["nodal_idempotence_error"] for row in rows),
        "minimum_coefficient_l1_norm": min(row["coefficient_l1_norm"] for row in rows),
        "maximum_coefficient_l1_norm": max(row["coefficient_l1_norm"] for row in rows),
        "maximum_coefficient_imaginary_leakage": max(row["coefficient_imaginary_leakage"] for row in rows),
        "minimum_vandermonde_condition_number": min(row["vandermonde_condition_number"] for row in rows),
        "maximum_vandermonde_condition_number": max(row["vandermonde_condition_number"] for row in rows),
        "endpoint_rows": rows,
        "route_coordinate": "real_conjugate_closed_idempotent_masks_obstructed_open_nonidempotent_quotient_grouping",
        "theorem_boundary": {
            "polynomial_idempotents_collapse_to_binary_spectral_masks": True,
            "real_conjugate_closed_resolved_window_idempotent_selectors_excluded": True,
            "complex_polynomial_coordinates_create_fractional_spectral_multiplicity": False,
            "non_idempotent_signed_quotient_grouping_excluded": False,
            "uniform_all_order_trace_envelope": False,
            "current_cloud_coefficient_bridge": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/polynomial_selector_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": payload[
            "real_conjugate_closed_idempotent_selector_pass_count"
        ],
        "maximum_interpolation_residual": payload["maximum_interpolation_residual"],
        "coefficient_l1_range": [payload["minimum_coefficient_l1_norm"], payload["maximum_coefficient_l1_norm"]],
        "condition_range": [payload["minimum_vandermonde_condition_number"], payload["maximum_vandermonde_condition_number"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
