"""Audit the exact Cauchy tail interface for the deterministic anchor."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH243 = PAPERS / "RH-243-deterministic-numerator-coefficient-anchor-dictionary"
sys.path.insert(0, str(ROOT / "src"))

from deterministic_tail import (  # noqa: E402
    cauchy_tail_factor,
    logarithmic_target_tail_bound,
    multiplicative_tail_error,
    scaled_zero_free_radius,
)


HARDY_RADIUS = 0.85
NUMERATOR_RADIUS = 1.6785735104283177
OUTER_RADII = (1.05, 1.15, 1.25, 1.35)
INNER_RADII = (0.8, 0.9, 1.0)
ORDERS = tuple(range(2, 13))


def truncated_log_supremum(coefficients: np.ndarray, radius: float, samples: int = 4096) -> float:
    angles = 2.0 * np.pi * np.arange(samples, dtype=float) / samples
    points = float(radius) * np.exp(1j * angles)
    values = np.zeros(samples, dtype=complex)
    for order, coefficient in zip(ORDERS, coefficients):
        values -= complex(coefficient) * points**order / float(order)
    return float(np.max(np.abs(values)))


def run() -> dict[str, object]:
    anchor = json.loads((RH243 / "results/coefficient_anchor_audit.json").read_text())
    coefficients = np.asarray(
        [row["hardy_scaled_one_step_anchor"] for row in anchor["coefficient_rows"]],
        dtype=float,
    )
    scaled_radius = scaled_zero_free_radius(HARDY_RADIUS, NUMERATOR_RADIUS)
    rows = []
    for outer in OUTER_RADII:
        diagnostic_sup = truncated_log_supremum(coefficients, outer)
        row = {
            "cauchy_radius": outer,
            "diagnostic_truncated_log_supremum": diagnostic_sup,
            "unit_disk_order_13_factor": cauchy_tail_factor(1.0, outer, 13),
            "unit_disk_order_13_diagnostic_product": diagnostic_sup
            * cauchy_tail_factor(1.0, outer, 13),
            "inner_radius_rows": [],
        }
        for inner in INNER_RADII:
            factor = cauchy_tail_factor(inner, outer, 13)
            row["inner_radius_rows"].append({
                "disk_radius": inner,
                "tail_factor_per_boundary_supremum": factor,
                "multiplicative_error_per_boundary_supremum": multiplicative_tail_error(factor),
            })
        rows.append(row)

    best = min(rows, key=lambda row: row["unit_disk_order_13_factor"])
    return {
        "status": "rh252_deterministic_numerator_analytic_tail_certificate",
        "hardy_radius": HARDY_RADIUS,
        "deterministic_numerator_zero_free_radius": NUMERATOR_RADIUS,
        "scaled_zero_free_radius": scaled_radius,
        "coefficient_orders_used_for_diagnostics": list(ORDERS),
        "outer_radii_inside_scaled_zero_free_disk": list(OUTER_RADII),
        "inner_radii_audited": list(INNER_RADII),
        "unit_disk_all_order_target_tail_exists": scaled_radius > 1.0,
        "finite_boundary_supremum_available": False,
        "best_unit_disk_order_13_tail_factor_per_M": best["unit_disk_order_13_factor"],
        "rows": rows,
        "analytic_tail_statement": (
            "For every 0<=R<S<r_H*lambda, M_S=sup_|z|=S|log G_H(z)| is finite and "
            "sum_{n>=N}|a_n|R^n/n <= M_S (R/S)^N/(1-R/S)."
        ),
        "theorem_boundary": {
            "analytic_all_order_target_tail": True,
            "cauchy_tail_bound_conditional_on_boundary_supremum": True,
            "numerical_uniform_target_tail_constant": False,
            "current_cloud_coefficient_bridge": False,
            "uniform_all_order_trace_envelope": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis_implication": False,
            "zeta_divisor_identification": False,
        },
        "route_coordinate": "analytic_target_tail_open_cloud_bridge_and_uniform_quotient_tail",
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/analytic_tail_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "scaled_zero_free_radius": payload["scaled_zero_free_radius"],
        "best_unit_disk_order_13_tail_factor_per_M": payload[
            "best_unit_disk_order_13_tail_factor_per_M"
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
