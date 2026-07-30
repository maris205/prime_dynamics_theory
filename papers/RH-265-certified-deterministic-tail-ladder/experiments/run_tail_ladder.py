"""Build an Arb-certified first-omitted-order tail ladder."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH13 = PAPERS / "RH-13-validated-reduced-sector-spectral-gap"
RH262 = PAPERS / "RH-262-certified-deterministic-numerator-boundary-budget"
RH264 = PAPERS / "RH-264-direct-factorwise-deterministic-tail-certificate"
sys.path[:0] = [str(ROOT / "src"), str(RH264 / "src"), str(RH262 / "src"), str(RH13 / "src")]

from tail_ladder import build_ladder  # noqa: E402
from validated_gap.certificate import certify_reduced_gap  # noqa: E402


ORDERS = (13, 21, 29, 37, 45, 53, 61)
CLAIMS = {
    13: ("0.023243607", "0.023515845"),
    21: ("0.000873261", "0.000873642"),
    29: ("0.000026624745", "0.000026625100"),
    37: ("0.000000932147", "0.000000932147"),
    45: ("0.00000004432615", "0.00000004432615"),
    53: ("0.000000001705725", "0.000000001705725"),
    61: ("0.00000000007175542", "0.00000000007175542"),
}


def record(value: arb) -> dict[str, object]:
    return {"interval": str(value), "float_midpoint": float(value)}


def replay(precision: int) -> dict[str, object]:
    ctx.dps = precision
    reduced = certify_reduced_gap(
        decimal_precision=precision, dimension=50, tail_degree=100
    )
    rows = []
    for tail in build_ladder(reduced, ORDERS):
        total_bound, error_bound = CLAIMS[tail.first_omitted_order]
        comparisons = {
            "total": tail.total < arb(total_bound),
            "multiplicative_error": tail.multiplicative_error < arb(error_bound),
        }
        if not all(comparisons.values()):
            raise RuntimeError(
                f"tail ladder comparison failed at order {tail.first_omitted_order}"
            )
        rows.append({
            "first_omitted_order": tail.first_omitted_order,
            "total": record(tail.total),
            "multiplicative_error": record(tail.multiplicative_error),
            "even_total": record(tail.even_total),
            "odd": record(tail.odd),
            "comparisons": comparisons,
        })
    return {"decimal_precision": precision, "rows": rows}


def run() -> dict[str, object]:
    replays = [replay(precision) for precision in (100, 200)]
    return {
        "status": "rh265_certified_deterministic_tail_ladder",
        "orders": list(ORDERS),
        "replays": replays,
        "order_29_is_current_anchor_aligned": True,
        "higher_orders_are_conditional_interfaces": True,
        "monotone_total_tail_in_200_dps_replay": all(
            left["total"]["float_midpoint"] > right["total"]["float_midpoint"]
            for left, right in zip(replays[-1]["rows"], replays[-1]["rows"][1:])
        ),
        "obligation_vector": {
            "legal_anchored_head": False,
            "coefficient_bridge": False,
            "uniform_quotient_tail": False,
            "analytic_target_tail": True,
            "certified_target_boundary_constant": True,
            "satisfied_count": 2,
            "complete": False,
        },
        "theorem_boundary": {
            "all_listed_tail_budgets_certified": True,
            "order_29_current_anchor_aligned": True,
            "higher_order_heads_constructed": False,
            "finite_tail_ladder_is_cloud_envelope": False,
            "legal_anchored_head": False,
            "coefficient_bridge": False,
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
            "deterministic_tail_ladder_certified_"
            "head_bridge_and_uniform_quotient_open"
        ),
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/tail_ladder.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "orders": payload["orders"],
        "replay_count": len(payload["replays"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
