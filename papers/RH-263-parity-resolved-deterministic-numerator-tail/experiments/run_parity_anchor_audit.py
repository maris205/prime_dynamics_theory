"""Cross-check the all-order parity formulas against the order-28 atlas."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH253 = PAPERS / "RH-253-extended-deterministic-anchor-atlas"
sys.path.insert(0, str(ROOT / "src"))

from parity_anchor import parity_anchor_from_physical_trace  # noqa: E402


LAMBDA = 1.6785735104283223
HARDY_RADIUS = 0.85
TOLERANCE = 1.0e-12


def run() -> dict[str, object]:
    atlas = json.loads((RH253 / "results/extended_anchor_atlas.json").read_text())
    rows = []
    for row in atlas["coefficient_rows"]:
        predicted = parity_anchor_from_physical_trace(
            row["order"], row["flat_periodic_trace"], LAMBDA, HARDY_RADIUS
        )
        residual = abs(predicted - row["hardy_scaled_anchor"])
        rows.append({
            "order": row["order"],
            "parity": "odd" if row["order"] % 2 else "even",
            "archived_anchor": row["hardy_scaled_anchor"],
            "formula_anchor": predicted,
            "absolute_residual": residual,
        })
    max_residual = max(row["absolute_residual"] for row in rows)
    odd_rows = [row for row in rows if row["parity"] == "odd"]
    even_rows = [row for row in rows if row["parity"] == "even"]
    if max_residual >= TOLERANCE:
        raise RuntimeError(f"parity formula cross-check failed: {max_residual}")
    return {
        "status": "rh263_parity_resolved_deterministic_numerator_tail",
        "hardy_radius": HARDY_RADIUS,
        "lambda": LAMBDA,
        "orders_cross_checked": len(rows),
        "odd_orders_cross_checked": len(odd_rows),
        "even_orders_cross_checked": len(even_rows),
        "maximum_absolute_cross_check_residual": max_residual,
        "cross_check_tolerance": TOLERANCE,
        "a_1_convention": 0.0,
        "exact_formulas": {
            "odd_order_n_ge_3": "a_n=(r_H*lambda)^(-n)/(1+lambda^(-n))",
            "even_order_2k": (
                "a_(2k)=r_H^(-2k)*(2 tr(T^k)+"
                "2 lambda^(-2k)/(1+lambda^(-k))-"
                "lambda^(-2k)/(1-lambda^(-2k)))"
            ),
        },
        "theorem_boundary": {
            "all_order_deterministic_parity_dictionary": True,
            "finite_atlas_cross_check": True,
            "finite_fit_promoted_to_all_order_cloud_theorem": False,
            "cloud_coefficient_bridge": False,
            "legal_anchored_head": False,
            "uniform_quotient_tail": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
            "hilbert_polya_operator": False,
            "riemann_zero_identification": False,
            "zeta_divisor_equality": False,
            "riemann_hypothesis_implication": False,
        },
        "route_coordinate": (
            "deterministic_parity_anchor_exact_"
            "cloud_bridge_open_quotient_uniformity_open"
        ),
        "rows": rows,
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/parity_anchor_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "orders": payload["orders_cross_checked"],
        "max_residual": payload["maximum_absolute_cross_check_residual"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
