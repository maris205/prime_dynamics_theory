"""Relax shell use to unbounded nonnegative weights and measure pathology."""

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
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src")]

from cone_reachability import (  # noqa: E402
    minimum_weight_cap_for_tolerance,
    solve_bounded_nonnegative,
    solve_nonnegative_cone,
)
from resonance_cloud import conjugate_shells  # noqa: E402


ORDERS = np.arange(2, 13)
CAP_AUDITS = (40.0, 41.0)


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def shell_power_matrix(shells: list[np.ndarray]) -> np.ndarray:
    return np.column_stack([
        [np.sum(np.asarray(shell, dtype=complex) ** order) for order in ORDERS]
        for shell in shells
    ]).real


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    anchor = json.loads((RH243 / "results/coefficient_anchor_audit.json").read_text(encoding="utf-8"))
    target = np.asarray([
        row["hardy_scaled_one_step_anchor"] for row in anchor["coefficient_rows"]
    ])
    trace_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in traces["endpoint_rows"]
    }
    rows = []
    for endpoint in atlas["endpoint_rows"]:
        sigma = float(endpoint["sigma"])
        side = str(endpoint["side"])
        full = values(trace_rows[(sigma, side)]["full_trace_powers"])[1:]
        base = full - scalar(endpoint["perron_scaled"]) ** ORDERS - scalar(endpoint["parity_scaled"]) ** ORDERS
        shells = conjugate_shells(values(endpoint["candidate_roots"]))
        matrix = shell_power_matrix(shells)
        difference = np.asarray((base - target).real)
        cone = solve_nonnegative_cone(difference, matrix, ORDERS)
        cap = minimum_weight_cap_for_tolerance(difference, matrix, ORDERS, sigma)
        bounded = {
            str(int(limit)): solve_bounded_nonnegative(difference, matrix, ORDERS, limit)["distance"]
            for limit in CAP_AUDITS
        }
        rows.append({
            "sigma": sigma,
            "side": side,
            "shell_count": len(shells),
            "cone_distance": float(cone["distance"]),
            "cone_distance_over_tolerance": float(cone["distance"] / sigma),
            "cone_pass": bool(cone["distance"] <= sigma + 1e-10),
            "cone_primal_dual_gap": float(cone["primal_dual_gap"]),
            "minimum_weight_cap_feasible": bool(cap["feasible"]),
            "minimum_weight_cap_for_tolerance": cap["minimum_cap"],
            "cap_40_distance": float(bounded["40"]),
            "cap_40_pass": bool(bounded["40"] <= sigma + 1e-10),
            "cap_41_distance": float(bounded["41"]),
            "cap_41_pass": bool(bounded["41"] <= sigma + 1e-10),
        })

    passing = [row for row in rows if row["cone_pass"]]
    failing = [row for row in rows if not row["cone_pass"]]
    caps = [float(row["minimum_weight_cap_for_tolerance"]) for row in passing]
    return {
        "status": "rh249_unbounded_shell_multiplicity_pathology",
        "endpoint_count": len(rows),
        "orders": ORDERS.tolist(),
        "cone_pass_count": len(passing),
        "cone_failure_count": len(failing),
        "cone_failure_endpoints": [
            {"sigma": row["sigma"], "side": row["side"], "distance": row["cone_distance"]}
            for row in failing
        ],
        "minimum_cone_distance": min(row["cone_distance"] for row in rows),
        "maximum_cone_distance": max(row["cone_distance"] for row in rows),
        "maximum_cone_primal_dual_gap": max(abs(row["cone_primal_dual_gap"]) for row in rows),
        "minimum_required_weight_cap_among_passing_endpoints": min(caps),
        "maximum_required_weight_cap_among_passing_endpoints": max(caps),
        "cap_40_pass_count": sum(row["cap_40_pass"] for row in rows),
        "cap_41_pass_count": sum(row["cap_41_pass"] for row in rows),
        "endpoint_rows": rows,
        "route_coordinate": "unbounded_shell_cone_partly_reachable_only_by_multiplicity_explosion",
        "theorem_boundary": {
            "nonnegative_cone_primal_dual_certificate": True,
            "six_frozen_endpoints_cone_unreachable": len(failing) == 6,
            "bounded_weight_40_all_endpoints_fail": not any(row["cap_40_pass"] for row in rows),
            "unbounded_real_weights_are_legal_spectral_multiplicities": False,
            "expanded_candidate_windows_excluded": False,
            "signed_or_complex_grouping_excluded": False,
            "uniform_all_order_trace_envelope": False,
            "deterministic_numerator_identification": False,
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
    output = ROOT / "results/cone_reachability_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cone_passes": payload["cone_pass_count"],
        "cone_failures": payload["cone_failure_count"],
        "required_cap_range": [
            payload["minimum_required_weight_cap_among_passing_endpoints"],
            payload["maximum_required_weight_cap_among_passing_endpoints"],
        ],
        "cap_passes": {"40": payload["cap_40_pass_count"], "41": payload["cap_41_pass_count"]},
    }, sort_keys=True))


if __name__ == "__main__":
    main()
