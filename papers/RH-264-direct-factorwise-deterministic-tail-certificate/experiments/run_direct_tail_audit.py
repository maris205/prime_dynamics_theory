"""Replay RH-13 and certify the direct order-29 factorwise tail."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH13 = PAPERS / "RH-13-validated-reduced-sector-spectral-gap"
RH262 = PAPERS / "RH-262-certified-deterministic-numerator-boundary-budget"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH262 / "src"))
sys.path.insert(0, str(RH13 / "src"))

from direct_tail import direct_tail_majorant  # noqa: E402
from validated_gap.certificate import certify_reduced_gap  # noqa: E402


CLAIMS = {
    "fredholm_lt": "0.000019045786",
    "astar_lt": "0.000003066234",
    "bfactor_lt": "0.000002376597",
    "even_total_lt": "0.000024488616",
    "odd_lt": "0.000002136130",
    "total_lt": "0.000026624745",
    "multiplicative_lt": "0.000026625100",
}


def record(value: arb) -> dict[str, object]:
    return {"interval": str(value), "float_midpoint": float(value)}


def replay(precision: int) -> dict[str, object]:
    ctx.dps = precision
    reduced = certify_reduced_gap(
        decimal_precision=precision, dimension=50, tail_degree=100
    )
    tail = direct_tail_majorant(
        reduced, inner_radius=arb(1), first_omitted_order=29
    )
    values = {
        "fredholm": tail.fredholm,
        "astar": tail.astar,
        "bfactor": tail.bfactor,
        "even_total": tail.even_total,
        "odd": tail.odd,
        "total": tail.total,
        "multiplicative_error": tail.multiplicative_error,
    }
    comparisons = {
        name: values[name] < arb(bound)
        for name, bound in (
            ("fredholm", CLAIMS["fredholm_lt"]),
            ("astar", CLAIMS["astar_lt"]),
            ("bfactor", CLAIMS["bfactor_lt"]),
            ("even_total", CLAIMS["even_total_lt"]),
            ("odd", CLAIMS["odd_lt"]),
            ("total", CLAIMS["total_lt"]),
            ("multiplicative_error", CLAIMS["multiplicative_lt"]),
        )
    }
    if not all(comparisons.values()):
        raise RuntimeError(f"failed direct-tail comparison at {precision} dps")
    return {
        "decimal_precision": precision,
        "first_omitted_order": 29,
        "values": {name: record(value) for name, value in values.items()},
        "comparisons": comparisons,
    }


def run() -> dict[str, object]:
    replays = [replay(precision) for precision in (100, 150, 200)]
    return {
        "status": "rh264_direct_factorwise_deterministic_tail_certificate",
        "protocol": {
            "hardy_radius": "17/20",
            "inner_radius": 1,
            "first_omitted_order": 29,
            "angular_sampling_used": False,
            "factorwise_endpoint_terms": ["Fredholm", "A_*", "B", "odd C"],
            "arb_precisions_replayed": [100, 150, 200],
        },
        "claims": CLAIMS,
        "replays": replays,
        "improvement_over_rh262_clean_tail_factor": 821.28,
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
            "direct_factorwise_all_order_target_tail": True,
            "finite_order_anchor_promoted_to_cloud_bridge": False,
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
            "deterministic_tail_factorwise_certified_"
            "legal_head_cloud_bridge_uniform_quotient_open"
        ),
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/direct_tail_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "total_lt": CLAIMS["total_lt"],
        "multiplicative_lt": CLAIMS["multiplicative_lt"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
