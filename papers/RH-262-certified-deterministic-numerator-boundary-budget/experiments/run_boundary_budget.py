"""Replay RH-13 and certify the RH-262 boundary and order-29 budgets."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH13 = PAPERS / "RH-13-validated-reduced-sector-spectral-gap"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH13 / "src"))

from boundary_budget import certified_tail_budget, certify_boundary_budget  # noqa: E402
from validated_gap.certificate import certify_reduced_gap  # noqa: E402


SAFE_CLAIMS = {
    "nuclear_norm_lt": "4.623248864",
    "operator_norm_lt": "0.633964866",
    "operator_square_norm_lt": "0.174350001",
    "cube_geometric_ratio_lt": "0.715126024",
    "fredholm_log_lt": "100.715071",
    "astar_log_lt": "3.291531",
    "bfactor_log_lt": "2.551222",
    "linear_c_log_lt": "1.348256",
    "total_log_lt": "107.906078",
    "clean_boundary_supremum_lt": "108",
    "order_29_factor_lt": "0.000202468",
    "clean_order_29_log_tail_lt": "0.021866475",
    "clean_order_29_multiplicative_error_lt": "0.022107298",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    value.update(path.read_bytes())
    return value.hexdigest()


def interval_record(value: arb) -> dict[str, object]:
    return {"interval": str(value), "float_midpoint": float(value)}


def one_replay(decimal_precision: int) -> dict[str, object]:
    ctx.dps = decimal_precision
    reduced = certify_reduced_gap(
        decimal_precision=decimal_precision,
        dimension=50,
        tail_degree=100,
    )
    budget = certify_boundary_budget(reduced)
    factor, clean_tail, clean_error = certified_tail_budget(
        boundary_supremum=arb(108),
        inner_radius=arb(1),
        outer_radius=arb(7) / 5,
        first_omitted_order=29,
    )
    values = {
        "nuclear_norm": budget.nuclear_norm,
        "operator_norm": budget.operator_norm,
        "operator_square_norm": budget.operator_square_norm,
        "cube_geometric_ratio": budget.cube_geometric_ratio,
        "fredholm_log": budget.fredholm_log,
        "astar_log": budget.astar_log,
        "bfactor_log": budget.bfactor_log,
        "linear_c_log": budget.linear_c_log,
        "total_log": budget.total_log,
        "order_29_factor": factor,
        "clean_order_29_log_tail": clean_tail,
        "clean_order_29_multiplicative_error": clean_error,
    }
    comparisons = {
        "nuclear_norm": values["nuclear_norm"] < arb(SAFE_CLAIMS["nuclear_norm_lt"]),
        "operator_norm": values["operator_norm"] < arb(SAFE_CLAIMS["operator_norm_lt"]),
        "operator_square_norm": values["operator_square_norm"]
        < arb(SAFE_CLAIMS["operator_square_norm_lt"]),
        "cube_geometric_ratio": values["cube_geometric_ratio"]
        < arb(SAFE_CLAIMS["cube_geometric_ratio_lt"]),
        "fredholm_log": values["fredholm_log"] < arb(SAFE_CLAIMS["fredholm_log_lt"]),
        "astar_log": values["astar_log"] < arb(SAFE_CLAIMS["astar_log_lt"]),
        "bfactor_log": values["bfactor_log"] < arb(SAFE_CLAIMS["bfactor_log_lt"]),
        "linear_c_log": values["linear_c_log"] < arb(SAFE_CLAIMS["linear_c_log_lt"]),
        "total_log": values["total_log"] < arb(SAFE_CLAIMS["total_log_lt"]),
        "order_29_factor": values["order_29_factor"]
        < arb(SAFE_CLAIMS["order_29_factor_lt"]),
        "clean_order_29_log_tail": values["clean_order_29_log_tail"]
        < arb(SAFE_CLAIMS["clean_order_29_log_tail_lt"]),
        "clean_order_29_multiplicative_error": values[
            "clean_order_29_multiplicative_error"
        ]
        < arb(SAFE_CLAIMS["clean_order_29_multiplicative_error_lt"]),
    }
    if not all(comparisons.values()):
        raise RuntimeError(f"failed outward comparisons at {decimal_precision} dps")
    return {
        "decimal_precision": decimal_precision,
        "dimension": 50,
        "tail_degree": 100,
        "scaled_circle": interval_record(budget.scaled_circle),
        "numerator_circle": interval_record(budget.numerator_circle),
        "lambda": interval_record(reduced.lam),
        "values": {name: interval_record(value) for name, value in values.items()},
        "comparisons": comparisons,
    }


def run() -> dict[str, object]:
    replays = [one_replay(precision) for precision in (100, 150, 200)]
    return {
        "status": "rh262_certified_deterministic_numerator_boundary_budget",
        "protocol": {
            "scaled_circle": "7/5",
            "hardy_radius": "17/20",
            "numerator_circle": "28/17",
            "inner_tail_radius": "1",
            "first_omitted_order": 29,
            "angular_sampling_used": False,
            "arb_precisions_replayed": [100, 150, 200],
        },
        "safe_claims": SAFE_CLAIMS,
        "replays": replays,
        "certified_conclusions": {
            "M_7_over_5_lt_108": True,
            "order_29_unit_disk_log_tail_lt_0_021866475": True,
            "order_29_unit_disk_multiplicative_error_lt_0_022107298": True,
        },
        "obligation_vector": {
            "legal_anchored_head": False,
            "coefficient_bridge": False,
            "uniform_quotient_tail": False,
            "analytic_target_tail": True,
            "certified_target_boundary_constant": True,
            "satisfied_count": 2,
            "complete": False,
        },
        "source_sha256": {
            "rh13_certificate.py": digest(RH13 / "src/validated_gap/certificate.py"),
            "rh262_core.py": digest(ROOT / "src/boundary_budget/core.py"),
        },
        "theorem_boundary": {
            "deterministic_target_boundary_constant": True,
            "deterministic_target_all_order_tail_budget": True,
            "legal_anchored_head": False,
            "current_cloud_coefficient_bridge": False,
            "uniform_quotient_tail": False,
            "finite_anchor_promoted_to_all_order_theorem": False,
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
            "legal_heads_obstructed_target_tail_certified_"
            "quotient_finite_nonuniform_coefficient_bridge_open"
        ),
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/certified_boundary_budget.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "precision_count": len(payload["replays"]),
        "M_7_over_5_lt_108": payload["certified_conclusions"]["M_7_over_5_lt_108"],
        "satisfied_obligations": payload["obligation_vector"]["satisfied_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
