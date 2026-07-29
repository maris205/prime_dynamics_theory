"""Optimize the expanded shell moments over weights in {-1,0,1}."""

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
RH257 = PAPERS / "RH-257-monodromy-integrality-barrier-for-signed-moment-fits"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH222 / "src"),
    str(RH255 / "src"),
]

from expanded_reachability import shell_power_matrix  # noqa: E402
from integer_selector import signed_lattice_size, solve_bounded_signed_integer  # noqa: E402
from resonance_cloud import conjugate_shells  # noqa: E402


ORDERS = np.arange(2, 13)
INTEGER_CAP = 1


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def run() -> dict[str, object]:
    expanded = json.loads((RH254 / "results/expanded_window_atlas.json").read_text())
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text())
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text())
    anchor = json.loads((RH243 / "results/coefficient_anchor_audit.json").read_text())
    continuous = json.loads((RH257 / "results/signed_moment_audit.json").read_text())
    target = np.asarray([row["hardy_scaled_one_step_anchor"] for row in anchor["coefficient_rows"]])
    reference = {(float(row["sigma"]), str(row["side"])): row for row in atlas["endpoint_rows"]}
    trace_rows = {(float(row["sigma"]), str(row["side"])): row for row in traces["endpoint_rows"]}
    continuous_rows = {
        (float(row["sigma"]), str(row["side"])): row for row in continuous["endpoint_rows"]
    }

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
        result = solve_bounded_signed_integer(difference, matrix, ORDERS, cap=INTEGER_CAP)
        weights = np.asarray(result["weights"], dtype=int)
        distance = float(result["distance"])
        continuous_distance = float(continuous_rows[key]["signed_fit_distance"])
        rows.append({
            "sigma": key[0],
            "side": key[1],
            "shell_count": len(shells),
            "signed_lattice_point_count": signed_lattice_size(len(shells), INTEGER_CAP),
            "integer_distance": distance,
            "integer_distance_over_tolerance": distance / key[0],
            "integer_failure_margin": distance - key[0],
            "integer_selector_pass": distance <= key[0],
            "continuous_signed_distance": continuous_distance,
            "integrality_gap": distance - continuous_distance,
            "negative_weight_count": int(np.sum(weights < 0)),
            "positive_weight_count": int(np.sum(weights > 0)),
            "zero_weight_count": int(np.sum(weights == 0)),
            "mip_gap": result["mip_gap"],
            "mip_node_count": result["mip_node_count"],
        })

    return {
        "status": "rh258_unit_cap_signed_integer_selector_obstruction",
        "endpoint_count": len(rows),
        "orders": ORDERS.tolist(),
        "integer_cap": INTEGER_CAP,
        "total_signed_lattice_point_count": sum(row["signed_lattice_point_count"] for row in rows),
        "integer_selector_pass_count": sum(row["integer_selector_pass"] for row in rows),
        "minimum_integer_distance": min(row["integer_distance"] for row in rows),
        "maximum_integer_distance": max(row["integer_distance"] for row in rows),
        "minimum_integer_distance_over_tolerance": min(row["integer_distance_over_tolerance"] for row in rows),
        "maximum_integer_distance_over_tolerance": max(row["integer_distance_over_tolerance"] for row in rows),
        "minimum_integer_failure_margin": min(row["integer_failure_margin"] for row in rows),
        "minimum_integrality_gap": min(row["integrality_gap"] for row in rows),
        "maximum_integrality_gap": max(row["integrality_gap"] for row in rows),
        "maximum_mip_gap": max(row["mip_gap"] for row in rows),
        "maximum_mip_node_count": max(row["mip_node_count"] for row in rows),
        "minimum_nonzero_weight_count": min(
            row["negative_weight_count"] + row["positive_weight_count"] for row in rows
        ),
        "maximum_nonzero_weight_count": max(
            row["negative_weight_count"] + row["positive_weight_count"] for row in rows
        ),
        "endpoint_rows": rows,
        "route_coordinate": "unit_cap_signed_integer_lattice_obstructed_open_larger_cap_or_quotient_block_tail",
        "theorem_boundary": {
            "unit_cap_signed_integer_class_excluded": True,
            "larger_integer_caps_excluded": False,
            "integer_mask_has_operator_realization": False,
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
    output = ROOT / "results/unit_cap_integer_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": payload["integer_selector_pass_count"],
        "distance_range": [payload["minimum_integer_distance"], payload["maximum_integer_distance"]],
        "ratio_range": [payload["minimum_integer_distance_over_tolerance"], payload["maximum_integer_distance_over_tolerance"]],
        "lattice_points": payload["total_signed_lattice_point_count"],
        "maximum_mip_gap": payload["maximum_mip_gap"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
