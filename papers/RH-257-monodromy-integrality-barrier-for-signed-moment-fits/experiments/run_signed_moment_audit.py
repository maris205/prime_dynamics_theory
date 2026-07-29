"""Fit expanded shell moments with arbitrary real signed weights."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
RH243 = PAPERS / "RH-243-deterministic-numerator-coefficient-anchor-dictionary"
RH254 = PAPERS / "RH-254-expanded-resolved-candidate-window-atlas"
RH255 = PAPERS / "RH-255-expanded-window-anchored-zonotope-obstruction"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src"), str(RH255 / "src")]

from expanded_reachability import shell_power_matrix  # noqa: E402
from resonance_cloud import conjugate_shells  # noqa: E402
from signed_monodromy import (  # noqa: E402
    integer_lattice_distance,
    minimum_norm_signed_fit,
    monodromy_defect,
    weighted_moment_distance,
)


ORDERS = np.arange(2, 13)
INTEGER_TOLERANCE = 1.0e-8


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def run() -> dict[str, object]:
    expanded = json.loads((RH254 / "results/expanded_window_atlas.json").read_text())
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text())
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text())
    anchor = json.loads((RH243 / "results/coefficient_anchor_audit.json").read_text())
    target = np.asarray([row["hardy_scaled_one_step_anchor"] for row in anchor["coefficient_rows"]])
    reference = {(float(row["sigma"]), str(row["side"])): row for row in atlas["endpoint_rows"]}
    trace_rows = {(float(row["sigma"]), str(row["side"])): row for row in traces["endpoint_rows"]}

    rows = []
    for endpoint in expanded["endpoint_rows"]:
        key = (float(endpoint["sigma"]), str(endpoint["side"]))
        old = reference[key]
        trace = trace_rows[key]
        full = values(trace["full_trace_powers"])[1:]
        base = full - scalar(old["perron_scaled"]) ** ORDERS - scalar(old["parity_scaled"]) ** ORDERS
        shells = conjugate_shells(values(endpoint["expanded_candidate_roots"]))
        matrix = np.asarray(shell_power_matrix(shells, ORDERS).real, dtype=float)
        difference = np.asarray((base - target).real, dtype=float)
        fit = minimum_norm_signed_fit(matrix, difference)
        weights = np.asarray(fit["weights"])
        residual = np.asarray(fit["residual"])
        lattice = integer_lattice_distance(weights)
        monodromy = monodromy_defect(weights)
        distance = weighted_moment_distance(residual, ORDERS)
        fractional = lattice > INTEGER_TOLERANCE
        singular = np.asarray(fit["singular_values"])
        rows.append({
            "sigma": key[0],
            "side": key[1],
            "shell_count": len(shells),
            "matrix_rank": fit["rank"],
            "minimum_singular_value": float(np.min(singular)),
            "maximum_singular_value": float(np.max(singular)),
            "signed_fit_distance": distance,
            "signed_fit_pass": distance <= key[0],
            "maximum_absolute_weight": float(np.max(np.abs(weights))),
            "weight_l2_norm": float(np.linalg.norm(weights)),
            "fractional_weight_count": int(np.sum(fractional)),
            "minimum_positive_integer_lattice_distance": float(np.min(lattice[fractional])) if np.any(fractional) else 0.0,
            "maximum_integer_lattice_distance": float(np.max(lattice)),
            "maximum_monodromy_defect": float(np.max(monodromy)),
            "all_weights_integral": bool(not np.any(fractional)),
        })

    return {
        "status": "rh257_monodromy_integrality_barrier_for_signed_moment_fits",
        "endpoint_count": len(rows),
        "orders": ORDERS.tolist(),
        "integer_tolerance": INTEGER_TOLERANCE,
        "full_row_rank_endpoint_count": sum(row["matrix_rank"] == ORDERS.size for row in rows),
        "signed_fit_pass_count": sum(row["signed_fit_pass"] for row in rows),
        "integer_weight_fit_count": sum(row["signed_fit_pass"] and row["all_weights_integral"] for row in rows),
        "minimum_signed_fit_distance": min(row["signed_fit_distance"] for row in rows),
        "maximum_signed_fit_distance": max(row["signed_fit_distance"] for row in rows),
        "minimum_fractional_weight_count": min(row["fractional_weight_count"] for row in rows),
        "maximum_fractional_weight_count": max(row["fractional_weight_count"] for row in rows),
        "minimum_positive_integer_lattice_distance": min(
            row["minimum_positive_integer_lattice_distance"] for row in rows
        ),
        "maximum_integer_lattice_distance": max(row["maximum_integer_lattice_distance"] for row in rows),
        "maximum_monodromy_defect": max(row["maximum_monodromy_defect"] for row in rows),
        "minimum_maximum_absolute_weight": min(row["maximum_absolute_weight"] for row in rows),
        "maximum_maximum_absolute_weight": max(row["maximum_absolute_weight"] for row in rows),
        "minimum_matrix_singular_value": min(row["minimum_singular_value"] for row in rows),
        "endpoint_rows": rows,
        "route_coordinate": "fractional_signed_moment_fits_trivial_but_monodromy_illegal_open_bounded_integer_quotient_lattice",
        "theorem_boundary": {
            "integer_weights_are_necessary_for_single_valued_meromorphic_product": True,
            "arbitrary_signed_finite_moment_fit_exists": True,
            "fractional_signed_fit_is_legal_determinant_quotient": False,
            "bounded_integer_signed_selector_audited": False,
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
    output = ROOT / "results/signed_moment_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": payload["signed_fit_pass_count"],
        "integer_fits": payload["integer_weight_fit_count"],
        "distance_range": [payload["minimum_signed_fit_distance"], payload["maximum_signed_fit_distance"]],
        "weight_range": [payload["minimum_maximum_absolute_weight"], payload["maximum_maximum_absolute_weight"]],
        "fractional_count_range": [payload["minimum_fractional_weight_count"], payload["maximum_fractional_weight_count"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
